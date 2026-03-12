# 🛡️ citeweb | AI Citation Auditor

**Developer:** Mohsin  
**Project Context:** Personal Student Software Project  
**Architecture:** Agent-Oriented Software Engineering (Modular Monolith)  
**Core Constraint:** Core i5 8th Gen, 8GB RAM, No Dedicated GPU

---

## 📅 Sprint Log: Day 0 - Project Architecture & Environment Initialization

### 🎯 Objective

Establish a secure, hardware-optimized workspace and design the foundational directory structure required for a multi-agent AI citation stress-testing environment.

### 🏗️ Architectural Setup (Modular Monolith)

- **Separation of Concerns:** Deployed a strict folder hierarchy to decouple the Streamlit UI, business logic, and data ingestion.
  - `modules/`: Deterministic background workers (`scrapers/`, `memory/`, `engine/`).
  - `services/`: Orchestration layer to manage data flow and prevent monolithic UI coupling.
  - `agents/`: Isolated environment for Gemini API probabilistic reasoning (Teacher, Judge, Consultant).
  - `ui/` & `docs/`: Frontend componentization and project documentation.

### ⚙️ Environment & Dependency Management

- **VENV Initialization:** Built a clean, localized Python virtual environment (`venv`) mapped to the new project directory.
- **Compiler Bypass (Hardware Optimization):** Encountered a fatal `Microsoft Visual C++ 14.0` build error when pip attempted to compile `chroma-hnswlib` from scratch.
- **Resolution:** Implemented Dependency Unpinning in `requirements.txt` to force pip to resolve and fetch pre-compiled Windows binaries (`.whl`), successfully bypassing the 6GB compiler requirement and protecting the Core i5 environment.

### 🔒 Software Configuration Management (SCM)

- Engineered a strict `.gitignore` to prevent repository bloat (ignoring the heavy local ChromaDB vector space, `.env` API keys, and `__pycache__`).
- Adopted an ephemeral `notes.md` logging strategy backed by Git commit history for daily sprint tracking.
