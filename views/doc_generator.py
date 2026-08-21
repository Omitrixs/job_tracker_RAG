import streamlit as st
import io, sys
from agents import generate_cover_letter
from components.cards import render_ai_output

def render(tracker):
    st.markdown("<h2 style='font-weight: 800;'>Cover Letter Drafting Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Generate tailored cover letters referencing application context.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    apps = tracker.get_all_applications()
    if not apps:
        st.info("No active records in database.")
        return

    app_dict = {f"ID #{app.id} — {app.role} at {app.company}": app for app in apps}
    selected_label = st.selectbox("Select Target Application Record:", list(app_dict.keys()))
    selected_app = app_dict[selected_label]

    col1, col2 = st.columns([2, 1])
    with col1:
        resume_text = st.text_area("Candidate Profile Summary:", height=180)
    with col2:
        tone = st.selectbox("Style Tone:", ["Professional", "Enthusiastic", "Concise", "Formal"])

    if st.button("Draft Document"):
        if resume_text:
            with st.spinner("Drafting cover letter via local Ollama..."):
                buffer = io.StringIO()
                sys.stdout = buffer
                generate_cover_letter(selected_app, resume_text, tone)
                sys.stdout = sys.__stdout__

                output = buffer.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                render_ai_output(output, f"GENERATED COVER LETTER ({selected_app.company.upper()})")
                
                st.download_button(
                    label="📥 Download Cover Letter (.txt)",
                    data=output,
                    file_name=f"cover_letter_{selected_app.company.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please enter candidate profile summary text.")