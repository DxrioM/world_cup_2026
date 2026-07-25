"""
Grafico de resumen para LinkedIn v4 — redistribucion completa:
- Grid 2x2: 2 graficos de barras (muchas categorias) + 2 donuts (pocas categorias)
- 5 bullets con numeros/datos de impacto (antes solo 2)
- INSIGHT con fondo solido dorado (maximo contraste) en vez de un borde sutil
- Paleta oficial de las 3 sedes: rojo (Canada) / verde (Mexico) / azul (USA) + dorado (trofeo)
"""
import cairosvg
import os
import math
import textwrap

P = {
    "bg": "#0e2919", "card": "#153524", "card2": "#1b422e", "border": "#2c5b41",
    "text": "#F2EFE3", "text2": "#A7C4AE", "muted": "#6E8F77",
    "gold": "#E0B23D", "red": "#D6483F", "green": "#3FA65C", "blue": "#3E7FC4",
    "dark": "#0e2919",
}

def soccer_ball(cx, cy, r, fill="#F2EFE3", accent="#0e2919"):
    pent_r = r * 0.42
    pts = [(cx + pent_r*math.cos(math.radians(-90+i*72)), cy + pent_r*math.sin(math.radians(-90+i*72))) for i in range(5)]
    pent_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    wedges = ""
    for i in range(5):
        a1, a2 = math.radians(-90+i*72-36), math.radians(-90+i*72+36)
        p1 = pts[i]
        o1 = (cx + r*0.92*math.cos(a1), cy + r*0.92*math.sin(a1))
        o2 = (cx + r*0.92*math.cos(a2), cy + r*0.92*math.sin(a2))
        wedges += (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{o1[0]:.1f},{o1[1]:.1f} '
                   f'A{r*0.92:.1f},{r*0.92:.1f} 0 0,1 {o2[0]:.1f},{o2[1]:.1f} Z" fill="{accent}" opacity="0.85"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>{wedges}'
            f'<path d="{pent_path}" fill="{accent}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="{r*0.06}"/>')

def trophy_icon(cx, top_y, w, color):
    bowl_w, bowl_h = w, w*0.85
    stem_w, stem_h = w*0.16, w*0.38
    base_w, base_h = w*0.62, w*0.13
    x0, y0 = cx-bowl_w/2, top_y
    handle_r = bowl_w*0.32
    return f'''
<g fill="{color}">
  <path d="M {x0} {y0} Q {x0} {y0+bowl_h*0.75} {cx} {y0+bowl_h} Q {cx+bowl_w/2} {y0+bowl_h*0.75} {cx+bowl_w/2} {y0} Z"/>
  <circle cx="{x0-handle_r*0.35}" cy="{y0+bowl_h*0.32}" r="{handle_r}" fill="none" stroke="{color}" stroke-width="{w*0.09}"/>
  <circle cx="{cx+bowl_w/2+handle_r*0.35}" cy="{y0+bowl_h*0.32}" r="{handle_r}" fill="none" stroke="{color}" stroke-width="{w*0.09}"/>
  <rect x="{cx-stem_w/2}" y="{y0+bowl_h}" width="{stem_w}" height="{stem_h}"/>
  <polygon points="{cx-base_w/2},{y0+bowl_h+stem_h+base_h} {cx+base_w/2},{y0+bowl_h+stem_h+base_h} {cx+base_w*0.38},{y0+bowl_h+stem_h} {cx-base_w*0.38},{y0+bowl_h+stem_h}"/>
  <circle cx="{cx}" cy="{y0+bowl_h*0.42}" r="{bowl_w*0.1}" fill="{P['bg']}" opacity="0.35"/>
</g>'''

def mini_hbar(x, y, w, items, max_val, colors, value_fmt="{:.0f}", bar_h=22, gap=13, label_size=15, val_size=14):
    svg = ""
    label_w = 92
    for i, (label, val) in enumerate(items):
        by = y + i*(bar_h+gap)
        bw = max(4, (val/max_val) * (w - label_w - 50))
        color = colors[i % len(colors)]
        svg += f'<text x="{x}" y="{by+bar_h*0.72}" font-size="{label_size}" fill="{P["text2"]}">{label}</text>'
        svg += f'<rect x="{x+label_w}" y="{by}" width="{w-label_w-50}" height="{bar_h}" rx="3" fill="{P["bg"]}"/>'
        svg += f'<rect x="{x+label_w}" y="{by}" width="{bw:.1f}" height="{bar_h}" rx="3" fill="{color}"/>'
        svg += f'<text x="{x+w-46}" y="{by+bar_h*0.72}" font-family="DejaVu Sans Mono" font-size="{val_size}" font-weight="bold" fill="{P["text"]}">{value_fmt.format(val)}</text>'
    return svg, y + len(items)*(bar_h+gap)

