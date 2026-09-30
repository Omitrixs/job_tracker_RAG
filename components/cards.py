import streamlit as st

def render_ai_output(content: str, title: str = "AI ANALYSIS OUTPUT") -> None:
    """
    Renders structured AI generated responses inside a styled output container.
    """
    st.markdown(
        f"""
        <div class="output-card">
            <div class="ai-header-badge">
                <span>⚡ {title}</span>
            </div>
            <div style="color: #F8FAFC; font-size: 0.95rem; line-height: 1.7;">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(
    label: str, 
    value: str | int, 
    subtext: str = "", 
    accent_color: str = "blue"
) -> None:
    """
    Renders an executive dashboard KPI card with status indicator pills.
    
    accent_color options: 'purple', 'green', 'red', 'amber', or 'blue' (default)
    """
    accent_class = f"accent-{accent_color}" if accent_color != "blue" else ""
    
    st.markdown(
        f"""
        <div class="metric-card {accent_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )