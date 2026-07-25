"""
Grafico de resumen para LinkedIn v3:
- Paleta oficial del torneo: rojo (Canada), verde (Mexico), azul (USA) + dorado (trofeo)
  (verificado: la pelota oficial Adidas Trionda y el sistema de marca usan estos 3 colores
  para representar a las 3 sedes; ver README para la fuente)
- Icono de trofeo generico (no la copia exacta del trofeo FIFA, que es una marca registrada)
- 2 mini-graficos de barras dibujados a mano en SVG (sin libreria de charts)
- Bullets cortos + insight destacado
"""
import cairosvg
import os
import math
import textwrap

P = {
    "bg": "#0e2919", "card": "#153524", "card2": "#1b422e", "border": "#2c5b41",
    "text": "#F2EFE3", "text2": "#A7C4AE", "muted": "#6E8F77",
    "gold": "#E0B23D",      # trofeo / emblema
    "red": "#D6483F",       # Canada
    "green": "#3FA65C",     # Mexico
    "blue": "#3E7FC4",      # USA
}

def soccer_ball(cx, cy, r, fill="#F2EFE3", accent="#0e2919"):
    pent_r = r * 0.42
    pent_pts = []
    for i in range(5):
        ang = math.radians(-90 + i * 72)
        pent_pts.append((cx + pent_r * math.cos(ang), cy + pent_r * math.sin(ang)))
    pent_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pent_pts) + " Z"
    wedges = ""
    for i in range(5):
        a1 = math.radians(-90 + i * 72 - 36)
        a2 = math.radians(-90 + i * 72 + 36)
        p1 = pent_pts[i]
        o1 = (cx + r * 0.92 * math.cos(a1), cy + r * 0.92 * math.sin(a1))
        o2 = (cx + r * 0.92 * math.cos(a2), cy + r * 0.92 * math.sin(a2))
        wedges += (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{o1[0]:.1f},{o1[1]:.1f} '
                   f'A{r*0.92:.1f},{r*0.92:.1f} 0 0,1 {o2[0]:.1f},{o2[1]:.1f} Z" fill="{accent}" opacity="0.85"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>{wedges}'
            f'<path d="{pent_path}" fill="{accent}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="{r*0.06}"/>')

def trophy_icon(cx, top_y, w, color):
    """Trofeo generico (copa + asas + base) - no replica el diseno especifico
    de la copa oficial FIFA, que esta protegido por marca registrada."""
    bowl_w = w
    bowl_h = w * 0.85
    stem_w = w * 0.16
    stem_h = w * 0.42
    base_w = w * 0.62
    base_h = w * 0.14
    x0 = cx - bowl_w/2
    y0 = top_y
    handle_r = bowl_w * 0.32
    return f'''
<g fill="{color}">
  <path d="M {x0} {y0}
           Q {x0} {y0+bowl_h*0.75} {cx} {y0+bowl_h}
           Q {cx+bowl_w/2} {y0+bowl_h*0.75} {cx+bowl_w/2} {y0}
           Z"/>
  <circle cx="{x0-handle_r*0.35}" cy="{y0+bowl_h*0.32}" r="{handle_r}" fill="none" stroke="{color}" stroke-width="{w*0.09}"/>
  <circle cx="{cx+bowl_w/2+handle_r*0.35}" cy="{y0+bowl_h*0.32}" r="{handle_r}" fill="none" stroke="{color}" stroke-width="{w*0.09}"/>
  <rect x="{cx-stem_w/2}" y="{y0+bowl_h}" width="{stem_w}" height="{stem_h}"/>
  <polygon points="{cx-base_w/2},{y0+bowl_h+stem_h+base_h} {cx+base_w/2},{y0+bowl_h+stem_h+base_h} {cx+base_w*0.38},{y0+bowl_h+stem_h} {cx-base_w*0.38},{y0+bowl_h+stem_h}"/>
  <circle cx="{cx}" cy="{y0+bowl_h*0.42}" r="{bowl_w*0.1}" fill="{P['bg']}" opacity="0.35"/>
</g>
'''

