"""
Reply generation service for Voice CBT.
Provides therapeutic responses based on user input and emotional state.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ReplyGenerator:
    """
    Generates therapeutic replies for CBT sessions.
    """
    
    def __init__(self):
        self.is_initialized = False
        self.cbt_techniques = {
            "cognitive_restructuring": [
                "Let's examine the evidence for this thought. What facts support it?",
                "What would you tell a friend who had this same thought?",
                "Are there alternative ways to look at this situation?"
            ],
            "mindfulness": [
                "Let's take a moment to breathe and ground ourselves.",
                "Notice what you're feeling right now without judgment.",
                "What sensations do you notice in your body?"
            ],
            "behavioral_activation": [
                "What's one small step you could take today?",
                "What activities usually bring you joy or satisfaction?",
                "How can we break this down into manageable pieces?"
            ]
        }
    
    def initialize(self) -> bool:
        """Initialize the reply generator."""
        try:
            self.is_initialized = True
            logger.info("Reply generator initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize reply generator: {e}")
            return False
    
    def generate_reply(self, 
                      user_input: str, 
                      emotion: str = "neutral", 
                      intensity: float = 0.5,
                      context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a therapeutic reply based on user input and emotional state.
        
        Args:
            user_input: User's text input
            emotion: Detected emotion
            intensity: Emotion intensity (0-1)
            context: Additional context information
            
        Returns:
            Generated therapeutic reply
        """
        if not self.is_initialized:
            return "I'm here to help you work through this. Can you tell me more about what you're experiencing?"
        
        try:
            # Select appropriate CBT technique based on emotion and input
            technique = self._select_technique(emotion, intensity, user_input)
            
            # Generate contextual response
            if technique == "cognitive_restructuring":
                return self._generate_cognitive_response(user_input, emotion)
            elif technique == "mindfulness":
                return self._generate_mindfulness_response(emotion, intensity)
            elif technique == "behavioral_activation":
                return self._generate_behavioral_response(user_input, emotion)
            else:
                return self._generate_general_response(user_input, emotion)
                
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            return "I understand this is difficult. Let's take this one step at a time. What would be most helpful right now?"
    
    def _select_technique(self, emotion: str, intensity: float, user_input: str) -> str:
        """Select the most appropriate CBT technique."""
        if emotion in ["anxious", "worried", "stressed"] and intensity > 0.7:
            return "mindfulness"
        elif "thought" in user_input.lower() or "think" in user_input.lower():
            return "cognitive_restructuring"
        elif emotion in ["sad", "depressed", "low"] or "motivation" in user_input.lower():
            return "behavioral_activation"
        else:
            return "cognitive_restructuring"
    
    def _generate_cognitive_response(self, user_input: str, emotion: str) -> str:
        """Generate cognitive restructuring response."""
        responses = [
            "I hear that you're experiencing some challenging thoughts. Let's examine this together.",
            "What evidence do you have for this belief? What evidence might contradict it?",
            "If a close friend came to you with this same concern, what would you tell them?",
            "Are there other ways to interpret this situation?"
        ]
        return responses[0]  # Simplified for now
    
    def _generate_mindfulness_response(self, emotion: str, intensity: float) -> str:
        """Generate mindfulness-based response."""
        if intensity > 0.8:
            return "I can sense this is really intense for you right now. Let's take a few deep breaths together. Inhale slowly... and exhale. What do you notice in this moment?"
        else:
            return "Let's pause for a moment and check in with yourself. What are you feeling right now, both emotionally and physically?"
    
    def _generate_behavioral_response(self, user_input: str, emotion: str) -> str:
        """Generate behavioral activation response."""
        return "I understand you're feeling this way. What's one small thing you could do today that might help you feel even slightly better? It doesn't have to be big - even tiny steps count."
    
    def _generate_general_response(self, user_input: str, emotion: str) -> str:
        """Generate general supportive response."""
        return "Thank you for sharing that with me. I can hear that this is important to you. What would be most helpful for us to focus on right now?"

# Global reply generator instance
_reply_generator = None

def get_reply_generator() -> ReplyGenerator:
    """Get the global reply generator instance."""
    global _reply_generator
    if _reply_generator is None:
        _reply_generator = ReplyGenerator()
        _reply_generator.initialize()
    return _reply_generator

# Global instance for direct access
reply_generator = get_reply_generator()
