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

def render_teacher_challenges(challenges: list):
    """Renders the complete audit loop: Teacher's Test, Student's Search, and Judge's Verdict."""
    st.divider()
    st.subheader("🎓 Adversarial Audit: The Complete Loop")
    st.write("Teacher tests memory ➔ Student retrieves vectors ➔ **Judge evaluates citation viability.**")
    
    for idx, challenge in enumerate(challenges):
        if "error" in challenge:
            st.error(challenge["error"])
            continue
            
        # Safely get the verdict, defaulting to ERROR if something went completely wrong
        verdict = challenge.get('verdict', 'ERROR')
        
        # 1. Determine the visual theme based on the Judge's 3-state logic
        if verdict == "YES":
            icon = "✅"
            verdict_text = "VERDICT: CITATION VIABLE"
            expander_state = False # Keep successes collapsed to save vertical space
        elif verdict == "NO":
            icon = "❌"
            verdict_text = "VERDICT: HALLUCINATION RISK (LOW RECALL)"
            expander_state = True # Auto-expand failures so the user sees the problem immediately
        else:
            icon = "⚠️"
            verdict_text = "VERDICT: AUDIT FAILED (API ERROR)"
            expander_state = True 
            
        # 2. Render the interactive UI Card
        with st.expander(f"{icon} Test Case #{idx + 1}: {challenge.get('question', 'N/A')}", expanded=expander_state):
            
            # Show the Verdict Alert
            if verdict == "YES":
                st.success(f"**{verdict_text}** - The AI successfully retrieved enough context to cite the source.")
            elif verdict == "NO":
                st.error(f"**{verdict_text}** - The semantic structure is too weak. An LLM would likely hallucinate here.")
            else:
                st.warning(f"**{verdict_text}** - The Judge Agent could not reach the LLM API to evaluate this chunk. Check your internet connection or API limits.")
            
            # Show the Ground Truth
            st.write("**Teacher's Ground Truth:**")
            st.info(challenge.get('answer', 'N/A'))
            
            # Show the Retrieved Evidence
            st.write("**🔎 Student's Retrieved Evidence:**")
            vectors = challenge.get('retrieved_vectors', [])
            if vectors:
                for v_idx, vec in enumerate(vectors):
                    st.caption(f"*Match {v_idx+1}:* {vec}")
            else:
                st.warning("The Student Agent could not find any mathematically relevant chunks.")
            
            # Show the Original Source
            st.write("**🟩 Original Source Memory Fragment:**")
            st.text(challenge.get('source_chunk', 'N/A'))