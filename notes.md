# 🛡️ citeweb.ai | AI Citation Auditor

**Developer:** Mohsin  
**Architecture:** Agent-Oriented Software Engineering (Modular Monolith)  
**Core Constraint:** Core i5 8th Gen, 8GB RAM, No Dedicated GPU

---

## 📅 Sprint Log: Day 1 - Deterministic Ingestion & UI Abstraction

### 🎯 Objective

Build a robust, memory-safe data ingestion engine to extract clean semantic text from unstructured websites and visualize the results through a user-friendly dashboard.

### 🏗️ Module Development (`modules/scrapers/`)

- **Abstract Base Class (ABC):** Engineered `base.py` to enforce a strict contract for all future scrapers.
- **Static Ingestion Engine:** Developed `static_scraper.py` using `BeautifulSoup4`. Successfully bypassed institutional SSL handshakes and implemented heuristic link extraction to map website navigation.
- **Token Waste Metric:** Implemented the mathematical algorithm: `(1 - (Clean/Raw)) * 100`. Tested on `pakjournals.com`, identifying a **90.9% waste ratio**, proving the necessity of semantic filtering for AI citations.

### orchestration Layer (`services/`)

- **Ingestion Service:** Created `ingestion_service.py` to decouple the UI from the backend workers. This prevents monolithic coupling and ensures the application remains scalable.

### 🖥️ User Interface (`ui/` & `app.py`)

- **Componentization:** Built `metrics_view.py` to isolate the visual logic.
- **UX Abstraction:** Replaced technical jargon with user-centric terms like "Understandable Text" and "Code Clutter."
- **Visual Feedback:** Integrated a native Streamlit progress bar to act as a hardware-safe "Clutter Gauge."
- **Immutable UI:** Set the Preview Area to `disabled=True` to prevent accidental data modification, ensuring citation integrity.

### 🔒 Hardware & V&V Verification

- **RAM Protection:** Implemented strict character slicing (`[:1000]`) on all UI text-area components to prevent 8GB RAM exhaustion.
- **State Management:** Resolved `KeyError` widget crashes by implementing explicit `session_state` keys for all interactive components.
