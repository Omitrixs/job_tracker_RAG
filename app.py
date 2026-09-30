import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add project root directory to Python's module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import config
from database import Tracker
from views import dashboard, kanban, log_app, gap_analysis, doc_generator

# Initialize Database Tracker
tracker = Tracker()

# Page Setup
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load External CSS
if os.path.exists(config.CSS_PATH):
    with open(config.CSS_PATH, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Navigation Router
st.sidebar.markdown("<h2 style='color: #F9FAFB; font-weight: 800; margin-bottom: 0;'>CareerOps</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 11px; font-weight: 600; margin-bottom: 25px;'>EXECUTIVE CAREER SUITE</p>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "SYSTEM MODULES",
    ["Executive Dashboard", "Kanban Pipeline", "Log Application", "Resume Gap Analysis", "Generate Document"]
)

st.sidebar.markdown("---")
st.sidebar.caption("System Core: **Ollama Llama3.2 (Local)**")

# Route to View Modules
if menu == "Executive Dashboard":
    dashboard.render(tracker)
elif menu == "Kanban Pipeline":
    kanban.render(tracker)
elif menu == "Log Application":
    log_app.render(tracker)
elif menu == "Resume Gap Analysis":
    gap_analysis.render()
elif menu == "Generate Document":
    doc_generator.render(tracker)