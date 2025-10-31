from openai import OpenAI
import streamlit as st
import numpy as np
from utils.text_utils import clean_text

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets("OPENAI_API_KEY"))

def get_embedding(text, model="text-embedding-3-small"):
    """Returns the embedding vector of a given text using OpenAI."""
    text = clean_text(text)
    response = client.embeddings.create(
        model=model,
        input=text
    )
    
    return np.array(response.data[0].embedding)

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def compute_match_percentage(resume_text, jd_text):
    """Compute similarity score between resume and job description."""
    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)
    
    similarity = cosine_similarity(resume_emb, jd_emb)
    
    # Convert to percentage
    match_percent = round(similarity * 100, 2)
    
    return match_percent