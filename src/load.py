import pandas as pd
import os
from sqlalchemy import create_engine

PROCESSED = "data/processed"
DB_PATH = "data/processed/olist.db"

def load_to_db():
    df = pd.read_csv(os.path.join(PROCESSED, "orders_clean.csv"))

    engine = create_engine(f"sqlite:///{DB_PATH}")

    df.to_sql("orders", engine, if_exists="replace", index=False)
    print(f"Table 'orders' créée : {len(df)} lignes chargées")

    return engine

if __name__ == "__main__":
    load_to_db()