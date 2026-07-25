"""
Etapa 7 — Generar variantes en ingles de los JSON exportados
================================================================
Solo se traducen las etiquetas categoricas generadas por nosotros
(etapa_final, fase, cluster_name, tipo_fase, feature names).
Nombres de equipos/jugadores/paises NO se tocan (son datos, no UI).
"""
import json

PROC = "/home/claude/worldcup_portfolio/data/processed/"

ETAPA_ES_EN = {
    "Fase de grupos": "Group stage",
    "Ronda de 32": "Round of 32",
    "Octavos de Final": "Round of 16",
    "Cuartos de Final": "Quarterfinals",
    "Semifinal": "Semifinal",
    "Cuarto puesto": "Fourth place",
    "Tercer puesto": "Third place",
    "Subcampeon": "Runner-up",
    "Campeon": "Champion",
    "Final": "Final",
}
CLUSTER_ES_EN = {
    "Elite ofensivo-defensivo": "Elite both ends",
    "Solido / avanza bien": "Solid / advances well",
    "Parejo / competitivo": "Even / competitive",
    "Justo lo necesario": "Just enough",
    "Eliminados temprano": "Eliminated early",
}
TIPO_FASE_ES_EN = {
    "Fase de grupos": "Group stage",
    "Eliminación directa": "Knockout stage",
}
FEATURE_ES_EN = {
    "grupo_pts": "group points",
    "goles_favor": "goals for",
    "goles_contra": "goals against",
    "dif_goles": "goal difference",
}
NOTA_ES_EN = {
    "Paraguay gana 4-3 en penales": "Paraguay wins 4-3 on penalties",
    "Marruecos gana 3-2 en penales": "Morocco wins 3-2 on penalties",
    "Tiempo extra": "Extra time",
    "Egipto gana 4-2 en penales": "Egypt wins 4-2 on penalties",
    "Suiza gana 4-3 en penales": "Switzerland wins 4-3 on penalties",
}

def tr_etapa(v): return ETAPA_ES_EN.get(v, v)
def tr_cluster(v): return CLUSTER_ES_EN.get(v, v)
def tr_nota(v): return NOTA_ES_EN.get(v, v) if v else v

# ---------- team_space.json ----------
space = json.load(open(PROC + "team_space.json", encoding="utf-8"))
for row in space:
    row["etapa_final"] = tr_etapa(row["etapa_final"])
    row["cluster_name"] = tr_cluster(row["cluster_name"])
json.dump(space, open(PROC + "team_space_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- top20_teams.json ----------
top20 = json.load(open(PROC + "top20_teams.json", encoding="utf-8"))
for row in top20:
    row["etapa_final"] = tr_etapa(row["etapa_final"])
json.dump(top20, open(PROC + "top20_teams_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- matches.json ----------
matches = json.load(open(PROC + "matches.json", encoding="utf-8"))
for row in matches:
    row["fase"] = tr_etapa(row["fase"])
    row["nota"] = tr_nota(row.get("nota"))
json.dump(matches, open(PROC + "matches_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- top_scorers.json ----------
scorers = json.load(open(PROC + "top_scorers.json", encoding="utf-8"))
SCORER_NOTES_EN = {
    "Kylian Mbappe": "Golden Boot winner. Also the World Cup's all-time top scorer (22 goals in his career).",
    "Lionel Messi": "2nd place. Set the record for World Cup all-time top scorer during the tournament.",
    "Jude Bellingham": "England's top scorer in a single World Cup.",
    "Harry Kane": "Passed Gary Lineker as England's all-time World Cup top scorer.",
}
for row in scorers:
    if row["jugador"] in SCORER_NOTES_EN:
        row["nota"] = SCORER_NOTES_EN[row["jugador"]]
json.dump(scorers, open(PROC + "top_scorers_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- eda_results.json ----------
eda = json.load(open(PROC + "eda_results.json", encoding="utf-8"))
eda_en = json.loads(json.dumps(eda))
for row in eda_en["goles_por_fase"]:
    row["tipo_fase"] = TIPO_FASE_ES_EN.get(row["tipo_fase"], row["tipo_fase"])
for row in eda_en["funnel_etapas"]:
    row["etapa_final"] = tr_etapa(row["etapa_final"])
for row in eda_en["anfitriones"]:
    row["etapa_final"] = tr_etapa(row["etapa_final"])
for row in eda_en["top_goleadores_equipo"]:
    row["etapa_final"] = tr_etapa(row["etapa_final"])
for row in eda_en["mayores_goleadas"]:
    row["fase"] = tr_etapa(row["fase"])
for row in eda_en["penales_tiempo_extra"]:
    row["fase"] = tr_etapa(row["fase"])
    row["nota"] = tr_nota(row.get("nota"))
json.dump(eda_en, open(PROC + "eda_results_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- ml_metrics.json ----------
metrics = json.load(open(PROC + "ml_metrics.json", encoding="utf-8"))
metrics["feature_importance"] = {FEATURE_ES_EN.get(k, k): v for k, v in metrics["feature_importance"].items()}
metrics["cluster_sizes"] = {CLUSTER_ES_EN.get(k, k): v for k, v in metrics["cluster_sizes"].items()}
json.dump(metrics, open(PROC + "ml_metrics_en.json", "w", encoding="utf-8"), ensure_ascii=False)

print("Variantes en ingles generadas:")
import os
for f in ["team_space_en.json","top20_teams_en.json","matches_en.json",
          "top_scorers_en.json","eda_results_en.json","ml_metrics_en.json"]:
    print(" ", f, os.path.getsize(PROC+f), "bytes")
