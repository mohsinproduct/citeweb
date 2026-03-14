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
            st.table(data['audit_log']) 
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
        col_m1.metric("Stored Fragments", mem_status['chunks_saved']) # Count of 500-char chunks 
        
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
                st.code(route, language="markdown")
        else:
            st.warning("No standard internal links detected.")


    # File: ui/metrics_view.py (Add this to the bottom of the file)

def render_teacher_challenges(challenges: list):
    """Renders the generated test cases from the Teacher Agent and retrieved vectors from the Student."""
    st.divider()
    st.subheader("🎓 Adversarial Audit: Teacher vs. Student")
    st.write("The Teacher generates a test based on a random memory. The Student searches the vector space for the exact chunks.")
    
    for idx, challenge in enumerate(challenges):
        if "error" in challenge:
            st.error(challenge["error"])
            continue
            
        # Creates a collapsible card for each question
        with st.expander(f"Test Case #{idx + 1}: {challenge.get('question', 'N/A')}"):
            
            st.write("**✅ Teacher's Ground Truth:**")
            st.success(challenge.get('answer', 'N/A'))
            
            # --- NEW: Show what the Student found ---
            st.write("**🔎 Student's Retrieved Vectors:**")
            vectors = challenge.get('retrieved_vectors', [])
            if vectors:
                for v_idx, vec in enumerate(vectors):
                    st.info(f"**Match {v_idx+1}:** {vec}")
            else:
                st.warning("The Student Agent could not find any mathematically relevant chunks.")
            
            st.write("**🟩 Original Source Memory Fragment:**")
            st.caption(challenge.get('source_chunk', 'N/A'))