# File: ui/metrics_view.py
import streamlit as st

def render_full_audit_report(data: dict, mem_status: dict):
    """
    Refactored 'Diagnostic Hub' layout. 
    Groups ingestion, structural, and memory data into a cohesive dashboard.
    """
    # 1. ZONE: EXECUTIVE SUMMARY
    st.subheader("🛡️ Executive Audit Summary")
    
    waste = data['waste_score']
    usable_percentage = 100.0 - waste
    
    # Visual Progress Bar
    st.write(f"**Data Cleanliness: {usable_percentage:.1f}% Understandable Text / {waste}% Code Clutter**")
    st.progress(int(usable_percentage))
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Raw Website Size", f"{data['raw_size']} chars")
    c2.metric("Understandable Text", f"{data['clean_size']} chars")
    c3.metric("Waste Score", f"{waste}%", 
              delta="⚠️ High Clutter" if waste > 80 else "✅ Optimized", 
              delta_color="inverse")

    st.divider()

    # 2. ZONE: STRUCTURAL ANALYSIS (Side-by-Side View)
    st.subheader("🛠️ Structural Diagnostic & AI Payload")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.write("**The 'Scalpel' Audit Log**")
        if data.get('audit_log'):
            st.table(data['audit_log']) # Displays the logic of what was removed [cite: 33, 34, 49]
        else:
            st.info("No structural changes recorded for this domain.")

    with col_right:
        st.write("**AI Semantic Preview**")
        st.text_area(
            label="What the AI actually sees:",
            value=data['clean_text'][:1000] + "\n\n... [PREVIEW TRUNCATED]",
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )

    st.divider()

    # 3. ZONE: PERSISTENCE & ROUTING (Technical Tabs)
    st.subheader("🧠 Local Intelligence & Memory")
    tab1, tab2 = st.tabs(["Local Memory Health", "Internal Route Map"])

    with tab1:
        col_m1, col_m2 = st.columns([1, 3])
        col_m1.metric("Stored Fragments", mem_status['chunks_saved']) # Count of 500-char chunks [cite: 16, 19, 47]
        
        display_count = min(mem_status['chunks_saved'], 50)
        chunk_icons = " ".join(["🟩" for _ in range(display_count)])
        if mem_status['chunks_saved'] > 50: chunk_icons += " ... (+)"
        
        col_m2.info(f"The website was split into {mem_status['chunks_saved']} optimized embedding chunks.")
        col_m2.caption(chunk_icons)
        col_m2.caption("Each 🟩 represents a 500-character vector stored in your local ChromaDB.")

    with tab2:
        if data.get("sub_urls"):
            st.write("Identified connected pages for future AI traversal:")
            for route in data["sub_urls"]:
                st.code(route, language="markdown") # [cite: 26, 43]
        else:
            st.warning("No standard internal links detected.")