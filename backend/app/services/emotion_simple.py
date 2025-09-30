"""
Simplified emotion detection service for development.
This version doesn't require SpeechBrain and heavy ML dependencies.
"""

import random

# Simple emotion detection without ML dependencies
def detect_emotion(audio_data):
    """
    Simplified emotion detection that returns random emotions for development.
    In production, this would use the actual SpeechBrain model.
    
    Args:
        audio_data: Raw audio data (not used in this simplified version)
    
    Returns:
        A random emotion label for testing purposes.
    """
    emotions = [
        "neutral", "happiness", "sadness", "anger", 
        "surprise", "frustration", "fear", "disgust", "excitement"
    ]
    
    # Return a random emotion for development
    return random.choice(emotions)

def load_emotion_model():
    """
    Placeholder for model loading.
    In production, this would load the actual SpeechBrain model.
    """
    print("Using simplified emotion detection for development.")
    return True

