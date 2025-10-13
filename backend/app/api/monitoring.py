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
        try:
            from ..models.database import get_database
            from ..services.database_service import DatabaseService
            from sqlalchemy import func, desc
            from ..models.database import Session, User, MoodEntry
            
            db = next(get_database())
            db_service = DatabaseService(db)
            
            # Calculate date range
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get actual data from database
            total_sessions = db.query(Session).filter(
                Session.created_at >= start_date,
                Session.created_at <= end_date
            ).count()
            
            total_interactions = db.query(Session).filter(
                Session.created_at >= start_date,
                Session.created_at <= end_date
            ).with_entities(func.sum(Session.interaction_count)).scalar() or 0
            
            unique_users = db.query(User).filter(
                User.created_at >= start_date,
                User.created_at <= end_date
            ).count()
            
            # Calculate average session duration
            sessions = db.query(Session).filter(
                Session.created_at >= start_date,
                Session.created_at <= end_date
            ).all()
            
            avg_duration = 0
            if sessions:
                total_duration = sum([
                    (session.updated_at - session.created_at).total_seconds() 
                    for session in sessions if session.updated_at
                ])
                avg_duration = total_duration / len(sessions) / 60  # Convert to minutes
            
            # Get most common emotions
            emotion_counts = db.query(
                MoodEntry.emotion_label,
                func.count(MoodEntry.emotion_label)
            ).filter(
                MoodEntry.timestamp >= start_date,
                MoodEntry.timestamp <= end_date
            ).group_by(MoodEntry.emotion_label).order_by(desc(func.count(MoodEntry.emotion_label))).limit(5).all()
            
            most_common_emotions = [{"emotion": emotion, "count": count} for emotion, count in emotion_counts]
            
            # Calculate peak usage hours
            hour_counts = db.query(
                func.extract('hour', Session.created_at),
                func.count(Session.id)
            ).filter(
                Session.created_at >= start_date,
                Session.created_at <= end_date
            ).group_by(func.extract('hour', Session.created_at)).order_by(desc(func.count(Session.id))).limit(3).all()
            
            peak_usage_hours = [{"hour": int(hour), "sessions": int(count)} for hour, count in hour_counts]
            
            usage_data = {
                "total_sessions": total_sessions,
                "total_interactions": total_interactions,
                "unique_users": unique_users,
                "average_session_duration": round(avg_duration, 2),
                "most_common_emotions": most_common_emotions,
                "peak_usage_hours": peak_usage_hours,
                "period_days": days
            }
            
        except Exception as e:
            # Fallback to placeholder data if database query fails
            usage_data = {
                "total_sessions": 0,
                "total_interactions": 0,
                "unique_users": 0,
                "average_session_duration": 0,
                "most_common_emotions": [],
                "peak_usage_hours": [],
                "period_days": days,
                "error": str(e)
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
