import google.generativeai as genai
import streamlit as st


# Configuring Gemini key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initializing the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_generate(prompt, temp=0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()

def rewrite_resume(resume_text, jd_text, target_match=0.8):
    """
    Rewrites the resume to match the job description.
    """
    prompt = f"""
Act as an expert Resume Optimization Engine.

Your Task: Rewrite the candidate's resume to target the specific Job Description (JD) below, ensuring an ATS match score of {int(target_match * 100)}%+.

### INPUT DATA:
RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

### STRICT CONSTRAINTS (READ CAREFULLY):
1. **NO CONVERSATIONAL FILLER:** Do not output sentences like "Here is the updated resume" or "I have optimized it." Output **ONLY** the resume content.
2. **ZERO DATA LOSS:** You must include ALL sections from the original resume (Contact Info, Education, Experience, Projects, Skills). Do not summarize or truncate older roles.
3. **FORMATTING:** Use valid Markdown.
   - Use `##` for Section Headers (e.g., ## EXPERIENCE).
   - Use `###` for Job Titles/Companies.
   - Use `-` for bullet points.
4. **KEYWORD OPTIMIZATION:** Swap generic verbs with specific keywords from the JD where truthfully applicable.
5. **LENGTH:** The output should be roughly the same length as the input resume. Do not shorten it.

### OUTPUT FORMAT:
[Start of Resume]
(The full resume content in Markdown)
[End of Resume]
"""

    response = gemini_generate(prompt, temp = 0.2)
    
    return response


