"""
Enhanced reply generation service with RAG and more interactive responses.
This service uses the knowledge base for more contextual and interactive responses.
"""

import os
import random
import re
from typing import List, Dict, Any
from pathlib import Path
from .conversation_memory import conversation_memory
from .llm_integration import llm_integration

class EnhancedReplyGenerator:
    """
    Enhanced reply generator with RAG knowledge base integration.
    """
    
    def __init__(self):
        self.knowledge_base = {}
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load the knowledge base from scraped data."""
        try:
            # Try multiple possible paths
            possible_paths = [
                Path("scraped_data"),
                Path("../scraped_data"), 
                Path("../../scraped_data"),
                Path("/app/scraped_data")
            ]
            
            knowledge_path = None
            for path in possible_paths:
                if path.exists():
                    knowledge_path = path
                    break
            
            if not knowledge_path:
                print("❌ Knowledge base not found in any expected location")
                print(f"Tried paths: {[str(p) for p in possible_paths]}")
                return
            
            print(f"✅ Found knowledge base at: {knowledge_path}")
            
            # Load CBT knowledge
            cbt_path = knowledge_path / "cbt"
            if cbt_path.exists():
                for file in cbt_path.glob("*.txt"):
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.knowledge_base[file.stem] = content
            
            # Load mindfulness knowledge
            mindfulness_path = knowledge_path / "mindfulness"
            if mindfulness_path.exists():
                for file in mindfulness_path.glob("*.txt"):
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.knowledge_base[file.stem] = content
            
            # Load stress management knowledge
            stress_path = knowledge_path / "stress_management"
            if stress_path.exists():
                for file in stress_path.glob("*.txt"):
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.knowledge_base[file.stem] = content
                        
            print(f"✅ Loaded {len(self.knowledge_base)} knowledge base files")
            
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            self.knowledge_base = {}
    
    def find_relevant_content(self, user_text: str, emotion: str) -> str:
        """Find relevant content from knowledge base based on user input and emotion."""
        user_lower = user_text.lower()
        relevant_content = []
        
        # Search for relevant content based on keywords
        for filename, content in self.knowledge_base.items():
            content_lower = content.lower()
            relevance_score = 0
            
            # Emotion-based keywords
            emotion_keywords = {
                "anxiety": ["anxiety", "worry", "nervous", "panic", "fear", "stress"],
                "sadness": ["depression", "sad", "down", "blue", "hopeless", "grief"],
                "anger": ["anger", "frustration", "irritation", "rage", "mad"],
                "happiness": ["happy", "joy", "positive", "good mood", "excited"]
            }
            
            # Check for emotion-specific keywords
            if emotion in emotion_keywords:
                for keyword in emotion_keywords[emotion]:
                    if keyword in content_lower:
                        relevance_score += 2
            
            # Check for general therapeutic keywords
            therapeutic_keywords = ["cbt", "therapy", "technique", "exercise", "practice", "mindfulness", "breathing"]
            for keyword in therapeutic_keywords:
                if keyword in content_lower:
                    relevance_score += 1
            
            # Check for user input keywords
            user_words = user_lower.split()
            for word in user_words:
                if len(word) > 3 and word in content_lower:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_content.append((filename, content, relevance_score))
        
        # Sort by relevance and return top content
        relevant_content.sort(key=lambda x: x[2], reverse=True)
        
        if relevant_content:
            # Return the most relevant content (truncated)
            top_content = relevant_content[0][1]
            return top_content[:1000] + "..." if len(top_content) > 1000 else top_content
        
        return ""
    
    def generate_interactive_response(self, user_text: str, emotion: str, session_id: str = None) -> str:
        """
        Generate an interactive response using LLM integration and RAG.
        
        Args:
            user_text: The user's input text
            emotion: Detected emotion
            session_id: Session ID for conversation memory
            
        Returns:
            Interactive response string
        """
        print(f"🤖 Generating enhanced response for: '{user_text}' (emotion: {emotion})")
        
        # Get conversation context
        context = ""
        session_history = []
        if session_id:
            context = conversation_memory.get_personalized_context(session_id)
            session_data = conversation_memory.get_session_context(session_id)
            if "exchanges" in session_data:
                session_history = list(session_data["exchanges"])
            print(f"📝 Session context: {context}")
        
        # Use LLM integration for dynamic responses
        try:
            response = llm_integration.generate_response(
                user_message=user_text,
                emotion=emotion,
                context=context,
                session_history=session_history,
                therapeutic_style="supportive"
            )
            print(f"🧠 LLM generated response: {response[:100]}...")
            return response
            
        except Exception as e:
            print(f"⚠️ LLM integration failed: {e}, falling back to RAG system")
            
            # Fallback to RAG system
            relevant_knowledge = self.find_relevant_content(user_text, emotion)
            print(f"📚 Relevant knowledge found: {len(relevant_knowledge)} chars")
            
            # Generate base response
            base_response = self._generate_base_response(user_text, emotion, context)
            
            # Add RAG suggestions if available
            if relevant_knowledge:
                suggestions = self.extract_practical_suggestions(relevant_knowledge, emotion)
                if suggestions:
                    print(f"💡 Found suggestions: {suggestions[:100]}...")
                    base_response += f"\n\nHere's something that might help: {suggestions}"
                else:
                    print("⚠️ No suggestions extracted from knowledge base")
            else:
                print("⚠️ No relevant knowledge found")
            
            # Add conversation memory context
            if context and "topics_discussed" in context:
                topics = context["topics_discussed"]
                if topics:
                    base_response += f"\n\nI remember we've talked about {', '.join(topics[:3])} before. How are you feeling about those topics now?"
            
            print(f"✅ Generated response: {base_response[:100]}...")
            return base_response
    
    def _generate_base_response(self, user_text: str, emotion: str, context: str) -> str:
        """Generate a base response using enhanced templates."""
        
        # Enhanced response templates with more variety
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
    
    def extract_practical_suggestions(self, content: str, emotion: str) -> str:
        """Extract practical suggestions from knowledge base content."""
        # Enhanced patterns for more specific therapeutic techniques
        patterns = [
            # Breathing techniques
            r"(?:deep breathing|breathing exercise|breathing technique|breath work)\s+[^.]*\.", 
            r"(?:inhale|exhale|breathe in|breathe out)\s+[^.]*\.", 
            r"(?:4-7-8 breathing|box breathing|diaphragmatic breathing)\s+[^.]*\.", 
            
            # CBT techniques
            r"(?:thought challenging|cognitive restructuring|thought record)\s+[^.]*\.", 
            r"(?:behavioral activation|activity scheduling|exposure therapy)\s+[^.]*\.", 
            r"(?:mindfulness|meditation|grounding technique)\s+[^.]*\.", 
            
            # Specific exercises
            r"(?:progressive muscle relaxation|PMR|body scan)\s+[^.]*\.", 
            r"(?:5-4-3-2-1 grounding|54321 technique|sensory grounding)\s+[^.]*\.", 
            r"(?:mindful walking|body awareness|present moment)\s+[^.]*\.", 
            
            # Action-oriented advice
            r"(?:try|consider|practice|do|use|start|begin)\s+[^.]*\.", 
            r"(?:exercise|technique|method|approach|strategy)\s+[^.]*\.", 
            r"(?:step|steps|process|procedure)\s+[^.]*\.", 
        ]
        
        suggestions = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                suggestions.extend(matches[:2])  # Take first 2 matches
        
        print(f"🔍 Found {len(suggestions)} suggestions: {suggestions}")
        
        if suggestions:
            return random.choice(suggestions)
        
        # Enhanced fallback: look for sentences with helpful keywords
        helpful_keywords = [
            # Breathing and relaxation
            "breathing", "breathe", "inhale", "exhale", "relax", "calm", "peaceful", 
            "gentle", "soothing", "slow", "deep", "controlled",
            
            # CBT and therapeutic techniques
            "exercise", "technique", "practice", "method", "approach", "strategy",
            "mindfulness", "meditation", "grounding", "focus", "concentrate", "center",
            
            # Specific therapeutic terms
            "progressive", "muscle", "relaxation", "body", "scan", "awareness",
            "thought", "challenging", "cognitive", "behavioral", "activation",
            "exposure", "therapy", "sensory", "present", "moment"
        ]
        
        sentences = content.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in helpful_keywords):
                if len(sentence.strip()) > 15 and len(sentence.strip()) < 200:  # Good length range
                    print(f"🎯 Found helpful sentence: {sentence.strip()}")
                    return sentence.strip()
        
        # Last resort: find any sentence with therapeutic keywords
        therapeutic_keywords = ["help", "support", "manage", "cope", "reduce", "improve", "better"]
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in therapeutic_keywords):
                if len(sentence.strip()) > 20 and len(sentence.strip()) < 150:
                    print(f"💡 Found therapeutic sentence: {sentence.strip()}")
                    return sentence.strip()
        
        return ""

def generate_reply(transcribed_text: str, emotion: str, session_id: str = None) -> str:
    """
    Enhanced reply generation with RAG knowledge base and conversation memory.
    
    Args:
        transcribed_text: The user's transcribed speech
        emotion: The detected emotion from the emotion service
        session_id: Optional session identifier for conversation memory
    
    Returns:
        A more interactive and contextual therapeutic response.
    """
    generator = EnhancedReplyGenerator()
    return generator.generate_interactive_response(transcribed_text, emotion, session_id)

def load_reply_model() -> bool:
    """
    Load the enhanced reply model.
    """
    print("Loading enhanced reply generation with RAG knowledge base...")
    return True
