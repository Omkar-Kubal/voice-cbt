"""
Google Gemini API Integration Service
Provides free AI responses using Google's Gemini API with generous free tier
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiIntegration:
    """
    Google Gemini API integration for free AI responses.
    Uses Gemini 2.5 Flash model with generous free tier limits.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-2.5-flash"  # Fast and free model
        self.client = None
        self.is_available = False
        
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model_name)
            self.is_available = True
            logger.info("Gemini API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.is_available = False
    
    def generate_response(
        self, 
        user_message: str, 
        emotion: str, 
        context: str = "",
        session_history: List[Dict] = None,
        therapeutic_style: str = "supportive"
    ) -> str:
        """
        Generate a therapeutic response using Gemini API.
        
        Args:
            user_message: The user's input message
            emotion: Detected emotion
            context: Additional context from conversation memory
            session_history: Previous conversation history
            therapeutic_style: Style of therapeutic response
        
        Returns:
            Generated therapeutic response
        """
        if not self.is_available:
            logger.warning("Gemini API not available, using fallback")
            return self._generate_fallback_response(user_message, emotion)
        
        try:
            # Build conversation context
            prompt = self._build_therapeutic_prompt(
                user_message, emotion, context, session_history, therapeutic_style
            )
            
            # Generate response
            response = self.client.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini, using fallback")
                return self._generate_fallback_response(user_message, emotion)
                
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            return self._generate_fallback_response(user_message, emotion)
    
    def _build_therapeutic_prompt(
        self, 
        user_message: str, 
        emotion: str, 
        context: str,
        session_history: List[Dict],
        therapeutic_style: str
    ) -> str:
        """Build a therapeutic prompt for Gemini."""
        
        # Base therapeutic instructions
        prompt_parts = [
            "You are a compassionate AI therapy companion. Your role is to provide supportive, empathetic responses that help users explore their thoughts and feelings.",
            f"User's message: {user_message}",
            f"Detected emotion: {emotion}",
            f"Therapeutic style: {therapeutic_style}"
        ]
        
        # Add context if available
        if context:
            prompt_parts.append(f"Context: {context}")
        
        # Add conversation history if available
        if session_history and len(session_history) > 0:
            history_text = "Recent conversation:\n"
            for exchange in session_history[-3:]:  # Last 3 exchanges
                history_text += f"- User: {exchange.get('user_message', '')}\n"
                history_text += f"- AI: {exchange.get('ai_response', '')}\n"
            prompt_parts.append(history_text)
        
        # Add therapeutic guidelines
        prompt_parts.extend([
            "Guidelines:",
            "- Be empathetic and supportive",
            "- Ask open-ended questions when appropriate",
            "- Acknowledge the user's emotions",
            "- Provide gentle guidance without being prescriptive",
            "- Keep responses conversational and natural",
            "- Use a warm, caring tone",
            "- Avoid repetitive phrases",
            "- Be curious about the user's experience"
        ])
        
        return "\n\n".join(prompt_parts)
    
    def _generate_fallback_response(self, user_message: str, emotion: str) -> str:
        """Generate a fallback response when Gemini is not available."""
        import random
        
        # Emotion-based responses
        if emotion.lower() in ["happy", "happiness", "joy"]:
            responses = [
                "That's wonderful to hear you're feeling happy! 😊 What's bringing you joy today?",
                "Your positive energy is contagious! ✨ What's been contributing to this great mood?",
                "It's so refreshing to hear about your happiness! 🌟 What's been going well for you lately?"
            ]
        elif emotion.lower() in ["sad", "sadness", "depressed"]:
            responses = [
                "I can sense you're going through a difficult time. I'm here to listen and support you. What's weighing on your mind right now?",
                "It sounds like you're feeling down. I'm here for you. Would you like to talk about what's been bothering you?",
                "I can hear the sadness in your words. You're not alone in this. What's been on your mind lately?"
            ]
        elif emotion.lower() in ["anxious", "anxiety", "worried"]:
            responses = [
                "I understand you're feeling anxious. Let's take this one step at a time. What's one thing that might help you feel more grounded right now?",
                "Anxiety can feel overwhelming. I'm here to help you work through this. What's been causing you the most concern?",
                "I can hear the worry in your words. Let's tackle this together, one step at a time. What's on your mind?"
            ]
        elif emotion.lower() in ["angry", "anger", "frustrated"]:
            responses = [
                "I can hear that you're feeling frustrated. That's completely understandable. What's the main thing that's bothering you right now?",
                "It sounds like you're dealing with some strong emotions. I'm here to help you work through this. What's been making you feel this way?",
                "I can feel the frustration in your message. Let's explore what's been bothering you. What's on your mind?"
            ]
        else:
            # General conversational responses
            responses = [
                "That's interesting! Tell me more about that. I'm curious to hear your perspective.",
                "I'd love to understand better. What's been on your mind lately?",
                "That sounds like something worth exploring. How are you feeling about it?",
                "I'm here to listen. What's been going on in your life? I'd love to hear your thoughts.",
                "That's a great question! What made you think about that?",
                "I'm curious to hear more. What's been happening with you?",
                "That sounds important. How are you feeling about everything?",
                "I'd love to know more about your experience. What's been going on?"
            ]
        
        return random.choice(responses)

# Global instance
gemini_integration = GeminiIntegration()
