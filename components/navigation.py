import streamlit as st

def render_sidebar() -> str:
    """
    Renders sidebar navigation with scroll support and compact spacing.
    """
    st.sidebar.markdown(
        """
        <div style="padding-top: 0px; margin-bottom: 10px;">
            <h2 style="color: #F9FAFB; font-weight: 800; margin: 0; font-size: 1.4rem;">
                CareerOps <span style="color: #6366F1;">AI</span>
            </h2>
            <p style="color: #9CA3AF; font-size: 10px; font-weight: 700; margin: 2px 0 0 0; text-transform: uppercase;">
                Executive Candidate Suite
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    selected_route = st.sidebar.radio(
        "SYSTEM MODULES",
        [
            "Executive Dashboard",
            "Kanban Pipeline",
            "Log Application",
            "Resume Gap Analysis",
            "Generate Document",
            "Interview Prep",
            "Career Memory (RAG)",
            "Resume Converter"
        ],
        key="main_navigation_radio"
    )

    st.sidebar.markdown("---")

    # Compact System Badge
    st.sidebar.markdown(
        """
        <div style="background-color: #1E293B; border: 1px solid #334155; border-radius: 6px; padding: 8px 10px; margin-top: 5px;">
            <p style="color: #38BDF8; font-size: 11px; font-weight: 600; margin: 0;">⚡ Groq Llama-3.3 70B</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    return selected_route