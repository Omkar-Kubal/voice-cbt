"""
Enhanced Emotion Detection Service
Supports multiple emotion detection approaches:
1. Audio-based emotion detection (CREMA-D style)
2. Text-based emotion detection
3. Hybrid approach combining both
"""

import torch
import torch.nn as nn
import torchaudio
import numpy as np
import librosa
from typing import Dict, List, Tuple, Optional
import os
import logging

logger = logging.getLogger(__name__)

class SimpleEmotionDetector:
    """
    Simple emotion detector using audio features and basic ML.
    This is a lightweight alternative to complex models.
    """
    
    def __init__(self):
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'
        ]
        self.sample_rate = 16000
        
    def extract_audio_features(self, audio_path: str) -> np.ndarray:
        """Extract basic audio features for emotion detection."""
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Extract features
            features = []
            
            # 1. MFCC features
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            features.extend(np.mean(mfccs, axis=1))
            features.extend(np.std(mfccs, axis=1))
            
            # 2. Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)
            features.extend([np.mean(spectral_centroids), np.std(spectral_centroids)])
            
            # 3. Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(audio)
            features.extend([np.mean(zcr), np.std(zcr)])
            
            # 4. Chroma features
            chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
            features.extend(np.mean(chroma, axis=1))
            
            # 5. Spectral rolloff
            rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
            features.extend([np.mean(rolloff), np.std(rolloff)])
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            return np.zeros(50)  # Return zero features if error
    
    def detect_emotion_from_audio(self, audio_path: str) -> Dict[str, float]:
        """
        Detect emotion from audio file using simple feature-based approach.
        Returns probability distribution over emotions.
        """
        try:
            features = self.extract_audio_features(audio_path)
            
            # Simple rule-based emotion detection
            # This is a basic implementation - in production, you'd use a trained model
            
            # Analyze features to determine emotion
            emotion_scores = {}
            
            # High energy + high pitch -> happy/excited
            if features[0] > 0.5 and features[2] > 0.3:
                emotion_scores['happy'] = 0.7
                emotion_scores['surprise'] = 0.3
            # Low energy + low pitch -> sad
            elif features[0] < -0.5 and features[2] < -0.3:
                emotion_scores['sad'] = 0.8
                emotion_scores['neutral'] = 0.2
            # High zero crossing rate -> angry
            elif features[4] > 0.5:
                emotion_scores['angry'] = 0.6
                emotion_scores['fear'] = 0.4
            # Medium values -> neutral
            else:
                emotion_scores['neutral'] = 0.9
                emotion_scores['happy'] = 0.1
            
            # Normalize scores
            total = sum(emotion_scores.values())
            if total > 0:
                emotion_scores = {k: v/total for k, v in emotion_scores.items()}
            
            return emotion_scores
            
        except Exception as e:
            logger.error(f"Error in emotion detection: {e}")
            return {'neutral': 1.0}

class TextEmotionDetector:
    """
    Detect emotions from text using keyword analysis and sentiment.
    """
    
    def __init__(self):
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'love', 'smile'],
            'sad': ['sad', 'depressed', 'down', 'lonely', 'hurt', 'cry', 'tears', 'grief'],
            'angry': ['angry', 'mad', 'furious', 'rage', 'hate', 'annoyed', 'frustrated'],
            'fear': ['scared', 'afraid', 'fear', 'worried', 'anxious', 'nervous', 'panic'],
            'surprise': ['surprised', 'shocked', 'amazed', 'wow', 'unexpected'],
            'disgust': ['disgusted', 'gross', 'sick', 'revolted', 'nauseated']
        }
    
    def detect_emotion_from_text(self, text: str) -> Dict[str, float]:
        """Detect emotion from text using keyword matching."""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Add neutral if no emotions detected
        if sum(emotion_scores.values()) == 0:
            emotion_scores['neutral'] = 1.0
        else:
            # Normalize scores
            total = sum(emotion_scores.values())
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        return emotion_scores

class HybridEmotionDetector:
    """
    Hybrid emotion detector combining audio and text analysis.
    """
    
    def __init__(self):
        self.audio_detector = SimpleEmotionDetector()
        self.text_detector = TextEmotionDetector()
    
    def detect_emotion(self, audio_path: Optional[str] = None, text: Optional[str] = None) -> Dict[str, float]:
        """
        Detect emotion using both audio and text if available.
        """
        audio_emotions = {}
        text_emotions = {}
        
        # Get audio emotions if audio provided
        if audio_path and os.path.exists(audio_path):
            audio_emotions = self.audio_detector.detect_emotion_from_audio(audio_path)
        
        # Get text emotions if text provided
        if text:
            text_emotions = self.text_detector.detect_emotion_from_text(text)
        
        # Combine results
        if audio_emotions and text_emotions:
            # Weighted combination (60% audio, 40% text)
            combined = {}
            for emotion in set(list(audio_emotions.keys()) + list(text_emotions.keys())):
                audio_score = audio_emotions.get(emotion, 0) * 0.6
                text_score = text_emotions.get(emotion, 0) * 0.4
                combined[emotion] = audio_score + text_score
            return combined
        elif audio_emotions:
            return audio_emotions
        elif text_emotions:
            return text_emotions
        else:
            return {'neutral': 1.0}
    
    def get_primary_emotion(self, emotions: Dict[str, float]) -> Tuple[str, float]:
        """Get the emotion with highest confidence."""
        if not emotions:
            return 'neutral', 0.0
        
        primary_emotion = max(emotions.items(), key=lambda x: x[1])
        return primary_emotion

# Global emotion detector instance
emotion_detector = HybridEmotionDetector()

def detect_emotion_from_audio(audio_path: str) -> Dict[str, float]:
    """Detect emotion from audio file."""
    return emotion_detector.detect_emotion(audio_path=audio_path)

def detect_emotion_from_text(text: str) -> Dict[str, float]:
    """Detect emotion from text."""
    return emotion_detector.detect_emotion(text=text)

def detect_emotion_hybrid(audio_path: Optional[str] = None, text: Optional[str] = None) -> Dict[str, float]:
    """Detect emotion using both audio and text."""
    return emotion_detector.detect_emotion(audio_path=audio_path, text=text)

def get_emotion_summary(emotions: Dict[str, float]) -> str:
    """Get a human-readable emotion summary."""
    if not emotions:
        return "No emotion detected"
    
    primary_emotion, confidence = emotion_detector.get_primary_emotion(emotions)
    
    confidence_percent = int(confidence * 100)
    
    emotion_descriptions = {
        'happy': 'positive and cheerful',
        'sad': 'sad or down',
        'angry': 'angry or frustrated',
        'fear': 'anxious or worried',
        'surprise': 'surprised or shocked',
        'disgust': 'disgusted or repulsed',
        'neutral': 'calm and neutral'
    }
    
    description = emotion_descriptions.get(primary_emotion, primary_emotion)
    return f"Detected {description} emotion ({confidence_percent}% confidence)"
