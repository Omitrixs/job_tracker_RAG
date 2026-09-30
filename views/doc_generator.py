import streamlit as st
from ai_service import generate_cover_letter
from components.cards import render_ai_output

def render(tracker=None):
    st.markdown("<h2 style='font-weight: 800;'>Executive Document Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Generate tailored cover letters and outreach strategy using Groq AI.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Form metadata inputs
    col_comp, col_role = st.columns(2)
    with col_comp:
        company_name = st.text_input(
            "Target Company Name:", 
            placeholder="e.g. Stripe, Vercel, Datadog",
            key="doc_company_input"
        )
    with col_role:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption("AI will personalize company alignment based on this target.")

    col_res, col_job = st.columns(2)
    with col_res:
        resume_text = st.text_area(
            "Candidate Resume / Background:", 
            height=220, 
            placeholder="Paste raw resume text or key technical accomplishments...",
            key="doc_resume_input"
        )
    with col_job:
        job_description = st.text_area(
            "Target Job Description:", 
            height=220, 
            placeholder="Paste job description, technical requirements, and responsibilities...",
            key="doc_job_input"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Tailored Cover Letter", use_container_width=True):
        if company_name.strip() and resume_text.strip() and job_description.strip():
            with st.spinner(f"⚡ Synthesizing personalized cover letter for {company_name} via Groq LPU..."):
                output = generate_cover_letter(resume_text, job_description, company_name)
                
            st.markdown("<br>", unsafe_allow_html=True)
            render_ai_output(output, f"TAILORED COVER LETTER FOR {company_name.upper()}")
        else:
            st.error("⚠️ Please fill in all fields (Company Name, Resume, and Job Description).")