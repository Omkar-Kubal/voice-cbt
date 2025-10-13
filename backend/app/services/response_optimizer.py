"""
Advanced Response Optimization Service
Optimizes AI responses for better therapeutic outcomes
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ResponseOptimizer:
    """Optimizes AI responses for maximum therapeutic impact"""
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
        self.therapeutic_techniques = self._load_therapeutic_techniques()
        self.optimization_rules = self._load_optimization_rules()
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load therapeutic response templates"""
        return {
            "anxiety": [
                "Let's take a moment to breathe together. Can you tell me what specific thoughts are making you feel anxious right now?",
                "I hear that you're feeling anxious. Let's explore this together - what's the worst thing that could happen, and how likely is it?",
                "Anxiety can feel overwhelming. Let's break this down into smaller, manageable pieces. What's one small step you could take?"
            ],
            "depression": [
                "I can sense that you're going through a difficult time. You're not alone in this, and it takes courage to share these feelings.",
                "Depression can make everything feel heavy. Let's focus on one small thing that brought you even a tiny bit of joy today.",
                "Your feelings are valid. Let's explore what might be contributing to these feelings and how we can work through them together."
            ],
            "anger": [
                "I can hear the frustration in your voice. Anger is a natural emotion - let's explore what's underneath it.",
                "It sounds like you're feeling really angry right now. Can you help me understand what triggered this feeling?",
                "Anger often protects us from other emotions. What might you be feeling underneath the anger?"
            ],
            "stress": [
                "Stress can feel overwhelming. Let's identify what's within your control and what isn't.",
                "I hear that you're feeling stressed. Let's take a step back and look at this situation from a different angle.",
                "Stress is your body's way of responding to pressure. What coping strategies have worked for you in the past?"
            ]
        }
    
    def _load_therapeutic_techniques(self) -> Dict[str, Dict]:
        """Load evidence-based therapeutic techniques"""
        return {
            "cognitive_restructuring": {
                "description": "Help identify and challenge negative thought patterns",
                "questions": [
                    "What evidence do you have for this thought?",
                    "What would you tell a friend in this situation?",
                    "What's another way to look at this?"
                ]
            },
            "mindfulness": {
                "description": "Present-moment awareness and acceptance",
                "techniques": [
                    "Let's take three deep breaths together",
                    "Notice what you're feeling right now without judgment",
                    "What sounds can you hear around you?"
                ]
            },
            "behavioral_activation": {
                "description": "Increase engagement in positive activities",
                "suggestions": [
                    "What's one small activity you could do today?",
                    "What used to bring you joy that you haven't done lately?",
                    "Let's plan one pleasant activity for this week"
                ]
            },
            "exposure_therapy": {
                "description": "Gradual exposure to feared situations",
                "approach": [
                    "Let's break this down into smaller steps",
                    "What's the smallest version of this you could try?",
                    "How can we build your confidence gradually?"
                ]
            }
        }
    
    def _load_optimization_rules(self) -> Dict[str, List[str]]:
        """Load response optimization rules"""
        return {
            "empathy_enhancement": [
                "Use validating language",
                "Acknowledge the user's feelings",
                "Show understanding and support"
            ],
            "therapeutic_structure": [
                "Start with validation",
                "Ask open-ended questions",
                "Provide practical tools",
                "End with encouragement"
            ],
            "language_optimization": [
                "Use 'we' instead of 'you'",
                "Avoid judgmental language",
                "Use present tense for current feelings",
                "Include hope and possibility"
            ]
        }
    
    def optimize_response(self, 
                         base_response: str, 
                         user_emotion: str, 
                         session_context: Dict,
                         user_profile: Dict) -> Dict[str, str]:
        """Optimize a response for maximum therapeutic impact"""
        
        try:
            # Analyze the base response
            response_analysis = self._analyze_response(base_response)
            
            # Select appropriate therapeutic technique
            technique = self._select_therapeutic_technique(user_emotion, session_context)
            
            # Optimize language and structure
            optimized_response = self._optimize_language(base_response, user_emotion)
            
            # Add therapeutic elements
            enhanced_response = self._add_therapeutic_elements(
                optimized_response, technique, user_emotion
            )
            
            # Create follow-up questions
            follow_up_questions = self._generate_follow_up_questions(
                user_emotion, session_context, user_profile
            )
            
            # Generate alternative responses
            alternatives = self._generate_alternative_responses(
                enhanced_response, user_emotion, technique
            )
            
            return {
                "optimized_response": enhanced_response,
                "therapeutic_technique": technique,
                "follow_up_questions": follow_up_questions,
                "alternative_responses": alternatives,
                "optimization_score": self._calculate_optimization_score(enhanced_response),
                "therapeutic_value": self._assess_therapeutic_value(enhanced_response),
                "empathy_level": self._assess_empathy_level(enhanced_response)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing response: {e}")
            return {
                "optimized_response": base_response,
                "error": str(e)
            }
    
    def _analyze_response(self, response: str) -> Dict:
        """Analyze the quality of a response"""
        return {
            "length": len(response),
            "empathy_indicators": self._count_empathy_indicators(response),
            "question_count": response.count('?'),
            "therapeutic_keywords": self._count_therapeutic_keywords(response),
            "tone": self._analyze_tone(response)
        }
    
    def _select_therapeutic_technique(self, emotion: str, context: Dict) -> str:
        """Select the most appropriate therapeutic technique"""
        technique_mapping = {
            "anxiety": "cognitive_restructuring",
            "depression": "behavioral_activation", 
            "anger": "mindfulness",
            "stress": "mindfulness",
            "fear": "exposure_therapy",
            "sadness": "behavioral_activation"
        }
        
        return technique_mapping.get(emotion, "mindfulness")
    
    def _optimize_language(self, response: str, emotion: str) -> str:
        """Optimize language for better therapeutic impact"""
        # Replace judgmental language
        response = response.replace("you should", "we could consider")
        response = response.replace("you need to", "it might help to")
        response = response.replace("you're wrong", "let's explore this together")
        
        # Add empathy markers
        empathy_starters = {
            "anxiety": "I can hear the worry in your voice",
            "depression": "I can sense the heaviness you're feeling",
            "anger": "I can feel the frustration you're experiencing",
            "stress": "I understand how overwhelming this feels"
        }
        
        if not any(marker in response.lower() for marker in ["i hear", "i understand", "i can sense"]):
            starter = empathy_starters.get(emotion, "I hear what you're saying")
            response = f"{starter}. {response}"
        
        return response
    
    def _add_therapeutic_elements(self, response: str, technique: str, emotion: str) -> str:
        """Add therapeutic elements to the response"""
        technique_data = self.therapeutic_techniques.get(technique, {})
        
        # Add technique-specific elements
        if technique == "cognitive_restructuring":
            response += "\n\nLet's explore this thought together. What evidence do you have for this belief?"
        elif technique == "mindfulness":
            response += "\n\nLet's take a moment to ground ourselves. Can you name three things you can see right now?"
        elif technique == "behavioral_activation":
            response += "\n\nWhat's one small step you could take today that might help you feel a bit better?"
        
        return response
    
    def _generate_follow_up_questions(self, emotion: str, context: Dict, profile: Dict) -> List[str]:
        """Generate therapeutic follow-up questions"""
        questions = []
        
        if emotion == "anxiety":
            questions = [
                "What's the worst thing that could happen, and how likely is it?",
                "What would you tell a friend in this situation?",
                "What coping strategies have worked for you before?"
            ]
        elif emotion == "depression":
            questions = [
                "What's one small thing that brought you even a tiny bit of joy today?",
                "What used to make you feel good that you haven't done lately?",
                "Who are the people in your life who care about you?"
            ]
        elif emotion == "anger":
            questions = [
                "What might you be feeling underneath the anger?",
                "What triggered this feeling?",
                "How can we work through this together?"
            ]
        
        return questions[:3]  # Return top 3 questions
    
    def _generate_alternative_responses(self, response: str, emotion: str, technique: str) -> List[str]:
        """Generate alternative therapeutic responses"""
        alternatives = []
        
        # Create variations with different therapeutic approaches
        if technique == "cognitive_restructuring":
            alternatives.append(response.replace("Let's explore", "I'd like to help you examine"))
            alternatives.append(response.replace("What evidence", "What would you tell a friend"))
        
        elif technique == "mindfulness":
            alternatives.append(response.replace("ground ourselves", "connect with the present moment"))
            alternatives.append(response.replace("three things you can see", "one thing you can hear"))
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def _calculate_optimization_score(self, response: str) -> float:
        """Calculate how well optimized a response is"""
        score = 0.0
        
        # Length optimization (not too short, not too long)
        if 50 <= len(response) <= 300:
            score += 0.3
        
        # Empathy indicators
        empathy_words = ["understand", "hear", "sense", "feel", "together", "support"]
        empathy_count = sum(1 for word in empathy_words if word in response.lower())
        score += min(empathy_count * 0.1, 0.3)
        
        # Question presence
        if "?" in response:
            score += 0.2
        
        # Therapeutic keywords
        therapeutic_words = ["explore", "consider", "perspective", "cope", "manage", "process"]
        therapeutic_count = sum(1 for word in therapeutic_words if word in response.lower())
        score += min(therapeutic_count * 0.1, 0.2)
        
        return min(score, 1.0)
    
    def _assess_therapeutic_value(self, response: str) -> str:
        """Assess the therapeutic value of a response"""
        therapeutic_indicators = [
            "let's", "together", "explore", "understand", "process", 
            "cope", "manage", "perspective", "consider"
        ]
        
        count = sum(1 for indicator in therapeutic_indicators if indicator in response.lower())
        
        if count >= 3:
            return "high"
        elif count >= 2:
            return "medium"
        else:
            return "low"
    
    def _assess_empathy_level(self, response: str) -> str:
        """Assess the empathy level of a response"""
        empathy_indicators = [
            "i hear", "i understand", "i can sense", "i feel", 
            "i know", "i'm here", "with you", "together"
        ]
        
        count = sum(1 for indicator in empathy_indicators if indicator in response.lower())
        
        if count >= 2:
            return "high"
        elif count >= 1:
            return "medium"
        else:
            return "low"
    
    def _count_empathy_indicators(self, response: str) -> int:
        """Count empathy indicators in response"""
        empathy_words = ["understand", "hear", "sense", "feel", "together", "support", "here"]
        return sum(1 for word in empathy_words if word in response.lower())
    
    def _count_therapeutic_keywords(self, response: str) -> int:
        """Count therapeutic keywords in response"""
        therapeutic_words = ["explore", "consider", "perspective", "cope", "manage", "process", "work through"]
        return sum(1 for word in therapeutic_words if word in response.lower())
    
    def _analyze_tone(self, response: str) -> str:
        """Analyze the tone of the response"""
        positive_words = ["good", "great", "wonderful", "excellent", "amazing", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "horrible", "disappointing"]
        
        pos_count = sum(1 for word in positive_words if word in response.lower())
        neg_count = sum(1 for word in negative_words if word in response.lower())
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
