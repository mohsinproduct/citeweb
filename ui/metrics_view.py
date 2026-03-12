# File: ui/metrics_view.py
import streamlit as st

def render_ingestion_metrics(data: dict):
    st.subheader("Website Audit Results")
    
    # 1. THE VISUAL GRAPH (Hardware-Safe)
    waste = data['waste_score']
    usable_percentage = 100.0 - waste
    
    st.write("**Understandable Text vs. Code Clutter**")
    st.progress(
        value=int(usable_percentage), 
        text=f"Only {usable_percentage:.1f}% is understandable text. The rest is hidden code clutter."
    )

    st.write("") # Small spacing

    # 2. SIMPLIFIED METRICS
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Website Size", f"{data['raw_size']} chars")
    c2.metric("Understandable Text", f"{data['clean_size']} chars")
    c3.metric("Waste Score", f"{waste}%", delta="High Clutter" if waste > 80 else "Clean", delta_color="inverse" if waste > 80 else "normal")

    st.divider()

    # 3. SIMPLIFIED ROUTING
    st.subheader("Internal Links Found")
    if data.get("sub_urls"):
        st.info("We found these connected pages that an AI might try to read:")
        for idx, route in enumerate(data["sub_urls"]):
            st.write(f"**{idx+1}.** `{route}`")
    else:
        st.warning("No standard internal links detected.")

    # 4. SIMPLIFIED PREVIEW (Read-Only)
    st.subheader("Text Preview")
    st.text_area(
        label="This is the semantic text pulled out of all the code clutter:", 
        value=data['clean_text'][:1000] + "\n\n... [PREVIEW CUT OFF TO SAVE MEMORY]", 
        height=200,
        disabled=True
    )