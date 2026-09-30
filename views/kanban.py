import streamlit as st
import database
from components.badges import render_status_badge

def render():
    st.markdown("<h2 style='font-weight: 800;'>Kanban Application Pipeline</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Track active recruitment stages across target companies.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch applications from SQLite Database
    try:
        applications = database.get_all_applications() if hasattr(database, "get_all_applications") else []
    except Exception as e:
        applications = []
        st.warning(f"Unable to load Kanban board data: {str(e)}")

    stage_names = ["Applied", "Interviewing", "Offer", "Rejected"]

    # Group applications by stage (normalized case handling)
    stages = {stage: [] for stage in stage_names}

    for app in applications:
        raw_status = str(app.get("status", "Applied")).strip().title()
        if raw_status in stages:
            stages[raw_status].append(app)
        else:
            stages["Applied"].append(app)

    # Render 4 Kanban Stage Columns
    cols = st.columns(4)

    for idx, stage in enumerate(stage_names):
        with cols[idx]:
            # Stage Header
            st.markdown(
                f"""
                <div class="kanban-col-header">
                    <span class="kanban-col-title">{stage}</span>
                    <span style="color: #9CA3AF; font-size: 0.8rem; font-weight: 700;">{len(stages[stage])}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

            # Render Cards in Stage
            if stages[stage]:
                for app in stages[stage]:
                    app_id = app.get("id")
                    company = app.get("company", "Unknown Company")
                    role = app.get("role", "Target Role")
                    date_applied = app.get("date_applied", "N/A")
                    badge_html = render_status_badge(stage)

                    # Pure Streamlit Native Container (No HTML encapsulation blocking events)
                    with st.container(border=True):
                        # Role & Company Titles
                        st.markdown(f"**{role}**")
                        st.markdown(f"<span style='color: #38BDF8; font-weight: 600; font-size: 0.85rem;'>{company}</span>", unsafe_allow_html=True)
                        
                        # Date & Badge Meta Row
                        c_date, c_badge = st.columns([1.2, 1])
                        with c_date:
                            st.caption(f"📅 {date_applied}")
                        with c_badge:
                            st.markdown(badge_html, unsafe_allow_html=True)

                        st.markdown("<hr style='margin: 8px 0; border-color: #1E293B;'>", unsafe_allow_html=True)

                        # Native Interactive Controls
                        if app_id:
                            col_sel, col_del = st.columns([3, 1])
                            
                            with col_sel:
                                current_idx = stage_names.index(stage) if stage in stage_names else 0
                                new_stage = st.selectbox(
                                    "Move Stage",
                                    options=stage_names,
                                    index=current_idx,
                                    key=f"kanban_stage_{app_id}",
                                    label_visibility="collapsed"
                                )
                                
                                # Instantly update DB & refresh page when selection changes
                                if new_stage != stage:
                                    if hasattr(database, "update_application_status"):
                                        database.update_application_status(app_id, new_stage)
                                        st.rerun()

                            with col_del:
                                if st.button("🗑️", key=f"kanban_del_{app_id}", help="Delete Application"):
                                    if hasattr(database, "delete_application"):
                                        database.delete_application(app_id)
                                        st.rerun()
            else:
                st.markdown(
                    """
                    <div style="border: 1px dashed #334155; border-radius: 8px; padding: 20px; text-align: center; color: #64748B; font-size: 0.8rem;">
                        No roles in this stage
                    </div>
                    """,
                    unsafe_allow_html=True
                )