import ollama

def generate_cover_letter(app, resume_text, tone="Professional"):
    """
    Tier 4 Agent: Generates a tailored cover letter using stored application
    details combined with your resume.
    """
    prompt = f"""
    You are an expert career agent and professional copywriter. 
    Write a targeted cover letter for the following job application.

    APPLICANT RESUME:
    {resume_text}

    TARGET ROLE:
    Company: {app.company}
    Role Title: {app.role}
    Notes/Context: {app.notes}

    TONE REQUIREMENT: {tone}

    INSTRUCTIONS:
    - Keep it under 300 words.
    - Highlight 2 specific qualifications from the resume that fit the role.
    - Sound genuine, engaging, and professional.
    - Do NOT include place-holder tags like [Insert Address] or [Date].
    """

    print(f"\n[Agent] Drafting cover letter for {app.role} at {app.company}...")
    
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        
        letter = response["message"]["content"]
        
        print("\n===================================")
        print(f"  COVER LETTER: {app.company} - {app.role}")
        print("===================================")
        print(letter)
        print("===================================")
        
        # Save generated letter directly to a text file
        filename = f"cover_letter_{app.company.lower().replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(letter)
            
        print(f"[Success] Draft saved to '{filename}'!")

    except Exception as e:
        print(f"\n[!] Error generating cover letter: {e}")
        print("    Ensure Ollama is running (`ollama run llama3.2`).")