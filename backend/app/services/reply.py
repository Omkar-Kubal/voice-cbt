import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Define the path to your ChromaDB vector store
CHROMA_DB_PATH = os.path.join(os.path.pardir, 'chroma_db')

# Placeholder for the RAG components
llm_model = None
tokenizer = None
retriever = None

def load_reply_model():
    """
    Loads the fine-tuned dialogue model and the RAG components.
    """
    global llm_model, tokenizer, retriever
    if llm_model is None:
        try:
            # Load the fine-tuned dialogue model
            # You will replace 'microsoft/DialoGPT-medium' with your fine-tuned model path.
            llm_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            print("Dialogue generation model loaded successfully.")

            # Load the RAG components
            print("Loading RAG components...")
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            chroma_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
            retriever = chroma_db.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks
            print("RAG pipeline loaded successfully.")

        except Exception as e:
            print(f"Error loading models or RAG components: {e}")
            llm_model = None
            retriever = None

# Define a prompt template for the RAG system
RAG_PROMPT_TEMPLATE = """You are a compassionate, helpful, and empathetic AI therapist.
You will answer the user's question based on the provided context. If you don't know the answer,
just say that you are not equipped to answer that question and will try to learn more.

Context: {context}

User's Emotion: {emotion}
User's Question: {question}

Therapist's Answer:"""
RAG_PROMPT = PromptTemplate(input_variables=["context", "emotion", "question"], template=RAG_PROMPT_TEMPLATE)

def generate_reply(transcribed_text: str, emotion: str) -> str:
    """
    Generates a therapeutic response using the RAG pipeline.
    
    Args:
        transcribed_text: The user's transcribed speech.
        emotion: The detected emotion from the emotion service.

    Returns:
        A human-like therapeutic response.
    """
    if not all([llm_model, tokenizer, retriever]):
        load_reply_model()
        if not all([llm_model, tokenizer, retriever]):
            return "I'm having trouble responding right now. Can you please try again?"
    
    try:
        # Step 1: Retrieve relevant documents from the knowledge base
        retrieved_docs = retriever.get_relevant_documents(transcribed_text)
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        
        # Step 2: Use the RAG prompt to generate the response
        prompt = RAG_PROMPT.format(context=context_text, emotion=emotion, question=transcribed_text)
        
        # This is a simplified LLM chain for demonstration
        # In a real application, you would use LangChain's LLM components
        # to connect the prompt to the model.
        inputs = tokenizer.encode(prompt, return_tensors='pt', max_length=1000, truncation=True)
        response_ids = llm_model.generate(
            inputs,
            max_length=150,
            pad_token_id=tokenizer.eos_token_id,
        )
        response_text = tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        
        return response_text
        
    except Exception as e:
        print(f"Reply generation failed: {e}")
        return "I'm sorry, I'm not able to process that right now. Could you rephrase?"