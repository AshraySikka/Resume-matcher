import openai
import os

# Make sure your API key is set in environment variables or here
openai.api_key = os.getenv("OPENAI_API_KEY")

def rewrite_resume(resume_text, jd_text, target_match=0.8):
    """
    Rewrites the resume to match the job description.
    """
    prompt = f"""
You are a professional career coach and resume writer. Improve and tailor the following resume so it aligns
with at least {int(target_match * 100)}% of the provided job description. 
Do not invent fake experiences—only rephrase and highlight relevant skills naturally.
Keep the formatting clean and professional.

Resume:
{resume_text}

Job Description:
{jd_text}

Task:
1. Rewrite the resume to highlight skills, experience, and keywords from the Job Description.
2. Keep all content truthful to the original resume.
3. Ensure the revised resume aligns with the JD at least 80% in skills and keywords.
4. Maintain professional formatting with bullet points and headings.
5. Return the resume in plain text format suitable for copy/paste or saving as Word/PDF.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a resume optimization AI."},
                  {"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2000
    )

    edited_resume = response['choices'][0]['message']['content'].strip()
    
    return edited_resume


