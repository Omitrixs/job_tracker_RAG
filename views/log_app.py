import streamlit as st
import database
from datetime import datetime

def render(tracker=None):
    st.markdown("<h2 style='font-weight: 800;'>Log New Job Application</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Add a new target opportunity to your active recruitment pipeline.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Application Input Form
    with st.form("log_application_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("Company Name *", placeholder="e.g. Stripe, Vercel, Datadog")
            role = st.text_input("Role Title *", placeholder="e.g. Senior Frontend Engineer")
            location = st.text_input("Location / Work Model", placeholder="e.g. Remote, San Francisco, Hybrid")

        with col2:
            status = st.selectbox(
                "Initial Application Status *",
                ["Applied", "Interviewing", "Offer", "Rejected"],
                index=0
            )
            date_applied = st.date_input("Date Applied", value=datetime.now())
            job_url = st.text_input("Job Posting URL", placeholder="https://careers.company.com/job/123")

        notes = st.text_area("Initial Notes / Recruiter Info", placeholder="e.g. Referred by Alex, stack uses Next.js & Go...")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Save Application Record", use_container_width=True)

        if submitted:
            if not company.strip() or not role.strip():
                st.error("⚠️ Please fill in all required fields (Company Name and Role Title).")
            else:
                try:
                    # Persist record via database.py
                    if tracker and hasattr(tracker, "add_application"):
                        tracker.add_application(
                            company=company.strip(),
                            role=role.strip(),
                            status=status,
                            date_applied=date_applied.strftime("%Y-%m-%d"),
                            location=location.strip(),
                            job_url=job_url.strip(),
                            notes=notes.strip()
                        )
                    else:
                        database.add_application(
                            company=company.strip(),
                            role=role.strip(),
                            status=status,
                            date_applied=date_applied.strftime("%Y-%m-%d"),
                            location=location.strip(),
                            job_url=job_url.strip(),
                            notes=notes.strip()
                        )
                    
                    st.success(f"✅ Successfully logged **{role}** at **{company}**!")
                except Exception as e:
                    st.error(f"⚠️ Database Error: Failed to log application. Details: {str(e)}")