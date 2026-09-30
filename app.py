import streamlit as st
import os

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

# Import Navigation Component and Views
from components.navigation import render_sidebar
from views import dashboard, kanban, log_app, gap_analysis, doc_generator

def main():
    # Route list matching navigation items
    route_options = [
        "Executive Dashboard",
        "Kanban Pipeline",
        "Log Application",
        "Resume Gap Analysis",
        "Generate Document"
    ]

    # Attempt rendering sidebar route selection
    try:
        selected_route = render_sidebar()
    except Exception:
        selected_route = None

    # Fallback to horizontal top menu if sidebar navigation returns None/Fails
    if not selected_route:
        st.markdown("### ⚡ **CareerOps AI Navigation**")
        selected_route = st.radio(
            "Select View Module:",
            route_options,
            horizontal=True,
            key="fallback_top_nav"
        )
        st.markdown("---")

    # View Dispatcher Map
    routes = {
        "Executive Dashboard": dashboard.render,
        "Kanban Pipeline": kanban.render,
        "Log Application": log_app.render,
        "Resume Gap Analysis": gap_analysis.render,
        "Generate Document": doc_generator.render
    }

    # Dispatch to Selected View
    view_func = routes.get(selected_route, dashboard.render)
    view_func()

if __name__ == "__main__":
    main()