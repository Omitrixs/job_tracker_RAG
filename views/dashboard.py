import sys
import os

# Dynamically add the root project directory to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from components.cards import render_metric_card
import config


def render(tracker):
    st.markdown("<h2 style='font-weight: 800;'>Application Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Real-time metrics, query controls, and database records.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    apps = tracker.get_all_applications()

    if not apps:
        st.info("No active records found. Select 'Log Application' from sidebar.")
        return

    df = pd.DataFrame([{
        "ID": app.id,
        "Company": app.company,
        "Role": app.role,
        "Status": app.status.title(),
        "Date Applied": app.date_applied,
        "Days Elapsed": app.days_since_applied(),
        "Notes": app.notes
    } for app in apps])

    reminders = tracker.get_followup_reminders(threshold_days=config.FOLLOWUP_THRESHOLD_DAYS)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Applications", len(df), "Active database records")
    with c2:
        render_metric_card("In Pipeline", len(df[df["Status"] == "Interviewing"]), "Interview stage reached", "accent-purple")
    with c3:
        render_metric_card("Offers Received", len(df[df["Status"] == "Offer"]), "Pending decisions", "accent-green")
    with c4:
        render_metric_card("Follow-Up Alerts", len(reminders), f"Pending > {config.FOLLOWUP_THRESHOLD_DAYS} days", "accent-red" if len(reminders) > 0 else "")

    st.markdown("<br>", unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("🔍 Search Record (Company / Role):", "")
    with f_col2:
        status_filter = st.selectbox("Filter Status:", ["All", "Applied", "Interviewing", "Offer", "Rejected"])
    with f_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv_data, file_name="job_applications.csv", mime="text/csv")

    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["Company"].str.contains(search_query, case=False) | filtered_df["Role"].str.contains(search_query, case=False)]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Active Records")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)