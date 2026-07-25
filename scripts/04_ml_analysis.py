"""
Etapa 5 — Machine Learning e IA aplicada
==========================================
1) Power Ranking: score compuesto ponderado para el Top 20 de equipos
   (etapa alcanzada + victorias + diferencia de gol + goles a favor).
2) KMeans: agrupa los 48 equipos en "perfiles de juego" segun sus
   estadisticas ofensivas/defensivas.
3) PCA a 2D: para visualizar el espacio de estilos de equipo.
4) Clasificador (RandomForest): ¿los stats de fase de grupos predicen
   si un equipo avanza a la eliminacion directa? (con aviso de muestra
   pequeña: 48 equipos).
"""
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

PROC = "/home/claude/worldcup_portfolio/data/processed/"
teams = pd.read_csv(PROC + "teams.csv")

# ============================================================
# 1) POWER RANKING — Top 20 equipos (score compuesto)
# ============================================================
print("[1/4] Calculando Power Ranking...")
# normalizar cada componente 0-1 antes de ponderar
def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

teams["score_etapa"] = norm(teams["etapa_final_code"])
teams["score_victorias"] = norm(teams["total_victorias"])
teams["score_dif_goles"] = norm(teams["dif_goles"])
teams["score_goles_favor"] = norm(teams["goles_favor"])

# ponderacion: la etapa alcanzada es lo mas importante en un torneo eliminatorio
teams["power_score"] = (
    teams["score_etapa"] * 0.50 +
    teams["score_victorias"] * 0.20 +
    teams["score_dif_goles"] * 0.20 +
    teams["score_goles_favor"] * 0.10
) * 100

top20_teams = teams.sort_values("power_score", ascending=False).head(20).reset_index(drop=True)
top20_teams["power_rank"] = top20_teams.index + 1
top20_teams[["power_rank","team","iso2","bandera","confederacion","etapa_final","goles_favor","goles_contra",
             "dif_goles","total_victorias","power_score"]].round(1).to_json(
    PROC + "top20_teams.json", orient="records", force_ascii=False)
print(top20_teams[["power_rank","team","etapa_final","power_score"]].head(10).round(1).to_string(index=False))

# ============================================================
# 2) KMEANS — perfiles de juego de los 48 equipos
# ============================================================
print("\n[2/4] Clustering KMeans (perfiles de equipo)...")
FEATURES = ["goles_favor", "goles_contra", "dif_goles", "grupo_pts", "total_victorias"]
scaler = StandardScaler()
X = scaler.fit_transform(teams[FEATURES])

k = 5
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
teams["cluster"] = kmeans.fit_predict(X)

profiles = teams.groupby("cluster")[FEATURES].mean().round(2)
print(profiles)

# nombrar clusters por su posicion relativa en diferencia de gol (mas robusto
# que umbrales fijos, ya que se adapta a la distribucion real de los datos)
ranked = profiles.sort_values("dif_goles", ascending=False)
tier_names = ["Elite ofensivo-defensivo", "Solido / avanza bien",
              "Parejo / competitivo", "Justo lo necesario",
              "Eliminados temprano"][:len(ranked)]
cluster_names = {int(c): tier_names[i] for i, c in enumerate(ranked.index)}
teams["cluster_name"] = teams["cluster"].map(cluster_names)

# ============================================================
# 3) PCA a 2D para visualizar el espacio de estilos
# ============================================================
print("\n[3/4] PCA a 2D...")
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X)
teams["pca_x"] = coords[:, 0].round(3)
teams["pca_y"] = coords[:, 1].round(3)
var_explained = pca.explained_variance_ratio_.sum()
print(f"  Varianza explicada: {var_explained:.1%}")

teams[["team","iso2","bandera","confederacion","cluster","cluster_name","etapa_final",
       "goles_favor","goles_contra","pca_x","pca_y"]].to_json(
    PROC + "team_space.json", orient="records", force_ascii=False)

# ============================================================
# 4) CLASIFICADOR — ¿los stats de fase de grupos predicen avance?
# ============================================================
print("\n[4/4] Clasificador de avance a eliminacion directa...")
CLF_FEATURES = ["grupo_pts", "goles_favor", "goles_contra", "dif_goles"]
X_clf = StandardScaler().fit_transform(teams[CLF_FEATURES])
y_clf = teams["avanzo_a_eliminacion"].astype(int)

rf = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)
# validacion cruzada dado el tamaño pequeño de muestra (48 equipos)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(rf, X_clf, y_clf, cv=cv)
rf.fit(X_clf, y_clf)

importances = dict(zip(CLF_FEATURES, rf.feature_importances_.round(3)))
metrics = {
    "n_teams": int(len(teams)),
    "n_advanced": int(y_clf.sum()),
    "cv_accuracy_mean": round(float(scores.mean()), 3),
    "cv_accuracy_std": round(float(scores.std()), 3),
    "baseline_majority_class": round(float(max(y_clf.mean(), 1 - y_clf.mean())), 3),
    "feature_importance": {k: float(v) for k, v in sorted(importances.items(), key=lambda x: -x[1])},
    "cluster_sizes": teams["cluster_name"].value_counts().to_dict(),
    "pca_variance_explained": round(float(var_explained), 3),
    "n_clusters": k,
}
with open(PROC + "ml_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

print(f"  Accuracy (validacion cruzada 5-fold): {scores.mean():.1%} ± {scores.std():.1%}")
print(f"  Baseline (clase mayoritaria): {metrics['baseline_majority_class']:.1%}")
print(f"  Feature mas importante: {max(importances, key=importances.get)}")

# guardar teams.csv actualizado con cluster info para uso posterior
teams.to_csv(PROC + "teams.csv", index=False)
print("\nListo. Archivos generados: top20_teams.json, team_space.json, ml_metrics.json")
