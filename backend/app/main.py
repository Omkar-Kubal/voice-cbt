from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .api import audio, mood, monitoring
from .middleware.security_middleware import SecurityMiddleware, AuthenticationMiddleware, InputValidationMiddleware
from .core.security import security_manager

app = FastAPI(
    title="Voice-Activated CBT",
    description="A voice-driven AI system for simulated CBT and mindfulness sessions.",
    version="0.1.0",
)

# Set up CORS middleware to allow cross-origin requests from your frontend.
# This is necessary because your frontend and backend will be on different ports/origins
# (e.g., frontend on 3000, backend on 8000/8080).
origins = [
    "http://localhost",
    "http://localhost:3000",  # Replace with your actual frontend URL
    "http://192.168.29.185:8080"
]

# Add security middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(InputValidationMiddleware)
app.add_middleware(AuthenticationMiddleware, protected_paths=["/api/v1/session", "/api/v1/mood"])

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for different modules
app.include_router(audio.router, prefix="/api/v1")
app.include_router(mood.router, prefix="/api/v1")
app.include_router(monitoring.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voice-Activated Emotionally Adaptive Therapy System API!"}

# Model initialization at startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Voice CBT Application Starting...")
    print("Loading AI models and services...")
    
    try:
        # Import and initialize model manager
        from .services.model_manager import initialize_models, get_model_status
        
        # Load all models
        loading_results = await initialize_models()
        
        # Get final status
        status = get_model_status()
        
        print("\n" + "="*60)
        print("🎯 VOICE CBT SYSTEM STATUS")
        print("="*60)
        
        for service, loaded in status["available_services"].items():
            status_icon = "✅" if loaded else "❌"
            print(f"{status_icon} {service.replace('_', ' ').title()}")
        
        if status["models_loaded"]:
            print("\n🎉 Voice CBT is ready for voice interactions!")
        else:
            print("\n⚠️  Some services are not available, but basic functionality should work.")
        
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during model initialization: {e}")
        print("⚠️  Application will start with limited functionality.")

@app.get("/health")
def health_check():
    """Health check endpoint with model status."""
    from .services.model_manager import get_model_status, is_system_ready
    
    status = get_model_status()
    return {
        "status": "healthy" if is_system_ready() else "degraded",
        "models": status["available_services"],
        "ready": is_system_ready()
    }

@app.get("/security/status")
def security_status():
    """Security status endpoint."""
    return security_manager.get_security_report()

@app.post("/security/block-ip")
def block_ip(ip_address: str, reason: str):
    """Block an IP address (admin only)."""
    security_manager.block_ip(ip_address, reason)
    return {"message": f"IP {ip_address} blocked", "reason": reason}

@app.post("/security/unblock-ip")
def unblock_ip(ip_address: str):
    """Unblock an IP address (admin only)."""
    security_manager.unblock_ip(ip_address)
    return {"message": f"IP {ip_address} unblocked"}