import streamlit as st
import database
from components.cards import render_metric_card

def render():
    st.markdown("<h2 style='font-weight: 800;'>Executive Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Overview of your job application pipeline and response analytics.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch stats from SQLite Database
    try:
        stats = database.get_application_stats()
    except Exception as e:
        stats = {"total": 0, "applied": 0, "interviewing": 0, "offered": 0, "rejected": 0}
        st.warning(f"Unable to load database metrics: {str(e)}")

    total_apps = stats.get("total", 0)
    applied_apps = stats.get("applied", 0)
    interviewing_apps = stats.get("interviewing", 0)
    offered_apps = stats.get("offered", 0)
    rejected_apps = stats.get("rejected", 0)

    # Compute response rate percentage
    response_rate = f"{round(((interviewing_apps + offered_apps) / total_apps) * 100, 1)}%" if total_apps > 0 else "0.0%"

    # Top KPI Summary Cards
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        render_metric_card(
            label="Total Applied", 
            value=total_apps, 
            subtext="All submitted roles", 
            accent_color="blue"
        )
    with col2:
        render_metric_card(
            label="In Pipeline", 
            value=applied_apps, 
            subtext="Awaiting response", 
            accent_color="amber"
        )
    with col3:
        render_metric_card(
            label="Interviewing", 
            value=interviewing_apps, 
            subtext="Active conversations", 
            accent_color="purple"
        )
    with col4:
        render_metric_card(
            label="Offers Received", 
            value=offered_apps, 
            subtext="Secured offers", 
            accent_color="green"
        )
    with col5:
        render_metric_card(
            label="Response Rate", 
            value=response_rate, 
            subtext="Interview conversion", 
            accent_color="blue"
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Breakdown Section
    st.markdown("### Application Pipeline Breakdown")
    
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Table of recent applications
        recent_apps = database.get_all_applications() if hasattr(database, "get_all_applications") else []
        if recent_apps:
            st.dataframe(
                recent_apps, 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("No job applications logged yet. Use the **Log Application** view to add your first role.")

    with col_right:
        st.markdown("#### Quick Metrics")
        st.markdown(f"- **Rejections:** {rejected_apps}")
        st.markdown(f"- **Active Pipelines:** {applied_apps + interviewing_apps}")
        st.markdown(f"- **Total Tracked:** {total_apps}")