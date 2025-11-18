Resume Matcher

A Streamlit app that analyzes how well your resume matches a job description and helps you rewrite weaker sections using AI.

What It Does
	•	Upload or paste your resume
	•	Paste any job description
	•	App generates embeddings and calculates a Match Score (%)
	•	Highlights missing skills and keywords
	•	Uses an LLM (Groq / Gemini / OpenAI—your choice) to rewrite and improve your resume
	•	Lets you download a clean PDF of the improved resume
	•	Gives you interview questions that you might need to prep for

Tech Used
	•	Python + Streamlit
	•	LLM APIs (Gemini / Groq / OpenAI)
	•	NumPy
	•	Regex
	•	ReportLab for PDF export

Run It
  pip install -r requirements.txt
  streamlit run app.py

Add your API key in .streamlit/secrets.toml:
  GEMINI_API_KEY = "add your key here" 

Why It Exists
Quickly score your resume, fix weak areas, and tailor it to any job—without spending hours rewriting.