def donut(cx, cy, r, stroke_w, segments, center_label, center_sub=""):
    circumference = 2*math.pi*r
    total = sum(v for v, _ in segments)
    svg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{P["bg"]}" stroke-width="{stroke_w}"/>'
    offset = 0
    for val, color in segments:
        frac = val/total
        dash = frac*circumference
        svg += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_w}" '
                f'stroke-dasharray="{dash:.1f} {circumference:.1f}" stroke-dashoffset="{-offset:.1f}" '
                f'transform="rotate(-90 {cx} {cy})"/>')
        offset += dash
    svg += f'<text x="{cx}" y="{cy+2}" font-size="30" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{center_label}</text>'
    if center_sub:
        svg += f'<text x="{cx}" y="{cy+22}" font-size="12" fill="{P["text2"]}" text-anchor="middle">{center_sub}</text>'
    return svg

def legend_row(x, y, items, colors, size=13):
    svg = ""
    cx = x
    for (label, _), color in zip(items, colors):
        svg += f'<circle cx="{cx+5}" cy="{y}" r="5" fill="{color}"/>'
        svg += f'<text x="{cx+16}" y="{y+4}" font-size="{size}" fill="{P["text2"]}">{label}</text>'
        cx += 16 + len(label)*7.2 + 22
    return svg

def pitch_background(W, H):
    mid_y = H*0.40
    return f'''<g stroke="rgba(242,239,227,0.055)" stroke-width="2.5" fill="none">
  <rect x="40" y="40" width="{W-80}" height="{H-80}" rx="4"/>
  <line x1="40" y1="{mid_y}" x2="{W-40}" y2="{mid_y}"/>
  <circle cx="{W/2}" cy="{mid_y}" r="130"/>
  <path d="M 40 100 A 60 60 0 0 0 100 40"/><path d="M {W-100} 40 A 60 60 0 0 0 {W-40} 100"/>
  <path d="M 40 {H-100} A 60 60 0 0 1 100 {H-40}"/><path d="M {W-100} {H-40} A 60 60 0 0 1 {W-40} {H-100}"/>
</g>'''

def build_svg(lang):
    if lang == "es":
        title1, title2 = "Radiografía", "de un Mundial"
        subtitle = "PORTAFOLIO DE DATA SCIENCE · FÚTBOL"
        c1_title, c1_items = "VICTORIAS POR CONFEDERACIÓN", [("UEFA", 42), ("CONMEBOL", 15), ("CAF", 11), ("CONCACAF", 9)]
        c2_title = "PARTIDOS DE INFARTO"
        c2_segments, c2_center, c2_sub = [(8, P['red']), (96, P['card2'])], "7.7%", "penales / T.E."
        c2_legend = [("Penales/T.E.", 8), ("Resto", 96)]
        c3_title, c3_items = "MODELO: ACCURACY", [("Azar", 66.7), ("Random Forest", 97.8)]
        c4_title = "DISTRIBUCIÓN DE GOLES"
        c4_segments, c4_center, c4_sub = [(215, P['gold']), (92, P['blue'])], "307", "goles totales"
        c4_legend = [("Grupos (215)", 215), ("Eliminación (92)", 92)]
        bullets = [
            "104 partidos verificados matemáticamente contra las 12 tablas oficiales",
            "España campeón: venció a Argentina 1-0 en la final (tiempo extra)",
            "Mbappé ganó la Bota de Oro con 10 goles, superando a Messi (8)",
            "CONMEBOL iguala en etapa promedio a confederaciones con el triple de equipos",
            "Mayor goleada del torneo: Alemania 7-1 vs. Curazao",
        ]
        insight_label = "💡 EL DATO QUE MÁS SORPRENDE"
        insight_big = "2.99 vs 2.88 goles/partido"
        insight_text = "Se anotó MÁS en fase de grupos que en eliminación directa — el miedo a perder pesa más que las ganas de anotar cuando es todo o nada."
        cta = "Demo interactivo + código completo →"
        cta2 = "link en el post · ES / EN"
    else:
        title1, title2 = "Anatomy of", "a World Cup"
        subtitle = "DATA SCIENCE PORTFOLIO · SOCCER"
        c1_title, c1_items = "WINS BY CONFEDERATION", [("UEFA", 42), ("CONMEBOL", 15), ("CAF", 11), ("CONCACAF", 9)]
        c2_title = "NAIL-BITER MATCHES"
        c2_segments, c2_center, c2_sub = [(8, P['red']), (96, P['card2'])], "7.7%", "pens / ET"
        c2_legend = [("Pens/ET", 8), ("Rest", 96)]
        c3_title, c3_items = "MODEL: ACCURACY", [("Random", 66.7), ("Random Forest", 97.8)]
        c4_title = "GOAL DISTRIBUTION"
        c4_segments, c4_center, c4_sub = [(215, P['gold']), (92, P['blue'])], "307", "total goals"
        c4_legend = [("Group (215)", 215), ("Knockout (92)", 92)]
        bullets = [
            "104 matches mathematically verified against the 12 official group tables",
            "Spain champion: beat Argentina 1-0 in the final (extra time)",
            "Mbappe won the Golden Boot with 10 goals, ahead of Messi (8)",
            "CONMEBOL matches the average stage of confederations with 3x the teams",
            "Biggest blowout of the tournament: Germany 7-1 vs. Curacao",
        ]
        insight_label = "💡 THE MOST SURPRISING FINDING"
        insight_big = "2.99 vs 2.88 goals/match"
        insight_text = "MORE goals were scored in the group stage than in the knockout stage — fear of losing outweighs the drive to score when it's win-or-go-home."
        cta = "Interactive demo + full code →"
        cta2 = "link in the post · ES / EN"

    W, H = 1080, 1400
    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">
