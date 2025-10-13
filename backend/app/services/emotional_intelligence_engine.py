"""
Emotional Intelligence Engine
Advanced emotional analysis and response generation
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import numpy as np

logger = logging.getLogger(__name__)

class EmotionalIntelligenceEngine:
    """Advanced emotional intelligence for therapeutic responses"""
    
    def __init__(self):
        self.emotion_patterns = self._load_emotion_patterns()
        self.emotional_triggers = self._load_emotional_triggers()
        self.therapeutic_interventions = self._load_therapeutic_interventions()
        self.emotion_history = {}
    
    def _load_emotion_patterns(self) -> Dict[str, Dict]:
        """Load patterns for different emotional states"""
        return {
            "anxiety": {
                "indicators": ["worry", "fear", "panic", "overwhelmed", "racing thoughts"],
                "physical_signs": ["tension", "rapid breathing", "sweating", "shaking"],
                "cognitive_patterns": ["catastrophizing", "what-if thinking", "perfectionism"],
                "intervention_priority": ["grounding", "breathing", "cognitive_restructuring"]
            },
            "depression": {
                "indicators": ["sadness", "hopelessness", "worthlessness", "fatigue", "isolation"],
                "physical_signs": ["low energy", "sleep changes", "appetite changes", "slowed movement"],
                "cognitive_patterns": ["negative_self_talk", "all_or_nothing", "personalization"],
                "intervention_priority": ["behavioral_activation", "mindfulness", "social_connection"]
            },
            "anger": {
                "indicators": ["frustration", "irritation", "rage", "resentment", "hostility"],
                "physical_signs": ["muscle_tension", "increased_heart_rate", "clenched_jaw"],
                "cognitive_patterns": ["blame", "unfairness", "injustice", "demands"],
                "intervention_priority": ["emotion_regulation", "mindfulness", "communication_skills"]
            },
            "stress": {
                "indicators": ["pressure", "overwhelm", "deadline_fear", "responsibility"],
                "physical_signs": ["tension", "headaches", "stomach_issues", "sleep_problems"],
                "cognitive_patterns": ["perfectionism", "control_issues", "time_pressure"],
                "intervention_priority": ["stress_management", "time_management", "relaxation"]
            }
        }
    
    def _load_emotional_triggers(self) -> Dict[str, List[str]]:
        """Load common emotional triggers"""
        return {
            "anxiety_triggers": [
                "uncertainty", "change", "social_situations", "performance", "health_concerns",
                "financial_worries", "relationships", "work_pressure", "future_planning"
            ],
            "depression_triggers": [
                "loss", "rejection", "failure", "criticism", "loneliness", "trauma",
                "seasonal_changes", "life_transitions", "health_issues", "relationship_problems"
            ],
            "anger_triggers": [
                "injustice", "disrespect", "boundary_violations", "frustration", "criticism",
                "control_issues", "unfairness", "betrayal", "disappointment", "powerlessness"
            ],
            "stress_triggers": [
                "workload", "deadlines", "conflict", "change", "responsibility", "perfectionism",
                "time_pressure", "financial_pressure", "relationship_stress", "health_concerns"
            ]
        }
    
    def _load_therapeutic_interventions(self) -> Dict[str, Dict]:
        """Load evidence-based therapeutic interventions"""
        return {
            "grounding_techniques": {
                "description": "Help user connect with present moment",
                "techniques": [
                    "5-4-3-2-1 grounding: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
                    "Box breathing: Inhale 4 counts, hold 4, exhale 4, hold 4",
                    "Progressive muscle relaxation: Tense and release each muscle group"
                ]
            },
            "cognitive_restructuring": {
                "description": "Challenge and reframe negative thoughts",
                "techniques": [
                    "Thought challenging: What evidence do you have for this thought?",
                    "Perspective taking: What would you tell a friend?",
                    "Alternative thinking: What's another way to see this?"
                ]
            },
            "behavioral_activation": {
                "description": "Increase engagement in positive activities",
                "techniques": [
                    "Activity scheduling: Plan one pleasant activity daily",
                    "Graded task assignment: Break large tasks into small steps",
                    "Social engagement: Connect with supportive people"
                ]
            },
            "mindfulness_practices": {
                "description": "Present-moment awareness and acceptance",
                "techniques": [
                    "Mindful breathing: Focus on breath for 5 minutes",
                    "Body scan: Notice sensations from head to toe",
                    "Loving-kindness meditation: Send compassion to self and others"
                ]
            }
        }
    
    def analyze_emotional_state(self, 
                              text_input: str, 
                              audio_features: Optional[Dict] = None,
                              user_history: Optional[Dict] = None) -> Dict[str, any]:
        """Comprehensive emotional state analysis"""
        
        try:
            # Text-based emotion analysis
            text_emotions = self._analyze_text_emotions(text_input)
            
            # Audio-based emotion analysis (if available)
            audio_emotions = self._analyze_audio_emotions(audio_features) if audio_features else {}
            
            # Historical context analysis
            historical_context = self._analyze_historical_context(user_history) if user_history else {}
            
            # Combine analyses
            combined_analysis = self._combine_emotional_analyses(
                text_emotions, audio_emotions, historical_context
            )
            
            # Identify emotional patterns
            emotional_patterns = self._identify_emotional_patterns(combined_analysis)
            
            # Assess emotional intensity
            intensity_level = self._assess_emotional_intensity(combined_analysis)
            
            # Identify triggers
            potential_triggers = self._identify_potential_triggers(text_input, combined_analysis)
            
            # Generate emotional insights
            insights = self._generate_emotional_insights(
                combined_analysis, emotional_patterns, potential_triggers
            )
            
            return {
                "primary_emotion": combined_analysis["primary_emotion"],
                "emotion_confidence": combined_analysis["confidence"],
                "emotional_intensity": intensity_level,
                "emotional_patterns": emotional_patterns,
                "potential_triggers": potential_triggers,
                "insights": insights,
                "recommended_interventions": self._recommend_interventions(
                    combined_analysis["primary_emotion"], intensity_level, emotional_patterns
                ),
                "emotional_safety": self._assess_emotional_safety(combined_analysis),
                "therapeutic_approach": self._determine_therapeutic_approach(
                    combined_analysis["primary_emotion"], intensity_level
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing emotional state: {e}")
            return {
                "primary_emotion": "neutral",
                "error": str(e)
            }
    
    def _analyze_text_emotions(self, text: str) -> Dict:
        """Analyze emotions from text input"""
        text_lower = text.lower()
        
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for indicator in patterns["indicators"]:
                if indicator in text_lower:
                    score += 1
            emotion_scores[emotion] = score / len(patterns["indicators"])
        
        # Find primary emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[primary_emotion]
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "emotion_scores": emotion_scores
        }
    
    def _analyze_audio_emotions(self, audio_features: Dict) -> Dict:
        """Analyze emotions from audio features"""
        try:
            # Extract key audio features
            energy = audio_features.get("energy", 0.5)
            pitch = audio_features.get("pitch", 0.5)
            tempo = audio_features.get("tempo", 120)
            spectral_centroid = audio_features.get("spectral_centroid", 0.5)
            
            # Analyze emotion based on audio features
            emotion_scores = {
                "happy": 0.0,
                "sad": 0.0,
                "angry": 0.0,
                "fearful": 0.0,
                "neutral": 0.5
            }
            
            # High energy + high pitch = happy
            if energy > 0.7 and pitch > 0.6:
                emotion_scores["happy"] = min(0.9, energy + pitch - 0.5)
            
            # Low energy + low pitch = sad
            elif energy < 0.4 and pitch < 0.4:
                emotion_scores["sad"] = min(0.9, (0.5 - energy) + (0.5 - pitch))
            
            # High energy + low pitch = angry
            elif energy > 0.7 and pitch < 0.4:
                emotion_scores["angry"] = min(0.9, energy + (0.5 - pitch))
            
            # High tempo + high spectral centroid = fearful/anxious
            elif tempo > 140 and spectral_centroid > 0.6:
                emotion_scores["fearful"] = min(0.9, (tempo - 120) / 100 + spectral_centroid)
            
            # Find primary emotion
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[primary_emotion]
            
            # Generate audio indicators
            indicators = []
            if energy > 0.7:
                indicators.append("high_energy")
            if pitch > 0.6:
                indicators.append("high_pitch")
            if tempo > 140:
                indicators.append("fast_tempo")
            if spectral_centroid > 0.6:
                indicators.append("bright_tone")
            
            return {
                "primary_emotion": primary_emotion,
                "confidence": confidence,
                "audio_indicators": indicators,
                "emotion_scores": emotion_scores
            }
            
        except Exception as e:
            logger.error(f"Error analyzing audio emotions: {e}")
            return {
                "primary_emotion": "neutral",
                "confidence": 0.5,
                "audio_indicators": [],
                "error": str(e)
            }
    
    def _analyze_historical_context(self, user_history: Dict) -> Dict:
        """Analyze historical emotional context"""
        if not user_history:
            return {}
        
        # Analyze emotional trends
        recent_emotions = user_history.get("recent_emotions", [])
        if recent_emotions:
            emotion_trend = self._calculate_emotion_trend(recent_emotions)
            return {
                "emotion_trend": emotion_trend,
                "recent_patterns": self._identify_recent_patterns(recent_emotions)
            }
        
        return {}
    
    def _combine_emotional_analyses(self, 
                                   text_emotions: Dict, 
                                   audio_emotions: Dict, 
                                   historical_context: Dict) -> Dict:
        """Combine different emotional analyses"""
        
        # Weight different sources
        text_weight = 0.6
        audio_weight = 0.3
        historical_weight = 0.1
        
        # Combine emotion scores
        combined_scores = {}
        for emotion in self.emotion_patterns.keys():
            score = 0
            if emotion in text_emotions.get("emotion_scores", {}):
                score += text_emotions["emotion_scores"][emotion] * text_weight
            if emotion in audio_emotions.get("emotion_scores", {}):
                score += audio_emotions["emotion_scores"][emotion] * audio_weight
            
            combined_scores[emotion] = score
        
        # Find primary emotion
        primary_emotion = max(combined_scores, key=combined_scores.get)
        confidence = combined_scores[primary_emotion]
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "combined_scores": combined_scores,
            "text_analysis": text_emotions,
            "audio_analysis": audio_emotions,
            "historical_context": historical_context
        }
    
    def _identify_emotional_patterns(self, analysis: Dict) -> List[str]:
        """Identify emotional patterns in the analysis"""
        patterns = []
        primary_emotion = analysis["primary_emotion"]
        
        if primary_emotion in self.emotion_patterns:
            emotion_data = self.emotion_patterns[primary_emotion]
            
            # Check for cognitive patterns
            for pattern in emotion_data["cognitive_patterns"]:
                patterns.append(f"cognitive_{pattern}")
            
            # Check for physical patterns
            for pattern in emotion_data["physical_signs"]:
                patterns.append(f"physical_{pattern}")
        
        return patterns
    
    def _assess_emotional_intensity(self, analysis: Dict) -> str:
        """Assess the intensity of emotional state"""
        confidence = analysis["confidence"]
        
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _identify_potential_triggers(self, text: str, analysis: Dict) -> List[str]:
        """Identify potential emotional triggers"""
        triggers = []
        text_lower = text.lower()
        
        for trigger_category, trigger_list in self.emotional_triggers.items():
            for trigger in trigger_list:
                if trigger in text_lower:
                    triggers.append(trigger)
        
        return triggers
    
    def _generate_emotional_insights(self, 
                                   analysis: Dict, 
                                   patterns: List[str], 
                                   triggers: List[str]) -> List[str]:
        """Generate insights about the emotional state"""
        insights = []
        primary_emotion = analysis["primary_emotion"]
        
        # Emotion-specific insights
        if primary_emotion == "anxiety":
            insights.append("You're experiencing anxiety, which is your mind's way of trying to protect you from perceived threats.")
            if "catastrophizing" in patterns:
                insights.append("Your mind is jumping to worst-case scenarios, which is common with anxiety.")
        
        elif primary_emotion == "depression":
            insights.append("You're feeling depressed, which can make everything seem heavy and difficult.")
            if "negative_self_talk" in patterns:
                insights.append("Your inner critic seems to be very active right now.")
        
        elif primary_emotion == "anger":
            insights.append("You're feeling angry, which often signals that something important to you has been threatened.")
            if "injustice" in triggers:
                insights.append("It sounds like you're feeling that something unfair has happened.")
        
        # General insights
        if triggers:
            insights.append(f"Some potential triggers I notice: {', '.join(triggers[:3])}")
        
        return insights
    
    def _recommend_interventions(self, 
                               emotion: str, 
                               intensity: str, 
                               patterns: List[str]) -> List[str]:
        """Recommend therapeutic interventions"""
        interventions = []
        
        if emotion in self.emotion_patterns:
            emotion_data = self.emotion_patterns[emotion]
            priority_interventions = emotion_data["intervention_priority"]
            
            for intervention in priority_interventions:
                if intervention in self.therapeutic_interventions:
                    intervention_data = self.therapeutic_interventions[intervention]
                    interventions.append({
                        "name": intervention,
                        "description": intervention_data["description"],
                        "techniques": intervention_data["techniques"][:2]  # Top 2 techniques
                    })
        
        return interventions[:3]  # Top 3 interventions
    
    def _assess_emotional_safety(self, analysis: Dict) -> str:
        """Assess emotional safety level"""
        primary_emotion = analysis["primary_emotion"]
        confidence = analysis["confidence"]
        
        # High-risk emotions
        high_risk_emotions = ["depression", "anger"]
        
        if primary_emotion in high_risk_emotions and confidence > 0.7:
            return "monitor_closely"
        elif confidence > 0.8:
            return "stable"
        else:
            return "unclear"
    
    def _determine_therapeutic_approach(self, emotion: str, intensity: str) -> str:
        """Determine the best therapeutic approach"""
        if intensity == "high":
            return "supportive_stabilization"
        elif emotion in ["anxiety", "stress"]:
            return "cognitive_behavioral"
        elif emotion == "depression":
            return "behavioral_activation"
        elif emotion == "anger":
            return "emotion_regulation"
        else:
            return "general_supportive"
    
    def _calculate_emotion_trend(self, recent_emotions: List[str]) -> str:
        """Calculate emotional trend from recent history"""
        if len(recent_emotions) < 3:
            return "insufficient_data"
        
        # Simple trend calculation
        positive_emotions = ["happy", "calm", "content", "peaceful"]
        negative_emotions = ["anxiety", "depression", "anger", "stress"]
        
        recent_positive = sum(1 for emotion in recent_emotions[-5:] if emotion in positive_emotions)
        recent_negative = sum(1 for emotion in recent_emotions[-5:] if emotion in negative_emotions)
        
        if recent_positive > recent_negative:
            return "improving"
        elif recent_negative > recent_positive:
            return "declining"
        else:
            return "stable"
    
    def _identify_recent_patterns(self, recent_emotions: List[str]) -> List[str]:
        """Identify patterns in recent emotional history"""
        patterns = []
        
        # Check for emotional cycling
        if len(set(recent_emotions)) > 3:
            patterns.append("emotional_cycling")
        
        # Check for emotional stability
        if len(set(recent_emotions)) == 1:
            patterns.append("emotional_stability")
        
        return patterns
