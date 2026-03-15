# ❄️ ColdHire AI

AI-powered job outreach tool
---

## 🚀 Quick Start
```bash
pip install streamlit langchain langchain-community langchain-groq chromadb pandas python-dotenv
```
Create `.env`:
```
GROQ_API_KEY=your_key_here
```
Run:
```bash
streamlit run main.py
```
---

## ✨ Features

| Feature | Description |
|---|---|
| ✉️ Email Generator | Paste job URL → AI writes a cold referral email |
| 💬 AI Assistant | General career advice OR job-specific Q&A |
| 🎯 Interview Prep | AI-generated questions tailored to the job |
| 📊 Job Fit Analyser | See how well your skills match the role |
| 📄 Cover Letter | Full cover letter from your profile |
| 🔗 LinkedIn Note | 300-char connection request note |
| 💰 Salary Script | Counter-offer negotiation email |
| 🔍 Job TL;DR | Summary + culture hints + red flags |

---

## 🗂️ Project Structure
```
├── main.py          → UI & all pages
├── chains.py        → All AI logic (LangChain + Groq)
├── portfolio.py     → ChromaDB vector search
├── utils.py         → Text cleaning helpers
├── .env             → API key
└── app/resource/
    └── my_portfolio.csv   → Your portfolio (Techstack, Links)
```
---

## 🔑 Tech Stack

- **LLM** — Groq `llama-3.3-70b-versatile`
- **Framework** — LangChain + Streamlit
- **Vector DB** — ChromaDB
- **Portfolio Matching** — Semantic search on your CSV
---

Built by [Srijan Kundu Chowdhury]
