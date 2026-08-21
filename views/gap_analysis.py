import streamlit as st
import io, sys
from ai_service import analyze_job_match
from components.cards import render_ai_output

def render():
    st.markdown("<h2 style='font-weight: 800;'>Resume & Role Alignment Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Local AI match scoring against job specs.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_res, col_job = st.columns(2)
    with col_res:
        resume_text = st.text_area("Candidate Profile Summary:", height=220)
    with col_job:
        job_description = st.text_area("Target Job Specification:", height=220)

    if st.button("Run Evaluation"):
        if resume_text and job_description:
            with st.spinner("Executing analysis via local Llama3.2..."):
                buffer = io.StringIO()
                sys.stdout = buffer
                analyze_job_match(resume_text, job_description)
                sys.stdout = sys.__stdout__
                
                output = buffer.getvalue()
                st.markdown("<br>", unsafe_allow_html=True)
                render_ai_output(output, "LOCAL RESUME GAP ANALYSIS RESULT")
        else:
            st.error("Provide both profile summary and job specification.")