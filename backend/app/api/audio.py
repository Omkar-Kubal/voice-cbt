from fastapi import APIRouter, UploadFile, File
from typing import Dict

router = APIRouter()

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)) -> Dict[str, str]:
    # TODO: wire SpeechBrain & DialoGPT
    return {"emotion": "calm", "reply": "I hear you. How does that make you feel?"}