def hbar_chart(x, y, w, items, max_val, colors, value_fmt="{:.0f}"):
    """items: [(label, value), ...] — grafico de barras horizontales dibujado a mano."""
    bar_h = 26
    gap = 16
    svg = ""
    for i, (label, val) in enumerate(items):
        by = y + i * (bar_h + gap)
        bar_w = max(6, (val / max_val) * (w - 210))
        color = colors[i % len(colors)]
        svg += f'<text x="{x}" y="{by+bar_h*0.72}" font-size="19" fill="{P["text2"]}">{label}</text>'
        svg += f'<rect x="{x+150}" y="{by}" width="{w-150-60}" height="{bar_h}" rx="4" fill="{P["bg"]}"/>'
        svg += f'<rect x="{x+150}" y="{by}" width="{bar_w}" height="{bar_h}" rx="4" fill="{color}"/>'
        svg += f'<text x="{x+150+ (w-150-60) +8}" y="{by+bar_h*0.72}" font-family="DejaVu Sans Mono" font-size="17" font-weight="bold" fill="{P["text"]}">{value_fmt.format(val)}</text>'
    return svg, y + len(items) * (bar_h + gap)

def pitch_background(W, H):
    mid_y = H * 0.40
    return f'''
<g stroke="rgba(242,239,227,0.06)" stroke-width="2.5" fill="none">
  <rect x="40" y="40" width="{W-80}" height="{H-80}" rx="4"/>
  <line x1="40" y1="{mid_y}" x2="{W-40}" y2="{mid_y}"/>
  <circle cx="{W/2}" cy="{mid_y}" r="130"/>
  <path d="M 40 100 A 60 60 0 0 0 100 40"/>
  <path d="M {W-100} 40 A 60 60 0 0 0 {W-40} 100"/>
  <path d="M 40 {H-100} A 60 60 0 0 1 100 {H-40}"/>
  <path d="M {W-100} {H-40} A 60 60 0 0 1 {W-40} {H-100}"/>
</g>
'''

def build_svg(lang):
    if lang == "es":
        title1, title2 = "Radiografía", "de un Mundial"
        subtitle = "PORTAFOLIO DE DATA SCIENCE · FÚTBOL"
        chart1_title = "VICTORIAS POR CONFEDERACIÓN"
        chart1_items = [("UEFA", 42), ("CONMEBOL", 15), ("CAF", 11), ("CONCACAF", 9)]
        chart2_title = "MODELO PREDICTIVO: ACCURACY"
        chart2_items = [("Azar (baseline)", 66.7), ("Random Forest", 97.8)]
        bullets = [
            "104 partidos verificados matemáticamente contra las 12 tablas oficiales de grupo",
            "8 de 104 partidos (7.7%) se definieron por penales o tiempo extra",
        ]
        insight_label = "INSIGHT"
        insight_text = "Se anotaron más goles en fase de grupos (2.99/partido) que en eliminación directa (2.88) — el miedo a perder pesa más que las ganas de anotar cuando es todo o nada."
        cta = "Demo interactivo + código completo →"
        cta2 = "link en el post · ES / EN"
    else:
        title1, title2 = "Anatomy of", "a World Cup"
        subtitle = "DATA SCIENCE PORTFOLIO · SOCCER"
        chart1_title = "WINS BY CONFEDERATION"
        chart1_items = [("UEFA", 42), ("CONMEBOL", 15), ("CAF", 11), ("CONCACAF", 9)]
        chart2_title = "PREDICTIVE MODEL: ACCURACY"
        chart2_items = [("Random baseline", 66.7), ("Random Forest", 97.8)]
        bullets = [
            "104 matches mathematically verified against the 12 official group tables",
            "8 of 104 matches (7.7%) were decided by penalties or extra time",
        ]
        insight_label = "INSIGHT"
        insight_text = "More goals were scored in the group stage (2.99/match) than in the knockout stage (2.88) — fear of losing outweighs the drive to score when it's win-or-go-home."
        cta = "Interactive demo + full code →"
        cta2 = "link in the post · ES / EN"

    W, H = 1080, 1350
    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">
<defs>
  <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{P['gold']}"/>
    <stop offset="100%" stop-color="{P['red']}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{P['bg']}"/>
{pitch_background(W, H)}
{trophy_icon(W-140, 50, 120, P['gold'])}

