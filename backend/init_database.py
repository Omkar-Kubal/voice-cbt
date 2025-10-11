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

from app.models.database import db_manager, Base, engine, DatabaseOperations
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
        from app.models.database import DatabaseOperations
        db_ops = DatabaseOperations(db)
        
        # Create a test user
        test_user = db_ops.create_user(
            username="test_user",
            email="test@example.com"
        )
        print(f"✅ Created test user: {test_user.username}")
        
        # Create a sample session
        session = db_ops.create_session(str(test_user.id))
        if session:
            print(f"✅ Created test session: {session.id}")
        
        # Create sample mood entries
        sample_moods = [
            {"emotion": "anxious", "intensity": 7, "context": "Work presentation"},
            {"emotion": "calm", "intensity": 3, "context": "After meditation"},
            {"emotion": "happy", "intensity": 8, "context": "Spending time with family"},
            {"emotion": "sad", "intensity": 6, "context": "Missing a friend"},
            {"emotion": "neutral", "intensity": 5, "context": "Regular day"}
        ]
        
        for mood in sample_moods:
            db_ops.create_mood_entry(
                user_id=str(test_user.id),
                emotion=mood["emotion"],
                intensity=mood["intensity"],
                context=mood["context"]
            )
        
        print("✅ Created sample mood entries")
        
        # Create sample system metrics
        db_ops.create_system_metric(
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
        
        # Test basic operations
        from app.models.database import DatabaseOperations
        db_ops = DatabaseOperations(db)
        user = db_ops.create_user("connection_test", "test@example.com")
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
        from app.models.database import DatabaseOperations
        db_ops = DatabaseOperations(db)
        
        # Get recent metrics
        metrics = db_ops.get_recent_metrics(24)
        if metrics:
            latest = metrics[0]
            print(f"Latest Response Time: {latest.response_time_ms}ms")
            print(f"Latest Memory Usage: {latest.memory_usage_mb}MB")
            print(f"Latest CPU Usage: {latest.cpu_usage_percent}%")
            print(f"Active Sessions: {latest.active_sessions}")
            print(f"Total Interactions: {latest.total_interactions}")
            print(f"Error Count: {latest.error_count}")
        else:
            print("No metrics available yet")
        
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
