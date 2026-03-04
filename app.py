import streamlit as st
from rag_chain import ask

# ── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="Gaming Analytics RAG Bot",
    page_icon="🎮",
    layout="wide"
)


# ── Header ────────────────────────────────────────────
st.title("🎮 Gaming Player Intelligence Bot")
st.caption(
    "Ask questions about your 200 player dataset in plain English. "
    "Powered by Llama 3.1 + FAISS + LangChain."
)
st.divider()

# ── Example questions sidebar ─────────────────────────
with st.sidebar:
    st.header("💡 Example Questions")
    examples = [
        "Which players have the highest churn risk?",
        "Show me Rummy players inactive for over 30 days",
        "Who has the most consecutive losses?",
        "Which players made the largest deposits?",
        "Find Fantasy players with a win rate above 60%",
        "Which high-risk players have used a bonus?",
        "Who has played more than 200 sessions?",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state["pending_question"] = example

    st.divider()
    st.caption("Dataset: 200 synthetic gaming players")
    st.caption("Model: Llama 3.1 8B via Groq")
    st.caption("Embeddings: all-MiniLM-L6-v2 (local)")
    
# ── Chat history ──────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            st.caption(f"📎 Sources: {', '.join(message['sources'])}")

# ── Handle sidebar button clicks ──────────────────────
if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
else:
    prompt = None

user_input = st.text_input("Ask anything about your players...", key="user_input")
if st.button("Ask", type="primary"):
    if user_input.strip():
        prompt = user_input
    
# ── Process question ──────────────────────────────────
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching player data..."):
            result = ask(prompt)

        st.markdown(result["answer"])
        st.caption(f"📎 Sources: {', '.join(result['sources'])}")

        st.session_state.messages.append({
            "role":    "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })
    