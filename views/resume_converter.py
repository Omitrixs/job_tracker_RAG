import streamlit as st
from resume_export_service import extract_text_from_pdf, generate_docx_resume
from ai_service import _execute_groq_completion, load_prompt_template
from rag_service import query_career_memory

def render():
    st.markdown("<h2 style='font-weight: 800;'>📄 ATS Resume Optimizer & Word Exporter</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Upload your current PDF resume, paste a target job description, and let Groq optimize your profile for ATS compliance and download it instantly as an executive Word document.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 1. Upload Master Resume (PDF)")
        uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
        
        extracted_text = ""
        if uploaded_pdf is not None:
            extracted_text = extract_text_from_pdf(uploaded_pdf)
            if extracted_text:
                st.success(f"✅ Extracted ~{len(extracted_text.split())} words from resume PDF.")
                with st.expander("🔍 View Extracted Raw Text"):
                    st.text_area("Raw Text Preview", extracted_text, height=150, disabled=True)
            else:
                st.error("❌ Could not extract text from this PDF. Try another file.")

        st.markdown("### 2. Target Job Description")
        job_description = st.text_area(
            "Paste Job Description / Role Requirements",
            placeholder="Paste the job description here to align keywords and experience...",
            height=200
        )

        optimize_btn = st.button("⚡ Optimize Resume for Role", type="primary", use_container_width=True)

    with col2:
        st.markdown("### 3. Optimized Result & Export")
        
        if optimize_btn:
            if not uploaded_pdf or not job_description:
                st.warning("⚠️ Please upload a resume PDF and provide a target job description.")
            else:
                with st.spinner("Analyzing resume against job description and optimizing via Groq AI..."):
                    # Optional: pull context from local RAG memory to enrich experience
                    rag_context = query_career_memory(job_description, n_results=2)
                    rag_str = "\n".join([c['content'] for c in rag_context]) if rag_context else ""

                    # Build prompt payload
                    payload = f"""### SOURCE RESUME TEXT:
{extracted_text}

### SUPPLEMENTARY RAG MEMORY ARCHIVES:
{rag_str}

### TARGET JOB DESCRIPTION:
{job_description}"""

                    # Execute Groq completion
                    optimized_output = _execute_groq_completion(
                        system_prompt_file="resume_optimizer.md",
                        user_content=payload,
                        temperature=0.3,
                        max_tokens=3000
                    )

                    st.session_state["optimized_resume"] = optimized_output

        # Display output if available in session state
        if "optimized_resume" in st.session_state:
            st.markdown("#### ✨ Tailored Resume Output")
            
            # Preview container
            with st.container(border=True):
                st.markdown(st.session_state["optimized_resume"])

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Word Document Generation & Download Button
            docx_buffer = generate_docx_resume(st.session_state["optimized_resume"])
            
            st.download_button(
                label="📥 Download Tailored Resume (.docx)",
                data=docx_buffer,
                file_name="CareerOps_Optimized_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True
            )
        else:
            st.info("💡 Upload your resume and click **Optimize Resume for Role** to generate your tailored version and Word download.")