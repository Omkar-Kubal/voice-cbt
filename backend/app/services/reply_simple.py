"""
Simplified reply generation service for development.
This version doesn't require heavy ML dependencies.
"""

import random

# Simple reply generation without ML dependencies
def generate_reply(transcribed_text: str, emotion: str) -> str:
    """
    Simplified reply generation that returns predefined responses.
    In production, this would use the actual DialoGPT model.
    
    Args:
        transcribed_text: The user's transcribed speech
        emotion: The detected emotion from the emotion service
    
    Returns:
        A therapeutic response based on the emotion.
    """
    
    # Predefined responses based on emotions
    responses = {
        "happiness": [
            "I'm glad to hear you're feeling positive! What's contributing to this good mood?",
            "It's wonderful that you're experiencing joy. Can you tell me more about what's making you happy?",
            "Your positive energy is contagious! What's been going well for you lately?"
        ],
        "sadness": [
            "I can sense that you're going through a difficult time. Would you like to talk about what's been weighing on you?",
            "It's okay to feel sad sometimes. What's been on your mind lately?",
            "I'm here to listen. What's been making you feel this way?"
        ],
        "anger": [
            "I can hear the frustration in your voice. What's been making you feel this way?",
            "It sounds like you're dealing with some strong emotions. Would you like to explore what's behind these feelings?",
            "Anger can be a powerful emotion. What's been triggering these feelings for you?"
        ],
        "fear": [
            "I understand that you might be feeling anxious or worried. What's been causing you concern?",
            "It's natural to feel afraid sometimes. What's been on your mind that's causing worry?",
            "I'm here to help you work through these feelings. What's been making you feel anxious?"
        ],
        "neutral": [
            "I'm here to listen. How are you feeling today?",
            "What's on your mind? I'm here to help you explore your thoughts.",
            "How has your day been? What would you like to talk about?"
        ]
    }
    
    # Get responses for the detected emotion, fallback to neutral
    emotion_responses = responses.get(emotion, responses["neutral"])
    
    # Return a random response for the emotion
    return random.choice(emotion_responses)

def load_reply_model():
    """
    Placeholder for model loading.
    In production, this would load the actual DialoGPT model.
    """
    print("Using simplified reply generation for development.")
    return True

