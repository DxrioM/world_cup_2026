# ⚽ Radiografía de un Mundial — Portafolio de Data Science Deportivo

Pipeline de datos de extremo a extremo sobre los **104 partidos del Mundial 2026**: extracción y verificación manual de datos (el torneo terminó apenas unos días antes de este proyecto), modelado relacional en SQL, machine learning (power ranking, clustering, clasificador predictivo) y un dashboard interactivo con tema de fútbol.

**🔴 Demo en vivo:** [https://dxriom.github.io/world_cup_2026/](https://dxriom.github.io/world_cup_2026/) *(una vez activado GitHub Pages)*

**📁 Repositorio:** [github.com/DxrioM/world_cup_2026](https://github.com/DxrioM/world_cup_2026)

Sin conexión o mientras Pages no esté activo: [docs/index.html](docs/index.html)

---

## Por qué este proyecto es distinto

A diferencia de un dataset de Kaggle ya armado, el Mundial 2026 terminó el 19 de julio — **no existía ningún dataset curado disponible**. Cada uno de los 104 resultados se recopiló y verificó manualmente cruzando 8+ fuentes (FIFA.com, Sky Sports, CBS Sports, Yahoo Sports, UEFA.com, entre otras), y **cada resultado de fase de grupos se validó aritméticamente** contra las tablas oficiales de los 12 grupos: los goles a favor/contra y el W-D-L de cada uno de los 104 partidos suman exactamente los puntos finales de cada selección. Esto refleja un desafío real de ingeniería de datos: trabajar con información que aún no está empaquetada.

## Restricción de diseño: sin fotos ni escudos

Las fotos de jugadores y los escudos oficiales de las federaciones tienen derechos de autor / marca registrada. En vez de eso, el dashboard usa:
- **Banderas** en formato emoji Unicode (libres de derechos, incluyendo los casos especiales de Inglaterra/Escocia con secuencias de "tag" Unicode)
- **Cromos** de jugador estilo "tarjeta coleccionable" con iniciales en vez de foto

## Estructura del proyecto

```
worldcup_portfolio/
├── data/
│   ├── raw/worldcup_2026_data.py   # datos crudos verificados (104 partidos, standings, goleadores)
│   └── processed/                  # CSV/JSON limpios + base SQLite
├── sql/
│   ├── 01_schema.sql                # esquema relacional (teams, matches, top_scorers)
│   └── 02_eda_queries.sql           # 8 queries de análisis exploratorio
├── scripts/
│   ├── 01_clean_transform.py        # limpieza + feature engineering (etapa final, banderas)
│   ├── 02_load_db.py                # carga a SQLite
│   ├── 03_run_eda.py                # ejecuta las queries SQL → JSON
│   ├── 04_ml_analysis.py            # power ranking, KMeans, PCA, clasificador
│   ├── 05_export_json.py            # exporta tablas adicionales a JSON
│   └── 06_build_dashboard.py        # inyecta datos + Chart.js en la plantilla
├── lib/
│   ├── chart.umd.min.js             # Chart.js empaquetado localmente
│   └── dashboard_template.html      # plantilla del dashboard
├── docs/index.html                  # ⭐ producto final, listo para GitHub Pages
└── README.md
```

## Cómo reproducirlo

```bash
pip install pandas numpy scikit-learn
cd scripts
python3 01_clean_transform.py
python3 02_load_db.py
python3 03_run_eda.py
python3 04_ml_analysis.py
python3 05_export_json.py
python3 06_build_dashboard.py
cp ../outputs/index.html ../docs/
```

## Metodología del Power Ranking (Top 20 equipos)

Score compuesto (0-100), sin depender de un único criterio:
- **50%** etapa final alcanzada (fase de grupos → campeón)
- **20%** victorias totales
- **20%** diferencia de gol
- **10%** goles a favor

## Metodología del modelo predictivo

Random Forest que predice si un equipo avanza a la eliminación directa usando solo estadísticas de fase de grupos (puntos, goles a favor/contra, diferencia de gol). Validado con **5-fold cross-validation** dado el tamaño pequeño de la muestra (48 equipos) — una sola partición train/test no sería confiable a esta escala. Resultado: ~97.8% de accuracy vs. 66.7% de baseline (clase mayoritaria), con los puntos de fase de grupos como variable más predictiva (esperable, ya que son el criterio real de clasificación — el modelo confirma que refleja las reglas del torneo, no un patrón oculto sorprendente).

## Principales hallazgos

- El promedio de goles por partido es prácticamente el mismo en fase de grupos (2.99) y en eliminación directa (2.88) — el fútbol de "todo o nada" no se vuelve necesariamente más abierto.
- UEFA (Europa) dominó en volumen de victorias (42 en total), pero CONMEBOL tuvo la etapa promedio más alta por selección — menos equipos, mejor rendimiento relativo.
- 8 de los 104 partidos (7.7%) se definieron por penales o tiempo extra.
- Kylian Mbappé ganó la Bota de Oro con 10 goles y se convirtió en el máximo goleador histórico del Mundial (22 goles en su carrera), superando a Messi en el partido por el tercer puesto.

## Stack técnico

`Python` · `pandas` · `numpy` · `scikit-learn` · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Datos: recopilados y verificados manualmente de fuentes públicas (FIFA.com, Sky Sports, CBS Sports, Yahoo Sports, UEFA.com, Olympics.com, NBC Sports, MSN) tras la conclusión del torneo el 19 de julio de 2026.*
