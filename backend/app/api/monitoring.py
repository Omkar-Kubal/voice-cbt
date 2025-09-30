"""
Monitoring and analytics API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from ..services.monitoring import monitoring_service
from ..models.database import get_database
from ..services.database_service import DatabaseService

router = APIRouter()

@router.get("/metrics/summary")
async def get_metrics_summary(
    hours: int = Query(24, description="Time period in hours"),
    db = Depends(get_database)
):
    """Get comprehensive metrics summary."""
    try:
        # Get monitoring service summary
        summary = monitoring_service.get_metrics_summary(hours)
        
        # Get database health
        db_service = DatabaseService(db)
        db_health = db_service.get_system_health(hours)
        
        # Combine summaries
        combined_summary = {
            "monitoring": summary,
            "database": db_health,
            "timestamp": datetime.now().isoformat()
        }
        
        return combined_summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def get_health_status():
    """Get overall system health status."""
    try:
        health_status = monitoring_service.get_health_status()
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def get_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity (warning, critical)"),
    limit: int = Query(50, description="Maximum number of alerts to return")
):
    """Get system alerts."""
    try:
        alerts = monitoring_service.get_alerts(severity)
        
        # Limit results
        if limit:
            alerts = alerts[-limit:]
        
        return {
            "alerts": alerts,
            "total_count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_performance_metrics(
    hours: int = Query(24, description="Time period in hours"),
    db = Depends(get_database)
):
    """Get performance metrics."""
    try:
        db_service = DatabaseService(db)
        
        # Get recent metrics from database
        recent_metrics = db_service.get_recent_metrics(hours)
        
        if not recent_metrics:
            return {"message": "No performance data available"}
        
        # Calculate performance metrics
        response_times = [m.response_time_ms for m in recent_metrics if m.response_time_ms]
        memory_usage = [m.memory_usage_mb for m in recent_metrics if m.memory_usage_mb]
        cpu_usage = [m.cpu_usage_percent for m in recent_metrics if m.cpu_usage_percent]
        
        performance_data = {
            "response_time": {
                "average": sum(response_times) / len(response_times) if response_times else 0,
                "max": max(response_times) if response_times else 0,
                "min": min(response_times) if response_times else 0,
                "p95": sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0
            },
            "memory_usage": {
                "average_mb": sum(memory_usage) / len(memory_usage) if memory_usage else 0,
                "max_mb": max(memory_usage) if memory_usage else 0,
                "min_mb": min(memory_usage) if memory_usage else 0
            },
            "cpu_usage": {
                "average_percent": sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0,
                "max_percent": max(cpu_usage) if cpu_usage else 0,
                "min_percent": min(cpu_usage) if cpu_usage else 0
            },
            "data_points": len(recent_metrics),
            "period_hours": hours
        }
        
        return performance_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usage")
async def get_usage_analytics(
    days: int = Query(30, description="Time period in days"),
    db = Depends(get_database)
):
    """Get usage analytics."""
    try:
        db_service = DatabaseService(db)
        
        # Get usage data from database
        # This would need to be implemented based on your specific analytics needs
        usage_data = {
            "total_sessions": 0,  # Placeholder
            "total_interactions": 0,  # Placeholder
            "unique_users": 0,  # Placeholder
            "average_session_duration": 0,  # Placeholder
            "most_common_emotions": [],  # Placeholder
            "peak_usage_hours": [],  # Placeholder
            "period_days": days
        }
        
        return usage_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/errors")
async def get_error_analytics(
    hours: int = Query(24, description="Time period in hours"),
    db = Depends(get_database)
):
    """Get error analytics."""
    try:
        db_service = DatabaseService(db)
        
        # Get recent metrics
        recent_metrics = db_service.get_recent_metrics(hours)
        
        if not recent_metrics:
            return {"message": "No error data available"}
        
        # Calculate error metrics
        total_errors = sum(m.error_count for m in recent_metrics)
        total_interactions = sum(m.total_interactions for m in recent_metrics)
        error_rate = total_errors / total_interactions if total_interactions > 0 else 0
        
        error_data = {
            "total_errors": total_errors,
            "total_interactions": total_interactions,
            "error_rate": error_rate,
            "error_trend": "stable",  # Placeholder - would need historical data
            "most_common_errors": [],  # Placeholder
            "period_hours": hours
        }
        
        return error_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/start")
async def start_monitoring(
    interval_seconds: int = Query(60, description="Monitoring interval in seconds")
):
    """Start system monitoring."""
    try:
        monitoring_service.start_monitoring(interval_seconds)
        return {"message": "Monitoring started", "interval_seconds": interval_seconds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/stop")
async def stop_monitoring():
    """Stop system monitoring."""
    try:
        monitoring_service.stop_monitoring()
        return {"message": "Monitoring stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/status")
async def get_monitoring_status():
    """Get monitoring service status."""
    try:
        return {
            "is_monitoring": monitoring_service.is_monitoring,
            "start_time": monitoring_service.start_time.isoformat(),
            "uptime_hours": (datetime.now() - monitoring_service.start_time).total_seconds() / 3600,
            "metrics_count": len(monitoring_service.metrics_history),
            "alerts_count": len(monitoring_service.alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
