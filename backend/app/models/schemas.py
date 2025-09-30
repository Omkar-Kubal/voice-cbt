from pydantic import BaseModel
from typing import Optional, List

# Schema for the incoming audio data
class AudioRequest(BaseModel):
    # This will likely be a base64 encoded string or a URL to an audio file
    audio_data: str

# Schema for the API response after processing
class TherapeuticResponse(BaseModel):
    response_text: str
    emotion: str
    timestamp: str

# Schema for storing historical mood data
class MoodEntry(BaseModel):
    timestamp: str
    emotion_label: str
    confidence: float

class MoodHistory(BaseModel):
    user_id: str
    mood_trend: List[MoodEntry]