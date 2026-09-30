import streamlit as st
from ai_service import analyze_job_match
from components.cards import render_ai_output

def render():
    st.markdown("<h2 style='font-weight: 800;'>Resume & Role Alignment Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>High-precision neural match scoring against target job specifications.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_res, col_job = st.columns(2)
    with col_res:
        resume_text = st.text_area(
            "Candidate Profile Summary:", 
            height=240, 
            placeholder="Paste raw resume text, skills summary, or key experience bullet points...",
            key="gap_resume_input"
        )
    with col_job:
        job_description = st.text_area(
            "Target Job Specification:", 
            height=240, 
            placeholder="Paste target role responsibilities, requirements, and tech stack...",
            key="gap_job_input"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Run Evaluation", use_container_width=True):
        if resume_text.strip() and job_description.strip():
            with st.spinner("⚡ Running deep alignment analysis via Groq LPU (Llama 3.3 70B)..."):
                # Clean function call returning string response directly
                output = analyze_job_match(resume_text, job_description)
                
            st.markdown("<br>", unsafe_allow_html=True)
            render_ai_output(output, "GROQ AI RESUME GAP ANALYSIS RESULT")
        else:
            st.error("⚠️ Please provide both a profile summary and a target job specification.")