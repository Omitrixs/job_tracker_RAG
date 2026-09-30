import os
import streamlit as st
from groq import Groq

def get_groq_client():
    """Retrieves the API key from Streamlit secrets or local environment variables."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in .env or Streamlit Secrets.")
    return Groq(api_key=api_key)

def generate_ai_response(prompt: str) -> str:
    """General helper function to send any prompt to Groq."""
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq AI Error: {str(e)}"

def analyze_job_match(resume_text: str, job_description: str) -> str:
    """Compares candidate resume against job description using Groq API."""
    prompt = f"""
    You are an expert tech career mentor. Compare the following Resume and Job Description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Provide a short structured breakdown with:
    1. Match Rating (0-100%)
    2. Top 2-3 Core Strengths matching the role
    3. Top 2-3 Skill Gaps or Missing Keywords
    4. 1 Concrete recommendation to improve fit.
    """

    print("\n[AI] Processing request via Groq API (llama-3.3-70b-versatile)... please wait...")
    return generate_ai_response(prompt)