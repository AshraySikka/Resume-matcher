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

    if not has_title or not has_company:
        st.warning("Some details were not found. Please fill them in to proceed.")
        if has_title:
                # If I have title but miss company, show title as "Read Only"
                st.success(f"Role: {st.session_state.title}")
        else:
                # Show input box. Now linking my 'key' as 'title' will update session_state automatically.
                st.text_input("Job Title", key="title")
        
        if has_company:
                st.success(f"Company: {st.session_state.company}")
        else:
                st.text_input("Company Name", key="company")

        st.stop()
    else:
        st.info(f"Targeting: **{st.session_state.title}** at **{st.session_state.company}**")
        
    title = st.session_state.title
    company = st.session_state.company

    return title, company

def generate_recruiter_message(jd_text, tone="Warm"):
    """Generate a short LinkedIn message to a recruiter."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
You are a career networking assistant.

Write a {tone.lower()} LinkedIn message for a candidate interested in the position:
Job Title: {job_title}
Company: {company_name}

Base it on this job description:
{jd_text}

Keep it concise (under 120 words), friendly, and professional.
Avoid fluff. End with an invitation to connect or discuss further.
"""

    response = gemini_generate(prompt)

    return response


def generate_cold_email(jd_text):
    """Generate a cold email to the recruiter or company."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
You are an email strategist for job seekers.

Write a professional cold email for a candidate applying to:
Job Title: {job_title}
Company: {company_name}

Base it on the following job description:
{jd_text}

Include:
1. A strong but humble subject line
2. A short intro that references the role
3. A sentence linking the candidate's skills (assume they are qualified)
4. A polite call-to-action
Keep it under 200 words.
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
Estimate the typical annual salary range for a {job_title} role in {location}, company{company_name}.
Include a one-line explanation of what factors can affect it.
Output example:
"$90K-$120K CAD. Depends on experience, company size, and city."
"""

    response = gemini_generate(prompt, temp = 0.4)

    return response