"""
Interactive features service for guided exercises and therapeutic activities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class InteractiveFeatures:
    """
    Provides interactive therapeutic exercises and guided activities.
    """
    
    def __init__(self):
        self.exercises = {
            "breathing": {
                "4-7-8_breathing": {
                    "name": "4-7-8 Breathing Exercise",
                    "description": "A calming breathing technique to reduce anxiety",
                    "steps": [
                        "Sit comfortably and close your eyes",
                        "Inhale through your nose for 4 counts",
                        "Hold your breath for 7 counts", 
                        "Exhale through your mouth for 8 counts",
                        "Repeat this cycle 4 times"
                    ],
                    "duration_minutes": 5,
                    "benefits": ["Reduces anxiety", "Promotes relaxation", "Improves focus"]
                },
                "box_breathing": {
                    "name": "Box Breathing",
                    "description": "A simple breathing exercise for stress relief",
                    "steps": [
                        "Inhale for 4 counts",
                        "Hold for 4 counts",
                        "Exhale for 4 counts", 
                        "Hold for 4 counts",
                        "Repeat for 5-10 minutes"
                    ],
                    "duration_minutes": 10,
                    "benefits": ["Reduces stress", "Improves concentration", "Calms nervous system"]
                }
            },
            "mindfulness": {
                "body_scan": {
                    "name": "Body Scan Meditation",
                    "description": "A mindfulness exercise to connect with your body",
                    "steps": [
                        "Lie down or sit comfortably",
                        "Close your eyes and take 3 deep breaths",
                        "Start at your toes and notice any sensations",
                        "Slowly move your attention up through your body",
                        "Spend 30 seconds on each body part",
                        "End with 3 deep breaths"
                    ],
                    "duration_minutes": 15,
                    "benefits": ["Reduces tension", "Improves body awareness", "Promotes relaxation"]
                },
                "5_4_3_2_1_grounding": {
                    "name": "5-4-3-2-1 Grounding Technique",
                    "description": "A grounding exercise for anxiety and panic",
                    "steps": [
                        "Name 5 things you can see around you",
                        "Name 4 things you can touch",
                        "Name 3 things you can hear",
                        "Name 2 things you can smell",
                        "Name 1 thing you can taste",
                        "Take 3 deep breaths"
                    ],
                    "duration_minutes": 3,
                    "benefits": ["Reduces panic", "Grounds you in present", "Calms anxiety"]
                }
            },
            "cbt": {
                "thought_challenging": {
                    "name": "Thought Challenging Exercise",
                    "description": "A CBT technique to challenge negative thoughts",
                    "steps": [
                        "Write down the negative thought",
                        "Ask: Is this thought 100% true?",
                        "What evidence supports this thought?",
                        "What evidence contradicts this thought?",
                        "What would you tell a friend in this situation?",
                        "Write a more balanced thought"
                    ],
                    "duration_minutes": 10,
                    "benefits": ["Challenges negative thinking", "Improves perspective", "Reduces anxiety"]
                },
                "gratitude_journal": {
                    "name": "Gratitude Journaling",
                    "description": "A positive psychology exercise",
                    "steps": [
                        "Write down 3 things you're grateful for today",
                        "For each item, explain why you're grateful",
                        "Notice how you feel after writing",
                        "Commit to doing this daily"
                    ],
                    "duration_minutes": 5,
                    "benefits": ["Increases positivity", "Improves mood", "Reduces depression"]
                }
            }
        }
        
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def start_exercise(self, user_id: str, exercise_type: str, exercise_name: str) -> Dict[str, Any]:
        """
        Start an interactive exercise.
        
        Args:
            user_id: User identifier
            exercise_type: Type of exercise (breathing, mindfulness, cbt)
            exercise_name: Name of the exercise
            
        Returns:
            Exercise session information
        """
        if exercise_type not in self.exercises:
            return {"error": "Invalid exercise type"}
        
        if exercise_name not in self.exercises[exercise_type]:
            return {"error": "Invalid exercise name"}
        
        exercise = self.exercises[exercise_type][exercise_name]
        session_id = f"exercise_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "exercise_type": exercise_type,
            "exercise_name": exercise_name,
            "exercise_data": exercise,
            "start_time": datetime.now().isoformat(),
            "current_step": 0,
            "completed": False,
            "progress": 0.0
        }
        
        self.active_sessions[session_id] = session
        
        print(f"🎯 Started exercise session: {exercise_name} for user {user_id}")
        return session
    
    def get_next_step(self, session_id: str) -> Dict[str, Any]:
        """
        Get the next step in an exercise.
        
        Args:
            session_id: Exercise session identifier
            
        Returns:
            Next step information
        """
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        exercise = session["exercise_data"]
        current_step = session["current_step"]
        
        if current_step >= len(exercise["steps"]):
            return {"message": "Exercise completed!", "completed": True}
        
        step_info = {
            "step_number": current_step + 1,
            "total_steps": len(exercise["steps"]),
            "step_instruction": exercise["steps"][current_step],
            "progress": (current_step + 1) / len(exercise["steps"]) * 100,
            "exercise_name": exercise["name"]
        }
        
        return step_info
    
    def complete_step(self, session_id: str) -> Dict[str, Any]:
        """
        Mark a step as completed and move to next.
        
        Args:
            session_id: Exercise session identifier
            
        Returns:
            Updated session information
        """
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        session["current_step"] += 1
        
        # Check if exercise is completed
        if session["current_step"] >= len(session["exercise_data"]["steps"]):
            session["completed"] = True
            session["end_time"] = datetime.now().isoformat()
            session["progress"] = 100.0
            
            print(f"✅ Exercise completed: {session['exercise_name']} for user {session['user_id']}")
        
        return session
    
    def get_exercise_recommendations(self, emotion: str, context: str = "") -> List[Dict[str, Any]]:
        """
        Get exercise recommendations based on emotion and context.
        
        Args:
            emotion: User's current emotion
            context: Additional context
            
        Returns:
            List of recommended exercises
        """
        recommendations = []
        
        # Emotion-based recommendations
        if emotion in ["anxiety", "fear", "panic"]:
            recommendations.extend([
                {"type": "breathing", "name": "4-7-8_breathing", "priority": "high"},
                {"type": "mindfulness", "name": "5_4_3_2_1_grounding", "priority": "high"},
                {"type": "breathing", "name": "box_breathing", "priority": "medium"}
            ])
        elif emotion in ["sadness", "depression"]:
            recommendations.extend([
                {"type": "cbt", "name": "gratitude_journal", "priority": "high"},
                {"type": "mindfulness", "name": "body_scan", "priority": "medium"},
                {"type": "cbt", "name": "thought_challenging", "priority": "medium"}
            ])
        elif emotion in ["anger", "frustration"]:
            recommendations.extend([
                {"type": "breathing", "name": "box_breathing", "priority": "high"},
                {"type": "mindfulness", "name": "body_scan", "priority": "medium"}
            ])
        else:  # neutral, happiness, etc.
            recommendations.extend([
                {"type": "mindfulness", "name": "body_scan", "priority": "medium"},
                {"type": "cbt", "name": "gratitude_journal", "priority": "low"}
            ])
        
        # Add exercise details
        for rec in recommendations:
            exercise_type = rec["type"]
            exercise_name = rec["name"]
            if exercise_type in self.exercises and exercise_name in self.exercises[exercise_type]:
                exercise = self.exercises[exercise_type][exercise_name]
                rec.update({
                    "title": exercise["name"],
                    "description": exercise["description"],
                    "duration_minutes": exercise["duration_minutes"],
                    "benefits": exercise["benefits"]
                })
        
        return recommendations
    
    def get_guided_session(self, user_id: str, emotion: str, duration_minutes: int = 15) -> Dict[str, Any]:
        """
        Create a guided therapeutic session.
        
        Args:
            user_id: User identifier
            emotion: User's current emotion
            duration_minutes: Desired session duration
            
        Returns:
            Guided session plan
        """
        recommendations = self.get_exercise_recommendations(emotion)
        
        # Select exercises based on duration
        selected_exercises = []
        total_duration = 0
        
        for rec in recommendations:
            if rec.get("duration_minutes", 0) + total_duration <= duration_minutes:
                selected_exercises.append(rec)
                total_duration += rec.get("duration_minutes", 0)
        
        session_plan = {
            "user_id": user_id,
            "emotion": emotion,
            "duration_minutes": duration_minutes,
            "exercises": selected_exercises,
            "total_exercises": len(selected_exercises),
            "estimated_duration": total_duration,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"🎯 Created guided session for user {user_id}: {len(selected_exercises)} exercises")
        return session_plan
    
    def get_exercise_categories(self) -> Dict[str, List[str]]:
        """
        Get available exercise categories and exercises.
        
        Returns:
            Dictionary of categories and exercises
        """
        categories = {}
        for category, exercises in self.exercises.items():
            categories[category] = list(exercises.keys())
        return categories
    
    def get_exercise_details(self, exercise_type: str, exercise_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific exercise.
        
        Args:
            exercise_type: Type of exercise
            exercise_name: Name of the exercise
            
        Returns:
            Exercise details
        """
        if exercise_type not in self.exercises:
            return {"error": "Invalid exercise type"}
        
        if exercise_name not in self.exercises[exercise_type]:
            return {"error": "Invalid exercise name"}
        
        return self.exercises[exercise_type][exercise_name]

# Global interactive features instance
interactive_features = InteractiveFeatures()
