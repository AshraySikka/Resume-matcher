from openai import OpenAI
from openai import RateLimitError
import streamlit as st
import numpy as np
from utils.text_utils import clean_text
import time
import hashlib
import pickle


# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Simple local cache for embeddings
CACHE_FILE = "embedding_cache.pkl"
try:
    with open(CACHE_FILE, "rb") as f:
        embedding_cache = pickle.load(f)
except FileNotFoundError:
    embedding_cache = {}

def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(embedding_cache, f)

def get_embedding(text, model="text-embedding-3-small", retries=6):
    """
    Returns the embedding vector of a given text using OpenAI.
    Caches embeddings locally to reduce API calls.
    Handles rate limits with exponential backoff.
    """
    text = clean_text(text)
    key = hashlib.sha256(text.encode()).hexdigest()  # unique key for text

    if key in embedding_cache:
        return embedding_cache[key]

    for i in range(retries):
        try:
            response = client.embeddings.create(
                model=model,
                input=text
            )
            embedding = np.array(response.data[0].embedding)
            embedding_cache[key] = embedding
            save_cache()
            return embedding
        except RateLimitError:
            wait_time = 2 ** i  # 1s, 2s, 4s...
            print(f"Rate limit hit, retrying in {wait_time}s...")
            time.sleep(wait_time)
        except TypeError as e:
            st.error("A type error occurred while computing match percentage.")
            st.write(f"Details: {e}")
        except Exception as e:
            st.error("An unexpected error occurred.")
            st.write(f"Details: {e}")

    raise Exception("Failed to get embedding after several retries")

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