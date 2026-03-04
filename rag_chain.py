from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from build_vectorstore import load_vectorstore

load_dotenv()

# ── 1. Load the vector store ──────────────────────────
vectorstore = load_vectorstore()
retriever   = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# ── 2. Set up the Groq LLM ────────────────────────────
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)
    
# ── 3. Prompt template ────────────────────────────────
prompt = PromptTemplate.from_template("""You are an expert gaming analytics assistant.
Use the following player data to answer the question accurately and concisely.
If the data does not contain enough information, say so clearly.

Player Data Context:
{context}

Question: {question}

Instructions:
- Answer directly based only on the player data provided
- Use specific player IDs, numbers, and dates when available
- If asked about multiple players, list them clearly
- Keep your answer concise and business-focused

Answer:""")

# ── 4. Format retrieved docs into a single string ─────
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ── 5. Build the chain using LCEL (modern syntax) ─────
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def ask(question: str) -> dict:
    """Ask a question and return answer + source players."""
    # Get source documents separately for citations
    source_docs = retriever.invoke(question)
    player_ids  = [doc.metadata["player_id"] for doc in source_docs]

    # Run the chain for the answer
    answer = chain.invoke(question)

    return {"answer": answer, "sources": player_ids}

# ── Quick test ────────────────────────────────────────
if __name__ == "__main__":
    test_questions = [
        "Which players have the highest churn risk?",
        "Show me Rummy players who haven't played in over 30 days",
        "Who has the most consecutive losses?"
    ]
    for q in test_questions:
        print(f"\nQ: {q}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")