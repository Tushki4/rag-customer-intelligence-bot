from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

def generate_player(player_id):
    signup_date = fake.date_between(start_date="-2y", end_date="-30d")
    last_active = fake.date_between(start_date=signup_date, end_date="today")
    days_since_active = (datetime.today().date() - last_active).days
    sessions = random.randint(1, 300)
    avg_session_minutes = round(random.uniform(5, 120), 1)
    total_deposits = round(random.uniform(100, 50000), 2)
    total_withdrawals = round(random.uniform(0, total_deposits * 0.8), 2)
    win_rate = round(random.uniform(0.2, 0.75), 2)
    consecutive_losses = random.randint(0, 15)
    bonus_used = random.choice([True, False])
    game_type = random.choice(["Rummy", "Poker", "Fantasy", "Ludo"])
    churn_risk = (
        "High" if days_since_active > 30 and win_rate < 0.4
        else "Medium" if days_since_active > 14
        else "Low"
    )

    return {
        "player_id": f"PLR{player_id:04d}",
        "name": fake.name(),
        "email": fake.email(),
        "signup_date": signup_date,
        "last_active_date": last_active,
        "days_since_active": days_since_active,
        "total_sessions": sessions,
        "avg_session_minutes": avg_session_minutes,
        "total_deposits_inr": total_deposits,
        "total_withdrawals_inr": total_withdrawals,
        "win_rate": win_rate,
        "consecutive_losses": consecutive_losses,
        "bonus_used": bonus_used,
        "preferred_game": game_type,
        "churn_risk": churn_risk
    }

# Generate 200 players
players = [generate_player(i) for i in range(1, 201)]
df = pd.DataFrame(players)
df.to_csv("player_data.csv", index=False)

print(f"✓ Generated {len(df)} players")
print(f"✓ Churn distribution:\n{df['churn_risk'].value_counts()}")
print(f"✓ Games distribution:\n{df['preferred_game'].value_counts()}")
print(f"\nSample player:")
print(df.iloc[0].to_string())