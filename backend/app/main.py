from fastapi import FastAPI
from app.api.audio import router as audio_router

app = FastAPI(title="Voice-CBT")
app.include_router(audio_router, prefix="/api")