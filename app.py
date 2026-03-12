# File: app.py
import streamlit as st
from services.ingestion_service import IngestionService
from ui.metrics_view import render_ingestion_metrics

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

# 3. User Input (FIXED: Added explicit memory key)
target_url = st.text_input(
    "Enter Website URL to Audit:", 
    placeholder="https://youdomain.here",
    key="url_input_widget" # Explicit State Tracker
)

# 4. Execution Logic (FIXED: Added explicit memory key)
if st.button("Run Citation Audit", key="run_audit_btn"):
    if target_url:
        service = IngestionService()
        
        with st.spinner("Executing Static Ingestion (CPU Safe)..."):
            data = service.process_url(target_url)
            
            if "error" in data:
                st.error(f"Audit Failed: {data['error']}")
            else:
                render_ingestion_metrics(data)
                st.success("✅ Semantic payload extracted successfully.")
    else:
        st.warning("Please enter a valid URL.")