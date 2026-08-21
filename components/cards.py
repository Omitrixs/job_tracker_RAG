import streamlit as st

def render_metric_card(label, value, subtext="", accent_class=""):
    st.markdown(f'''
        <div class="metric-card {accent_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
    ''', unsafe_allow_html=True)

def render_ai_output(content, title="LOCAL AI EXECUTION ENGINE"):
    st.markdown(f'''
        <div class="output-card">
            <div class="ai-header-badge">⚡ {title}</div>
            <div>{content}</div>
        </div>
    ''', unsafe_allow_html=True)