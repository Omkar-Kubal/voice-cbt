import pyttsx3
import os

def synthesize_speech(text: str, output_path: str = "response.mp3"):
    """
    Synthesizes speech from a given text string and saves it to a file.

    Args:
        text: The text to be converted to speech.
        output_path: The file path to save the synthesized audio.
    """
    engine = pyttsx3.init()
    
    # You can customize the voice, rate, and volume here
    # engine.setProperty('rate', 150)    # Speed of speech
    # engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    print(f"Speech synthesized and saved to {output_path}")

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