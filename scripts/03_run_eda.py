"""
Etapa 4 — Ejecutar EDA en SQL y exportar resultados a JSON
"""
import sqlite3
import pandas as pd
import json
import re

DB_PATH = "/home/claude/worldcup_portfolio/data/processed/worldcup.db"
SQL_PATH = "/home/claude/worldcup_portfolio/sql/02_eda_queries.sql"
OUT_PATH = "/home/claude/worldcup_portfolio/data/processed/eda_results.json"

conn = sqlite3.connect(DB_PATH)
with open(SQL_PATH) as f:
    content = f.read()

blocks = re.split(r'-- \d+\.', content)[1:]
keys = ["goles_por_fase", "rendimiento_confederacion", "mayores_goleadas",
        "anfitriones", "penales_tiempo_extra", "top_goleadores_equipo",
        "ventaja_localia", "funnel_etapas"]

results = {}
for key, block in zip(keys, blocks):
    idx = block.upper().find("SELECT")
    query = block[idx:].strip().rstrip(";")
    df = pd.read_sql(query, conn)
    results[key] = df.to_dict(orient="records")
    print(f"{key}: {len(df)} filas")

conn.close()
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nResultados guardados en: {OUT_PATH}")
