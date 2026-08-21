# CareerOps Executive Suite

**CareerOps Executive Suite** is a modular, AI-powered career management platform designed to streamline and automate job application tracking, resume match analysis, and document generation. Built with Python and Streamlit, it runs lightweight local AI models via Ollama to keep your personal data, resume details, and career context entirely private.

---

## Key Features

* **Executive Dashboard:** High-level metrics tracking total applications, active pipeline stages, offers received, and follow-up alerts with instant CSV data export.
* **Visual Kanban Board:** Interactive, stage-by-stage pipeline management (`Applied`, `Interviewing`, `Offer`, `Rejected`).
* **Application Logger:** Simple form interface to record new job entries, context notes, and application dates into a local SQLite database.
* **Resume Gap Analysis:** Powered by local AI (`Llama 3.2`), compares candidate profile summaries against target job descriptions to extract alignment scores, missing keywords, and profile recommendations.
* **Cover Letter Drafting Engine:** Automatically generates tailored, tone-specific cover letters using stored application records and profile contexts.

---

## Project Architecture

The repository is built around a decoupled design pattern to ensure clean separation of concerns:

```text
job_tracker/
├── assets/
│   └── style.css            # Global CSS styling & design tokens
├── components/              # Reusable UI components
│   ├── __init__.py
│   ├── cards.py             # Metric cards and AI output frames
│   └── badges.py            # Status indicator badges
├── views/                   # Independent page handlers
│   ├── __init__.py
│   ├── dashboard.py         # Main metrics & active records view
│   ├── kanban.py            # Pipeline board view
│   ├── log_app.py           # Application logging form
│   ├── gap_analysis.py      # Resume & job specification matcher
│   └── doc_generator.py     # Tailored cover letter generator
├── prompts/                 # Isolated system prompt templates
│   ├── gap_analysis.md
│   └── cover_letter.md
├── config.py                # Global app settings & paths
├── database.py              # SQLite persistence layer
├── models.py                # Data classes
├── ai_service.py            # Local Ollama execution engine
├── app.py                   # Central routing & entry point
└── requirements.txt         # Project dependencies

```

---

## Getting Started

### Prerequisites

* **Python 3.10+** installed on your system.
* **Ollama** running locally with the `llama3.2` model pulled:
```bash
ollama run llama3.2

```



### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Omitrixs/job_tracker_RAG.git
cd job_tracker_RAG

```


2. **Set up a virtual environment:**
* **Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate

```


* **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Launch the application:**
```bash
streamlit run app.py

```



---

## Future Roadmap: RAG Integration

The next major release will incorporate Retrieval-Augmented Generation (RAG) using a local vector database (ChromaDB / LanceDB). This will enable:

* **Automated Context Retrieval:** Instant semantic indexing across your full work history, PDFs, past project write-ups, and portfolio items.
* **Targeted Interview Prep:** Real-time generation of STAR-format answers for behavioral questions based on your actual indexed experience.
* **Hyper-Personalized Content:** Fully automated cover letter drafts pulling relevant achievements directly from your vector store.
