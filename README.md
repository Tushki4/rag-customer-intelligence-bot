# 🎮 RAG Customer Intelligence Bot

> Ask questions about gaming player data in plain English.
> Powered by Llama 3.1 + FAISS + LangChain + Streamlit.

## 🔗 Live Demo
[**Try it here →**](https://tushar-boharapi-rag-customer-intelligence-bot.streamlit.app/)

## 🧠 What it does
Natural language querying over a 200-player synthetic gaming dataset.
Ask things like:
- "Which players have the highest churn risk?"
- "Show me Rummy players inactive for 30+ days"
- "Who has the most consecutive losses?"

## 🏗️ Architecture
Faker → Pandas → HuggingFace Embeddings → FAISS → LangChain RAG → Groq LLM → Streamlit

## 📦 Tech Stack
- **LLM**: Llama 3.1 8B via Groq (free)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (local, free)
- **Vector Store**: FAISS
- **Framework**: LangChain
- **UI**: Streamlit
- **Data**: 200 synthetic players via Faker

## 🚀 Run locally
```bash
git clone https://github.com/your-username/rag-customer-intelligence-bot
cd rag-customer-intelligence-bot
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
# Add GROQ_API_KEY to .env file
python build_vectorstore.py
streamlit run app.py
```

## 💡 Key learnings
- RAG architecture for structured data
- Vector embeddings and semantic search with FAISS
- LangChain RetrievalQA chain design
- Prompt engineering for domain-specific analytics
