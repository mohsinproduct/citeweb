============================================================
DAY 5: THE JUDGE AGENT & ADVERSARIAL PIPELINE
============================================================

### The Judge Agent (Deterministic LLM Evaluation)

**Goal:** Automate the grading of the Student Agent's retrieved vectors to prove if a website's semantic structure is citation-viable.
**Status:** ✅ Complete & Tested.

**Architectural Decisions & Trade-offs:**

1. **Temperature 0.0 for Strict Grading:** The Judge relies on Gemini 2.5 Flash via LangChain. We explicitly locked the temperature at 0.0. The Judge is not allowed to generate conversational text; it must output a strict binary `[YES]` or `[NO]`. This ensures the audit is mathematically deterministic rather than probabilistic.
2. **The 3-State Logic Patch (Error Handling):** Initially, API drops caused the Judge to default to `NO`, which created False Negatives (blaming the website for a Wi-Fi drop). We introduced an `ERROR` state. If the API fails, the pipeline catches the exception and flags an API error, preserving the purity of the website's semantic score.
3. **Chunking Fidelity (top_k=3):** We consciously decided to keep the Student Agent's retrieval at `top_k=3` instead of `top_k=1`.
   - _Why:_ Real-world LLMs (like Perplexity or ChatGPT) synthesize multiple paragraphs to build context. `top_k=3` (retrieving ~1500 characters) accurately mimics this context window.
