"""
Etapa 2 — Limpieza y transformacion de datos
=============================================
Combina fase de grupos + eliminacion directa para calcular estadisticas
completas por equipo (no solo fase de grupos), determina la etapa final
alcanzada por cada uno de los 48 equipos, y arma las tablas limpias.
"""
import sys, os
sys.path.insert(0, "/home/claude/worldcup_portfolio/data/raw")
import worldcup_2026_data as raw
import pandas as pd

OUT_DIR = "/home/claude/worldcup_portfolio/data/processed"

# Codigos ISO2 para banderas (unicode flag emoji, sin usar escudos con marca registrada)
ISO2 = {
    "Mexico":"mx","South Africa":"za","Korea Republic":"kr","Czechia":"cz",
    "Canada":"ca","Switzerland":"ch","Bosnia and Herzegovina":"ba","Qatar":"qa",
    "Brazil":"br","Morocco":"ma","Scotland":"gb-sct","Haiti":"ht",
    "USA":"us","Australia":"au","Paraguay":"py","Turkiye":"tr",
    "Germany":"de","Ivory Coast":"ci","Ecuador":"ec","Curacao":"cw",
    "Netherlands":"nl","Japan":"jp","Sweden":"se","Tunisia":"tn",
    "Belgium":"be","Egypt":"eg","IR Iran":"ir","New Zealand":"nz",
    "Spain":"es","Cape Verde":"cv","Uruguay":"uy","Saudi Arabia":"sa",
    "France":"fr","Norway":"no","Senegal":"sn","Iraq":"iq",
    "Argentina":"ar","Austria":"at","Algeria":"dz","Jordan":"jo",
    "Colombia":"co","Portugal":"pt","Congo DR":"cd","Uzbekistan":"uz",
    "England":"gb-eng","Croatia":"hr","Ghana":"gh","Panama":"pa",
}

HOSTS = {"USA", "Canada", "Mexico"}

def flag_emoji(iso2):
    """Convierte codigo ISO2 a bandera emoji Unicode. Maneja los casos
    especiales de Inglaterra/Escocia (usan secuencias de 'tag', no ISO2)."""
    special = {
        "gb-eng": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F",
        "gb-sct": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",
    }
    if iso2 in special:
        return special[iso2]
    return "".join(chr(0x1F1E6 + ord(c) - ord("a")) for c in iso2.lower())

# Etapas ordenadas (para ranking y comparaciones)
STAGE_ORDER = {
    "Fase de grupos": 0, "Ronda de 32": 1, "Octavos de Final": 2,
    "Cuartos de Final": 3, "Semifinal": 4, "Cuarto puesto": 5,
    "Tercer puesto": 6, "Subcampeon": 7, "Campeon": 8,
}
STAGE_LABEL_ES = {v: k for k, v in STAGE_ORDER.items()}

def build_matches_df():
    rows = []
    mid = 1
    for fecha, grp, jornada, local, gl, visit, gv in raw.GROUP_MATCHES:
        rows.append({
            "match_id": mid, "fecha": fecha, "fase": "Fase de grupos", "grupo": grp,
            "jornada": jornada, "local": local, "goles_local": gl,
            "visitante": visit, "goles_visitante": gv, "nota": None,
        })
        mid += 1
    for fecha, fase, local, gl, visit, gv, nota in raw.KNOCKOUT_MATCHES:
        rows.append({
            "match_id": mid, "fecha": fecha, "fase": fase, "grupo": None,
            "jornada": None, "local": local, "goles_local": gl,
            "visitante": visit, "goles_visitante": gv, "nota": nota,
        })
        mid += 1

    df = pd.DataFrame(rows)
    df["total_goles"] = df["goles_local"] + df["goles_visitante"]
    df["dif_goles"] = (df["goles_local"] - df["goles_visitante"]).abs()
    df["resultado"] = df.apply(
        lambda r: "Local" if r.goles_local > r.goles_visitante
        else ("Visitante" if r.goles_visitante > r.goles_local else "Empate"), axis=1)
    df["es_eliminacion_directa"] = df["fase"] != "Fase de grupos"
    df["fue_penales"] = df["nota"].fillna("").str.contains("penales")
    df["fue_tiempo_extra"] = df["nota"].fillna("").str.contains("[Tt]iempo extra")
    return df

