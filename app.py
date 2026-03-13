# File: app.py
import streamlit as st
from services.ingestion_service import IngestionService
from services.memory_service import MemoryService
from services.audit_service import AuditService
from ui.metrics_view import render_full_audit_report, render_teacher_challenges

# 1. Page Configuration
st.set_page_config(page_title="citeweb.ai | AI Citation Auditor", layout="wide")

# 2. Header
st.markdown("""
    <div style="text-align: center;">
        <h1>🛡️ citeweb.ai</h1>
        <p><strong>Automated AI Citation Auditor</strong></p>
        <hr>
    </div>
""", unsafe_allow_html=True)

# 3. User Input
target_url = st.text_input(
    "Enter Website URL to Audit:", 
    placeholder="https://example.com",
    key="url_input_widget"
)

# 4. Execution Logic (The 1-Click Pipeline)
if st.button("Run Full Citation Audit", key="run_audit_btn"):
    if target_url:
        # Initialize all services at the start
        ingest_service = IngestionService()
        memory_service = MemoryService() 
        audit_service = AuditService()
        
        # --- PHASE 1: INGESTION ---
        with st.spinner("Step 1: Analyzing website structure & cleaning clutter..."):
            data = ingest_service.process_url(target_url)
            
        if "error" in data:
            st.error(f"Audit Failed: {data['error']}")
        else:
            # --- PHASE 2: MEMORY STORAGE ---
            with st.spinner("Step 2: Encoding semantic fragments into local memory..."):
                mem_status = memory_service.store_website_data(
                    data['clean_text'], 
                    data['url']
                )
            
            # --- PHASE 3: RENDERING & AUTOMATED TEACHER ---
            if "error" in mem_status:
                st.error(f"Memory Storage Failed: {mem_status['error']}")
            else:
                # 1. Render the Diagnostic Hub
                render_full_audit_report(data, mem_status)
                st.toast("Website Memorized!", icon="🧠")
                
                # 2. Automatically wake up the Teacher Agent!
                with st.spinner("Step 3: Teacher Agent is generating factual test cases from memory..."):
                    challenges = audit_service.generate_audit_batch(
                        target_url=data['url'],
                        batch_size=3
                    )

                    # Render the UI cards right below the hub
                    render_teacher_challenges(challenges)
                    st.toast("Synthetic Exam Ready!", icon="🎓")
                    
    else:
        st.warning("Please enter a valid URL.")