"""
Etapa 5b — Exportar tablas adicionales a JSON para el dashboard
"""
import pandas as pd
import json

PROC = "/home/claude/worldcup_portfolio/data/processed/"

matches = pd.read_csv(PROC + "matches.csv")
scorers = pd.read_csv(PROC + "top_scorers.csv")
teams = pd.read_csv(PROC + "teams.csv")

flag_lookup = dict(zip(teams["team"], teams["bandera"]))
matches["bandera_local"] = matches["local"].map(flag_lookup)
matches["bandera_visitante"] = matches["visitante"].map(flag_lookup)

matches.to_json(PROC + "matches.json", orient="records", force_ascii=False)
scorers.to_json(PROC + "top_scorers.json", orient="records", force_ascii=False)

print(f"matches.json: {len(matches)} partidos")
print(f"top_scorers.json: {len(scorers)} jugadores")
