import streamlit as st
from components.badges import render_badge

def render(tracker):
    st.markdown("<h2 style='font-weight: 800;'>Visual Pipeline Board</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Stage breakdown across current application pipeline.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    apps = tracker.get_all_applications()
    stages = ["applied", "interviewing", "offer", "rejected"]
    cols = st.columns(4)

    for idx, stage in enumerate(stages):
        with cols[idx]:
            stage_apps = [a for a in apps if a.status.lower() == stage]
            
            st.markdown(f'''
                <div class="kanban-col-header">
                    <span class="kanban-col-title">{stage.upper()}</span>
                    {render_badge(stage)}
                </div>
            ''', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if not stage_apps:
                st.caption("No records in stage.")
            for a in stage_apps:
                st.markdown(f'''
                    <div class="kanban-card">
                        <div class="kanban-card-title">{a.role}</div>
                        <div class="kanban-card-company">{a.company}</div>
                        <div class="kanban-card-meta">
                            <span>Applied: {a.date_applied}</span>
                            <span><b>{a.days_since_applied()}d ago</b></span>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)