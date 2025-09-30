"""
Model management service for loading and initializing all AI models.
This service handles the loading of emotion detection, dialogue generation, and RAG models.
"""

import os
import asyncio
from typing import Dict, Any, Optional
from .emotion_detector import emotion_detector, load_emotion_model
from .reply_generator import reply_generator, load_reply_model
from .speech_to_text_config import get_speech_to_text_service

class ModelManager:
    """
    Manages loading and initialization of all AI models.
    """
    
    def __init__(self):
        self.models_loaded = False
        self.loading_status = {
            "emotion_detection": False,
            "dialogue_generation": False,
            "speech_to_text": False,
            "rag_system": False
        }
        self.model_errors = {}
    
    async def load_all_models(self) -> Dict[str, Any]:
        """
        Load all models asynchronously.
        
        Returns:
            Dictionary with loading results
        """
        print("Starting model loading process...")
        
        # Load models in parallel
        tasks = [
            self._load_emotion_model(),
            self._load_dialogue_model(),
            self._load_speech_to_text(),
            self._load_rag_system()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        loading_results = {
            "emotion_detection": results[0] if not isinstance(results[0], Exception) else False,
            "dialogue_generation": results[1] if not isinstance(results[1], Exception) else False,
            "speech_to_text": results[2] if not isinstance(results[2], Exception) else False,
            "rag_system": results[3] if not isinstance(results[3], Exception) else False
        }
        
        # Update status
        self.loading_status = loading_results
        self.models_loaded = any(loading_results.values())
        
        # Log results
        self._log_loading_results(loading_results)
        
        return loading_results
    
    async def _load_emotion_model(self) -> bool:
        """
        Load the emotion detection model.
        
        Returns:
            True if loaded successfully
        """
        try:
            print("Loading emotion detection model...")
            success = load_emotion_model()
            if success:
                print("✅ Emotion detection model loaded successfully")
            else:
                print("❌ Emotion detection model failed to load")
            return success
        except Exception as e:
            print(f"❌ Error loading emotion model: {e}")
            self.model_errors["emotion_detection"] = str(e)
            return False
    
    async def _load_dialogue_model(self) -> bool:
        """
        Load the dialogue generation model.
        
        Returns:
            True if loaded successfully
        """
        try:
            print("Loading dialogue generation model...")
            success = load_reply_model()
            if success:
                print("✅ Dialogue generation model loaded successfully")
            else:
                print("❌ Dialogue generation model failed to load")
            return success
        except Exception as e:
            print(f"❌ Error loading dialogue model: {e}")
            self.model_errors["dialogue_generation"] = str(e)
            return False
    
    async def _load_speech_to_text(self) -> bool:
        """
        Load the speech-to-text service.
        
        Returns:
            True if loaded successfully
        """
        try:
            print("Loading speech-to-text service...")
            service = get_speech_to_text_service()
            if service is not None:
                print("✅ Speech-to-text service loaded successfully")
                return True
            else:
                print("❌ Speech-to-text service failed to load")
                return False
        except Exception as e:
            print(f"❌ Error loading speech-to-text: {e}")
            self.model_errors["speech_to_text"] = str(e)
            return False
    
    async def _load_rag_system(self) -> bool:
        """
        Load the RAG system.
        
        Returns:
            True if loaded successfully
        """
        try:
            print("Loading RAG system...")
            # RAG system is loaded as part of the reply generator
            if reply_generator.use_rag and reply_generator.retriever is not None:
                print("✅ RAG system loaded successfully")
                return True
            else:
                print("⚠️  RAG system not available (using fallback responses)")
                return False
        except Exception as e:
            print(f"❌ Error loading RAG system: {e}")
            self.model_errors["rag_system"] = str(e)
            return False
    
    def _log_loading_results(self, results: Dict[str, bool]):
        """
        Log the model loading results.
        
        Args:
            results: Dictionary with loading results
        """
        print("\n" + "="*50)
        print("MODEL LOADING SUMMARY")
        print("="*50)
        
        for model_name, success in results.items():
            status = "✅ LOADED" if success else "❌ FAILED"
            print(f"{model_name.replace('_', ' ').title()}: {status}")
        
        if any(results.values()):
            print("\n🎉 Some models are ready for use!")
        else:
            print("\n⚠️  No models loaded successfully")
        
        print("="*50)
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Get the current status of all models.
        
        Returns:
            Dictionary with model status information
        """
        return {
            "models_loaded": self.models_loaded,
            "loading_status": self.loading_status,
            "errors": self.model_errors,
            "available_services": {
                "emotion_detection": self.loading_status.get("emotion_detection", False),
                "dialogue_generation": self.loading_status.get("dialogue_generation", False),
                "speech_to_text": self.loading_status.get("speech_to_text", False),
                "rag_system": self.loading_status.get("rag_system", False)
            }
        }
    
    def is_ready_for_production(self) -> bool:
        """
        Check if the system is ready for production use.
        
        Returns:
            True if at least basic services are available
        """
        # Need at least speech-to-text and some form of response generation
        return (
            self.loading_status.get("speech_to_text", False) and
            (self.loading_status.get("dialogue_generation", False) or 
             self.loading_status.get("emotion_detection", False))
        )

# Global model manager instance
model_manager = ModelManager()

async def initialize_models() -> Dict[str, Any]:
    """
    Initialize all models.
    
    Returns:
        Dictionary with initialization results
    """
    return await model_manager.load_all_models()

def get_model_status() -> Dict[str, Any]:
    """
    Get the current model status.
    
    Returns:
        Dictionary with model status
    """
    return model_manager.get_model_status()

def is_system_ready() -> bool:
    """
    Check if the system is ready for use.
    
    Returns:
        True if system is ready
    """
    return model_manager.is_ready_for_production()
