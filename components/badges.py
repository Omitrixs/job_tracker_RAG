import streamlit as st

def render_status_badge(status: str) -> str:
    """
    Returns an HTML status badge string matching the CSS tokens in assets/style.css.
    """
    status_clean = str(status).strip().lower()
    
    badge_class_map = {
        "applied": "badge-applied",
        "interviewing": "badge-interviewing",
        "interview": "badge-interviewing",
        "offer": "badge-offer",
        "offered": "badge-offer",
        "rejected": "badge-rejected"
    }
    
    css_class = badge_class_map.get(status_clean, "badge-applied")
    formatted_status = str(status).upper()
    
    return f'<span class="badge {css_class}">{formatted_status}</span>'

def display_badge(status: str) -> None:
    """
    Directly renders the status badge HTML in Streamlit.
    """
    st.markdown(render_status_badge(status), unsafe_allow_html=True)