import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///data/processed/olist.db")

with engine.connect() as con:

    print("=== Q1 : Global ===")
    q1 = pd.read_sql(text("""
        SELECT
            ROUND(AVG(delivery_days), 1) AS delai_moyen_jours,
            ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS taux_retard_pct,
            COUNT(*) AS nb_commandes
        FROM orders
    """), con)
    print(q1.to_string(index=False))

    print("\n=== Q2 : Par état (top 10 pires délais) ===")
    q2 = pd.read_sql(text("""
        SELECT customer_state,
            ROUND(AVG(delivery_days), 1) AS delai_moyen_jours,
            ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS taux_retard_pct,
            COUNT(*) AS nb_commandes
        FROM orders
        GROUP BY customer_state
        ORDER BY delai_moyen_jours DESC
        LIMIT 10
    """), con)
    print(q2.to_string(index=False))

    print("\n=== Q3 : Evolution mensuelle ===")
    q3 = pd.read_sql(text("""
        SELECT order_month,
            COUNT(*) AS nb_commandes,
            ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS taux_retard_pct
        FROM orders
        GROUP BY order_month
        ORDER BY order_month
    """), con)
    print(q3.to_string(index=False))