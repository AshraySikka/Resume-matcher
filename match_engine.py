import google.generativeai as genai
import streamlit as st
import numpy as np
from utils.text_utils import clean_text

# Configuring Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initializing the Gemini model
model = genai.GenerativeModel("gemini-pro")

def gemini_generate(prompt, temp=0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()


def get_embedding(text):
    """
    Generate a semantic embedding for the given text using Gemini.
    """
    text = clean_text(text)
    
    embed_model = genai.embed_content(
        model = "models/embedding-001",
        content = text,
        task_type = "retrieval_document"
    )

    embedding = np.array(embed_model["embedding"])

    return embedding


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    
    if vec1 is None or vec2 is None:
        raise ValueError("One of the input vectors is None.")
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    if vec1.size == 0 or vec2.size == 0:
        raise ValueError("One of the input vectors is empty.")
    
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def compute_match_percentage(resume_text, jd_text):
    """Compute similarity score between resume and job description."""
    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)
    
    similarity = cosine_similarity(resume_emb, jd_emb)
    
    # Convert to percentage
    match_percent = round(similarity * 100, 2)
    
    return match_percent