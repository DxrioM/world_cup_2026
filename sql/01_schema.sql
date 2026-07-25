-- ============================================================
-- Esquema — Portafolio de Análisis del Mundial 2026
-- ============================================================
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS top_scorers;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team            TEXT PRIMARY KEY,
    grupo           TEXT NOT NULL,
    confederacion   TEXT NOT NULL,
    iso2            TEXT NOT NULL,
    bandera         TEXT,
    es_anfitrion    INTEGER NOT NULL,
    grupo_rank      INTEGER,
    grupo_w         INTEGER, grupo_d INTEGER, grupo_l INTEGER, grupo_pts INTEGER,
    total_partidos  INTEGER,
    total_victorias INTEGER,
    goles_favor     INTEGER,
    goles_contra    INTEGER,
    dif_goles       INTEGER,
    etapa_final_code INTEGER,
    etapa_final     TEXT,
    avanzo_a_eliminacion INTEGER,
    posicion_final  INTEGER
);

CREATE TABLE matches (
    match_id        INTEGER PRIMARY KEY,
    fecha           TEXT,
    fase            TEXT NOT NULL,
    grupo           TEXT,
    jornada         INTEGER,
    local           TEXT NOT NULL REFERENCES teams(team),
    goles_local     INTEGER NOT NULL,
    visitante       TEXT NOT NULL REFERENCES teams(team),
    goles_visitante INTEGER NOT NULL,
    nota            TEXT,
    total_goles     INTEGER,
    dif_goles       INTEGER,
    resultado       TEXT,
    es_eliminacion_directa INTEGER,
    fue_penales     INTEGER,
    fue_tiempo_extra INTEGER
);

CREATE TABLE top_scorers (
    rank        INTEGER PRIMARY KEY,
    jugador     TEXT NOT NULL,
    equipo      TEXT NOT NULL REFERENCES teams(team),
    iso2        TEXT NOT NULL,
    bandera     TEXT,
    goles       INTEGER NOT NULL,
    asistencias INTEGER,
    nota        TEXT
);

CREATE INDEX idx_matches_fase ON matches(fase);
CREATE INDEX idx_matches_local ON matches(local);
CREATE INDEX idx_matches_visitante ON matches(visitante);
CREATE INDEX idx_teams_confed ON teams(confederacion);
