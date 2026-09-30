import streamlit as st
import database
from ai_service import generate_interview_prep

def render():
    st.markdown("<h2 style='font-weight: 800;'>AI Interview Preparation Suite</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Generate tailored technical, behavioral, and strategic interview briefs powered by Groq.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch existing applications to let users quick-select target companies if available
    try:
        applications = database.get_all_applications() if hasattr(database, "get_all_applications") else []
    except Exception:
        applications = []

    app_options = {f"{app.get('role')} at {app.get('company')}": app for app in applications}

    with st.form("interview_prep_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Target Company Name", placeholder="e.g. Microsoft, TechCorp")
            
        with col2:
            # Optional quick-fill from tracked applications
            if app_options:
                selected_app_label = st.selectbox("Quick-fill from Tracked Roles", options=["-- Custom Entry --"] + list(app_options.keys()))
                if selected_app_label != "-- Custom Entry --":
                    chosen_app = app_options[selected_app_label]
                    company_name = chosen_app.get("company", company_name)

        job_description = st.text_area(
            "Target Job Description", 
            placeholder="Paste the full job description or core requirements here...",
            height=180
        )
        
        resume_text = st.text_area(
            "Candidate Resume Summary / Core Stack", 
            placeholder="Paste your resume markdown or key career highlights...",
            height=180
        )

        submitted = st.form_submit_button("🚀 Generate Executive Prep Brief")

    if submitted:
        if not company_name or not job_description or not resume_text:
            st.warning("⚠️ Please fill in all fields (Company Name, Job Description, and Resume) to generate a precise brief.")
            return

        with st.spinner(f"Synthesizing interview intelligence for {company_name}..."):
            result_markdown = generate_interview_prep(resume_text, job_description, company_name)
            
            # Store in session state so output persists across interactions
            st.session_state["interview_prep_result"] = result_markdown
            st.session_state["interview_prep_company"] = company_name

    # Display Results if present in Session State
    if "interview_prep_result" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="ai-header-badge">
                🎯 INTERVIEW INTELLIGENCE BRIEF: {st.session_state.get('interview_prep_company', '').upper()}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        with st.container(border=True):
            st.markdown(st.session_state["interview_prep_result"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Export option
        st.download_button(
            label="📥 Download Interview Brief (Markdown)",
            data=st.session_state["interview_prep_result"],
            file_name=f"Interview_Prep_{st.session_state.get('interview_prep_company', 'Target').replace(' ', '_')}.md",
            mime="text/markdown"
        )