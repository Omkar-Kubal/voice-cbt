"""
Comprehensive monitoring and analytics service for Voice CBT application.
"""

import time
import psutil
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import json
import os
from pathlib import Path

from ..models.database import get_database
from ..services.database_service import DatabaseService

logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    network_sent_mb: float
    network_recv_mb: float
    load_average: List[float]
    active_connections: int
    response_time_ms: float
    error_count: int
    warning_count: int

@dataclass
class ApplicationMetrics:
    """Application-specific metrics."""
    timestamp: datetime
    active_sessions: int
    total_interactions: int
    successful_interactions: int
    failed_interactions: int
    emotion_detection_accuracy: float
    stt_accuracy: float
    average_response_time_ms: float
    model_loading_time_ms: float
    cache_hit_rate: float
    database_connections: int
    queue_size: int

class MonitoringService:
    """Comprehensive monitoring service."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.metrics_history = []
        self.alert_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_usage_percent": 90.0,
            "response_time_ms": 5000.0,
            "error_rate": 0.1
        }
        self.alerts = []
        self.is_monitoring = False
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring."""
        if self.is_monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.is_monitoring = True
        logger.info(f"Starting monitoring with {interval_seconds}s interval")
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop(interval_seconds))
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.is_monitoring = False
        logger.info("Monitoring stopped")
    
    async def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Collect metrics
                system_metrics = self._collect_system_metrics()
                app_metrics = await self._collect_application_metrics()
                
                # Store metrics
                self.metrics_history.append({
                    "system": asdict(system_metrics),
                    "application": asdict(app_metrics)
                })
                
                # Keep only last 1000 entries
                if len(self.metrics_history) > 1000:
                    self.metrics_history.pop(0)
                
                # Check for alerts
                await self._check_alerts(system_metrics, app_metrics)
                
                # Log metrics to database
                await self._log_metrics_to_database(system_metrics, app_metrics)
                
                logger.debug(f"Collected metrics: CPU {system_metrics.cpu_percent:.1f}%, "
                           f"Memory {system_metrics.memory_percent:.1f}%, "
                           f"Response time {system_metrics.response_time_ms:.1f}ms")
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            await asyncio.sleep(interval_seconds)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics."""
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Network I/O
        network = psutil.net_io_counters()
        
        # Load average (Unix-like systems)
        try:
            load_avg = list(psutil.getloadavg())
        except AttributeError:
            load_avg = [0.0, 0.0, 0.0]
        
        # Active connections
        try:
            connections = len(psutil.net_connections())
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            connections = 0
        
        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            disk_usage_percent=disk.percent,
            disk_free_gb=disk.free / (1024 * 1024 * 1024),
            network_sent_mb=network.bytes_sent / (1024 * 1024),
            network_recv_mb=network.bytes_recv / (1024 * 1024),
            load_average=load_avg,
            active_connections=connections,
            response_time_ms=0.0,  # Will be updated by application
            error_count=0,  # Will be updated by application
            warning_count=0  # Will be updated by application
        )
    
    async def _collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics."""
        # Get database session
        db = next(get_database())
        db_service = DatabaseService(db)
        
        try:
            # Get recent metrics from database
            recent_metrics = db_service.get_recent_metrics(hours=1)
            
            # Calculate application metrics
            active_sessions = len([m for m in recent_metrics if m.active_sessions])
            total_interactions = sum(m.total_interactions for m in recent_metrics)
            successful_interactions = total_interactions - sum(m.error_count for m in recent_metrics)
            failed_interactions = sum(m.error_count for m in recent_metrics)
            
            # Calculate averages
            response_times = [m.response_time_ms for m in recent_metrics if m.response_time_ms]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Calculate accuracy metrics (placeholder - would need actual data)
            emotion_accuracy = 0.85  # Placeholder
            stt_accuracy = 0.90  # Placeholder
            
            return ApplicationMetrics(
                timestamp=datetime.now(),
                active_sessions=active_sessions,
                total_interactions=total_interactions,
                successful_interactions=successful_interactions,
                failed_interactions=failed_interactions,
                emotion_detection_accuracy=emotion_accuracy,
                stt_accuracy=stt_accuracy,
                average_response_time_ms=avg_response_time,
                model_loading_time_ms=0.0,  # Placeholder
                cache_hit_rate=0.0,  # Placeholder
                database_connections=1,  # Placeholder
                queue_size=0  # Placeholder
            )
        finally:
            db.close()
    
    async def _check_alerts(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Check for alert conditions."""
        alerts = []
        
        # CPU alert
        if system_metrics.cpu_percent > self.alert_thresholds["cpu_percent"]:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"High CPU usage: {system_metrics.cpu_percent:.1f}%",
                "timestamp": datetime.now(),
                "value": system_metrics.cpu_percent,
                "threshold": self.alert_thresholds["cpu_percent"]
            })
        
        # Memory alert
        if system_metrics.memory_percent > self.alert_thresholds["memory_percent"]:
            alerts.append({
                "type": "high_memory",
                "severity": "warning",
                "message": f"High memory usage: {system_metrics.memory_percent:.1f}%",
                "timestamp": datetime.now(),
                "value": system_metrics.memory_percent,
                "threshold": self.alert_thresholds["memory_percent"]
            })
        
        # Disk alert
        if system_metrics.disk_usage_percent > self.alert_thresholds["disk_usage_percent"]:
            alerts.append({
                "type": "high_disk",
                "severity": "critical",
                "message": f"High disk usage: {system_metrics.disk_usage_percent:.1f}%",
                "timestamp": datetime.now(),
                "value": system_metrics.disk_usage_percent,
                "threshold": self.alert_thresholds["disk_usage_percent"]
            })
        
        # Response time alert
        if system_metrics.response_time_ms > self.alert_thresholds["response_time_ms"]:
            alerts.append({
                "type": "slow_response",
                "severity": "warning",
                "message": f"Slow response time: {system_metrics.response_time_ms:.1f}ms",
                "timestamp": datetime.now(),
                "value": system_metrics.response_time_ms,
                "threshold": self.alert_thresholds["response_time_ms"]
            })
        
        # Error rate alert
        if app_metrics.total_interactions > 0:
            error_rate = app_metrics.failed_interactions / app_metrics.total_interactions
            if error_rate > self.alert_thresholds["error_rate"]:
                alerts.append({
                    "type": "high_error_rate",
                    "severity": "critical",
                    "message": f"High error rate: {error_rate:.1%}",
                    "timestamp": datetime.now(),
                    "value": error_rate,
                    "threshold": self.alert_thresholds["error_rate"]
                })
        
        # Store alerts
        self.alerts.extend(alerts)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
        
        # Log critical alerts
        for alert in alerts:
            if alert["severity"] == "critical":
                logger.critical(f"CRITICAL ALERT: {alert['message']}")
            else:
                logger.warning(f"WARNING: {alert['message']}")
    
    async def _log_metrics_to_database(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Log metrics to database."""
        try:
            db = next(get_database())
            db_service = DatabaseService(db)
            
            # Log system metrics
            db_service.log_system_metrics(
                response_time_ms=system_metrics.response_time_ms,
                memory_usage_mb=system_metrics.memory_used_mb,
                cpu_usage_percent=system_metrics.cpu_percent,
                active_sessions=app_metrics.active_sessions,
                total_interactions=app_metrics.total_interactions,
                error_count=app_metrics.failed_interactions
            )
            
            db.close()
        except Exception as e:
            logger.error(f"Error logging metrics to database: {e}")
    
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for the specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter recent metrics
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m["system"]["timestamp"]) >= cutoff_time
        ]
        
        if not recent_metrics:
            return {"message": "No metrics available for the specified period"}
        
        # Calculate summary statistics
        system_metrics = [m["system"] for m in recent_metrics]
        app_metrics = [m["application"] for m in recent_metrics]
        
        # System metrics summary
        cpu_values = [m["cpu_percent"] for m in system_metrics]
        memory_values = [m["memory_percent"] for m in system_metrics]
        response_times = [m["response_time_ms"] for m in system_metrics]
        
        # Application metrics summary
        total_sessions = sum(m["active_sessions"] for m in app_metrics)
        total_interactions = sum(m["total_interactions"] for m in app_metrics)
        successful_interactions = sum(m["successful_interactions"] for m in app_metrics)
        failed_interactions = sum(m["failed_interactions"] for m in app_metrics)
        
        return {
            "period_hours": hours,
            "data_points": len(recent_metrics),
            "system": {
                "cpu": {
                    "average": sum(cpu_values) / len(cpu_values),
                    "max": max(cpu_values),
                    "min": min(cpu_values)
                },
                "memory": {
                    "average": sum(memory_values) / len(memory_values),
                    "max": max(memory_values),
                    "min": min(memory_values)
                },
                "response_time": {
                    "average": sum(response_times) / len(response_times) if response_times else 0,
                    "max": max(response_times) if response_times else 0,
                    "min": min(response_times) if response_times else 0
                }
            },
            "application": {
                "total_sessions": total_sessions,
                "total_interactions": total_interactions,
                "successful_interactions": successful_interactions,
                "failed_interactions": failed_interactions,
                "success_rate": successful_interactions / total_interactions if total_interactions > 0 else 0
            },
            "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600
        }
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get alerts, optionally filtered by severity."""
        if severity:
            return [alert for alert in self.alerts if alert["severity"] == severity]
        return self.alerts
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status."""
        if not self.metrics_history:
            return {"status": "unknown", "message": "No metrics available"}
        
        # Get latest metrics
        latest = self.metrics_history[-1]
        system = latest["system"]
        app = latest["application"]
        
        # Determine health status
        health_issues = []
        
        if system["cpu_percent"] > 90:
            health_issues.append("High CPU usage")
        
        if system["memory_percent"] > 90:
            health_issues.append("High memory usage")
        
        if system["disk_usage_percent"] > 95:
            health_issues.append("High disk usage")
        
        if system["response_time_ms"] > 10000:
            health_issues.append("Slow response time")
        
        if app["total_interactions"] > 0 and app["failed_interactions"] / app["total_interactions"] > 0.2:
            health_issues.append("High error rate")
        
        # Determine overall status
        if not health_issues:
            status = "healthy"
        elif len(health_issues) <= 2:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return {
            "status": status,
            "issues": health_issues,
            "timestamp": datetime.now().isoformat(),
            "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600
        }

# Global monitoring service instance
monitoring_service = MonitoringService()

# Auto-start monitoring when module is imported
if os.getenv("ENABLE_MONITORING", "true").lower() == "true":
    monitoring_service.start_monitoring()
