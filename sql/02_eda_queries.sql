-- ============================================================
-- Análisis Exploratorio de Datos (EDA) — Mundial 2026
-- ============================================================

-- 1. Promedio de goles por partido: fase de grupos vs eliminación directa
SELECT
    CASE WHEN es_eliminacion_directa = 1 THEN 'Eliminación directa' ELSE 'Fase de grupos' END AS tipo_fase,
    COUNT(*) AS num_partidos,
    ROUND(AVG(total_goles), 2) AS goles_promedio_por_partido,
    SUM(total_goles) AS goles_totales
FROM matches
GROUP BY es_eliminacion_directa;

-- 2. Rendimiento por confederación (equipos, promedio de etapa alcanzada, victorias)
SELECT
    confederacion,
    COUNT(*) AS num_equipos,
    ROUND(AVG(etapa_final_code), 2) AS etapa_promedio,
    SUM(total_victorias) AS victorias_totales,
    ROUND(AVG(goles_favor), 1) AS goles_favor_promedio
FROM teams
GROUP BY confederacion
ORDER BY etapa_promedio DESC;

-- 3. Las 10 mayores goleadas del torneo (por diferencia de gol)
SELECT fase, local, goles_local, visitante, goles_visitante, dif_goles
FROM matches
ORDER BY dif_goles DESC, total_goles DESC
LIMIT 10;

-- 4. Rendimiento de las selecciones anfitrionas (USA, Canadá, México)
SELECT team, etapa_final, grupo_pts, goles_favor, goles_contra, dif_goles
FROM teams
WHERE es_anfitrion = 1
ORDER BY etapa_final_code DESC;

-- 5. Partidos decididos por penales o tiempo extra (el drama del Mundial)
SELECT fase, local, goles_local, visitante, goles_visitante, nota
FROM matches
WHERE fue_penales = 1 OR fue_tiempo_extra = 1
ORDER BY fecha;

-- 6. Top 10 equipos más goleadores (goles a favor totales, todas las fases)
SELECT team, confederacion, etapa_final, goles_favor, goles_contra, dif_goles
FROM teams
ORDER BY goles_favor DESC
LIMIT 10;

-- 7. Ventaja de localía: ¿gana más el equipo que aparece como "local"?
SELECT resultado, COUNT(*) AS num_partidos,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM matches), 1) AS porcentaje
FROM matches
GROUP BY resultado
ORDER BY num_partidos DESC;

-- 8. Distribución de equipos por etapa final alcanzada (funnel del torneo)
SELECT etapa_final, etapa_final_code, COUNT(*) AS num_equipos
FROM teams
GROUP BY etapa_final, etapa_final_code
ORDER BY etapa_final_code;
