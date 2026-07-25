"""
Etapa 3 — Carga a base de datos SQL (SQLite)
"""
import sqlite3
import pandas as pd

DB_PATH = "/home/claude/worldcup_portfolio/data/processed/worldcup.db"
SCHEMA_PATH = "/home/claude/worldcup_portfolio/sql/01_schema.sql"
PROC = "/home/claude/worldcup_portfolio/data/processed/"

teams = pd.read_csv(PROC + "teams.csv")
matches = pd.read_csv(PROC + "matches.csv")
scorers = pd.read_csv(PROC + "top_scorers.csv")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
with open(SCHEMA_PATH) as f:
    cur.executescript(f.read())

teams.to_sql("teams", conn, if_exists="append", index=False)
matches.to_sql("matches", conn, if_exists="append", index=False)
scorers.to_sql("top_scorers", conn, if_exists="append", index=False)
conn.commit()

for table in ["teams", "matches", "top_scorers"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {n} filas")

conn.close()
print(f"\nBase de datos creada en: {DB_PATH}")
