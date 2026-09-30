import os
import streamlit as st
from groq import Groq, GroqError

# Active, production-ready Groq model IDs
CANDIDATE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]

def get_api_key() -> str:
    """Retrieves API key from Streamlit secrets or OS environment variables."""
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.environ.get("GROQ_API_KEY", "")

def get_groq_client() -> Groq | None:
    """Lazily initializes the Groq client with the current API key."""
    api_key = get_api_key()
    return Groq(api_key=api_key) if api_key else None

def load_prompt_template(filename: str) -> str:
    """Safely loads a markdown prompt template from the root /prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt template missing: {prompt_path}")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def _execute_groq_completion(
    system_prompt_file: str, 
    user_content: str, 
    temperature: float = 0.2, 
    max_tokens: int = 2048
) -> str:
    """Internal helper to execute Groq completion calls with automatic model failover."""
    client = get_groq_client()
    if not client:
        return "⚠️ **Configuration Error:** `GROQ_API_KEY` missing. Add it to `.streamlit/secrets.toml` as `GROQ_API_KEY = 'gsk_...'`."

    try:
        system_prompt = load_prompt_template(system_prompt_file)
    except FileNotFoundError as e:
        return f"⚠️ **Configuration Error:** {str(e)}"

    last_error = None

    # Iterate through candidates until one succeeds
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except (GroqError, Exception) as e:
            last_error = e
            # Log error and immediately try the next model candidate
            continue

    return f"⚠️ **AI Service Error:** Unable to reach Groq services. Last error details: {str(last_error)}"

def analyze_job_match(resume_text: str, job_description: str) -> str:
    """Executes gap analysis evaluation via Groq Cloud API."""
    user_content = f"### CANDIDATE RESUME\n{resume_text}\n\n### TARGET JOB DESCRIPTION\n{job_description}"
    return _execute_groq_completion(
        system_prompt_file="gap_analysis.md",
        user_content=user_content,
        temperature=0.2,
        max_tokens=2048
    )

def generate_cover_letter(resume_text: str, job_description: str, company_name: str) -> str:
    """Generates a tailored cover letter via Groq Cloud API."""
    user_content = f"### COMPANY NAME\n{company_name}\n\n### CANDIDATE RESUME\n{resume_text}\n\n### TARGET JOB DESCRIPTION\n{job_description}"
    return _execute_groq_completion(
        system_prompt_file="cover_letter.md",
        user_content=user_content,
        temperature=0.4,
        max_tokens=2048
    )