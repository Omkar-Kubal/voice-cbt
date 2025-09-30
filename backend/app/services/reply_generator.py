"""
Reply generation service using RAG (Retrieval-Augmented Generation).
This service combines the fine-tuned dialogue model with the RAG knowledge base.
"""

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from typing import Optional, Dict, Any, List
import random

class ReplyGenerator:
    """
    Service for generating therapeutic responses using RAG.
    """
    
    def __init__(self, 
                 model_path: str = "./dialogue_model_finetuned",
                 chroma_db_path: str = "../chroma_db",
                 use_rag: bool = True):
        self.model_path = model_path
        self.chroma_db_path = chroma_db_path
        self.use_rag = use_rag
        
        # Model components
        self.llm_model = None
        self.tokenizer = None
        self.retriever = None
        self.embeddings = None
        
        # RAG prompt template
        self.rag_prompt_template = """You are a compassionate, helpful, and empathetic AI therapist specializing in Cognitive Behavioral Therapy (CBT).

Context from knowledge base:
{context}

User's Emotion: {emotion}
User's Message: {message}

Instructions:
- Provide a therapeutic response based on the context and user's emotional state
- Use CBT techniques and evidence-based approaches
- Be empathetic and supportive
- Keep responses concise but meaningful
- Focus on helping the user explore their thoughts and feelings

Therapist's Response:"""
        
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "emotion", "message"], 
            template=self.rag_prompt_template
        )
        
        # Fallback responses for when models aren't available
        self.fallback_responses = {
            "happiness": [
                "I'm glad to hear you're feeling positive! What's contributing to this good mood?",
                "It's wonderful that you're experiencing joy. Can you tell me more about what's making you happy?",
                "Your positive energy is contagious! What's been going well for you lately?"
            ],
            "sadness": [
                "I can sense that you're going through a difficult time. Would you like to talk about what's been weighing on you?",
                "It's okay to feel sad sometimes. What's been on your mind lately?",
                "I'm here to listen. What's been making you feel this way?"
            ],
            "anger": [
                "I can hear the frustration in your voice. What's been making you feel this way?",
                "It sounds like you're dealing with some strong emotions. Would you like to explore what's behind these feelings?",
                "Anger can be a powerful emotion. What's been triggering these feelings for you?"
            ],
            "fear": [
                "I understand that you might be feeling anxious or worried. What's been causing you concern?",
                "It's natural to feel afraid sometimes. What's been on your mind that's causing worry?",
                "I'm here to help you work through these feelings. What's been making you feel anxious?"
            ],
            "neutral": [
                "I'm here to listen. How are you feeling today?",
                "What's on your mind? I'm here to help you explore your thoughts.",
                "How has your day been? What would you like to talk about?"
            ]
        }
    
    def load_models(self) -> bool:
        """
        Load the dialogue model and RAG components.
        
        Returns:
            True if models loaded successfully
        """
        try:
            # Load dialogue model
            if os.path.exists(self.model_path):
                print(f"Loading fine-tuned dialogue model from {self.model_path}")
                self.llm_model = AutoModelForCausalLM.from_pretrained(self.model_path)
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            else:
                print(f"Fine-tuned model not found at {self.model_path}, using base model")
                self.llm_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
                self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            
            # Add padding token if needed
            if self.tokenizer.pad_token is None:
                self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                self.llm_model.resize_token_embeddings(len(self.tokenizer))
            
            print("Dialogue model loaded successfully")
            
            # Load RAG components if enabled
            if self.use_rag:
                try:
                    print("Loading RAG components...")
                    self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                    
                    if os.path.exists(self.chroma_db_path):
                        self.retriever = Chroma(
                            persist_directory=self.chroma_db_path, 
                            embedding_function=self.embeddings
                        ).as_retriever(search_kwargs={"k": 3})
                        print("RAG knowledge base loaded successfully")
                    else:
                        print(f"RAG knowledge base not found at {self.chroma_db_path}")
                        self.use_rag = False
                        
                except Exception as e:
                    print(f"Error loading RAG components: {e}")
                    self.use_rag = False
            
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def retrieve_relevant_context(self, query: str) -> str:
        """
        Retrieve relevant context from the knowledge base.
        
        Args:
            query: User's message to find relevant context for
            
        Returns:
            Relevant context from knowledge base
        """
        if not self.use_rag or self.retriever is None:
            return "No knowledge base available."
        
        try:
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(query)
            
            # Combine document content
            context_parts = []
            for doc in docs:
                context_parts.append(doc.page_content)
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return "Error retrieving knowledge base context."
    
    def generate_response_with_rag(self, message: str, emotion: str) -> str:
        """
        Generate response using RAG (Retrieval-Augmented Generation).
        
        Args:
            message: User's message
            emotion: Detected emotion
            
        Returns:
            Generated therapeutic response
        """
        try:
            # Retrieve relevant context
            context = self.retrieve_relevant_context(message)
            
            # Create prompt
            prompt = self.rag_prompt.format(
                context=context,
                emotion=emotion,
                message=message
            )
            
            # Generate response
            inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=1000, truncation=True)
            response_ids = self.llm_model.generate(
                inputs,
                max_length=inputs.shape[1] + 150,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            # Decode response
            response_text = self.tokenizer.decode(
                response_ids[:, inputs.shape[1]:][0], 
                skip_special_tokens=True
            ).strip()
            
            return response_text if response_text else self.get_fallback_response(emotion)
            
        except Exception as e:
            print(f"Error generating RAG response: {e}")
            return self.get_fallback_response(emotion)
    
    def generate_response_without_rag(self, message: str, emotion: str) -> str:
        """
        Generate response without RAG (direct model generation).
        
        Args:
            message: User's message
            emotion: Detected emotion
            
        Returns:
            Generated therapeutic response
        """
        try:
            # Create a simple prompt
            prompt = f"User: {message}\nTherapist:"
            
            # Generate response
            inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=500, truncation=True)
            response_ids = self.llm_model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7
            )
            
            # Decode response
            response_text = self.tokenizer.decode(
                response_ids[:, inputs.shape[1]:][0], 
                skip_special_tokens=True
            ).strip()
            
            return response_text if response_text else self.get_fallback_response(emotion)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.get_fallback_response(emotion)
    
    def get_fallback_response(self, emotion: str) -> str:
        """
        Get a fallback response when models fail.
        
        Args:
            emotion: Detected emotion
            
        Returns:
            Fallback response
        """
        responses = self.fallback_responses.get(emotion, self.fallback_responses["neutral"])
        return random.choice(responses)
    
    def generate_reply(self, message: str, emotion: str) -> str:
        """
        Generate a therapeutic reply.
        
        Args:
            message: User's message
            emotion: Detected emotion
            
        Returns:
            Therapeutic response
        """
        # Load models if not already loaded
        if self.llm_model is None:
            if not self.load_models():
                print("Warning: Could not load dialogue model, using fallback responses")
                return self.get_fallback_response(emotion)
        
        # Generate response
        try:
            if self.use_rag and self.retriever is not None:
                return self.generate_response_with_rag(message, emotion)
            else:
                return self.generate_response_without_rag(message, emotion)
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.get_fallback_response(emotion)

# Global instance
reply_generator = ReplyGenerator()

def generate_reply(message: str, emotion: str) -> str:
    """
    Main function to generate a therapeutic reply.
    
    Args:
        message: User's message
        emotion: Detected emotion
        
    Returns:
        Therapeutic response
    """
    return reply_generator.generate_reply(message, emotion)

def load_reply_model() -> bool:
    """
    Load the reply generation model.
    
    Returns:
        True if model loaded successfully
    """
    return reply_generator.load_models()
