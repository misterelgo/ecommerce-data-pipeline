import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sqlalchemy import create_engine, text
import os

engine = create_engine("sqlite:///data/processed/olist.db")
os.makedirs("outputs", exist_ok=True)

with engine.connect() as con:
    df = pd.read_sql(text("""
        SELECT customer_state,
            ROUND(AVG(delivery_days), 1) AS delai_moyen_jours,
            ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS taux_retard_pct,
            COUNT(*) AS nb_commandes
        FROM orders
        GROUP BY customer_state
        ORDER BY delai_moyen_jours DESC
    """), con)

fig, ax = plt.subplots(figsize=(12, 6))

colors = ["#d62728" if x >= 20 else "#1f77b4" for x in df["delai_moyen_jours"]]

bars = ax.bar(df["customer_state"], df["delai_moyen_jours"], color=colors)

ax.axhline(y=12.0, color="gray", linestyle="--", linewidth=1.2, label="Moyenne nationale (12j)")

ax.set_title("Délai moyen de livraison par état brésilien", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("État", fontsize=11)
ax.set_ylabel("Délai moyen (jours)", fontsize=11)
ax.legend(fontsize=10)
ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
ax.set_ylim(0, 32)

for bar, row in zip(bars, df.itertuples()):
    if row.taux_retard_pct >= 15:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{row.taux_retard_pct}%", ha="center", va="bottom",
                fontsize=8, color="#d62728", fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/delivery_by_state.png", dpi=150, bbox_inches="tight")
print("Graphique sauvegardé : outputs/delivery_by_state.png")
plt.show()