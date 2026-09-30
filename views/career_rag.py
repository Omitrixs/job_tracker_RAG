import streamlit as str_lit
import uuid
from rag_service import ingest_career_artifact, query_career_memory
from ai_service import _execute_groq_completion, load_prompt_template

def render():
    str_lit.markdown("<h2 style='font-weight: 800;'>🧠 CareerOps Memory (Local RAG Engine)</h2>", unsafe_allow_html=True)
    str_lit.markdown("<p style='color: #9CA3AF;'>Index your career artifacts, projects, and achievements into a local vector database to generate highly contextual, evidence-backed career outputs.</p>", unsafe_allow_html=True)
    str_lit.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = str_lit.tabs(["📥 Index Career Artifact", "🤖 Query Knowledge Base"])

    # TAB 1: INGESTION PIPELINE
    with tab1:
        str_lit.markdown("### Add Artifact to Vector Memory")
        str_lit.markdown("Store code snippets, project architectures, quantifiable metrics, or resume highlights so your RAG memory can reference them later.")
        
        with str_lit.form("rag_ingest_form"):
            artifact_title = str_lit.text_input("Artifact Title / Identifier", placeholder="e.g. Next.js SaaS State Management Architecture")
            artifact_category = str_lit.selectbox("Category", ["Technical Project", "Resume Highlight", "Achievement / Metric", "Leadership / Soft Skill"])
            artifact_text = str_lit.text_area(
                "Artifact Content / Details", 
                placeholder="Describe what you built, the tech stack used (e.g. React, Go, Tailwind, Ollama), scale metrics, and business impact...",
                height=180
            )
            
            submitted = str_lit.form_submit_button("💾 Index into Vector Store")

        if submitted:
            if not artifact_title or not artifact_text:
                str_lit.warning("⚠️ Please provide both a title and content to index.")
            else:
                doc_id = str(uuid.uuid4())
                metadata = {"title": artifact_title, "category": artifact_category}
                success = ingest_career_artifact(doc_id, artifact_text, metadata)
                if success:
                    str_lit.success(f"✨ Successfully indexed **{artifact_title}** into local vector memory!")
                else:
                    str_lit.error("❌ Failed to index artifact. Check logs for details.")

    # TAB 2: RAG QUERY & SYNTHESIS CONSOLE
    with tab2:
        str_lit.markdown("### Contextual RAG Synthesis")
        str_lit.markdown("Ask complex career questions, request custom bullet points, or draft pitch responses. The system will retrieve your most relevant historical artifacts and synthesize an answer.")

        user_query = str_lit.text_area(
            "Enter your query or objective",
            placeholder="e.g. Write a compelling technical summary highlighting how I integrated local LLMs with Streamlit and Playwright...",
            height=120
        )

        if str_lit.button("⚡ Execute RAG Synthesis", type="primary"):
            if not user_query:
                str_lit.warning("⚠️ Please enter a query.")
            else:
                with str_lit.spinner("Searching local vector memory and synthesizing via Groq AI..."):
                    # Step 1: Retrieve context from local vector storage
                    retrieved_chunks = query_career_memory(user_query, n_results=3)
                    
                    # Format context for prompt injection
                    if retrieved_chunks:
                        context_str = "\n\n".join([
                            f"--- Source: {chunk['metadata'].get('title', 'Unknown')} ({chunk['metadata'].get('category', 'General')}) ---\n{chunk['content']}"
                            for chunk in retrieved_chunks
                        ])
                    else:
                        context_str = "No specific indexed artifacts found in local memory. Rely on general professional background."

                    # Step 2: Bundle retrieved context and user query into user payload
                    user_payload = f"""### RETRIEVED CAREER MEMORY (RAG CHUNKS):
{context_str}

### USER OBJECTIVE / QUERY:
{user_query}"""

                    # Step 3: Execute completion call via Groq
                    response_output = _execute_groq_completion(
                        system_prompt_file="rag_synthesizer.md",
                        user_content=user_payload,
                        temperature=0.3,
                        max_tokens=2048
                    )

                    # Store results in session state
                    str_lit.session_state["rag_response"] = response_output
                    str_lit.session_state["rag_chunks"] = retrieved_chunks

        # Render RAG Output if available
        if "rag_response" in str_lit.session_state:
            str_lit.markdown("<br>", unsafe_allow_html=True)
            str_lit.markdown("### 📋 RAG Synthesis Result", unsafe_allow_html=True)
            
            with str_lit.container(border=True):
                str_lit.markdown(str_lit.session_state["rag_response"])

            # Show inspected retrieved sources for auditability (elite feature for engineering reviews)
            with str_lit.expander("🔍 Inspected Vector Memory Sources (Retrieved Chunks)"):
                chunks = str_lit.session_state.get("rag_chunks", [])
                if chunks:
                    for idx, chunk in enumerate(chunks, 1):
                        str_lit.markdown(f"**Source {idx}:** {chunk['metadata'].get('title', 'Untitled')} (*{chunk['metadata'].get('category', 'General')}*)")
                        str_lit.text(chunk['content'])
                        str_lit.markdown("---")
                else:
                    str_lit.info("No documents were matched for this query.")