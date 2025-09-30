#!/usr/bin/env python3
"""
Database initialization script for Voice CBT application.
This script sets up the database tables and initial data.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models.database import db_manager, Base, engine
from app.services.database_service import DatabaseService
from sqlalchemy.orm import Session

def create_database_tables():
    """Create all database tables."""
    print("🗄️  Creating database tables...")
    try:
        db_manager.create_tables()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def create_initial_data():
    """Create initial data for the application."""
    print("📊 Creating initial data...")
    
    try:
        # Get database session
        db = db_manager.get_db()
        db_service = DatabaseService(db)
        
        # Create a test user
        test_user = db_service.create_or_get_user(
            username="test_user",
            email="test@example.com"
        )
        print(f"✅ Created test user: {test_user.username}")
        
        # Create a sample session
        session_data = db_service.start_therapy_session(str(test_user.id))
        if session_data:
            print(f"✅ Created test session: {session_data['session_id']}")
        
        # Create sample mood entries
        sample_moods = [
            {"emotion": "anxious", "intensity": 7, "context": "Work presentation"},
            {"emotion": "calm", "intensity": 3, "context": "After meditation"},
            {"emotion": "happy", "intensity": 8, "context": "Spending time with family"},
            {"emotion": "sad", "intensity": 6, "context": "Missing a friend"},
            {"emotion": "neutral", "intensity": 5, "context": "Regular day"}
        ]
        
        for mood in sample_moods:
            db_service.log_mood_entry(
                user_id=str(test_user.id),
                emotion=mood["emotion"],
                intensity=mood["intensity"],
                context=mood["context"],
                source="sample_data"
            )
        
        print("✅ Created sample mood entries")
        
        # Create sample system metrics
        db_service.log_system_metrics(
            response_time_ms=1500,
            memory_usage_mb=512.5,
            cpu_usage_percent=25.3,
            active_sessions=1,
            total_interactions=5,
            error_count=0
        )
        
        print("✅ Created sample system metrics")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating initial data: {e}")
        return False

def verify_database_connection():
    """Verify database connection."""
    print("🔍 Verifying database connection...")
    
    try:
        # Test connection
        db = db_manager.get_db()
        db_service = DatabaseService(db)
        
        # Test basic operations
        user = db_service.create_or_get_user("connection_test")
        if user:
            print("✅ Database connection successful")
            db.close()
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def reset_database():
    """Reset database by dropping and recreating tables."""
    print("🔄 Resetting database...")
    
    try:
        db_manager.reset_database()
        print("✅ Database reset successfully")
        return True
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False

def show_database_status():
    """Show database status and statistics."""
    print("📈 Database Status:")
    print("=" * 50)
    
    try:
        db = db_manager.get_db()
        db_service = DatabaseService(db)
        
        # Get system health
        health = db_service.get_system_health()
        print(f"System Status: {health.get('status', 'unknown')}")
        
        if 'metrics' in health:
            metrics = health['metrics']
            print(f"Average Response Time: {metrics.get('average_response_time_ms', 0)}ms")
            print(f"Average Memory Usage: {metrics.get('average_memory_usage_mb', 0)}MB")
            print(f"Total Errors: {metrics.get('total_errors', 0)}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error getting database status: {e}")
        return False

def main():
    """Main initialization function."""
    print("🚀 Voice CBT Database Initialization")
    print("=" * 60)
    
    # Check if we should reset the database
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        if not reset_database():
            sys.exit(1)
    
    # Verify connection first
    if not verify_database_connection():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Create tables
    if not create_database_tables():
        print("❌ Failed to create database tables")
        sys.exit(1)
    
    # Create initial data
    if not create_initial_data():
        print("❌ Failed to create initial data")
        sys.exit(1)
    
    # Show status
    show_database_status()
    
    print("\n🎉 Database initialization completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend server: python -m uvicorn app.main:app --reload")
    print("2. Test the API endpoints")
    print("3. Run tests: python run_tests.py")

if __name__ == "__main__":
    main()