<defs><linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="{P['gold']}"/><stop offset="100%" stop-color="{P['red']}"/>
</linearGradient></defs>
<rect width="{W}" height="{H}" fill="{P['bg']}"/>
{pitch_background(W, H)}
{trophy_icon(W-125, 42, 100, P['gold'])}

<text x="80" y="90" font-size="20" font-weight="bold" letter-spacing="1.8" fill="{P['gold']}">{subtitle}</text>
<text x="76" y="160" font-size="62" font-weight="bold" fill="{P['text']}">{title1}</text>
<text x="76" y="226" font-size="62" font-weight="bold" fill="url(#titleGrad)">{title2}</text>

<rect x="80" y="254" width="205" height="6" fill="{P['red']}"/>
<rect x="291" y="254" width="205" height="6" fill="{P['green']}"/>
<rect x="502" y="254" width="205" height="6" fill="{P['blue']}"/>
<rect x="713" y="254" width="127" height="6" fill="{P['gold']}"/>
'''

    # ============ GRID 2x2 DE MINI-GRAFICOS ============
    grid_y = 290
    col_w = (W - 160 - 30) / 2   # dos columnas con gap de 30
    col1_x, col2_x = 80, 80 + col_w + 30
    row1_h = 210

    # -- celda 1: barras confederaciones --
    svg += f'<text x="{col1_x}" y="{grid_y}" font-size="14.5" font-weight="bold" letter-spacing="1" fill="{P["gold"]}">{c1_title}</text>'
    bars1, _ = mini_hbar(col1_x, grid_y+18, col_w, c1_items, 42, [P['blue'],P['red'],P['gold'],P['green']])
    svg += bars1

    # -- celda 2: donut penales/TE --
    svg += f'<text x="{col2_x}" y="{grid_y}" font-size="14.5" font-weight="bold" letter-spacing="1" fill="{P["gold"]}">{c2_title}</text>'
    donut_cx = col2_x + 68
    donut_cy = grid_y + 90
    svg += donut(donut_cx, donut_cy, 58, 18, c2_segments, c2_center, c2_sub)
    lx = col2_x + 150
    svg += f'<circle cx="{lx+5}" cy="{donut_cy-22}" r="5" fill="{P["red"]}"/><text x="{lx+16}" y="{donut_cy-18}" font-size="13" fill="{P["text2"]}">{c2_legend[0][0]} ({c2_legend[0][1]})</text>'
    svg += f'<circle cx="{lx+5}" cy="{donut_cy+8}" r="5" fill="{P["card2"]}" stroke="{P["border"]}"/><text x="{lx+16}" y="{donut_cy+12}" font-size="13" fill="{P["text2"]}">{c2_legend[1][0]} ({c2_legend[1][1]})</text>'

    row2_y = grid_y + row1_h
    # -- celda 3: barras modelo --
    svg += f'<text x="{col1_x}" y="{row2_y}" font-size="14.5" font-weight="bold" letter-spacing="1" fill="{P["gold"]}">{c3_title}</text>'
    bars2, _ = mini_hbar(col1_x, row2_y+18, col_w, c3_items, 100, [P['muted'],P['green']], value_fmt="{:.1f}%")
    svg += bars2

    # -- celda 4: donut goles --
    svg += f'<text x="{col2_x}" y="{row2_y}" font-size="14.5" font-weight="bold" letter-spacing="1" fill="{P["gold"]}">{c4_title}</text>'
    donut2_cx, donut2_cy = col2_x + 68, row2_y + 90
    svg += donut(donut2_cx, donut2_cy, 58, 18, c4_segments, c4_center, c4_sub)
    lx2 = col2_x + 150
    svg += f'<circle cx="{lx2+5}" cy="{donut2_cy-22}" r="5" fill="{P["gold"]}"/><text x="{lx2+16}" y="{donut2_cy-18}" font-size="13" fill="{P["text2"]}">{c4_legend[0][0]}</text>'
    svg += f'<circle cx="{lx2+5}" cy="{donut2_cy+8}" r="5" fill="{P["blue"]}"/><text x="{lx2+16}" y="{donut2_cy+12}" font-size="13" fill="{P["text2"]}">{c4_legend[1][0]}</text>'

    grid_end = row2_y + row1_h - 20

    # ============ INSIGHT — maximo contraste, fondo solido dorado ============
    insight_y = grid_end + 24
    insight_wrapped = textwrap.wrap(insight_text, width=58)
    insight_h = 128 + len(insight_wrapped)*26
    svg += f'''