<text x="80" y="98" font-size="22" font-weight="bold" letter-spacing="2" fill="{P['gold']}">{subtitle}</text>
<text x="76" y="178" font-size="72" font-weight="bold" fill="{P['text']}">{title1}</text>
<text x="76" y="255" font-size="72" font-weight="bold" fill="url(#titleGrad)">{title2}</text>

<!-- franja de color de las 3 sedes + dorado del trofeo -->
<rect x="80" y="288" width="220" height="7" fill="{P['red']}"/>
<rect x="304" y="288" width="220" height="7" fill="{P['green']}"/>
<rect x="528" y="288" width="220" height="7" fill="{P['blue']}"/>
<rect x="752" y="288" width="168" height="7" fill="{P['gold']}"/>
'''

    # --- chart 1: confederaciones ---
    chart_y = 330
    svg += f'<text x="80" y="{chart_y}" font-size="17" font-weight="bold" letter-spacing="1.2" fill="{P["gold"]}">{chart1_title}</text>'
    bars_svg, chart1_end = hbar_chart(80, chart_y+22, W-160, chart1_items, 42, [P['blue'],P['red'],P['gold'],P['green']])
    svg += bars_svg

    # --- chart 2: accuracy modelo ---
    chart2_y = chart1_end + 46
    svg += f'<text x="80" y="{chart2_y}" font-size="17" font-weight="bold" letter-spacing="1.2" fill="{P["gold"]}">{chart2_title}</text>'
    bars_svg2, chart2_end = hbar_chart(80, chart2_y+22, W-160, chart2_items, 100, [P['muted'],P['green']], value_fmt="{:.1f}%")
    svg += bars_svg2

    # --- bullets ---
    by0 = chart2_end + 40
    row_h = 92
    for i, bullet in enumerate(bullets):
        by = by0 + i * row_h
        svg += soccer_ball(112, by + 6, 22)
        wrapped = textwrap.wrap(bullet, width=52)
        lines_svg = "".join(f'<tspan x="158" dy="{0 if j==0 else 27}">{ln}</tspan>' for j, ln in enumerate(wrapped))
        svg += f'<text x="158" y="{by-2}" font-size="21" fill="{P["text"]}">{lines_svg}</text>'

    # --- insight ---
    insight_y = by0 + len(bullets) * row_h + 6
    insight_wrapped = textwrap.wrap(insight_text, width=64)
    insight_h = 62 + len(insight_wrapped) * 25
    insight_lines = "".join(f'<tspan x="118" dy="{0 if j==0 else 25}">{ln}</tspan>' for j, ln in enumerate(insight_wrapped))
    svg += f'''
<rect x="80" y="{insight_y}" width="{W-160}" height="{insight_h}" rx="10" fill="{P['card2']}" stroke="{P['gold']}" stroke-width="1.5"/>
{soccer_ball(118, insight_y+38, 18, fill=P['gold'], accent=P['bg'])}
<text x="150" y="{insight_y+32}" font-size="15" font-weight="bold" letter-spacing="1.4" fill="{P['gold']}">{insight_label}</text>
<text x="118" y="{insight_y+62}" font-size="19" fill="{P['text2']}">{insight_lines}</text>
'''

    footer_y = insight_y + insight_h + 22
    svg += f'''
<text x="80" y="{footer_y+16}" font-family="DejaVu Sans Mono" font-size="17" fill="{P['muted']}">Python · scikit-learn · SQL · SQLite · Chart.js</text>
<rect x="80" y="{footer_y+38}" width="{W-160}" height="70" rx="12" fill="{P['card2']}" stroke="{P['border']}"/>
<text x="{W/2}" y="{footer_y+76}" font-size="23" font-weight="bold" fill="{P['text']}" text-anchor="middle">{cta}</text>
<text x="{W/2}" y="{footer_y+99}" font-family="DejaVu Sans Mono" font-size="15" fill="{P['gold']}" text-anchor="middle">{cta2}</text>
</svg>'''
    return svg, footer_y + 38 + 70

OUT = "/home/claude/worldcup_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)
for lang in ["es", "en"]:
    svg_code, bottom = build_svg(lang)
    print(f"{lang}: contenido termina en y={bottom:.0f} (canvas=1350)")
    svg_path = f"{OUT}/linkedin_card_{lang}.svg"
    png_path = f"{OUT}/linkedin_card_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1080, output_height=1350)
    print(f"Generado: {png_path}")
