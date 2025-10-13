"""
Authentication API endpoints for Voice CBT application.
Handles Google OAuth and user management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

from ..models.database import get_database, User
from ..core.logging import get_logger, LogContext
from ..core.exceptions import AuthenticationError, DatabaseError, ValidationError

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
logger = get_logger('voice-cbt.auth')

@router.post("/sync")
async def sync_user(
    user_data: Dict[str, Any],
    db: Session = Depends(get_database)
):
    """
    Sync Firebase user data with backend database.
    Creates or updates user record.
    """
    
    with LogContext(logger, endpoint="sync_user", user_id=user_data.get('uid')):
        try:
            # Validate required fields
            required_fields = ['uid', 'email', 'provider']
            for field in required_fields:
                if field not in user_data:
                    raise ValidationError(f"Missing required field: {field}")
            
            uid = user_data['uid']
            email = user_data['email']
            display_name = user_data.get('displayName', '')
            photo_url = user_data.get('photoURL', '')
            provider = user_data['provider']
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            
            if existing_user:
                # Update existing user
                existing_user.username = display_name or email.split('@')[0]
                existing_user.preferences = existing_user.preferences or {}
                existing_user.preferences.update({
                    'firebase_uid': uid,
                    'provider': provider,
                    'photo_url': photo_url,
                    'last_login': datetime.utcnow().isoformat()
                })
                existing_user.is_active = True
                
                db.commit()
                db.refresh(existing_user)
                
                logger.info(f"Updated existing user: {email}")
                
                return {
                    "success": True,
                    "user": {
                        "id": str(existing_user.id),
                        "username": existing_user.username,
                        "email": existing_user.email,
                        "display_name": display_name,
                        "photo_url": photo_url,
                        "is_new_user": False
                    }
                }
            else:
                # Create new user
                new_user = User(
                    username=display_name or email.split('@')[0],
                    email=email,
                    is_active=True,
                    preferences={
                        'firebase_uid': uid,
                        'provider': provider,
                        'photo_url': photo_url,
                        'created_via': 'google_oauth',
                        'last_login': datetime.utcnow().isoformat(),
                        'voice_speed': 180,
                        'voice_volume': 0.9,
                        'preferred_voice': 'female'
                    }
                )
                
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                logger.info(f"Created new user: {email}")
                
                return {
                    "success": True,
                    "user": {
                        "id": str(new_user.id),
                        "username": new_user.username,
                        "email": new_user.email,
                        "display_name": display_name,
                        "photo_url": photo_url,
                        "is_new_user": True
                    }
                }
                
        except ValidationError as e:
            logger.error(f"Validation error in sync_user: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error syncing user: {e}")
            raise DatabaseError("Failed to sync user data")

@router.get("/me")
async def get_current_user(
    firebase_uid: str,
    db: Session = Depends(get_database)
):
    """
    Get current user information by Firebase UID.
    """
    
    with LogContext(logger, endpoint="get_current_user", firebase_uid=firebase_uid):
        try:
            # Find user by Firebase UID in preferences
            user = db.query(User).filter(
                User.preferences['firebase_uid'].astext == firebase_uid
            ).first()
            
            if not user:
                raise AuthenticationError("User not found")
            
            if not user.is_active:
                raise AuthenticationError("User account is inactive")
            
            return {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "display_name": user.preferences.get('display_name', user.username),
                "photo_url": user.preferences.get('photo_url', ''),
                "preferences": user.preferences,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "is_active": user.is_active
            }
            
        except AuthenticationError as e:
            logger.error(f"Authentication error in get_current_user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            raise DatabaseError("Failed to get user information")

@router.put("/preferences")
async def update_user_preferences(
    firebase_uid: str,
    preferences: Dict[str, Any],
    db: Session = Depends(get_database)
):
    """
    Update user preferences.
    """
    
    with LogContext(logger, endpoint="update_preferences", firebase_uid=firebase_uid):
        try:
            # Find user by Firebase UID
            user = db.query(User).filter(
                User.preferences['firebase_uid'].astext == firebase_uid
            ).first()
            
            if not user:
                raise AuthenticationError("User not found")
            
            # Update preferences
            current_preferences = user.preferences or {}
            current_preferences.update(preferences)
            user.preferences = current_preferences
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"Updated preferences for user: {user.email}")
            
            return {
                "success": True,
                "preferences": user.preferences
            }
            
        except AuthenticationError as e:
            logger.error(f"Authentication error in update_preferences: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            raise DatabaseError("Failed to update preferences")

@router.delete("/account")
async def deactivate_account(
    firebase_uid: str,
    db: Session = Depends(get_database)
):
    """
    Deactivate user account.
    """
    
    with LogContext(logger, endpoint="deactivate_account", firebase_uid=firebase_uid):
        try:
            # Find user by Firebase UID
            user = db.query(User).filter(
                User.preferences['firebase_uid'].astext == firebase_uid
            ).first()
            
            if not user:
                raise AuthenticationError("User not found")
            
            # Deactivate account
            user.is_active = False
            user.preferences = user.preferences or {}
            user.preferences['deactivated_at'] = datetime.utcnow().isoformat()
            
            db.commit()
            
            logger.info(f"Deactivated account for user: {user.email}")
            
            return {
                "success": True,
                "message": "Account deactivated successfully"
            }
            
        except AuthenticationError as e:
            logger.error(f"Authentication error in deactivate_account: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error deactivating account: {e}")
            raise DatabaseError("Failed to deactivate account")
