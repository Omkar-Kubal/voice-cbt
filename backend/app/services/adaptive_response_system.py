"""
Adaptive Response System
Dynamically adapts responses based on real-time user feedback and engagement
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import numpy as np

logger = logging.getLogger(__name__)

class AdaptiveResponseSystem:
    """Adapts responses based on user engagement and feedback"""
    
    def __init__(self):
        self.user_engagement_history = {}
        self.response_effectiveness = {}
        self.adaptation_rules = self._load_adaptation_rules()
        self.engagement_metrics = {}
    
    def _load_adaptation_rules(self) -> Dict[str, Dict]:
        """Load rules for response adaptation"""
        return {
            "engagement_based": {
                "low_engagement": {
                    "response_length": "shorter",
                    "question_frequency": "higher",
                    "tone": "more_encouraging",
                    "techniques": ["mindfulness", "validation"]
                },
                "high_engagement": {
                    "response_length": "longer",
                    "question_frequency": "lower", 
                    "tone": "more_therapeutic",
                    "techniques": ["cognitive_restructuring", "behavioral_activation"]
                }
            },
            "emotion_based": {
                "anxiety": {
                    "pace": "slower",
                    "validation": "high",
                    "techniques": ["grounding", "cognitive_restructuring"]
                },
                "depression": {
                    "pace": "gentle",
                    "validation": "very_high",
                    "techniques": ["behavioral_activation", "mindfulness"]
                },
                "anger": {
                    "pace": "calm",
                    "validation": "acknowledging",
                    "techniques": ["mindfulness", "emotion_regulation"]
                }
            },
            "session_based": {
                "early_session": {
                    "rapport_building": "high",
                    "technique_introduction": "gentle",
                    "depth": "surface_level"
                },
                "middle_session": {
                    "rapport_building": "medium",
                    "technique_introduction": "moderate",
                    "depth": "deeper_exploration"
                },
                "late_session": {
                    "rapport_building": "low",
                    "technique_introduction": "direct",
                    "depth": "therapeutic_work"
                }
            }
        }
    
    def adapt_response(self, 
                      base_response: str,
                      user_id: str,
                      current_emotion: str,
                      session_context: Dict,
                      real_time_metrics: Dict) -> Dict[str, str]:
        """Adapt response based on real-time data"""
        
        try:
            # Get user engagement profile
            engagement_profile = self._get_user_engagement_profile(user_id)
            
            # Analyze current session dynamics
            session_dynamics = self._analyze_session_dynamics(session_context, real_time_metrics)
            
            # Select adaptation strategy
            adaptation_strategy = self._select_adaptation_strategy(
                engagement_profile, current_emotion, session_dynamics
            )
            
            # Apply adaptations
            adapted_response = self._apply_adaptations(
                base_response, adaptation_strategy, current_emotion
            )
            
            # Generate adaptive follow-ups
            adaptive_follow_ups = self._generate_adaptive_follow_ups(
                adapted_response, engagement_profile, current_emotion
            )
            
            # Update engagement tracking
            self._update_engagement_tracking(user_id, real_time_metrics)
            
            return {
                "adapted_response": adapted_response,
                "adaptation_strategy": adaptation_strategy,
                "adaptive_follow_ups": adaptive_follow_ups,
                "engagement_level": engagement_profile["level"],
                "adaptation_score": self._calculate_adaptation_score(adapted_response),
                "predicted_effectiveness": self._predict_response_effectiveness(
                    adapted_response, engagement_profile
                )
            }
            
        except Exception as e:
            logger.error(f"Error adapting response: {e}")
            return {
                "adapted_response": base_response,
                "error": str(e)
            }
    
    def _get_user_engagement_profile(self, user_id: str) -> Dict:
        """Get user's engagement profile"""
        if user_id not in self.user_engagement_history:
            self.user_engagement_history[user_id] = {
                "total_sessions": 0,
                "avg_response_time": 0,
                "preferred_response_length": "medium",
                "engagement_trend": "stable",
                "effective_techniques": [],
                "challenging_areas": []
            }
        
        return self.user_engagement_history[user_id]
    
    def _analyze_session_dynamics(self, session_context: Dict, metrics: Dict) -> Dict:
        """Analyze current session dynamics"""
        return {
            "session_stage": self._determine_session_stage(session_context),
            "user_responsiveness": metrics.get("response_time", 0),
            "emotional_intensity": metrics.get("emotion_intensity", 0.5),
            "conversation_flow": metrics.get("conversation_flow", "normal"),
            "user_comfort_level": metrics.get("comfort_level", 0.5)
        }
    
    def _determine_session_stage(self, context: Dict) -> str:
        """Determine the stage of the current session"""
        session_duration = context.get("session_duration", 0)
        
        if session_duration < 5:  # minutes
            return "early_session"
        elif session_duration < 15:
            return "middle_session"
        else:
            return "late_session"
    
    def _select_adaptation_strategy(self, 
                                  engagement_profile: Dict,
                                  emotion: str,
                                  session_dynamics: Dict) -> Dict:
        """Select the best adaptation strategy"""
        
        # Base strategy from engagement level
        if engagement_profile.get("engagement_level", "medium") == "low":
            base_strategy = self.adaptation_rules["engagement_based"]["low_engagement"]
        else:
            base_strategy = self.adaptation_rules["engagement_based"]["high_engagement"]
        
        # Emotion-based adjustments
        emotion_adjustments = self.adaptation_rules["emotion_based"].get(emotion, {})
        
        # Session-based adjustments
        session_stage = session_dynamics["session_stage"]
        session_adjustments = self.adaptation_rules["session_based"].get(session_stage, {})
        
        # Combine strategies
        strategy = {
            **base_strategy,
            **emotion_adjustments,
            **session_adjustments
        }
        
        return strategy
    
    def _apply_adaptations(self, 
                          response: str, 
                          strategy: Dict, 
                          emotion: str) -> str:
        """Apply adaptations to the response"""
        
        adapted_response = response
        
        # Adjust response length
        if strategy.get("response_length") == "shorter":
            adapted_response = self._shorten_response(adapted_response)
        elif strategy.get("response_length") == "longer":
            adapted_response = self._lengthen_response(adapted_response)
        
        # Adjust tone
        if strategy.get("tone") == "more_encouraging":
            adapted_response = self._make_more_encouraging(adapted_response)
        elif strategy.get("tone") == "more_therapeutic":
            adapted_response = self._make_more_therapeutic(adapted_response)
        
        # Adjust pace
        if strategy.get("pace") == "slower":
            adapted_response = self._slow_down_pace(adapted_response)
        elif strategy.get("pace") == "calm":
            adapted_response = self._calm_tone(adapted_response)
        
        # Add validation based on level
        validation_level = strategy.get("validation", "medium")
        if validation_level == "high":
            adapted_response = self._add_high_validation(adapted_response, emotion)
        elif validation_level == "very_high":
            adapted_response = self._add_very_high_validation(adapted_response, emotion)
        
        return adapted_response
    
    def _shorten_response(self, response: str) -> str:
        """Shorten response while maintaining therapeutic value"""
        sentences = response.split('. ')
        if len(sentences) > 2:
            # Keep the most important sentences
            return '. '.join(sentences[:2]) + '.'
        return response
    
    def _lengthen_response(self, response: str) -> str:
        """Lengthen response with additional therapeutic content"""
        if not response.endswith('?'):
            response += " How does that feel to you?"
        return response
    
    def _make_more_encouraging(self, response: str) -> str:
        """Make response more encouraging"""
        encouraging_starters = [
            "I believe in your ability to work through this",
            "You're taking important steps forward",
            "Your courage in sharing this is admirable"
        ]
        
        if not any(starter in response for starter in encouraging_starters):
            response = f"{encouraging_starters[0]}. {response}"
        
        return response
    
    def _make_more_therapeutic(self, response: str) -> str:
        """Make response more therapeutically focused"""
        if "let's explore" not in response.lower():
            response += " Let's explore this together and find a path forward."
        return response
    
    def _slow_down_pace(self, response: str) -> str:
        """Slow down the pace of the response"""
        response = response.replace("!", ".")
        response = response.replace("urgent", "important")
        return response
    
    def _calm_tone(self, response: str) -> str:
        """Make the tone more calm"""
        response = response.replace("!", ".")
        response = response.replace("need to", "might consider")
        return response
    
    def _add_high_validation(self, response: str, emotion: str) -> str:
        """Add high level of validation"""
        validation_phrases = {
            "anxiety": "Your anxiety is completely understandable",
            "depression": "What you're feeling is valid and important",
            "anger": "Your anger makes sense given the situation",
            "stress": "It's completely normal to feel stressed"
        }
        
        phrase = validation_phrases.get(emotion, "Your feelings are completely valid")
        if phrase not in response:
            response = f"{phrase}. {response}"
        
        return response
    
    def _add_very_high_validation(self, response: str, emotion: str) -> str:
        """Add very high level of validation"""
        response = self._add_high_validation(response, emotion)
        response = f"I want you to know that you're not alone in this. {response}"
        return response
    
    def _generate_adaptive_follow_ups(self, 
                                   response: str, 
                                   engagement_profile: Dict,
                                   emotion: str) -> List[str]:
        """Generate adaptive follow-up questions"""
        
        follow_ups = []
        
        # Based on engagement level
        if engagement_profile.get("engagement_level") == "low":
            follow_ups.extend([
                "How are you feeling about what we've discussed?",
                "What would be most helpful for you right now?"
            ])
        else:
            follow_ups.extend([
                "What insights are you gaining from this conversation?",
                "How can we build on what we've discovered?"
            ])
        
        # Based on emotion
        if emotion == "anxiety":
            follow_ups.append("What's one small step you could take to feel more grounded?")
        elif emotion == "depression":
            follow_ups.append("What's one thing that might bring you a moment of peace?")
        elif emotion == "anger":
            follow_ups.append("What might be underneath this feeling?")
        
        return follow_ups[:3]  # Return top 3
    
    def _update_engagement_tracking(self, user_id: str, metrics: Dict):
        """Update user engagement tracking"""
        if user_id not in self.engagement_metrics:
            self.engagement_metrics[user_id] = []
        
        self.engagement_metrics[user_id].append({
            "timestamp": datetime.now(),
            "response_time": metrics.get("response_time", 0),
            "emotion_intensity": metrics.get("emotion_intensity", 0.5),
            "conversation_flow": metrics.get("conversation_flow", "normal")
        })
        
        # Keep only last 50 entries
        if len(self.engagement_metrics[user_id]) > 50:
            self.engagement_metrics[user_id] = self.engagement_metrics[user_id][-50:]
    
    def _calculate_adaptation_score(self, response: str) -> float:
        """Calculate how well the response was adapted"""
        score = 0.0
        
        # Length appropriateness
        if 30 <= len(response) <= 400:
            score += 0.3
        
        # Empathy presence
        if any(word in response.lower() for word in ["understand", "hear", "sense", "feel"]):
            score += 0.3
        
        # Question presence
        if "?" in response:
            score += 0.2
        
        # Therapeutic language
        therapeutic_words = ["explore", "together", "process", "work through", "cope"]
        if any(word in response.lower() for word in therapeutic_words):
            score += 0.2
        
        return min(score, 1.0)
    
    def _predict_response_effectiveness(self, response: str, engagement_profile: Dict) -> str:
        """Predict how effective the response will be"""
        
        # Base prediction on engagement level
        base_effectiveness = {
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }.get(engagement_profile.get("engagement_level", "medium"), 0.6)
        
        # Adjust based on response quality
        if "?" in response and len(response) > 50:
            base_effectiveness += 0.1
        
        if any(word in response.lower() for word in ["together", "explore", "understand"]):
            base_effectiveness += 0.1
        
        # Final prediction
        if base_effectiveness >= 0.8:
            return "high"
        elif base_effectiveness >= 0.6:
            return "medium"
        else:
            return "low"
