import pandas as pd
import os

PROCESSED = "data/processed"

def transform_orders():
    df = pd.read_csv(
        os.path.join(PROCESSED, "orders_raw.csv"),
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    # 1. On garde uniquement les commandes livrées
    df = df[df["order_status"] == "delivered"]
    print(f"Après filtre statut 'delivered' : {len(df)} lignes")

    # 2. On supprime les lignes sans date de livraison réelle
    df = df.dropna(subset=["order_delivered_customer_date"])
    print(f"Après suppression nulls livraison : {len(df)} lignes")

    # 3. Délai réel de livraison en jours
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # 4. Retard : livré après la date promise ?
    df["is_late"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    ).astype(int)

    # 5. Mois de commande (pour l'analyse temporelle)
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # 6. Filtre valeurs aberrantes
    df = df[df["delivery_days"].between(0, 120)]
    print(f"Après filtre aberrants : {len(df)} lignes")

    # Sauvegarde
    df.to_csv(os.path.join(PROCESSED, "orders_clean.csv"), index=False)
    print("Sauvegardé : data/processed/orders_clean.csv")
    return df

if __name__ == "__main__":
    transform_orders()