def determine_final_stage(team, matches_df):
    """Determina la etapa mas lejana alcanzada por un equipo."""
    if team == raw.FINAL_RESULTS_SUMMARY["champion"]:
        return STAGE_ORDER["Campeon"]
    if team == raw.FINAL_RESULTS_SUMMARY["runner_up"]:
        return STAGE_ORDER["Subcampeon"]
    if team == raw.FINAL_RESULTS_SUMMARY["third_place"]:
        return STAGE_ORDER["Tercer puesto"]
    if team == raw.FINAL_RESULTS_SUMMARY["fourth_place"]:
        return STAGE_ORDER["Cuarto puesto"]
    # etapa mas avanzada en la que el equipo jugo (eliminatoria)
    ko = matches_df[matches_df.es_eliminacion_directa &
                     ((matches_df.local == team) | (matches_df.visitante == team))]
    if ko.empty:
        return STAGE_ORDER["Fase de grupos"]
    fases_jugadas = ko["fase"].map(STAGE_ORDER)
    return int(fases_jugadas.max())

def build_teams_df(matches_df):
    rows = []
    for rank, team, grp, w, d, l, pts in raw.FINAL_STANDINGS:
        team_matches = matches_df[(matches_df.local == team) | (matches_df.visitante == team)]
        gf = ga = 0
        for _, m in team_matches.iterrows():
            if m.local == team:
                gf += m.goles_local; ga += m.goles_visitante
            else:
                gf += m.goles_visitante; ga += m.goles_local

        stage_code = determine_final_stage(team, matches_df)
        total_partidos = len(team_matches)
        total_victorias = len(team_matches[
            ((team_matches.local == team) & (team_matches.resultado == "Local")) |
            ((team_matches.visitante == team) & (team_matches.resultado == "Visitante"))
        ])

        rows.append({
            "team": team, "grupo": grp, "confederacion": raw.CONFEDERATION[team],
            "iso2": ISO2[team], "bandera": flag_emoji(ISO2[team]), "es_anfitrion": team in HOSTS,
            "grupo_rank": rank, "grupo_w": w, "grupo_d": d, "grupo_l": l, "grupo_pts": pts,
            "total_partidos": total_partidos, "total_victorias": total_victorias,
            "goles_favor": gf, "goles_contra": ga, "dif_goles": gf - ga,
            "etapa_final_code": stage_code, "etapa_final": STAGE_LABEL_ES[stage_code],
            "avanzo_a_eliminacion": stage_code >= STAGE_ORDER["Ronda de 32"],
        })
    df = pd.DataFrame(rows).sort_values(
        ["etapa_final_code", "dif_goles", "goles_favor"], ascending=[False, False, False]
    ).reset_index(drop=True)
    df["posicion_final"] = df.index + 1
    return df

def build_scorers_df():
    rows = []
    for i, (nombre, equipo, goles, asist, nota) in enumerate(raw.TOP_SCORERS, start=1):
        rows.append({
            "rank": i, "jugador": nombre, "equipo": equipo, "iso2": ISO2[equipo],
            "bandera": flag_emoji(ISO2[equipo]), "goles": goles, "asistencias": asist, "nota": nota,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    matches_df = build_matches_df()
    teams_df = build_teams_df(matches_df)
    scorers_df = build_scorers_df()

    os.makedirs(OUT_DIR, exist_ok=True)
    matches_df.to_csv(f"{OUT_DIR}/matches.csv", index=False)
    teams_df.to_csv(f"{OUT_DIR}/teams.csv", index=False)
    scorers_df.to_csv(f"{OUT_DIR}/top_scorers.csv", index=False)

    print(f"matches.csv: {len(matches_df)} partidos")
    print(f"teams.csv: {len(teams_df)} equipos")
    print(f"top_scorers.csv: {len(scorers_df)} jugadores")
    print("\nTop 8 equipos por etapa final alcanzada:")
    print(teams_df[["posicion_final","team","etapa_final","goles_favor","goles_contra","dif_goles"]].head(8).to_string(index=False))
