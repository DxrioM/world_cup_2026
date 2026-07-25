"""
Etapa 1 — Datos crudos COMPLETOS del Mundial 2026 (104/104 partidos)
=======================================================================
Fuentes cruzadas: herramienta de datos deportivos (standings + box scores
autoritativos), Yahoo Sports, CBS Sports, Sky Sports, FOX Sports, FIFA.com,
UEFA.com, Olympics.com, NBC Sports, MSN.

Cada resultado de fase de grupos fue verificado aritmeticamente contra la
tabla final oficial (W/D/L/Puntos) de cada uno de los 12 grupos.

Torneo: 11 junio - 19 julio 2026. 48 equipos, 12 grupos, 104 partidos.
Campeon: España (venció a Argentina 1-0 en la final, tiempo extra).
"""

GROUPS = {
    "A": ["Mexico", "South Africa", "Korea Republic", "Czechia"],
    "B": ["Canada", "Switzerland", "Bosnia and Herzegovina", "Qatar"],
    "C": ["Brazil", "Morocco", "Scotland", "Haiti"],
    "D": ["USA", "Australia", "Paraguay", "Turkiye"],
    "E": ["Germany", "Ivory Coast", "Ecuador", "Curacao"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "IR Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Uruguay", "Saudi Arabia"],
    "I": ["France", "Norway", "Senegal", "Iraq"],
    "J": ["Argentina", "Austria", "Algeria", "Jordan"],
    "K": ["Colombia", "Portugal", "Congo DR", "Uzbekistan"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

CONFEDERATION = {
    "Mexico": "CONCACAF", "South Africa": "CAF", "Korea Republic": "AFC", "Czechia": "UEFA",
    "Canada": "CONCACAF", "Switzerland": "UEFA", "Bosnia and Herzegovina": "UEFA", "Qatar": "AFC",
    "Brazil": "CONMEBOL", "Morocco": "CAF", "Scotland": "UEFA", "Haiti": "CONCACAF",
    "USA": "CONCACAF", "Australia": "AFC", "Paraguay": "CONMEBOL", "Turkiye": "UEFA",
    "Germany": "UEFA", "Ivory Coast": "CAF", "Ecuador": "CONMEBOL", "Curacao": "CONCACAF",
    "Netherlands": "UEFA", "Japan": "AFC", "Sweden": "UEFA", "Tunisia": "CAF",
    "Belgium": "UEFA", "Egypt": "CAF", "IR Iran": "AFC", "New Zealand": "OFC",
    "Spain": "UEFA", "Cape Verde": "CAF", "Uruguay": "CONMEBOL", "Saudi Arabia": "AFC",
    "France": "UEFA", "Norway": "UEFA", "Senegal": "CAF", "Iraq": "AFC",
    "Argentina": "CONMEBOL", "Austria": "UEFA", "Algeria": "CAF", "Jordan": "AFC",
    "Colombia": "CONMEBOL", "Portugal": "UEFA", "Congo DR": "CAF", "Uzbekistan": "AFC",
    "England": "UEFA", "Croatia": "UEFA", "Ghana": "CAF", "Panama": "CONCACAF",
}

FINAL_STANDINGS = [
    (1,"Mexico","A",3,0,0,9), (2,"South Africa","A",1,1,1,4),
    (3,"Korea Republic","A",1,0,2,3), (4,"Czechia","A",0,1,2,1),

    (1,"Switzerland","B",2,1,0,7), (2,"Canada","B",1,1,1,4),
    (3,"Bosnia and Herzegovina","B",1,1,1,4), (4,"Qatar","B",0,1,2,1),

    (1,"Brazil","C",2,1,0,7), (2,"Morocco","C",2,1,0,7),
    (3,"Scotland","C",1,0,2,3), (4,"Haiti","C",0,0,3,0),

    (1,"USA","D",2,0,1,6), (2,"Australia","D",1,1,1,4),
    (3,"Paraguay","D",1,1,1,4), (4,"Turkiye","D",1,0,2,3),

    (1,"Germany","E",2,0,1,6), (2,"Ivory Coast","E",2,0,1,6),
    (3,"Ecuador","E",1,1,1,4), (4,"Curacao","E",0,1,2,1),

    (1,"Netherlands","F",2,1,0,7), (2,"Japan","F",1,2,0,5),
    (3,"Sweden","F",1,1,1,4), (4,"Tunisia","F",0,0,3,0),

    (1,"Belgium","G",1,2,0,5), (2,"Egypt","G",1,2,0,5),
    (3,"IR Iran","G",0,3,0,3), (4,"New Zealand","G",0,1,2,1),

    (1,"Spain","H",2,1,0,7), (2,"Cape Verde","H",0,3,0,3),
    (3,"Uruguay","H",0,2,1,2), (4,"Saudi Arabia","H",0,2,1,2),

    (1,"France","I",3,0,0,9), (2,"Norway","I",2,0,1,6),
    (3,"Senegal","I",1,0,2,3), (4,"Iraq","I",0,0,3,0),

    (1,"Argentina","J",3,0,0,9), (2,"Austria","J",1,1,1,4),
    (3,"Algeria","J",1,1,1,4), (4,"Jordan","J",0,0,3,0),

    (1,"Colombia","K",2,1,0,7), (2,"Portugal","K",1,2,0,5),
    (3,"Congo DR","K",1,1,1,4), (4,"Uzbekistan","K",0,0,3,0),

    (1,"England","L",2,1,0,7), (2,"Croatia","L",2,0,1,6),
    (3,"Ghana","L",1,1,1,4), (4,"Panama","L",0,0,3,0),
]

GROUP_MATCHES = [
    ("2026-06-11","A",1,"Mexico",2,"South Africa",0),
    ("2026-06-11","A",1,"Korea Republic",2,"Czechia",1),
    ("2026-06-18","A",2,"Czechia",1,"South Africa",1),
    ("2026-06-18","A",2,"Mexico",1,"Korea Republic",0),
    ("2026-06-24","A",3,"Czechia",0,"Mexico",3),
    ("2026-06-24","A",3,"South Africa",1,"Korea Republic",0),

    ("2026-06-12","B",1,"Canada",1,"Bosnia and Herzegovina",1),
    ("2026-06-13","B",1,"Switzerland",1,"Qatar",1),
    ("2026-06-18","B",2,"Switzerland",4,"Bosnia and Herzegovina",1),
    ("2026-06-18","B",2,"Canada",6,"Qatar",0),
    ("2026-06-24","B",3,"Switzerland",2,"Canada",1),
    ("2026-06-24","B",3,"Bosnia and Herzegovina",3,"Qatar",1),

    ("2026-06-13","C",1,"Brazil",1,"Morocco",1),
    ("2026-06-13","C",1,"Scotland",1,"Haiti",0),
    ("2026-06-19","C",2,"Morocco",1,"Scotland",0),
    ("2026-06-19","C",2,"Brazil",3,"Haiti",0),
    ("2026-06-24","C",3,"Scotland",0,"Brazil",3),
    ("2026-06-24","C",3,"Morocco",4,"Haiti",2),

    ("2026-06-12","D",1,"USA",4,"Paraguay",1),
    ("2026-06-13","D",1,"Australia",2,"Turkiye",0),
    ("2026-06-19","D",2,"USA",2,"Australia",0),
    ("2026-06-19","D",2,"Paraguay",1,"Turkiye",0),
    ("2026-06-25","D",3,"Turkiye",3,"USA",2),
    ("2026-06-25","D",3,"Paraguay",0,"Australia",0),

    ("2026-06-14","E",1,"Germany",7,"Curacao",1),
    ("2026-06-14","E",1,"Ivory Coast",1,"Ecuador",0),
    ("2026-06-20","E",2,"Germany",2,"Ivory Coast",1),
    ("2026-06-20","E",2,"Ecuador",0,"Curacao",0),
    ("2026-06-25","E",3,"Ecuador",2,"Germany",1),
    ("2026-06-25","E",3,"Curacao",0,"Ivory Coast",2),

    ("2026-06-14","F",1,"Netherlands",2,"Japan",2),
    ("2026-06-14","F",1,"Sweden",5,"Tunisia",1),
    ("2026-06-20","F",2,"Netherlands",5,"Sweden",1),
    ("2026-06-20","F",2,"Japan",4,"Tunisia",0),
    ("2026-06-25","F",3,"Japan",1,"Sweden",1),
    ("2026-06-25","F",3,"Netherlands",3,"Tunisia",1),

    ("2026-06-15","G",1,"Belgium",1,"Egypt",1),
    ("2026-06-15","G",1,"IR Iran",2,"New Zealand",2),
    ("2026-06-21","G",2,"Belgium",0,"IR Iran",0),
    ("2026-06-21","G",2,"Egypt",3,"New Zealand",1),
    ("2026-06-27","G",3,"Egypt",1,"IR Iran",1),
    ("2026-06-27","G",3,"Belgium",5,"New Zealand",1),

    ("2026-06-15","H",1,"Spain",0,"Cape Verde",0),
    ("2026-06-15","H",1,"Saudi Arabia",1,"Uruguay",1),
    ("2026-06-21","H",2,"Spain",4,"Saudi Arabia",0),
    ("2026-06-21","H",2,"Uruguay",2,"Cape Verde",2),
    ("2026-06-26","H",3,"Cape Verde",0,"Saudi Arabia",0),
    ("2026-06-26","H",3,"Spain",1,"Uruguay",0),

    ("2026-06-16","I",1,"France",3,"Senegal",1),
    ("2026-06-16","I",1,"Norway",4,"Iraq",1),
    ("2026-06-22","I",2,"France",3,"Iraq",0),
    ("2026-06-22","I",2,"Norway",3,"Senegal",2),
    ("2026-06-26","I",3,"France",4,"Norway",1),
    ("2026-06-26","I",3,"Senegal",5,"Iraq",0),

    ("2026-06-16","J",1,"Argentina",3,"Algeria",0),
    ("2026-06-16","J",1,"Austria",3,"Jordan",1),
    ("2026-06-22","J",2,"Argentina",2,"Austria",0),
    ("2026-06-22","J",2,"Jordan",1,"Algeria",2),
    ("2026-06-27","J",3,"Argentina",3,"Jordan",1),
    ("2026-06-27","J",3,"Austria",3,"Algeria",3),

    ("2026-06-17","K",1,"Portugal",1,"Congo DR",1),
    ("2026-06-17","K",1,"Uzbekistan",1,"Colombia",3),
    ("2026-06-23","K",2,"Portugal",5,"Uzbekistan",0),
    ("2026-06-23","K",2,"Colombia",1,"Congo DR",0),
    ("2026-06-27","K",3,"Colombia",0,"Portugal",0),
    ("2026-06-27","K",3,"Congo DR",3,"Uzbekistan",1),

    ("2026-06-17","L",1,"England",4,"Croatia",2),
    ("2026-06-17","L",1,"Ghana",1,"Panama",0),
    ("2026-06-23","L",2,"England",0,"Ghana",0),
    ("2026-06-23","L",2,"Croatia",1,"Panama",0),
    ("2026-06-27","L",3,"England",2,"Panama",0),
    ("2026-06-27","L",3,"Croatia",2,"Ghana",1),
]

KNOCKOUT_MATCHES = [
    ("2026-06-28","Ronda de 32","South Africa",0,"Canada",1,None),
    ("2026-06-29","Ronda de 32","Brazil",2,"Japan",1,None),
    ("2026-06-29","Ronda de 32","Germany",1,"Paraguay",1,"Paraguay gana 4-3 en penales"),
    ("2026-06-29","Ronda de 32","Netherlands",1,"Morocco",1,"Marruecos gana 3-2 en penales"),
    ("2026-06-30","Ronda de 32","Ivory Coast",1,"Norway",2,None),
    ("2026-06-30","Ronda de 32","France",3,"Sweden",0,None),
    ("2026-06-30","Ronda de 32","Mexico",2,"Ecuador",0,None),
    ("2026-07-01","Ronda de 32","England",2,"Congo DR",1,None),
    ("2026-07-01","Ronda de 32","Belgium",3,"Senegal",2,"Tiempo extra"),
    ("2026-07-01","Ronda de 32","USA",2,"Bosnia and Herzegovina",0,None),
    ("2026-07-02","Ronda de 32","Spain",3,"Austria",0,None),
    ("2026-07-02","Ronda de 32","Portugal",2,"Croatia",1,None),
    ("2026-07-02","Ronda de 32","Switzerland",2,"Algeria",0,None),
    ("2026-07-03","Ronda de 32","Australia",1,"Egypt",1,"Egipto gana 4-2 en penales"),
    ("2026-07-03","Ronda de 32","Argentina",3,"Cape Verde",2,"Tiempo extra"),
    ("2026-07-03","Ronda de 32","Colombia",1,"Ghana",0,None),

    ("2026-07-04","Octavos de Final","Morocco",3,"Canada",0,None),
    ("2026-07-04","Octavos de Final","France",1,"Paraguay",0,None),
    ("2026-07-05","Octavos de Final","Brazil",0,"Norway",2,None),
    ("2026-07-05","Octavos de Final","Mexico",2,"England",3,None),
    ("2026-07-06","Octavos de Final","Spain",1,"Portugal",0,None),
    ("2026-07-06","Octavos de Final","Belgium",4,"USA",1,None),
    ("2026-07-07","Octavos de Final","Argentina",3,"Egypt",2,None),
    ("2026-07-07","Octavos de Final","Switzerland",0,"Colombia",0,"Suiza gana 4-3 en penales"),

    ("2026-07-09","Cuartos de Final","France",2,"Morocco",0,None),
    ("2026-07-10","Cuartos de Final","Spain",2,"Belgium",1,None),
    ("2026-07-11","Cuartos de Final","Norway",1,"England",2,"Tiempo extra"),
    ("2026-07-11","Cuartos de Final","Argentina",3,"Switzerland",1,None),

    ("2026-07-14","Semifinal","France",0,"Spain",2,None),
    ("2026-07-15","Semifinal","England",1,"Argentina",2,None),

    ("2026-07-18","Tercer puesto","France",4,"England",6,None),

    ("2026-07-19","Final","Spain",1,"Argentina",0,"Tiempo extra"),
]

TOP_SCORERS = [
    # (nombre, equipo, goles, asistencias, nota)
    ("Kylian Mbappe", "France", 10, 4, "Ganador Bota de Oro. Maximo goleador historico del Mundial (22 en su carrera)."),
    ("Lionel Messi", "Argentina", 8, 4, "2do lugar. Establecio el record de goleador historico del Mundial durante el torneo."),
    ("Jude Bellingham", "England", 7, 1, "Maximo goleador ingles en un solo Mundial."),
    ("Erling Haaland", "Norway", 7, 0, None),
    ("Ousmane Dembele", "France", 6, 0, None),
    ("Harry Kane", "England", 6, 0, "Supero a Gary Lineker como maximo goleador historico de Inglaterra."),
    ("Mikel Oyarzabal", "Spain", 5, 0, None),
    ("Ismaila Sarr", "Senegal", 4, 0, None),
    ("Julian Quinones", "Mexico", 4, 0, None),
    ("Vinicius Junior", "Brazil", 4, 0, None),
    ("Bukayo Saka", "England", 3, 0, None),
    ("Romelu Lukaku", "Belgium", 3, 0, None),
    ("Lautaro Martinez", "Argentina", 3, 0, None),
    ("Cody Gakpo", "Netherlands", 3, 0, None),
    ("Bradley Barcola", "France", 3, 0, None),
    ("Matheus Cunha", "Brazil", 3, 0, None),
    ("Raul Jimenez", "Mexico", 3, 0, None),
    ("Kai Havertz", "Germany", 3, 0, None),
    ("Jonathan David", "Canada", 3, 0, None),
    ("Charles De Ketelaere", "Belgium", 3, 0, None),
]

FINAL_RESULTS_SUMMARY = {
    "champion": "Spain",
    "runner_up": "Argentina",
    "third_place": "England",
    "fourth_place": "France",
    "golden_boot": "Kylian Mbappe (10 goles)",
    "host_countries": ["USA", "Canada", "Mexico"],
    "total_teams": 48,
    "total_matches": 104,
    "dates": "11 junio - 19 julio 2026",
}

if __name__ == "__main__":
    print(f"Grupos: {len(GROUPS)}")
    print(f"Equipos en standings: {len(FINAL_STANDINGS)}")
    print(f"Partidos de fase de grupos: {len(GROUP_MATCHES)} / 72 esperados")
    print(f"Partidos de eliminacion directa: {len(KNOCKOUT_MATCHES)} / 32 esperados")
    print(f"Total partidos: {len(GROUP_MATCHES) + len(KNOCKOUT_MATCHES)} / 104 esperados")
    print(f"Top goleadores: {len(TOP_SCORERS)}")

    from collections import defaultdict
    stats = defaultdict(lambda: [0,0,0])
    for _, grp, jornada, local, gl, visit, gv in GROUP_MATCHES:
        if gl > gv: stats[local][0]+=1; stats[visit][2]+=1
        elif gl < gv: stats[visit][0]+=1; stats[local][2]+=1
        else: stats[local][1]+=1; stats[visit][1]+=1

    errores = 0
    for rank, team, grp, w, d, l, pts in FINAL_STANDINGS:
        calc = stats[team]
        if calc != [w,d,l]:
            print(f"  DISCREPANCIA: {team} — standings dice {[w,d,l]}, partidos dan {calc}")
            errores += 1
    if errores == 0:
        print("\nLos 72 partidos de fase de grupos cuadran EXACTAMENTE con las 48 tablas de equipos.")
    else:
        print(f"\n{errores} discrepancias encontradas.")
