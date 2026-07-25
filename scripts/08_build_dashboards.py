"""
Etapa 8 — Construir dashboard.html en ES y EN
"""
import os, shutil

BASE = "/home/claude/worldcup_portfolio"
TEMPLATE = f"{BASE}/lib/dashboard_template_i18n.html"
CHARTJS = f"{BASE}/lib/chart.umd.min.js"
PROC = f"{BASE}/data/processed/"
OUT_DIR = f"{BASE}/outputs"
DOCS_DIR = f"{BASE}/docs"

with open(TEMPLATE, encoding="utf-8") as f:
    template = f.read()
with open(CHARTJS, encoding="utf-8") as f:
    chartjs_lib = f.read()

def load(name):
    with open(PROC + name, encoding="utf-8") as f:
        return f.read()

CONFIGS = {
    "es": {
        "html_lang": "es",
        "page_title": "Radiografía de un Mundial — Portafolio de Data Science Deportivo",
        "og_desc": "Los 104 partidos del Mundial 2026 analizados con SQL, Python y Machine Learning. Top 20 goleadores, ranking de equipos, y un modelo predictivo.",
        "canonical": "https://dxriom.github.io/world_cup_2026/",
        "eda": "eda_results.json", "space": "team_space.json", "top20": "top20_teams.json",
        "scorers": "top_scorers.json", "matches": "matches.json", "metrics": "ml_metrics.json",
        "out": "index.html",
        "link_es": "index.html", "link_en": "dashboard_en.html",
        "es_active": "active", "en_active": "",
    },
    "en": {
        "html_lang": "en",
        "page_title": "Anatomy of a World Cup — Sports Data Science Portfolio",
        "og_desc": "All 104 matches of the 2026 World Cup analyzed with SQL, Python and Machine Learning. Top 20 scorers, team ranking, and a predictive model.",
        "canonical": "https://dxriom.github.io/world_cup_2026/dashboard_en.html",
        "eda": "eda_results_en.json", "space": "team_space_en.json", "top20": "top20_teams_en.json",
        "scorers": "top_scorers_en.json", "matches": "matches_en.json", "metrics": "ml_metrics_en.json",
        "out": "dashboard_en.html",
        "link_es": "index.html", "link_en": "dashboard_en.html",
        "es_active": "", "en_active": "active",
    },
}

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

for lang, cfg in CONFIGS.items():
    html = template
    html = html.replace("__CHARTJS_LIB__", chartjs_lib)
    html = html.replace("__HTML_LANG__", cfg["html_lang"])
    html = html.replace("__PAGE_TITLE__", cfg["page_title"])
    html = html.replace("__OG_DESC__", cfg["og_desc"])
    html = html.replace("__CANONICAL_URL__", cfg["canonical"])
    html = html.replace("__LANG__", lang)
    html = html.replace("__LINK_ES__", cfg["link_es"])
    html = html.replace("__LINK_EN__", cfg["link_en"])
    html = html.replace("__ES_ACTIVE__", cfg["es_active"])
    html = html.replace("__EN_ACTIVE__", cfg["en_active"])
    html = html.replace("__EDA_JSON__", load(cfg["eda"]))
    html = html.replace("__TEAMS_SPACE_JSON__", load(cfg["space"]))
    html = html.replace("__TOP20_TEAMS_JSON__", load(cfg["top20"]))
    html = html.replace("__SCORERS_JSON__", load(cfg["scorers"]))
    html = html.replace("__MATCHES_JSON__", load(cfg["matches"]))
    html = html.replace("__METRICS_JSON__", load(cfg["metrics"]))

    out_path = f"{OUT_DIR}/{cfg['out']}"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    placeholders = ["__CHARTJS_LIB__","__HTML_LANG__","__PAGE_TITLE__","__OG_DESC__","__CANONICAL_URL__",
                     "__LANG__","__LINK_ES__","__LINK_EN__","__ES_ACTIVE__","__EN_ACTIVE__",
                     "__EDA_JSON__","__TEAMS_SPACE_JSON__","__TOP20_TEAMS_JSON__","__SCORERS_JSON__",
                     "__MATCHES_JSON__","__METRICS_JSON__"]
    leftover = [p for p in placeholders if p in html]
    size_mb = os.path.getsize(out_path) / (1024*1024)
    print(f"{lang}: {out_path} ({size_mb:.2f} MB) — sin resolver: {leftover}")

    shutil.copy(out_path, f"{DOCS_DIR}/{cfg['out']}")

print("Copiados a docs/")
