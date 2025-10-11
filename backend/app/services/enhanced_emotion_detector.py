"""
Enhanced emotion detection service with more nuanced detection and confidence scoring.
"""

import re
from typing import Dict, List, Tuple, Any
from datetime import datetime

class EnhancedEmotionDetector:
    """
    Enhanced emotion detector with nuanced detection and confidence scoring.
    """
    
    def __init__(self):
        # Enhanced emotion keywords with intensity levels
        self.emotion_patterns = {
            "anxiety": {
                "high_intensity": ["panic", "terrified", "overwhelmed", "frozen", "paralyzed", "crippling"],
                "medium_intensity": ["anxious", "worried", "nervous", "stressed", "uneasy", "restless"],
                "low_intensity": ["concerned", "apprehensive", "uncertain", "hesitant", "cautious"]
            },
            "sadness": {
                "high_intensity": ["devastated", "crushed", "heartbroken", "despair", "hopeless", "empty"],
                "medium_intensity": ["sad", "depressed", "down", "blue", "miserable", "gloomy"],
                "low_intensity": ["melancholy", "somber", "subdued", "low", "disappointed"]
            },
            "anger": {
                "high_intensity": ["furious", "enraged", "livid", "seething", "explosive", "volatile"],
                "medium_intensity": ["angry", "mad", "irritated", "annoyed", "frustrated", "upset"],
                "low_intensity": ["irritated", "bothered", "agitated", "displeased", "resentful"]
            },
            "happiness": {
                "high_intensity": ["ecstatic", "thrilled", "elated", "overjoyed", "euphoric", "blissful"],
                "medium_intensity": ["happy", "joyful", "cheerful", "content", "pleased", "satisfied"],
                "low_intensity": ["content", "pleased", "satisfied", "comfortable", "at ease"]
            },
            "fear": {
                "high_intensity": ["terrified", "petrified", "frozen", "horrified", "dread", "terror"],
                "medium_intensity": ["scared", "afraid", "frightened", "alarmed", "worried", "concerned"],
                "low_intensity": ["uneasy", "apprehensive", "cautious", "wary", "nervous"]
            },
            "disgust": {
                "high_intensity": ["revolted", "repulsed", "sickened", "disgusted", "nauseated"],
                "medium_intensity": ["disgusted", "repelled", "offended", "disturbed", "uncomfortable"],
                "low_intensity": ["uncomfortable", "bothered", "disturbed", "unsettled"]
            },
            "surprise": {
                "high_intensity": ["shocked", "stunned", "astounded", "amazed", "bewildered"],
                "medium_intensity": ["surprised", "startled", "taken aback", "caught off guard"],
                "low_intensity": ["curious", "intrigued", "interested", "perplexed"]
            }
        }
        
        # Contextual indicators
        self.context_indicators = {
            "anxiety": ["interview", "test", "presentation", "meeting", "deadline", "performance"],
            "sadness": ["loss", "death", "breakup", "failure", "rejection", "lonely"],
            "anger": ["unfair", "wrong", "mistake", "problem", "issue", "conflict"],
            "happiness": ["success", "achievement", "good news", "celebration", "accomplishment"],
            "fear": ["danger", "threat", "risk", "unknown", "uncertainty", "change"]
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            "very": 1.5, "extremely": 2.0, "incredibly": 2.0, "totally": 1.8,
            "completely": 1.8, "absolutely": 1.8, "really": 1.3, "quite": 1.2,
            "somewhat": 0.8, "slightly": 0.6, "a bit": 0.7, "kind of": 0.8
        }
    
    def detect_emotion(self, text: str, context: str = "") -> Tuple[str, float, Dict[str, Any]]:
        """
        Detect emotion with enhanced analysis and confidence scoring.
        
        Args:
            text: Input text to analyze
            context: Optional conversation context
            
        Returns:
            Tuple of (emotion, confidence, analysis_details)
        """
        text_lower = text.lower()
        emotion_scores = {}
        analysis_details = {
            "detected_keywords": {},
            "intensity_levels": {},
            "context_matches": {},
            "confidence_factors": []
        }
        
        # Score each emotion
        for emotion, patterns in self.emotion_patterns.items():
            score = 0.0
            detected_keywords = []
            intensity_scores = {"high": 0, "medium": 0, "low": 0}
            
            # Check intensity levels
            for intensity, keywords in patterns.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        detected_keywords.append(keyword)
                        # Map intensity names to score keys
                        intensity_key = intensity.replace("_intensity", "")
                        intensity_scores[intensity_key] += 1
                        
                        # Base score based on intensity
                        if intensity == "high_intensity":
                            score += 3.0
                        elif intensity == "medium_intensity":
                            score += 2.0
                        else:  # low_intensity
                            score += 1.0
            
            # Check for intensity modifiers
            for modifier, multiplier in self.intensity_modifiers.items():
                if modifier in text_lower:
                    # Find nearby emotion keywords
                    words = text_lower.split()
                    for i, word in enumerate(words):
                        if word == modifier:
                            # Check surrounding words for emotion keywords
                            for j in range(max(0, i-2), min(len(words), i+3)):
                                if words[j] in [kw for kws in patterns.values() for kw in kws]:
                                    score *= multiplier
                                    analysis_details["confidence_factors"].append(f"Intensity modifier: {modifier}")
                                    break
            
            # Check context indicators
            context_score = 0
            if context:
                for indicator in self.context_indicators.get(emotion, []):
                    if indicator in context.lower():
                        context_score += 0.5
                        analysis_details["context_matches"][emotion] = analysis_details["context_matches"].get(emotion, []) + [indicator]
            
            # Apply context bonus
            score += context_score
            
            if score > 0:
                emotion_scores[emotion] = score
                analysis_details["detected_keywords"][emotion] = detected_keywords
                analysis_details["intensity_levels"][emotion] = intensity_scores
        
        # Determine primary emotion
        if not emotion_scores:
            return "neutral", 0.5, analysis_details
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[primary_emotion]
        
        # Calculate confidence based on score and competition
        total_score = sum(emotion_scores.values())
        confidence = min(0.95, max_score / max(total_score, 1.0))
        
        # Adjust confidence based on factors
        if len(analysis_details["detected_keywords"].get(primary_emotion, [])) > 1:
            confidence += 0.1
        if analysis_details["intensity_levels"].get(primary_emotion, {}).get("high", 0) > 0:
            confidence += 0.15
        if analysis_details["context_matches"].get(primary_emotion):
            confidence += 0.1
        
        # Ensure confidence is within bounds
        confidence = max(0.1, min(0.95, confidence))
        
        analysis_details["emotion_scores"] = emotion_scores
        analysis_details["confidence_factors"].append(f"Primary emotion score: {max_score:.2f}")
        analysis_details["confidence_factors"].append(f"Total emotion score: {total_score:.2f}")
        
        return primary_emotion, confidence, analysis_details
    
    def get_emotion_insights(self, emotion: str, confidence: float, analysis: Dict[str, Any]) -> str:
        """
        Generate insights about the detected emotion.
        
        Args:
            emotion: Detected emotion
            confidence: Confidence score
            analysis: Analysis details
            
        Returns:
            Human-readable insights
        """
        insights = []
        
        # Confidence level description
        if confidence >= 0.8:
            insights.append("High confidence emotion detection")
        elif confidence >= 0.6:
            insights.append("Moderate confidence emotion detection")
        else:
            insights.append("Low confidence emotion detection")
        
        # Intensity analysis
        intensity_levels = analysis.get("intensity_levels", {}).get(emotion, {})
        if intensity_levels.get("high", 0) > 0:
            insights.append("High intensity emotional expression detected")
        elif intensity_levels.get("medium", 0) > 0:
            insights.append("Medium intensity emotional expression detected")
        elif intensity_levels.get("low", 0) > 0:
            insights.append("Low intensity emotional expression detected")
        
        # Context relevance
        if analysis.get("context_matches", {}).get(emotion):
            insights.append("Context-appropriate emotion detection")
        
        return " | ".join(insights)

# Global enhanced emotion detector instance
enhanced_emotion_detector = EnhancedEmotionDetector()
