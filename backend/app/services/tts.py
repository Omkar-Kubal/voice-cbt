import pyttsx3
import os
import requests
import json
from typing import Optional

def synthesize_speech(text: str, output_path: str = "response.mp3", use_google: bool = False):
    """
    Synthesizes speech from a given text string and saves it to a file.
    Uses pyttsx3 by default, Google TTS as backup.

    Args:
        text: The text to be converted to speech.
        output_path: The file path to save the synthesized audio.
        use_google: Whether to use Google TTS instead of pyttsx3.
    """
    if use_google:
        return synthesize_with_google_tts(text, output_path)
    else:
        return synthesize_with_pyttsx3(text, output_path)

def synthesize_with_pyttsx3(text: str, output_path: str):
    """
    Synthesizes speech using pyttsx3 (local, free).
    """
    try:
        engine = pyttsx3.init()
        
        # Configure voice settings for better quality
        voices = engine.getProperty('voices')
        if voices:
            # Try to find a female voice (usually sounds more natural for CBT)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        engine.setProperty('rate', 180)    # Speed of speech (words per minute)
        engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
        
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        print(f"Speech synthesized with pyttsx3 and saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error with pyttsx3: {e}")
        return False

def synthesize_with_google_tts(text: str, output_path: str):
    """
    Synthesizes speech using Google TTS (free, online).
    """
    try:
        # Google TTS API (free tier)
        url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        
        # This is a simplified version - you'd need to set up Google Cloud credentials
        # For now, we'll fall back to pyttsx3
        print("Google TTS not configured, falling back to pyttsx3")
        return synthesize_with_pyttsx3(text, output_path)
        
    except Exception as e:
        print(f"Error with Google TTS: {e}")
        return False

def get_available_voices():
    """
    Prints a list of available voices on the system.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender}")

if __name__ == '__main__':
    # Example usage
    sample_text = "Hello, I am your voice-activated CBT assistant. How are you feeling today?"
    synthesize_speech(sample_text)
    get_available_voices()