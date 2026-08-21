import ollama

def analyze_job_match(resume_text, job_description):
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

    print("\n[AI] Processing locally via Ollama (llama3.2)... please wait...")
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        print("\n===================================")
        print("   LOCAL AI RESUME MATCH ANALYSIS  ")
        print("===================================")
        print(response["message"]["content"])
    except Exception as e:
        print(f"\n[!] Error connecting to Ollama: {e}")