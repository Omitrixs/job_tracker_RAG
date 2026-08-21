import streamlit as st
from models import Application

def render(tracker):
    st.markdown("<h2 style='font-weight: 800;'>Log Application Record</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Create new persistent SQLite records.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("add_app_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company Name")
            status = st.selectbox("Current Status", ["applied", "interviewing", "offer", "rejected"])
        with col2:
            role = st.text_input("Role / Job Title")
            date_applied = st.date_input("Date Applied")

        notes = st.text_area("Context / Key Requirements", height=120)
        submitted = st.form_submit_button("Save Application")

        if submitted:
            if company and role:
                app = Application(company=company, role=role, status=status, date_applied=str(date_applied), notes=notes)
                tracker.add_application(app)
                st.success(f"Record created: {role} at {company}")
            else:
                st.error("Company Name and Role Title are required fields.")