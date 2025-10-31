import openai

# Make sure your API key is set in environment variables or here
openai.api_key = "YOUR_OPENAI_API_KEY"

def rewrite_resume(resume_text, jd_text):
    """
    Rewrites the resume to match the job description.
    """
    prompt = f"""
You are a professional career coach and resume writer.

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

    edited_resume = response['choices'][0]['message']['content']
    
    return edited_resume