"""
Security middleware for Voice CBT application.
"""

import time
import json
from typing import Callable
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

from ..core.security import security_manager

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for request filtering and monitoring."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_manager = security_manager
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through security checks."""
        start_time = time.time()
        client_ip = self._get_client_ip(request)
        
        try:
            # Check if IP is blocked
            if self.security_manager.is_ip_blocked(client_ip):
                logger.warning(f"Blocked IP attempted access: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Access denied"}
                )
            
            # Check rate limiting
            endpoint = f"{request.method}:{request.url.path}"
            if not self.security_manager.check_rate_limit(client_ip, endpoint):
                logger.warning(f"Rate limit exceeded for IP {client_ip} on {endpoint}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded"}
                )
            
            # Check for suspicious patterns
            if self._is_suspicious_request(request):
                logger.warning(f"Suspicious request from {client_ip}: {request.url}")
                self.security_manager._log_suspicious_activity(
                    "suspicious_request",
                    f"Suspicious request pattern: {request.method} {request.url.path}",
                    client_ip
                )
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            response = self._add_security_headers(response)
            
            # Log request
            self._log_request(request, response, client_ip, time.time() - start_time)
            
            return response
            
        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            self.security_manager._log_suspicious_activity(
                "middleware_error",
                f"Security middleware error: {str(e)}",
                client_ip
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address."""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def _is_suspicious_request(self, request: Request) -> bool:
        """Check if request exhibits suspicious patterns."""
        # Check for SQL injection patterns
        sql_patterns = [
            r"union\s+select", r"drop\s+table", r"delete\s+from",
            r"insert\s+into", r"update\s+set", r"exec\s*\(",
            r"script\s*>", r"<script", r"javascript:",
            r"onload\s*=", r"onerror\s*=", r"onclick\s*="
        ]
        
        # Check URL path
        for pattern in sql_patterns:
            if re.search(pattern, request.url.path, re.IGNORECASE):
                return True
        
        # Check query parameters
        for param_name, param_value in request.query_params.items():
            for pattern in sql_patterns:
                if re.search(pattern, param_value, re.IGNORECASE):
                    return True
        
        # Check for excessive path traversal
        if ".." in request.url.path:
            return True
        
        # Check for suspicious file extensions
        suspicious_extensions = [".php", ".asp", ".jsp", ".cgi", ".pl"]
        for ext in suspicious_extensions:
            if ext in request.url.path.lower():
                return True
        
        return False
    
    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response."""
        # Content Security Policy - Allow Swagger UI resources
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Other security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response
    
    def _log_request(self, request: Request, response: Response, client_ip: str, duration: float):
        """Log request details."""
        log_data = {
            "timestamp": time.time(),
            "client_ip": client_ip,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_agent": request.headers.get("User-Agent", ""),
            "referer": request.headers.get("Referer", "")
        }
        
        # Log based on status code
        if response.status_code >= 500:
            logger.error(f"Server error: {json.dumps(log_data)}")
        elif response.status_code >= 400:
            logger.warning(f"Client error: {json.dumps(log_data)}")
        else:
            logger.info(f"Request: {json.dumps(log_data)}")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for protected endpoints."""
    
    def __init__(self, app: ASGIApp, protected_paths: list = None):
        super().__init__(app)
        self.protected_paths = protected_paths or ["/api/v1/session", "/api/v1/mood"]
        self.security_manager = security_manager
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check authentication for protected paths."""
        # Skip authentication for non-protected paths
        if not any(request.url.path.startswith(path) for path in self.protected_paths):
            return await call_next(request)
        
        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authentication required"}
            )
        
        # Verify token
        token = auth_header.split(" ")[1]
        payload = self.security_manager.verify_token(token)
        
        if not payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )
        
        # Add user info to request state
        request.state.user = payload
        
        return await call_next(request)

class InputValidationMiddleware(BaseHTTPMiddleware):
    """Input validation middleware."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_manager = security_manager
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate input data."""
        # Validate request size
        content_length = request.headers.get("Content-Length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"detail": "Request too large"}
            )
        
        # Validate audio data for audio endpoints
        if request.url.path.startswith("/api/v1/session/start"):
            try:
                body = await request.body()
                if body:
                    data = json.loads(body)
                    audio_data = data.get("audio_data", "")
                    
                    if audio_data and not self.security_manager.validate_audio_data(audio_data):
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={"detail": "Invalid audio data format"}
                        )
            except (json.JSONDecodeError, KeyError):
                pass  # Let the endpoint handle validation errors
        
        return await call_next(request)

# Import regex for pattern matching
import re
