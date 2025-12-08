import streamlit as st
import google.generativeai as genai

genai.configure(api_key = st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_generate(prompt, temp = 0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()

def interview_questions(resume_text, jd_text):
    """
    Generates interview questions based on the jd and experience of the user.
    """

    prompt = f"""
You are a professional career coach. Give atleast 10 good interview questions based on the following
profile.

Resume:
{resume_text}

Job Description:
{jd_text}

Make sure the questions cover all the skills required by the job description and also prompts the candidate to
highlight on their experience from previos roles and how they will be a good fit for the postion they are applying
for.
"""
    
    response = gemini_generate(prompt)

    return response