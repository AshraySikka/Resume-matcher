import google.generativeai as genai
import streamlit as st
import re

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def gemini_generate(prompt, temp=0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()

def extract_job_info(jd_text):
    """Extract job title and company name from a job description."""
    
    #Will be storing the job title and company name in the session state to make sure we do not ask the user again
    if "title" not in st.session_state:
        st.session_state.title = ""

    if "company" not in st.session_state:
        st.session_state.company = "" 

    # Trying to find something like: "Company Name is hiring a Job Title" or "at Company Name"
    if not st.session_state.title:
        title_match = re.search(r'(?i)(?<=for\s)([A-Z][\w\s&/-]+)(?=\s(at|@))', jd_text)
        if title_match:
            st.session_state.title = title_match.group(1).strip()
    
    if not st.session_state.company:
        company_match = re.search(r'(?i)(?<=at\s)([A-Z][\w\s&/-]+)', jd_text)
        if company_match:
            st.session_state.company = company_match.group(1).strip()
     
    #Checking what my regex has
    has_title = bool(st.session_state.title)
    has_company = bool(st.session_state.company)

    if not has_title: # Assigning generic title as it was not found in the JD
        st.session_state.title = "[Job Title]"
        
    if not has_company:
        st.session_state.company = "[Company Name]"

    title = st.session_state.title
    company = st.session_state.company

    return title, company

def generate_recruiter_message(jd_text, tone="Warm"):
    """Generate a short LinkedIn message to a recruiter."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
You are an expert career networker who writes messages that get replies.

Write a {tone.lower()} LinkedIn connection message (under 300 characters) to a recruiter regarding the {job_title} role at {company_name}.

Context from Job Description:
{jd_text}

### STRICT RULES FOR "HUMAN" TONE:
1. **NO ROBOTIC OPENERS:** Do NOT use "I hope this finds you well," "I am writing to express interest," or "I was impressed by." Start directly with why the specific team or project looks interesting.
2. **BE SPECIFIC:** Mention ONE specific technology, project, or goal from the JD that excites you. Do not just say "your company values."
3. **USE CONTRACTIONS:** Use "I'm," "I'd," "It's" to sound natural.
4. **LOW-FRICTION CLOSE:** Do not ask for a "30-minute meeting." Ask a simple "Yes/No" question or just ask to connect to follow their updates.

### EXAMPLE OF WHAT I WANT:
"Hi [Name], I saw {company_name} is moving into [Topic]—as a dev who loves [Skill], that caught my eye immediately. I'd love to connect and keep up with the team's work."

Generate the message now.
"""

    response = gemini_generate(prompt)

    return response


def generate_cold_email(jd_text):
    """Generate a cold email to the recruiter or company."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
You are an expert career coach who writes high-converting, human-sounding emails.

Draft a warm, personal cold email for a candidate applying to:
Role: {job_title}
Company: {company_name}

Using this Job Description as context:
{jd_text}

### Instructions for Tone & Style:
1. **Subject Line:** Make it intriguing but casual (e.g., "Question about the {job_title} role" or "{company_name} + {job_title}"). Avoid stiff phrases like "Application for...".
2. **The Opening:** Do NOT start with "I hope this email finds you well" or "I am writing to apply." Start with a genuine compliment about the company or a specific detail from the job description that excited the candidate.
3. **The Middle:** connect ONE key skill from the JD to the candidate's experience casually. Show, don't just tell.
4. **The Close (Crucial):** Make the call-to-action "low friction." Do not ask for a 30-minute interview. Ask for a quick piece of advice or a simple "yes/no" question to gauge interest.
5. **Human Touch:** Use contractions (e.g., "I'm" instead of "I am"). Sound enthusiastic but not desperate.

Keep it under 150 words. The goal is to start a conversation, not just submit a resume.
"""

    response = gemini_generate(prompt)

    return response


def suggest_contact_titles(jd_text):
    """Suggest typical people to reach out to in the company."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
Given the job title "{job_title}", in the company {company_name}, list 5 relevant job titles or roles of people
in a company that the candidate should reach out to for the best chance of being hired.
Example format: Recruiter, Hiring Manager, Vice President of Engineering, Team Lead, CTO
"""

    response = gemini_generate(prompt, temp = 0.3)

    if response:
        titles_list = [title.strip() for title in response.split(',')]
        return titles_list
    else:
        return []


def estimate_salary(jd_text, location="Canada"):
    """Estimate salary range using GPT reasoning."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
You are a salary estimation assistant.

Analyze the following inputs:
Role: {job_title}
Company: {company_name}
Location: {location}

### LOGIC CHECK:
If the Role or Company listed above are empty, "None", "Unknown", or generic placeholders (like "[Company Name]"), output EXACTLY this sentence and nothing else:
"Currently there is not enough data available online to generate the salary."

### ESTIMATION TASK:
If valid specific details are provided, estimate the typical annual salary range.
Output format:
"$MINk-$MAXk CAD. [One-line explanation of factors like experience or company size]"
"""

    response = gemini_generate(prompt, temp = 0.4)

    return response