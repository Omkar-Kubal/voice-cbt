"""
Advanced security features for Voice CBT application.
"""

import os
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import re
import ipaddress
from functools import wraps
import time

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Security settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))

# In-memory storage for security tracking (use Redis in production)
_login_attempts = {}
_rate_limit_tracker = {}
_blocked_ips = set()
_suspicious_activities = []

class SecurityManager:
    """Advanced security manager for the application."""
    
    def __init__(self):
        self.pwd_context = pwd_context
        self.jwt_secret = JWT_SECRET_KEY
        self.jwt_algorithm = JWT_ALGORITHM
    
    # Password Security
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength."""
        issues = []
        score = 0
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        else:
            score += 1
        
        if not re.search(r'[A-Z]', password):
            issues.append("Password must contain at least one uppercase letter")
        else:
            score += 1
        
        if not re.search(r'[a-z]', password):
            issues.append("Password must contain at least one lowercase letter")
        else:
            score += 1
        
        if not re.search(r'\d', password):
            issues.append("Password must contain at least one digit")
        else:
            score += 1
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Password must contain at least one special character")
        else:
            score += 1
        
        # Check for common patterns
        common_patterns = [
            r'(.)\1{2,}',  # Repeated characters
            r'123|abc|qwe',  # Sequential patterns
            r'password|admin|user',  # Common words
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                issues.append("Password contains common patterns")
                score -= 1
                break
        
        strength_levels = {
            0: "Very Weak",
            1: "Weak", 
            2: "Fair",
            3: "Good",
            4: "Strong",
            5: "Very Strong"
        }
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "score": max(0, score),
            "strength": strength_levels.get(max(0, score), "Unknown")
        }
    
    # JWT Token Management
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh a JWT token if it's still valid."""
        payload = self.verify_token(token)
        if payload and payload.get("exp", 0) > datetime.utcnow().timestamp():
            # Create new token with same data but new expiry
            new_token = self.create_access_token(
                {"sub": payload.get("sub"), "user_id": payload.get("user_id")}
            )
            return new_token
        return None
    
    # Rate Limiting
    def check_rate_limit(self, client_ip: str, endpoint: str) -> bool:
        """Check if client has exceeded rate limit."""
        key = f"{client_ip}:{endpoint}"
        current_time = time.time()
        
        if key not in _rate_limit_tracker:
            _rate_limit_tracker[key] = []
        
        # Clean old entries
        _rate_limit_tracker[key] = [
            timestamp for timestamp in _rate_limit_tracker[key]
            if current_time - timestamp < RATE_LIMIT_WINDOW
        ]
        
        # Check if limit exceeded
        if len(_rate_limit_tracker[key]) >= RATE_LIMIT_REQUESTS:
            return False
        
        # Add current request
        _rate_limit_tracker[key].append(current_time)
        return True
    
    # Login Security
    def record_login_attempt(self, client_ip: str, username: str, success: bool):
        """Record login attempt for security tracking."""
        key = f"{client_ip}:{username}"
        current_time = datetime.utcnow()
        
        if key not in _login_attempts:
            _login_attempts[key] = {"attempts": 0, "last_attempt": None, "locked_until": None}
        
        attempt_data = _login_attempts[key]
        
        if success:
            # Reset on successful login
            attempt_data["attempts"] = 0
            attempt_data["last_attempt"] = current_time
            attempt_data["locked_until"] = None
        else:
            # Increment failed attempts
            attempt_data["attempts"] += 1
            attempt_data["last_attempt"] = current_time
            
            # Lock account if too many attempts
            if attempt_data["attempts"] >= MAX_LOGIN_ATTEMPTS:
                attempt_data["locked_until"] = current_time + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
                self._log_suspicious_activity(
                    "account_locked",
                    f"Account locked due to {attempt_data['attempts']} failed login attempts",
                    client_ip
                )
    
    def is_account_locked(self, client_ip: str, username: str) -> bool:
        """Check if account is locked due to failed attempts."""
        key = f"{client_ip}:{username}"
        
        if key not in _login_attempts:
            return False
        
        attempt_data = _login_attempts[key]
        
        if attempt_data["locked_until"] and datetime.utcnow() < attempt_data["locked_until"]:
            return True
        
        # Unlock if lockout period has passed
        if attempt_data["locked_until"] and datetime.utcnow() >= attempt_data["locked_until"]:
            attempt_data["locked_until"] = None
            attempt_data["attempts"] = 0
        
        return False
    
    # IP Security
    def is_ip_blocked(self, client_ip: str) -> bool:
        """Check if IP is blocked."""
        return client_ip in _blocked_ips
    
    def block_ip(self, client_ip: str, reason: str):
        """Block an IP address."""
        _blocked_ips.add(client_ip)
        self._log_suspicious_activity("ip_blocked", reason, client_ip)
    
    def unblock_ip(self, client_ip: str):
        """Unblock an IP address."""
        _blocked_ips.discard(client_ip)
    
    def is_suspicious_ip(self, client_ip: str) -> bool:
        """Check if IP exhibits suspicious behavior."""
        # Check for rapid requests from same IP
        recent_requests = [
            timestamp for timestamp in _rate_limit_tracker.get(client_ip, [])
            if time.time() - timestamp < 60  # Last minute
        ]
        
        return len(recent_requests) > 50  # More than 50 requests per minute
    
    # Input Validation
    def sanitize_input(self, input_string: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_string)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    def validate_audio_data(self, audio_data: str) -> bool:
        """Validate audio data format and size."""
        try:
            import base64
            # Decode base64
            decoded = base64.b64decode(audio_data)
            
            # Check size (max 50MB)
            if len(decoded) > 50 * 1024 * 1024:
                return False
            
            # Check if it's valid audio format (basic check)
            if decoded[:4] in [b'RIFF', b'ID3 ', b'\xff\xfb', b'\xff\xf3']:
                return True
            
            return False
        except Exception:
            return False
    
    # Security Logging
    def _log_suspicious_activity(self, activity_type: str, description: str, client_ip: str):
        """Log suspicious activity."""
        activity = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": activity_type,
            "description": description,
            "client_ip": client_ip
        }
        _suspicious_activities.append(activity)
        
        # Keep only last 1000 activities
        if len(_suspicious_activities) > 1000:
            _suspicious_activities.pop(0)
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get security report."""
        current_time = datetime.utcnow()
        
        # Count recent suspicious activities
        recent_activities = [
            activity for activity in _suspicious_activities
            if (current_time - datetime.fromisoformat(activity["timestamp"])).total_seconds() < 3600
        ]
        
        return {
            "blocked_ips": len(_blocked_ips),
            "recent_suspicious_activities": len(recent_activities),
            "active_rate_limits": len(_rate_limit_tracker),
            "locked_accounts": len([
                key for key, data in _login_attempts.items()
                if data.get("locked_until") and current_time < data["locked_until"]
            ]),
            "recent_activities": recent_activities[-10:]  # Last 10 activities
        }

# Global security manager instance
security_manager = SecurityManager()

# FastAPI Security Dependencies
security_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> Dict[str, Any]:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = security_manager.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

def require_authentication(func):
    """Decorator to require authentication."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This would be used with FastAPI dependency injection
        return await func(*args, **kwargs)
    return wrapper

def rate_limit_check(client_ip: str, endpoint: str):
    """Check rate limit for endpoint."""
    if not security_manager.check_rate_limit(client_ip, endpoint):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )

def security_headers_middleware(request: Request, call_next):
    """Add security headers to responses."""
    response = call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response

# Legacy functions for backward compatibility
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Legacy function for password verification."""
    return security_manager.verify_password(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Legacy function for password hashing."""
    return security_manager.hash_password(password)