<rect x="80" y="{insight_y}" width="{W-160}" height="{insight_h}" rx="14" fill="{P['gold']}"/>
<text x="115" y="{insight_y+42}" font-size="19" font-weight="bold" letter-spacing="0.5" fill="{P['dark']}">{insight_label}</text>
<text x="115" y="{insight_y+92}" font-family="DejaVu Sans Mono" font-size="38" font-weight="bold" fill="{P['dark']}">{insight_big}</text>
'''
    insight_text_y = insight_y + 128
    insight_lines = "".join(f'<tspan x="115" dy="{0 if j==0 else 26}">{ln}</tspan>' for j, ln in enumerate(insight_wrapped))
    svg += f'<text x="115" y="{insight_text_y}" font-size="18" fill="#2a3a1f">{insight_lines}</text>'

    # ============ BULLETS (5, una linea cada uno) ============
    by0 = insight_y + insight_h + 30
    row_h = 46
    for i, bullet in enumerate(bullets):
        by = by0 + i*row_h
        svg += soccer_ball(100, by, 16)
        svg += f'<text x="132" y="{by+6}" font-size="18.5" fill="{P["text"]}">{bullet}</text>'

    bullets_end = by0 + len(bullets)*row_h

    # ============ FOOTER ============
    footer_y = bullets_end + 20
    svg += f'''
<text x="80" y="{footer_y+16}" font-family="DejaVu Sans Mono" font-size="16" fill="{P['muted']}">Python · scikit-learn · SQL · SQLite · Chart.js</text>
<rect x="80" y="{footer_y+36}" width="{W-160}" height="66" rx="12" fill="{P['card2']}" stroke="{P['border']}"/>
<text x="{W/2}" y="{footer_y+70}" font-size="21" font-weight="bold" fill="{P['text']}" text-anchor="middle">{cta}</text>
<text x="{W/2}" y="{footer_y+91}" font-family="DejaVu Sans Mono" font-size="14" fill="{P['gold']}" text-anchor="middle">{cta2}</text>
</svg>'''
    return svg, footer_y + 36 + 66, H

OUT = "/home/claude/worldcup_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)
for lang in ["es", "en"]:
    svg_code, bottom, H = build_svg(lang)
    print(f"{lang}: contenido termina en y={bottom:.0f} (canvas={H}) — margen={H-bottom:.0f}px")
    svg_path = f"{OUT}/linkedin_card_{lang}.svg"
    png_path = f"{OUT}/linkedin_card_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1080, output_height=H)
    print(f"Generado: {png_path}")
