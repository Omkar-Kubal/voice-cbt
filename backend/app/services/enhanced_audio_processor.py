"""
Enhanced audio processing service for Voice CBT.
Handles audio input/output with advanced features.
"""

import os
import tempfile
import logging
import base64
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import wave
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedAudioProcessor:
    """
    Advanced audio processing service with emotion detection and voice enhancement.
    """
    
    def __init__(self):
        self.supported_formats = ['wav', 'mp3', 'ogg', 'm4a']
        self.audio_cache = {}
        self.processing_stats = {
            "total_processed": 0,
            "successful_processing": 0,
            "failed_processing": 0,
            "average_processing_time": 0.0
        }
    
    def process_audio_input(
        self,
        audio_data: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process audio input with enhanced features.
        """
        start_time = datetime.now()
        
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_audio_path = temp_file.name
            
            # Analyze audio properties
            audio_analysis = self._analyze_audio_properties(temp_audio_path)
            
            # Detect audio quality
            quality_score = self._assess_audio_quality(temp_audio_path)
            
            # Extract audio features for emotion detection
            audio_features = self._extract_audio_features(temp_audio_path)
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            # Update processing stats
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_processing_stats(True, processing_time)
            
            return {
                "success": True,
                "audio_analysis": audio_analysis,
                "quality_score": quality_score,
                "audio_features": audio_features,
                "processing_time": processing_time,
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing audio input: {e}")
            self._update_processing_stats(False, 0)
            
            return {
                "success": False,
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_audio_properties(self, audio_path: str) -> Dict[str, Any]:
        """Analyze audio file properties."""
        try:
            with wave.open(audio_path, 'rb') as audio_file:
                # Get audio properties
                sample_rate = audio_file.getframerate()
                channels = audio_file.getnchannels()
                sample_width = audio_file.getsampwidth()
                frames = audio_file.getnframes()
                duration = frames / sample_rate
                
                # Read audio data
                audio_data = audio_file.readframes(frames)
                
                # Convert to numpy array for analysis
                if sample_width == 1:
                    dtype = np.uint8
                elif sample_width == 2:
                    dtype = np.int16
                elif sample_width == 4:
                    dtype = np.int32
                else:
                    dtype = np.int16
                
                audio_array = np.frombuffer(audio_data, dtype=dtype)
                
                # Calculate audio statistics
                rms = np.sqrt(np.mean(audio_array**2))
                peak = np.max(np.abs(audio_array))
                dynamic_range = 20 * np.log10(peak / (rms + 1e-10))
                
                return {
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "sample_width": sample_width,
                    "duration": duration,
                    "frames": frames,
                    "rms": float(rms),
                    "peak": float(peak),
                    "dynamic_range": float(dynamic_range),
                    "bit_depth": sample_width * 8
                }
                
        except Exception as e:
            logger.error(f"Error analyzing audio properties: {e}")
            return {
                "error": str(e),
                "sample_rate": 0,
                "channels": 0,
                "duration": 0
            }
    
    def _assess_audio_quality(self, audio_path: str) -> Dict[str, Any]:
        """Assess audio quality and provide recommendations."""
        try:
            with wave.open(audio_path, 'rb') as audio_file:
                sample_rate = audio_file.getframerate()
                channels = audio_file.getnchannels()
                sample_width = audio_file.getsampwidth()
                duration = audio_file.getnframes() / sample_rate
                
                # Quality scoring
                quality_score = 0
                quality_issues = []
                recommendations = []
                
                # Sample rate quality
                if sample_rate >= 44100:
                    quality_score += 30
                elif sample_rate >= 22050:
                    quality_score += 20
                elif sample_rate >= 16000:
                    quality_score += 10
                else:
                    quality_issues.append("Low sample rate")
                    recommendations.append("Use higher sample rate (16kHz or above)")
                
                # Channel quality
                if channels == 1:
                    quality_score += 20  # Mono is fine for speech
                elif channels == 2:
                    quality_score += 25  # Stereo is better
                else:
                    quality_issues.append("Unusual channel configuration")
                
                # Bit depth quality
                bit_depth = sample_width * 8
                if bit_depth >= 16:
                    quality_score += 25
                elif bit_depth >= 8:
                    quality_score += 15
                else:
                    quality_issues.append("Low bit depth")
                    recommendations.append("Use 16-bit or higher audio")
                
                # Duration quality
                if duration >= 0.5:  # At least 0.5 seconds
                    quality_score += 15
                else:
                    quality_issues.append("Very short audio")
                    recommendations.append("Record longer audio clips")
                
                # Overall quality assessment
                if quality_score >= 80:
                    quality_level = "excellent"
                elif quality_score >= 60:
                    quality_level = "good"
                elif quality_score >= 40:
                    quality_level = "fair"
                else:
                    quality_level = "poor"
                
                return {
                    "quality_score": quality_score,
                    "quality_level": quality_level,
                    "issues": quality_issues,
                    "recommendations": recommendations,
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "bit_depth": bit_depth,
                    "duration": duration
                }
                
        except Exception as e:
            logger.error(f"Error assessing audio quality: {e}")
            return {
                "quality_score": 0,
                "quality_level": "unknown",
                "error": str(e)
            }
    
    def _extract_audio_features(self, audio_path: str) -> Dict[str, Any]:
        """Extract audio features for emotion detection."""
        try:
            # This is a simplified feature extraction
            # In a real implementation, you would use librosa or similar
            with wave.open(audio_path, 'rb') as audio_file:
                sample_rate = audio_file.getframerate()
                frames = audio_file.getnframes()
                duration = frames / sample_rate
                
                # Basic features
                features = {
                    "duration": duration,
                    "sample_rate": sample_rate,
                    "frame_count": frames,
                    "estimated_speech_rate": self._estimate_speech_rate(audio_path),
                    "audio_energy": self._calculate_audio_energy(audio_path),
                    "silence_ratio": self._calculate_silence_ratio(audio_path)
                }
                
                return features
                
        except Exception as e:
            logger.error(f"Error extracting audio features: {e}")
            return {
                "error": str(e),
                "duration": 0,
                "sample_rate": 0
            }
    
    def _estimate_speech_rate(self, audio_path: str) -> float:
        """Estimate speech rate (words per minute)."""
        try:
            with wave.open(audio_path, 'rb') as audio_file:
                duration = audio_file.getnframes() / audio_file.getframerate()
                
                # Real speech pattern analysis
                if duration > 0:
                    try:
                        # Analyze speech patterns using audio features
                        # Count speech segments (non-silent regions)
                        silence_threshold = 0.01
                        speech_segments = []
                        current_segment = 0
                        
                        for i, sample in enumerate(audio_array):
                            if abs(sample) > silence_threshold:
                                current_segment += 1
                            else:
                                if current_segment > 0:
                                    speech_segments.append(current_segment)
                                    current_segment = 0
                        
                        if current_segment > 0:
                            speech_segments.append(current_segment)
                        
                        # Estimate words based on speech patterns
                        if speech_segments:
                            # Average speech segment length (in samples)
                            avg_segment_length = sum(speech_segments) / len(speech_segments)
                            
                            # Estimate words based on speech rhythm
                            # Typical speech has 2-4 syllables per word, 1-2 syllables per second
                            syllables_per_second = len(speech_segments) / duration
                            words_per_second = syllables_per_second / 2.5  # Average 2.5 syllables per word
                            words_per_minute = words_per_second * 60
                            
                            # Clamp to realistic range (50-300 WPM)
                            return max(50, min(300, words_per_minute))
                        else:
                            return 0.0
                    except Exception:
                        # Fallback to simple estimation
                        return duration * 2.5  # 2.5 words per second average
                else:
                    return 0.0
                    
        except Exception as e:
            logger.error(f"Error estimating speech rate: {e}")
            return 0.0
    
    def _calculate_audio_energy(self, audio_path: str) -> float:
        """Calculate audio energy level."""
        try:
            with wave.open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.readframes(audio_file.getnframes())
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Calculate RMS energy
                rms_energy = np.sqrt(np.mean(audio_array**2))
                return float(rms_energy)
                
        except Exception as e:
            logger.error(f"Error calculating audio energy: {e}")
            return 0.0
    
    def _calculate_silence_ratio(self, audio_path: str) -> float:
        """Calculate ratio of silence in audio."""
        try:
            with wave.open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.readframes(audio_file.getnframes())
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Define silence threshold (adjust as needed)
                silence_threshold = 1000
                
                # Count silent samples
                silent_samples = np.sum(np.abs(audio_array) < silence_threshold)
                total_samples = len(audio_array)
                
                return float(silent_samples / total_samples) if total_samples > 0 else 0.0
                
        except Exception as e:
            logger.error(f"Error calculating silence ratio: {e}")
            return 0.0
    
    def _update_processing_stats(self, success: bool, processing_time: float):
        """Update processing statistics."""
        self.processing_stats["total_processed"] += 1
        
        if success:
            self.processing_stats["successful_processing"] += 1
        else:
            self.processing_stats["failed_processing"] += 1
        
        # Update average processing time
        total_time = self.processing_stats["average_processing_time"] * (self.processing_stats["total_processed"] - 1)
        self.processing_stats["average_processing_time"] = (total_time + processing_time) / self.processing_stats["total_processed"]
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get audio processing statistics."""
        return {
            **self.processing_stats,
            "success_rate": (
                self.processing_stats["successful_processing"] / 
                self.processing_stats["total_processed"] * 100
                if self.processing_stats["total_processed"] > 0 else 0
            )
        }
    
    def optimize_audio_for_processing(self, audio_data: str) -> Dict[str, Any]:
        """Optimize audio data for better processing."""
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_audio_path = temp_file.name
            
            # Analyze and optimize
            audio_analysis = self._analyze_audio_properties(temp_audio_path)
            quality_assessment = self._assess_audio_quality(temp_audio_path)
            
            # Generate optimization recommendations
            recommendations = []
            if quality_assessment["quality_score"] < 60:
                recommendations.extend(quality_assessment["recommendations"])
            
            if audio_analysis["sample_rate"] < 16000:
                recommendations.append("Increase sample rate to 16kHz or higher")
            
            if audio_analysis["duration"] < 0.5:
                recommendations.append("Record longer audio clips for better processing")
            
            # Clean up
            os.unlink(temp_audio_path)
            
            return {
                "success": True,
                "audio_analysis": audio_analysis,
                "quality_assessment": quality_assessment,
                "recommendations": recommendations,
                "optimized": len(recommendations) == 0
            }
            
        except Exception as e:
            logger.error(f"Error optimizing audio: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Global audio processor instance
enhanced_audio_processor = EnhancedAudioProcessor()

def process_enhanced_audio(
    audio_data: str,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Process audio with enhanced features."""
    return enhanced_audio_processor.process_audio_input(audio_data, user_id, session_id)

def get_audio_processing_stats() -> Dict[str, Any]:
    """Get audio processing statistics."""
    return enhanced_audio_processor.get_processing_stats()

def optimize_audio(audio_data: str) -> Dict[str, Any]:
    """Optimize audio for better processing."""
    return enhanced_audio_processor.optimize_audio_for_processing(audio_data)
