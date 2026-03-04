import pandas as pd
from langchain_core.documents import Document

def row_to_text(row):
    """Convert a player row into a natural language document."""
    return (
        f"Player {row['player_id']} named {row['name']} (email: {row['email']}) "
        f"signed up on {row['signup_date']} and was last active {row['days_since_active']} days ago. "
        f"They prefer {row['preferred_game']} and have played {row['total_sessions']} sessions "
        f"with an average session length of {row['avg_session_minutes']} minutes. "
        f"Win rate: {row['win_rate']*100:.1f}%. Consecutive losses: {row['consecutive_losses']}. "
        f"Total deposits: ₹{row['total_deposits_inr']:,.2f}. "
        f"Total withdrawals: ₹{row['total_withdrawals_inr']:,.2f}. "
        f"Bonus used: {row['bonus_used']}. Churn risk: {row['churn_risk']}."
    )

def load_documents():
    df = pd.read_csv("player_data.csv")
    docs = []
    for _, row in df.iterrows():
        text = row_to_text(row)
        doc  = Document(
            page_content=text,
            metadata={
                "player_id":  row["player_id"],
                "churn_risk": row["churn_risk"],
                "game":       row["preferred_game"]
            }
        )
        docs.append(doc)
    print(f"✓ Prepared {len(docs)} documents")
    print(f"\nSample document:\n{docs[0].page_content}")
    return docs

if __name__ == "__main__":
    load_documents()