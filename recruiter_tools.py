from openai import OpenAI
import streamlit as st
import re

# Initialize OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def extract_job_info(jd_text):
    """Extract job title and company name heuristically from a job description."""
    # Try to find something like: "Company Name is hiring a Job Title" or "at Company Name"
    title_match = re.search(r'(?i)(?<=for\s)([A-Z][\w\s&/-]+)(?=\s(at|@))', jd_text)
    company_match = re.search(r'(?i)(?<=at\s)([A-Z][\w\s&/-]+)', jd_text)

    # Fallbacks
    title = title_match.group(1).strip() if title_match else "the role"
    company = company_match.group(1).strip() if company_match else "the company"

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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional recruiter assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You write concise and effective cold emails for professionals."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


def suggest_contact_titles(jd_text):
    """Suggest typical people to reach out to in the company."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
Given the job title "{job_title}", in the company {company_name}, list 5 relevant job titles or roles of people
in a company that the candidate should reach out to for the best chance of being hired.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a recruiting expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def estimate_salary(jd_text, location="Canada"):
    """Estimate salary range using GPT reasoning."""
    job_title, company_name = extract_job_info(jd_text)
    prompt = f"""
Estimate the typical annual salary range for a {job_title} role in {location}, company{company_name}.
Include a one-line explanation of what factors can affect it.
Output example:
"$90K-$120K CAD. Depends on experience, company size, and city."
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a labor market and salary analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content