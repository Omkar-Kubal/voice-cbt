"""
Emotion detection service using the trained emotion model.
This service loads and uses the actual trained emotion recognition model.
"""

import os
import torch
import torch.nn as nn
import numpy as np
import librosa
from typing import Optional, Dict, Any
import pickle

class EmotionModel(nn.Module):
    """
    Simple CNN model for emotion recognition (matching the training script).
    """
    
    def __init__(self, num_classes=9):
        super(EmotionModel, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv1d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        
        # Pooling
        self.pool = nn.MaxPool1d(2)
        
        # Fully connected layers
        self.fc1 = nn.Linear(128 * 2000, 256)  # Adjusted for max_length=16000
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, num_classes)
        
        # Dropout
        self.dropout = nn.Dropout(0.5)
        
        # Activation
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # Reshape for conv1d (batch_size, channels, length)
        x = x.unsqueeze(1)
        
        # Convolutional layers
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # Fully connected layers
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.fc3(x)
        
        return x

class EmotionDetector:
    """
    Service for detecting emotions from audio using the trained model.
    """
    
    def __init__(self, model_path: str = "simple_emotion_model.pth"):
        self.model_path = model_path
        self.model = None
        self.label_encoder = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.emotion_labels = [
            "neutral", "happiness", "sadness", "anger", 
            "surprise", "frustration", "fear", "disgust", "excitement"
        ]
        
    def load_model(self) -> bool:
        """
        Load the trained emotion detection model.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.model_path):
                print(f"Model file not found: {self.model_path}")
                return False
            
            # Load the model
            self.model = EmotionModel(num_classes=len(self.emotion_labels))
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            
            print(f"Emotion detection model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            self.model = None
            return False
    
    def preprocess_audio(self, audio: np.ndarray, sample_rate: int = 16000) -> torch.Tensor:
        """
        Preprocess audio for emotion detection.
        
        Args:
            audio: Audio array
            sample_rate: Sample rate of the audio
            
        Returns:
            Preprocessed audio tensor
        """
        try:
            # Ensure audio is the right length (16 seconds at 16kHz = 16000 samples)
            max_length = 16000
            
            if len(audio) > max_length:
                audio = audio[:max_length]
            else:
                audio = np.pad(audio, (0, max_length - len(audio)), 'constant')
            
            # Convert to tensor
            audio_tensor = torch.FloatTensor(audio).unsqueeze(0)  # Add batch dimension
            
            return audio_tensor
            
        except Exception as e:
            print(f"Error preprocessing audio: {e}")
            raise
    
    def detect_emotion(self, audio: np.ndarray, sample_rate: int = 16000) -> Dict[str, Any]:
        """
        Detect emotion from audio.
        
        Args:
            audio: Audio array
            sample_rate: Sample rate of the audio
            
        Returns:
            Dictionary with emotion detection results
        """
        if self.model is None:
            if not self.load_model():
                # Return a fallback response if model loading fails
                return {
                    "emotion": "neutral",
                    "confidence": 0.0,
                    "error": "Model not loaded - using fallback"
                }
        
        try:
            # Preprocess audio
            audio_tensor = self.preprocess_audio(audio, sample_rate)
            audio_tensor = audio_tensor.to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(audio_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
                emotion_idx = predicted.item()
                confidence_score = confidence.item()
                emotion = self.emotion_labels[emotion_idx]
            
            return {
                "emotion": emotion,
                "confidence": confidence_score,
                "probabilities": probabilities.cpu().numpy()[0].tolist(),
                "error": None
            }
            
        except Exception as e:
            print(f"Error detecting emotion: {e}")
            return {
                "emotion": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def detect_emotion_from_base64(self, base64_audio: str) -> Dict[str, Any]:
        """
        Detect emotion from base64 encoded audio.
        
        Args:
            base64_audio: Base64 encoded audio string
            
        Returns:
            Dictionary with emotion detection results
        """
        try:
            # Decode base64 audio
            import base64
            audio_bytes = base64.b64decode(base64_audio)
            
            # Save to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            # Load audio
            audio, sample_rate = librosa.load(temp_path, sr=16000)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            # Detect emotion
            return self.detect_emotion(audio, sample_rate)
            
        except Exception as e:
            print(f"Error processing base64 audio: {e}")
            return {
                "emotion": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }

# Global instance
emotion_detector = EmotionDetector()

def detect_emotion(audio_data: str) -> str:
    """
    Main function to detect emotion from audio data.
    
    Args:
        audio_data: Base64 encoded audio string
        
    Returns:
        Detected emotion label
    """
    result = emotion_detector.detect_emotion_from_base64(audio_data)
    return result["emotion"]

def load_emotion_model() -> bool:
    """
    Load the emotion detection model.
    
    Returns:
        True if model loaded successfully
    """
    return emotion_detector.load_model()
