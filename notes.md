# 🛡️ citeweb.ai | AI Citation Auditor

**Developer:** Mohsin  
**Architecture:** Agent-Oriented Software Engineering (Modular Monolith)  
**Core Constraint:** Core i5 8th Gen, 8GB RAM, No Dedicated GPU

---

## 📅 Sprint Log: Day 2 - Persistent Memory & Diagnostic Visualization

### 🎯 Objective

Establish a long-term storage solution for audited website data and provide a professional visual "receipt" of the AI's structural decision-making process.

### 🏗️ Memory Architecture (`modules/memory/`)

- [cite_start]**Local Vector Store:** Implemented `vector_store.py` using **ChromaDB**[cite: 14]. Designed to run entirely on the local file system (`/chroma_db`) to ensure data persistence without cloud costs[cite: 15].
- [cite_start]**CPU-Optimized Embeddings:** Integrated the `all-MiniLM-L6-v2` transformer model (22MB)[cite: 14]. [cite_start]Successfully verified that weights load and run on the Core i5 CPU without spiking 8GB RAM[cite: 12].
- [cite_start]**Recursive Chunking:** Developed a logic-based text splitter using 500-character chunks with a 50-character overlap to preserve semantic context across fragments[cite: 16].

### 🛠️ Diagnostic Layer & UI Refactor

- [cite_start]**The "Scalpel" Audit:** Updated `static_scraper.py` to generate a `audit_log`. [cite_start]This tracks exactly which HTML tags were ❌ Removed (clutter) vs. ✅ Preserved (signal)[cite: 34, 35].
- [cite_start]**Diagnostic Hub:** Refactored `ui/metrics_view.py` into a consolidated dashboard (`render_full_audit_report`)[cite: 41, 46].
- **Side-by-Side Validation:** Implemented a split-view to show the Structural Audit Log directly next to the AI Semantic Preview for immediate human verification.
- [cite_start]**Memory Health Map:** Added a visual "Data Integrity Map" (🟩) to prove successful persistence of vector fragments in the local database[cite: 47, 48].

### ⚙️ Hardware & V&V Verification

- [cite_start]**Network Optimization:** Identified that current routing extracts `.pdf` and `.jpg` links but verified they are not ingested into memory to prevent OOM (Out of Memory) errors on 8GB RAM[cite: 30].
- [cite_start]**State Integrity:** Confirmed that ChromaDB utilizes "lazy loading," only pulling specific indexed search results into active memory during queries[cite: 9].
- [cite_start]**Persistence Check:** Verified that the `/chroma_db` folder correctly populates on the hard drive after an audit, surviving system restarts[cite: 8, 15].
