import os
import time
import pandas as pd
from sqlalchemy import create_engine, inspect
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

# ---- Run interval (seconds) ----
RUN_INTERVAL_SECONDS = 0.5

# ---- PostgreSQL credentials file ----
CREDENTIAL_FILE = "database_credentials.txt"

# ---- PostgreSQL schema ----
DB_SCHEMA = "public"

# ---- Output folder for CSV files ----
OUTPUT_DIR = "/home/nicolai/postgres_exports"

# ---- CSV options ----
ENCODING = "utf-8"

# =========================================================
# LOAD DATABASE CREDENTIALS
# =========================================================

creds = {}
with open(CREDENTIAL_FILE, "r") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            creds[key] = value

DB_HOST = creds["host"]
DB_PORT = int(creds.get("port", 5433))
DB_NAME = creds["database"]
DB_USER = creds["user"]
DB_PASSWORD = creds.get("password")

# =========================================================
# EXPORT FUNCTION
# =========================================================

def run_export_cycle():
    print(f"[{datetime.now()}] Starting export cycle")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    inspector = inspect(engine)
    tables = inspector.get_table_names(schema=DB_SCHEMA)

    print(f"[{datetime.now()}] Found {len(tables)} tables in schema '{DB_SCHEMA}'")

    for table in tables:
        try:
            print(f"[{datetime.now()}] Exporting table: {table}")

            query = f'SELECT * FROM "{DB_SCHEMA}"."{table}"'
            df = pd.read_sql(query, engine)

            output_file = os.path.join(OUTPUT_DIR, f"{table}.csv")
            df.to_csv(output_file, index=False, encoding=ENCODING)

            print(f"[{datetime.now()}] ✓ Saved {table}.csv ({len(df)} rows)")

        except Exception as e:
            print(f"[{datetime.now()}] ✗ Failed to export {table}: {e}")

    engine.dispose()
    print(f"[{datetime.now()}] Export cycle completed")

# =========================================================
# MAIN LOOP
# =========================================================

if __name__ == "__main__":
    print(f"[{datetime.now()}] CSV export loop started")

    while True:
        try:
            run_export_cycle()
        except Exception as e:
            print(f"[{datetime.now()}] Unexpected error: {e}")

        time.sleep(RUN_INTERVAL_SECONDS)