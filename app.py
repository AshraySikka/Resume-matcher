import streamlit as st
from resume_parser import extract_text_from_resume
from match_engine import compute_match_percentage
from gpt_writer import rewrite_resume
from docx import Document
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from jd_parser import *
from recruiter_tools import (
    generate_recruiter_message,
    generate_cold_email,
    suggest_contact_titles,
    estimate_salary
)
from interview_questions import interview_questions


st.set_page_config(page_title="Resume Editor", layout="wide")
st.title("JobMatch - Resume & Job Description Analyzer")


# Defining a function for downloading the edited resume as a pdf
def download_resume_pdf(resume_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(40, 750)
    for line in resume_text.split('\n'):
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Defining a function for downloading the edited resume as word doc
def download_resume_docx(resume_text):
    doc = Document()
    doc.add_paragraph(resume_text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ----- Resume Upload or Paste -----
st.header("Step 1: Upload or Paste Your Resume")

resume_input_method = st.radio("How do you want to provide your resume?", ("Upload File", "Paste Text"))

resume_text = ""
if resume_input_method == "Upload File":
    resume_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
    
    if resume_file:
        resume_text = extract_text_from_resume(resume_file).strip()
        st.success("Resume loaded successfully!")

elif resume_input_method == "Paste Text":
    resume_text = st.markdown("Paste your resume here", height=200)

# ----- Job Description Input -----
st.header("Step 2: Paste Job Description")
job_description = st.markdown("Paste the job description here", height=200)

if job_description.strip(): # Only parse if text exists
    job_description_parsed = parse_jd(job_description)
    job_description = job_description_parsed["clean_text"]  # will be using this for matching/GPT
    st.success("Job Description parsed successfully!")
else:
    job_description = ""

# ----- Matching & Editing the Resume -----
st.header("Step 3: Match Results")

# Only calculate if both inputs exist
# Adding a button to calculate the percentage match
if resume_text and job_description:
    if st.button("Compute Match %"):
        with st.spinner("Analyzing..."):
            match_percent = compute_match_percentage(resume_text, job_description)
        st.success(f"Resume Match: {match_percent}%")

# Adding a button to rewirte the resume as per the Job Description
    if st.button("Rewrite Resume"):
        with st.spinner("Generating optimized resume..."):
            edited_resume = rewrite_resume(resume_text, job_description)
        st.success("Edited Resume Ready!")

        # Streamlit download button for word doc
        if 'edited_resume' in locals():
            docx_file = download_resume_docx(edited_resume)
            st.download_button(
                label="Download Edited Resume (.docx)",
                data=docx_file,
                file_name="Edited_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # Streamlit download button for pdf
        if 'edited_resume' in locals():
            pdf_file = download_resume_pdf(edited_resume)
            st.download_button(
                label="Download Edited Resume (.pdf)",
                data=pdf_file,
                file_name="Edited_Resume.pdf",
                mime="application/pdf"
            )

else:
    st.info("Please upload a resume and paste a job description above to generate results.")

# ----- Reach Out Section - Tools -----
st.header("Step 4: Recruiter Communication & Salary Insights")

if resume_text and job_description:
    if st.button("Generate Recruiter Message"):
        with st.spinner("Creating recruiter message..."):
            recruiter_msg = generate_recruiter_message(job_description)
        st.markdown("LinkedIn Message", recruiter_msg, height=150)


    if st.button("Generate Cold Email"):
        with st.spinner("Writing email..."):
            cold_email = generate_cold_email(job_description)
        st.markdown("Cold Email Template", cold_email, height=450)


    if st.button("Suggest People to Contact"):
        with st.spinner("Finding roles..."):
            titles = (", ".join(suggest_contact_titles(job_description)))
        st.markdown("Recommended Contacts", titles, height=250)


    if st.button("Estimate Salary Range"):
        with st.spinner("Estimating salary..."):
            salary = estimate_salary(job_description)
        st.success(f"Estimated Salary: {salary}")

else:
    st.info("Please upload a resume and paste a job description above to generate results.")


# ----- Potential Interview Questions -----
st.header("Step 5: Potential Interview Prep")

if resume_text and job_description:
    if st.button("Generate Potentail Interview Questions"):
        with st.spinner("Generating interview questions..."):
            questions = interview_questions(resume_text, job_description)
        st.markdown("Interview Questions", questions, height=650)

else:
    st.info("Please upload a resume and paste a job description above to generate results.")