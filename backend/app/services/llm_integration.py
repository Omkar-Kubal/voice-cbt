"""
LLM Integration Service for ChatGPT-like responses.
This service provides dynamic, contextual, and intelligent responses using various LLM backends.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LLMIntegration:
    """
    LLM Integration service for dynamic, ChatGPT-like responses.
    Supports multiple LLM backends including OpenAI, local models, and fallbacks.
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.use_local_llm = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
        self.local_llm_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
        self.fallback_enabled = True
        
    def generate_response(self, 
                        user_message: str, 
                        emotion: str, 
                        context: str = "",
                        session_history: List[Dict] = None,
                        therapeutic_style: str = "supportive") -> str:
        """
        Generate a dynamic, ChatGPT-like response using the best available LLM.
        
        Args:
            user_message: The user's input message
            emotion: Detected emotion
            context: Additional context from conversation memory
            session_history: Previous conversation history
            therapeutic_style: Style of therapeutic response (supportive, analytical, etc.)
        
        Returns:
            Dynamic, contextual response
        """
        try:
            # Try OpenAI first if API key is available
            if self.openai_api_key:
                return self._generate_openai_response(
                    user_message, emotion, context, session_history, therapeutic_style
                )
            
            # Try local LLM if configured
            elif self.use_local_llm:
                return self._generate_local_llm_response(
                    user_message, emotion, context, session_history, therapeutic_style
                )
            
            # Fallback to enhanced rule-based system
            else:
                return self._generate_fallback_response(
                    user_message, emotion, context, session_history, therapeutic_style
                )
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._generate_fallback_response(
                user_message, emotion, context, session_history, therapeutic_style
            )
    
    def _generate_openai_response(self, 
                                user_message: str, 
                                emotion: str, 
                                context: str,
                                session_history: List[Dict],
                                therapeutic_style: str) -> str:
        """Generate response using OpenAI GPT models."""
        
        # Build conversation history for context
        messages = self._build_conversation_context(
            user_message, emotion, context, session_history, therapeutic_style
        )
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
                
        except Exception as e:
            logger.error(f"OpenAI API request failed: {e}")
            return self._generate_fallback_response(
                user_message, emotion, context, session_history, therapeutic_style
            )
    
    def _generate_local_llm_response(self, 
                                   user_message: str, 
                                   emotion: str, 
                                   context: str,
                                   session_history: List[Dict],
                                   therapeutic_style: str) -> str:
        """Generate response using local LLM (Ollama, etc.)."""
        
        prompt = self._build_local_llm_prompt(
            user_message, emotion, context, session_history, therapeutic_style
        )
        
        try:
            response = requests.post(
                f"{self.local_llm_url}/api/generate",
                json={
                    "model": "llama2",  # or other local model
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 300
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"].strip()
            else:
                logger.error(f"Local LLM error: {response.status_code}")
                return self._generate_fallback_response(
                    user_message, emotion, context, session_history, therapeutic_style
                )
                
        except Exception as e:
            logger.error(f"Local LLM request failed: {e}")
            return self._generate_fallback_response(
                user_message, emotion, context, session_history, therapeutic_style
            )
    
    def _generate_fallback_response(self, 
                                 user_message: str, 
                                 emotion: str, 
                                 context: str,
                                 session_history: List[Dict],
                                 therapeutic_style: str) -> str:
        """Generate response using enhanced rule-based system as fallback."""
        
        # Dynamic response templates based on emotion and context
        response_templates = {
            "happiness": [
                "I'm so glad to hear you're feeling happy! 😊 What's been contributing to this positive energy?",
                "Your joy is wonderful to witness! Can you tell me more about what's been going well for you?",
                "It's wonderful to see you in such a good mood! What's been making you feel this way?",
                "I love hearing about your positive energy! What's been contributing to this good mood?"
            ],
            "sadness": [
                "I can sense you might be going through a difficult time. I'm here to listen and support you.",
                "It sounds like you're feeling down. Would you like to talk about what's been weighing on you?",
                "I'm here for you during this tough time. What's been on your mind lately?",
                "It takes courage to share when you're feeling sad. I'm here to listen and help."
            ],
            "anxiety": [
                "I can hear the worry in your words. Let's work through this together, one step at a time.",
                "Anxiety can feel overwhelming. What's been causing you the most concern lately?",
                "I'm here to help you navigate through these anxious feelings. What's on your mind?",
                "It's completely normal to feel anxious sometimes. What's been making you feel this way?"
            ],
            "anger": [
                "I can feel the frustration in your message. Let's explore what's been bothering you.",
                "It sounds like you're dealing with some strong emotions. What's been making you feel this way?",
                "I'm here to help you work through these feelings. What's been on your mind?",
                "Anger is a valid emotion. Let's talk about what's been frustrating you lately."
            ],
            "fear": [
                "I can sense some fear in your words. You're safe here, and I'm here to support you.",
                "Fear can be overwhelming. What's been making you feel afraid?",
                "I'm here to help you feel more secure. What's been on your mind?",
                "It's okay to feel afraid sometimes. What's been causing you concern?"
            ],
            "neutral": [
                "I'm here to listen and help you explore your thoughts. What's on your mind today?",
                "How are you feeling right now? I'm here to support you in whatever way feels helpful.",
                "What would you like to talk about? I'm here to help you process whatever you're experiencing.",
                "I'm here to listen. What's been going on in your life lately?"
            ]
        }
        
        # Select appropriate response based on emotion
        templates = response_templates.get(emotion, response_templates["neutral"])
        base_response = random.choice(templates)
        
        # Add contextual follow-up questions
        follow_up_questions = {
            "happiness": [
                "What's been the highlight of your day so far?",
                "Is there something specific that's been making you feel this way?",
                "How long have you been feeling this positive energy?"
            ],
            "sadness": [
                "Would you like to talk about what's been difficult for you?",
                "What's been weighing on your mind lately?",
                "Is there something specific that's been making you feel this way?"
            ],
            "anxiety": [
                "What's been causing you the most worry?",
                "Is there something specific that's been making you feel anxious?",
                "What would help you feel more calm right now?"
            ],
            "anger": [
                "What's been frustrating you the most lately?",
                "Is there something specific that's been bothering you?",
                "What would help you feel more at peace?"
            ],
            "fear": [
                "What's been making you feel afraid?",
                "Is there something specific that's been causing you concern?",
                "What would help you feel more secure?"
            ]
        }
        
        # Add contextual follow-up if appropriate
        if emotion in follow_up_questions:
            follow_up = random.choice(follow_up_questions[emotion])
            base_response += f" {follow_up}"
        
        # Add personalized context if available
        if context:
            if "topics_discussed" in context and context["topics_discussed"]:
                topics = ", ".join(context["topics_discussed"][:3])  # Last 3 topics
                base_response += f" I remember we've talked about {topics} before."
        
        return base_response
    
    def _build_conversation_context(self, 
                                  user_message: str, 
                                  emotion: str, 
                                  context: str,
                                  session_history: List[Dict],
                                  therapeutic_style: str) -> List[Dict]:
        """Build conversation context for LLM."""
        
        system_prompt = f"""You are a compassionate, professional AI therapist specializing in CBT (Cognitive Behavioral Therapy). 

Your role:
- Provide supportive, empathetic responses
- Use therapeutic techniques like active listening, reflection, and gentle guidance
- Help users explore their thoughts and feelings
- Offer practical coping strategies when appropriate
- Maintain a warm, non-judgmental tone

Therapeutic style: {therapeutic_style}
Detected emotion: {emotion}

Guidelines:
- Keep responses conversational and natural (like ChatGPT)
- Avoid repetitive or generic responses
- Ask thoughtful follow-up questions
- Provide specific, actionable advice when helpful
- Be genuine and authentic in your responses
- Adapt your tone to match the user's emotional state

Context: {context if context else "No previous context available"}

Respond naturally and helpfully to the user's message."""

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if available
        if session_history:
            for exchange in session_history[-6:]:  # Last 6 exchanges
                if "user" in exchange:
                    messages.append({"role": "user", "content": exchange["user"]})
                if "bot" in exchange:
                    messages.append({"role": "assistant", "content": exchange["bot"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _build_local_llm_prompt(self, 
                              user_message: str, 
                              emotion: str, 
                              context: str,
                              session_history: List[Dict],
                              therapeutic_style: str) -> str:
        """Build prompt for local LLM."""
        
        prompt = f"""You are a professional AI therapist specializing in CBT. Respond naturally and helpfully.

User's message: {user_message}
Detected emotion: {emotion}
Context: {context}
Therapeutic style: {therapeutic_style}

Guidelines:
- Be conversational and natural (like ChatGPT)
- Avoid repetitive responses
- Ask thoughtful questions
- Provide specific, helpful advice
- Match your tone to the user's emotional state

Respond:"""

        return prompt

# Global instance
llm_integration = LLMIntegration()
