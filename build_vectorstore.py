from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from prepare_docs import load_documents
import os

VECTORSTORE_PATH = "vectorstore"
EMBEDDING_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"

def build_vectorstore():
    print("Loading documents...")
    docs = load_documents()

    print("Loading embedding model (first run downloads ~90MB)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"✓ Vector store saved to ./{VECTORSTORE_PATH}/")
    return vectorstore

def load_vectorstore():
    if not os.path.exists(VECTORSTORE_PATH):
        print("Vector store not found — building now...")
        return build_vectorstore()
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(
        VECTORSTORE_PATH, embeddings,
        allow_dangerous_deserialization=True
    )

if __name__ == "__main__":
    vs = build_vectorstore()
    # Test: search for high churn players
    results = vs.similarity_search("players with high churn risk", k=3)
    print("\n--- Test search: high churn risk ---")
    for r in results:
        print(f"• {r.page_content[:120]}...")