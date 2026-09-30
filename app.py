import os
import streamlit as st
from views import dashboard, kanban, log_app, gap_analysis, doc_generator, interview_prep, career_rag, resume_converter

# Page Configuration - Enterprise SaaS Theme
st.set_page_config(
    page_title="CareerOps AI | Candidate Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Tokenized Design System (assets/style.css)
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Import Navigation Component and All View Modules
from components.navigation import render_sidebar
from views import (
    dashboard, 
    kanban, 
    log_app, 
    gap_analysis, 
    doc_generator, 
    interview_prep,
    career_rag,
    resume_converter
)

def main():
    # Route list matching all application navigation items
    route_options = [
        "Executive Dashboard",
        "Kanban Pipeline",
        "Log Application",
        "Resume Gap Analysis",
        "Generate Document",
        "Interview Prep",
        "Career Memory (RAG)",
        "Resume Converter"
    ]

    # Attempt rendering sidebar route selection
    selected_route = None
    try:
        selected_route = render_sidebar()
    except Exception:
        selected_route = None

    # Fallback to horizontal top menu if sidebar navigation returns None or throws an error
    if not selected_route or selected_route not in route_options:
        st.markdown("### ⚡ **CareerOps AI Navigation**")
        selected_route = st.radio(
            "Select View Module:",
            route_options,
            horizontal=True,
            key="fallback_top_nav"
        )
        st.markdown("---")

    # View Dispatcher Map (Clean O(1) Routing Pattern)
    routes = {
        "Executive Dashboard": dashboard.render,
        "Kanban Pipeline": kanban.render,
        "Log Application": log_app.render,
        "Resume Gap Analysis": gap_analysis.render,
        "Generate Document": doc_generator.render,
        "Interview Prep": interview_prep.render,
        "Career Memory (RAG)": career_rag.render,
        "Resume Converter": resume_converter.render
    }

    # Dispatch to Selected View safely with fallback to Dashboard
    view_func = routes.get(selected_route, dashboard.render)
    view_func()

if __name__ == "__main__":
    main()