#!/usr/bin/env python3
"""
Simple database initialization for Voice CBT.
Uses SQLite - no complex setup needed!
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import Base, engine, SessionLocal
from app.models.database import User, Session, MoodEntry, Interaction, SystemMetrics

def create_database():
    """Create the database and tables."""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_sample_data():
    """Create sample data for testing."""
    print("Creating sample data...")
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.username == "test_user").first()
        if existing_user:
            print(" Test user already exists")
            return True
        
        # Create test user
        test_user = User(
            username="test_user",
            email="test@example.com",
            preferences={
                "voice_speed": 180,
                "voice_volume": 0.9,
                "preferred_voice": "female"
            }
        )
        db.add(test_user)
        db.commit()
        
        # Create a sample session
        sample_session = Session(
            user_id=test_user.id,
            session_type="therapy",
            status="completed",
            duration_minutes=15
        )
        db.add(sample_session)
        db.commit()
        
        # Create sample mood entries
        mood_entries = [
            MoodEntry(
                user_id=test_user.id,
                emotion="neutral",
                confidence=0.8,
                context="Initial assessment"
            ),
            MoodEntry(
                user_id=test_user.id,
                emotion="happy",
                confidence=0.9,
                context="Positive therapy session"
            )
        ]
        
        for mood in mood_entries:
            db.add(mood)
        db.commit()
        
        print(" Sample data created successfully")
        return True
        
    except Exception as e:
        print(f" Error creating sample data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_database():
    """Verify the database is working."""
    print("Verifying database...")
    
    db = SessionLocal()
    try:
        # Test basic queries
        user_count = db.query(User).count()
        session_count = db.query(Session).count()
        mood_count = db.query(MoodEntry).count()
        
        print(f" Database verification successful:")
        print(f"   Users: {user_count}")
        print(f"   Sessions: {session_count}")
        print(f"   Mood entries: {mood_count}")
        
        return True
        
    except Exception as e:
        print(f" Database verification failed: {e}")
        return False
    finally:
        db.close()

def main():
    """Main initialization function."""
    print("Voice CBT - Simple Database Setup")
    print("=" * 50)
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Step 1: Create database
    if not create_database():
        print(" Failed to create database")
        sys.exit(1)
    
    # Step 2: Create sample data
    if not create_sample_data():
        print(" Failed to create sample data")
        sys.exit(1)
    
    # Step 3: Verify database
    if not verify_database():
        print(" Database verification failed")
        sys.exit(1)
    
    print("\nDatabase setup complete!")
    print(" SQLite database is ready")
    print(" Sample data created")
    print(" System ready for use")

if __name__ == "__main__":
    main()
