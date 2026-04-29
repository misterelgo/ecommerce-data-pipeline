import pandas as pd
import os

RAW = "data/raw"
PROCESSED = "data/processed"

def load_orders():
    df = pd.read_csv(
        os.path.join(RAW, "olist_orders_dataset.csv"),
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )
    print(f"Orders chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df

def load_customers():
    df = pd.read_csv(os.path.join(RAW, "olist_customers_dataset.csv"))
    print(f"Customers chargé : {df.shape[0]} lignes")
    return df

def extract_all():
    orders    = load_orders()
    customers = load_customers()

    merged = orders.merge(customers, on="customer_id", how="left")
    print(f"Merge orders+customers : {merged.shape[0]} lignes")

    os.makedirs(PROCESSED, exist_ok=True)
    merged.to_csv(os.path.join(PROCESSED, "orders_raw.csv"), index=False)
    print("Sauvegardé : data/processed/orders_raw.csv")
    return merged

if __name__ == "__main__":
    extract_all()