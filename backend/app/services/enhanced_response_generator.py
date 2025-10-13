"""
Enhanced response generation service for Voice CBT.
Provides personalized, empathetic, and context-aware responses.
"""

import openai
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

logger = logging.getLogger(__name__)

class EnhancedResponseGenerator:
    """
    Advanced response generator with personalization and emotion awareness.
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.openai_api_key
        
        # CBT-specific response templates
        self.cbt_techniques = {
            "cognitive_restructuring": [
                "Let's examine the evidence for this thought. What facts support it?",
                "I'd like to help you challenge this belief. What would you tell a friend in this situation?",
                "Let's look at this from a different angle. What's another way to view this?"
            ],
            "behavioral_activation": [
                "What activities usually bring you joy or satisfaction?",
                "Let's identify one small step you could take today to improve your mood.",
                "Sometimes action can help us feel better. What would you like to try?"
            ],
            "mindfulness": [
                "Let's take a moment to breathe and ground yourself in the present.",
                "Notice what you're feeling right now, without judgment.",
                "What's one thing you can see, hear, or feel in this moment?"
            ],
            "problem_solving": [
                "Let's break this down into smaller, manageable steps.",
                "What resources or support do you have available?",
                "What would success look like in this situation?"
            ]
        }
        
        # Emotion-specific responses
        self.emotion_responses = {
            "sad": {
                "acknowledgment": "I can hear that you're feeling sad, and I want you to know that your feelings are valid.",
                "techniques": ["mindfulness", "behavioral_activation"],
                "tone": "gentle, supportive"
            },
            "angry": {
                "acknowledgment": "I understand you're feeling angry. Let's work through this together.",
                "techniques": ["mindfulness", "cognitive_restructuring"],
                "tone": "calm, understanding"
            },
            "anxious": {
                "acknowledgment": "I can sense your anxiety. Let's take this one step at a time.",
                "techniques": ["mindfulness", "cognitive_restructuring"],
                "tone": "reassuring, patient"
            },
            "happy": {
                "acknowledgment": "It's wonderful to hear that you're feeling happy!",
                "techniques": ["behavioral_activation"],
                "tone": "enthusiastic, celebratory"
            },
            "neutral": {
                "acknowledgment": "I'm here to listen and support you.",
                "techniques": ["problem_solving", "behavioral_activation"],
                "tone": "warm, professional"
            }
        }
    
    def generate_personalized_response(
        self,
        user_message: str,
        user_emotion: str,
        conversation_history: List[Dict[str, Any]],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a personalized, empathetic response based on user input and context.
        """
        try:
            # Get emotion-specific configuration
            emotion_config = self.emotion_responses.get(user_emotion, self.emotion_responses["neutral"])
            
            # Build context for the AI
            context = self._build_context(user_message, user_emotion, conversation_history, user_profile)
            
            # Generate response using OpenAI
            response = self._generate_ai_response(context, emotion_config)
            
            # Enhance response with CBT techniques
            enhanced_response = self._enhance_with_cbt_techniques(
                response, user_emotion, emotion_config
            )
            
            # Add voice synthesis instructions
            voice_instructions = self._generate_voice_instructions(enhanced_response, user_emotion)
            
            return {
                "text": enhanced_response,
                "emotion": user_emotion,
                "techniques_used": emotion_config["techniques"],
                "tone": emotion_config["tone"],
                "voice_instructions": voice_instructions,
                "timestamp": datetime.now().isoformat(),
                "personalized": True
            }
            
        except Exception as e:
            logger.error(f"Error generating personalized response: {e}")
            # Use contextual fallback instead of generic fallback
            context = self._build_context(user_message, user_emotion, conversation_history, user_profile)
            contextual_response = self._generate_contextual_fallback(context)
            
            return {
                "text": contextual_response,
                "emotion": user_emotion,
                "techniques_used": ["active_listening"],
                "tone": "supportive",
                "voice_instructions": {
                    "rate": 0.8,
                    "pitch": 1.0,
                    "volume": 0.8,
                    "emphasis": "warm, supportive"
                },
                "timestamp": datetime.now().isoformat(),
                "personalized": False,
                "fallback": True
            }
    
    def _build_context(
        self,
        user_message: str,
        user_emotion: str,
        conversation_history: List[Dict[str, Any]],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build comprehensive context for AI response generation."""
        
        context_parts = [
            "You are a compassionate, professional CBT therapist conducting a therapy session.",
            "Your goal is to provide empathetic, evidence-based support while maintaining professional boundaries.",
            f"The user is currently feeling: {user_emotion}",
            f"User's message: {user_message}"
        ]
        
        # Add user profile context
        if user_profile:
            if user_profile.get('preferences', {}).get('therapy_style'):
                context_parts.append(f"Therapy style preference: {user_profile['preferences']['therapy_style']}")
            
            if user_profile.get('preferences', {}).get('voice_speed'):
                context_parts.append(f"User prefers: {user_profile['preferences']['voice_speed']} WPM speech")
        
        # Add conversation history
        if conversation_history:
            context_parts.append("\nRecent conversation context:")
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = "User" if msg.get('type') == 'user' else "Therapist"
                content = msg.get('content', '')
                context_parts.append(f"{role}: {content}")
        
        # Add CBT guidelines
        context_parts.extend([
            "\nCBT Guidelines:",
            "- Use evidence-based techniques",
            "- Be empathetic and non-judgmental",
            "- Encourage self-reflection",
            "- Provide practical coping strategies",
            "- Validate emotions while promoting positive change",
            "- Keep responses conversational and natural",
            "- Ask open-ended questions when appropriate"
        ])
        
        return "\n".join(context_parts)
    
    def _generate_ai_response(self, context: str, emotion_config: Dict[str, Any]) -> str:
        """Generate AI response using Gemini API (free) or OpenAI as fallback."""
        
        # Try Gemini API first (free tier)
        try:
            from .gemini_integration import gemini_integration
            
            if gemini_integration.is_available:
                logger.info("Using Gemini API for response generation")
                # Extract user message and emotion from context
                user_message = self._extract_user_message_from_context(context)
                emotion = self._extract_emotion_from_context(context)
                
                return gemini_integration.generate_response(
                    user_message=user_message,
                    emotion=emotion,
                    context=context,
                    session_history=[],
                    therapeutic_style="supportive"
                )
        except Exception as e:
            logger.warning(f"Gemini API failed: {e}, trying OpenAI fallback")
        
        # Fallback to OpenAI if Gemini is not available
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_new_openai_api_key_here":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": context
                        },
                        {
                            "role": "user",
                            "content": "Please provide a supportive, therapeutic response that acknowledges the user's emotion and offers helpful guidance."
                        }
                    ],
                    max_tokens=300,
                    temperature=0.7,
                    presence_penalty=0.1,
                    frequency_penalty=0.1
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.error(f"OpenAI API also failed: {e}")
        
        # Final fallback to contextual responses
        logger.info("Using free contextual responses as final fallback")
        return self._generate_contextual_fallback(context)
    
    def _extract_user_message_from_context(self, context: str) -> str:
        """Extract user message from context."""
        # Simple extraction - look for "User's message:" pattern
        if "User's message:" in context:
            return context.split("User's message:")[1].split("\n")[0].strip()
        return "Hello"
    
    def _extract_emotion_from_context(self, context: str) -> str:
        """Extract emotion from context."""
        # Simple extraction - look for "Detected emotion:" pattern
        if "Detected emotion:" in context:
            return context.split("Detected emotion:")[1].split("\n")[0].strip()
        return "neutral"
    
    def _enhance_with_cbt_techniques(
        self,
        response: str,
        user_emotion: str,
        emotion_config: Dict[str, Any]
    ) -> str:
        """Enhance response with specific CBT techniques."""
        
        # Add emotion acknowledgment
        if emotion_config.get("acknowledgment"):
            response = f"{emotion_config['acknowledgment']} {response}"
        
        # Add technique-specific questions if appropriate
        techniques = emotion_config.get("techniques", [])
        if techniques and "cognitive_restructuring" in techniques:
            # Add a gentle challenge question
            if "thought" in response.lower() or "believe" in response.lower():
                response += " What evidence do you have for this thought?"
        
        return response
    
    def _generate_voice_instructions(
        self,
        response: str,
        user_emotion: str
    ) -> Dict[str, Any]:
        """Generate voice synthesis instructions based on response and emotion."""
        
        # Emotion-based voice parameters
        voice_params = {
            "sad": {
                "rate": 0.8,
                "pitch": 0.9,
                "volume": 0.8,
                "emphasis": "gentle, supportive"
            },
            "angry": {
                "rate": 0.7,
                "pitch": 0.8,
                "volume": 0.7,
                "emphasis": "calm, steady"
            },
            "anxious": {
                "rate": 0.6,
                "pitch": 0.9,
                "volume": 0.8,
                "emphasis": "reassuring, slow"
            },
            "happy": {
                "rate": 0.9,
                "pitch": 1.1,
                "volume": 0.9,
                "emphasis": "warm, encouraging"
            },
            "neutral": {
                "rate": 0.8,
                "pitch": 1.0,
                "volume": 0.8,
                "emphasis": "professional, warm"
            }
        }
        
        params = voice_params.get(user_emotion, voice_params["neutral"])
        
        return {
            "rate": params["rate"],
            "pitch": params["pitch"],
            "volume": params["volume"],
            "emphasis": params["emphasis"],
            "pause_points": self._identify_pause_points(response),
            "emphasis_words": self._identify_emphasis_words(response, user_emotion)
        }
    
    def _identify_pause_points(self, text: str) -> List[int]:
        """Identify natural pause points in the text."""
        pause_indicators = ['.', '!', '?', ',', ';', ':']
        pause_points = []
        
        for i, char in enumerate(text):
            if char in pause_indicators:
                pause_points.append(i)
        
        return pause_points
    
    def _identify_emphasis_words(self, text: str, emotion: str) -> List[str]:
        """Identify words that should be emphasized in speech."""
        emphasis_words = []
        
        # Common therapeutic emphasis words
        therapeutic_words = [
            "important", "valid", "understand", "support", "care", "listen",
            "together", "progress", "strength", "courage", "hope"
        ]
        
        words = text.lower().split()
        for word in words:
            if word in therapeutic_words:
                emphasis_words.append(word)
        
        return emphasis_words
    
    def _generate_contextual_fallback(self, context: str) -> str:
        """Generate a more contextual fallback response."""
        import random
        
        # Extract emotion from context if available
        if "happiness" in context.lower() or "happy" in context.lower():
            responses = [
                "That's wonderful to hear you're feeling happy! 😊 What's bringing you joy today? I'd love to hear more about what's making you feel good.",
                "Your positive energy is contagious! ✨ What's been contributing to this great mood? I'm excited to hear more!",
                "It's so refreshing to hear about your happiness! 🌟 What's been going well for you lately?",
                "I love hearing about your joy! 💫 What's been making you feel this amazing way?"
            ]
            return random.choice(responses)
        elif "sad" in context.lower() or "sadness" in context.lower():
            responses = [
                "I can sense you're going through a difficult time. I'm here to listen and support you. What's weighing on your mind right now?",
                "It sounds like you're feeling down. I'm here for you. Would you like to talk about what's been bothering you?",
                "I can hear the sadness in your words. You're not alone in this. What's been on your mind lately?",
                "It takes courage to share when you're feeling sad. I'm here to listen and help however I can."
            ]
            return random.choice(responses)
        elif "anxious" in context.lower() or "anxiety" in context.lower():
            responses = [
                "I understand you're feeling anxious. Let's take this one step at a time. What's one thing that might help you feel more grounded right now?",
                "Anxiety can feel overwhelming. I'm here to help you work through this. What's been causing you the most concern?",
                "I can hear the worry in your words. Let's tackle this together, one step at a time. What's on your mind?",
                "It's completely normal to feel anxious sometimes. What's been making you feel this way? I'm here to help."
            ]
            return random.choice(responses)
        elif "angry" in context.lower() or "anger" in context.lower():
            responses = [
                "I can hear that you're feeling frustrated. That's completely understandable. What's the main thing that's bothering you right now?",
                "It sounds like you're dealing with some strong emotions. I'm here to help you work through this. What's been making you feel this way?",
                "I can feel the frustration in your message. Let's explore what's been bothering you. What's on your mind?",
                "Anger is a valid emotion. Let's talk about what's been frustrating you lately. I'm here to listen."
            ]
            return random.choice(responses)
        else:
            # More ChatGPT-like responses for general conversation
            responses = [
                "That's interesting! Tell me more about that. I'm curious to hear your perspective.",
                "I'd love to understand better. What's been on your mind lately?",
                "That sounds like something worth exploring. How are you feeling about it?",
                "I'm here to listen. What's been going on in your life? I'd love to hear your thoughts.",
                "That's a great question! What made you think about that?",
                "I'm curious to hear more. What's been happening with you?",
                "That sounds important. How are you feeling about everything?",
                "I'd love to know more about your experience. What's been going on?",
                "That's fascinating! I'd love to hear more about your thoughts on this.",
                "I'm really interested in what you have to say. What's been on your mind?",
                "That's a thoughtful perspective. Can you tell me more about that?",
                "I appreciate you sharing that with me. What else is going on?"
            ]
            return random.choice(responses)
    
    def _generate_fallback_response(self, user_message: str, user_emotion: str) -> Dict[str, Any]:
        """Generate a fallback response when AI generation fails."""
        
        fallback_responses = {
            "sad": "I can hear that you're going through a difficult time. I'm here to listen and support you. What would be most helpful for you right now?",
            "angry": "I understand you're feeling frustrated. Let's work through this together. What's the main thing that's bothering you?",
            "anxious": "I can sense your anxiety. Let's take this one step at a time. What's one thing that might help you feel more grounded?",
            "happy": "It's wonderful to hear that you're feeling good! What's contributing to your positive mood today?",
            "neutral": "I'm here to listen and support you. What's on your mind today?"
        }
        
        return {
            "text": fallback_responses.get(user_emotion, fallback_responses["neutral"]),
            "emotion": user_emotion,
            "techniques_used": ["active_listening"],
            "tone": "supportive",
            "voice_instructions": {
                "rate": 0.8,
                "pitch": 1.0,
                "volume": 0.8,
                "emphasis": "warm, supportive"
            },
            "timestamp": datetime.now().isoformat(),
            "personalized": False,
            "fallback": True
        }

# Global instance
enhanced_response_generator = EnhancedResponseGenerator()

def generate_enhanced_response(
    user_message: str,
    user_emotion: str,
    conversation_history: List[Dict[str, Any]] = None,
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate an enhanced, personalized response."""
    return enhanced_response_generator.generate_personalized_response(
        user_message, user_emotion, conversation_history or [], user_profile
    )
