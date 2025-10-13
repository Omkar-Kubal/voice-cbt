"""
Emotion Model Manager
Handles downloading, loading, and managing emotion detection models.
"""

import os
import torch
import torch.nn as nn
import torchaudio
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SimpleEmotionCNN(nn.Module):
    """
    Simple CNN for emotion detection from audio spectrograms.
    This is a lightweight model that can be trained or used as a baseline.
    """
    
    def __init__(self, num_classes: int = 7, input_size: int = 128):
        super(SimpleEmotionCNN, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.5)
        
        # Calculate the size after convolutions
        # Assuming input is 128x128 (adjust based on your spectrogram size)
        self.fc1 = nn.Linear(128 * 16 * 16, 512)  # Adjust based on actual size
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, num_classes)
        
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.fc3(x)
        
        return self.softmax(x)

class EmotionModelManager:
    """
    Manages emotion detection models.
    """
    
    def __init__(self, model_dir: str = "./trained_models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'
        ]
        
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def create_placeholder_model(self) -> bool:
        """Create a placeholder model for testing."""
        try:
            model = SimpleEmotionCNN(num_classes=len(self.emotion_labels))
            
            # Save the model
            model_path = self.model_dir / "simple_emotion_model.pth"
            torch.save({
                'model_state_dict': model.state_dict(),
                'emotion_labels': self.emotion_labels,
                'model_type': 'SimpleEmotionCNN'
            }, model_path)
            
            logger.info(f"Placeholder model created at {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating placeholder model: {e}")
            return False
    
    def load_model(self, model_path: str) -> bool:
        """Load a trained emotion detection model."""
        try:
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found: {model_path}")
                return False
            
            checkpoint = torch.load(model_path, map_location=self.device)
            
            if 'model_type' in checkpoint and checkpoint['model_type'] == 'SimpleEmotionCNN':
                self.model = SimpleEmotionCNN(num_classes=len(self.emotion_labels))
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.to(self.device)
                self.model.eval()
                
                logger.info(f"Model loaded successfully from {model_path}")
                return True
            else:
                logger.warning(f"Unknown model type in {model_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def preprocess_audio(self, audio_path: str) -> torch.Tensor:
        """Preprocess audio file for emotion detection."""
        try:
            # Load audio
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Resample to 16kHz if needed
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(sample_rate, 16000)
                waveform = resampler(waveform)
            
            # Convert to spectrogram
            spectrogram = torchaudio.transforms.MelSpectrogram(
                sample_rate=16000,
                n_mels=128,
                n_fft=1024,
                hop_length=512
            )(waveform)
            
            # Convert to log scale
            log_spectrogram = torch.log(spectrogram + 1e-8)
            
            # Resize to fixed size (128x128)
            log_spectrogram = torch.nn.functional.interpolate(
                log_spectrogram.unsqueeze(0),
                size=(128, 128),
                mode='bilinear',
                align_corners=False
            ).squeeze(0)
            
            return log_spectrogram.unsqueeze(0)  # Add batch dimension
            
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            return torch.zeros(1, 1, 128, 128)
    
    def predict_emotion(self, audio_path: str) -> Dict[str, float]:
        """Predict emotion from audio file."""
        if self.model is None:
            logger.warning("No model loaded, returning neutral emotion")
            return {'neutral': 1.0}
        
        try:
            # Preprocess audio
            input_tensor = self.preprocess_audio(audio_path)
            input_tensor = input_tensor.to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = outputs.cpu().numpy()[0]
            
            # Convert to emotion dictionary
            emotions = {}
            for i, emotion in enumerate(self.emotion_labels):
                emotions[emotion] = float(probabilities[i])
            
            return emotions
            
        except Exception as e:
            logger.error(f"Error predicting emotion: {e}")
            return {'neutral': 1.0}
    
    def get_model_status(self) -> Dict[str, any]:
        """Get the status of the emotion detection model."""
        return {
            'model_loaded': self.model is not None,
            'model_path': str(self.model_dir),
            'device': str(self.device),
            'emotion_labels': self.emotion_labels,
            'available_models': list(self.model_dir.glob("*.pth"))
        }

# Global model manager instance
model_manager = EmotionModelManager()

def initialize_emotion_models() -> bool:
    """Initialize emotion detection models."""
    try:
        # Create placeholder model if none exists
        model_path = model_manager.model_dir / "simple_emotion_model.pth"
        if not model_path.exists():
            logger.info("Creating placeholder emotion model...")
            model_manager.create_placeholder_model()
        
        # Try to load the model
        success = model_manager.load_model(str(model_path))
        
        if success:
            logger.info("Emotion detection model loaded successfully")
        else:
            logger.warning("Emotion detection model not available")
        
        return success
        
    except Exception as e:
        logger.error(f"Error initializing emotion models: {e}")
        return False

def detect_emotion_with_model(audio_path: str) -> Dict[str, float]:
    """Detect emotion using the loaded model."""
    return model_manager.predict_emotion(audio_path)

def get_emotion_model_status() -> Dict[str, any]:
    """Get emotion model status."""
    return model_manager.get_model_status()
