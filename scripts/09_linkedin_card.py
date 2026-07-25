"""
Grafico de resumen para LinkedIn v2 — con tematica de futbol mas fuerte:
- Fondo con lineas de cancha (circulo central, banda de medio campo, areas)
- Balones de futbol (dibujados en SVG, no emoji) como vinetas de cada bullet
- Bullets con los hallazgos reales del analisis + un insight destacado
"""
import cairosvg
import os
import math
import textwrap

P = {
    "bg": "#0e2919", "bg2": "#153524", "card": "#1b422e", "border": "#2c5b41",
    "text": "#F2EFE3", "text2": "#A7C4AE", "muted": "#6E8F77",
    "gold": "#E0B23D", "red": "#C4453F", "blue": "#3E90B0", "violet": "#9B7FC4", "lime": "#9BC24A",
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
        outer1 = (cx + r * 0.92 * math.cos(a1), cy + r * 0.92 * math.sin(a1))
        outer2 = (cx + r * 0.92 * math.cos(a2), cy + r * 0.92 * math.sin(a2))
        wedges += (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{outer1[0]:.1f},{outer1[1]:.1f} '
                   f'A{r*0.92:.1f},{r*0.92:.1f} 0 0,1 {outer2[0]:.1f},{outer2[1]:.1f} Z" '
                   f'fill="{accent}" opacity="0.85"/>')

    return f'''
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>
{wedges}
<path d="{pent_path}" fill="{accent}"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="{r*0.06}"/>
'''

def pitch_background(W, H):
    mid_y = H * 0.40
    return f'''
<g stroke="rgba(242,239,227,0.07)" stroke-width="2.5" fill="none">
  <rect x="40" y="40" width="{W-80}" height="{H-80}" rx="4"/>
  <line x1="40" y1="{mid_y}" x2="{W-40}" y2="{mid_y}"/>
  <circle cx="{W/2}" cy="{mid_y}" r="130"/>
  <circle cx="{W/2}" cy="{mid_y}" r="4" fill="rgba(242,239,227,0.10)"/>
  <rect x="{W/2-220}" y="40" width="440" height="130"/>
  <rect x="{W/2-120}" y="40" width="240" height="55"/>
  <rect x="{W/2-220}" y="{H-170}" width="440" height="130"/>
  <rect x="{W/2-120}" y="{H-95}" width="240" height="55"/>
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
        bullets = [
            "104 partidos analizados y verificados matemáticamente contra las 12 tablas oficiales de grupo",
            "CONMEBOL: con solo 6 selecciones, alcanzó en promedio la misma etapa que confederaciones con el triple de equipos",
            "8 de 104 partidos (7.7%) se definieron por penales o tiempo extra",
            "Modelo predictivo con 97.8% de accuracy anticipando el avance a octavos (vs. 66.7% del azar)",
        ]
        insight_label = "INSIGHT"
        insight_text = "Se anotaron más goles en fase de grupos (2.99/partido) que en eliminación directa (2.88) — el miedo a perder pesa más que las ganas de anotar cuando es todo o nada."
        cta = "Demo interactivo + código completo →"
        cta2 = "link en el post · ES / EN"
    else:
        title1, title2 = "Anatomy of", "a World Cup"
        subtitle = "DATA SCIENCE PORTFOLIO · SOCCER"
        bullets = [
            "104 matches analyzed and mathematically verified against the 12 official group tables",
            "CONMEBOL: with only 6 teams, reached the same average stage as confederations with three times as many",
            "8 of 104 matches (7.7%) were decided by penalties or extra time",
            "Predictive model with 97.8% accuracy forecasting advancement to the round of 16 (vs. 66.7% baseline)",
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

<text x="80" y="98" font-size="23" font-weight="bold" letter-spacing="2.2" fill="{P['gold']}">{subtitle}</text>
<text x="76" y="182" font-size="76" font-weight="bold" fill="{P['text']}">{title1}</text>
<text x="76" y="262" font-size="76" font-weight="bold" fill="url(#titleGrad)">{title2}</text>
'''

    by0 = 340
    row_h = 128
    for i, bullet in enumerate(bullets):
        by = by0 + i * row_h
        svg += soccer_ball(115, by + 8, 26)
        wrapped = textwrap.wrap(bullet, width=48)
        lines_svg = "".join(f'<tspan x="168" dy="{0 if j==0 else 30}">{ln}</tspan>' for j, ln in enumerate(wrapped))
        svg += f'<text x="168" y="{by-6}" font-size="24" fill="{P["text"]}">{lines_svg}</text>\n'

    insight_y = by0 + len(bullets) * row_h + 10
    insight_wrapped = textwrap.wrap(insight_text, width=62)
    insight_h = 70 + len(insight_wrapped) * 27
    insight_lines_svg = "".join(
        f'<tspan x="120" dy="{0 if j==0 else 27}">{ln}</tspan>' for j, ln in enumerate(insight_wrapped))
    svg += f'''
<rect x="80" y="{insight_y}" width="{W-160}" height="{insight_h}" rx="10" fill="{P['card']}" stroke="{P['gold']}" stroke-width="1.5"/>
{soccer_ball(120, insight_y+42, 20, fill=P['gold'], accent=P['bg'])}
<text x="160" y="{insight_y+35}" font-size="16" font-weight="bold" letter-spacing="1.5" fill="{P['gold']}">{insight_label}</text>
<text x="120" y="{insight_y+68}" font-size="21" fill="{P['text2']}">{insight_lines_svg}</text>
'''

    footer_y = insight_y + insight_h + 26
    svg += f'''
<text x="80" y="{footer_y+18}" font-family="DejaVu Sans Mono" font-size="19" fill="{P['muted']}">Python · scikit-learn · SQL · SQLite · Chart.js</text>
<rect x="80" y="{footer_y+42}" width="{W-160}" height="76" rx="12" fill="{P['card']}" stroke="{P['border']}"/>
<text x="{W/2}" y="{footer_y+84}" font-size="25" font-weight="bold" fill="{P['text']}" text-anchor="middle">{cta}</text>
<text x="{W/2}" y="{footer_y+109}" font-family="DejaVu Sans Mono" font-size="16" fill="{P['gold']}" text-anchor="middle">{cta2}</text>
</svg>'''
    return svg, footer_y + 42 + 76

OUT = "/home/claude/worldcup_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)
for lang in ["es", "en"]:
    svg_code, bottom = build_svg(lang)
    print(f"{lang}: contenido termina en y={bottom} (canvas=1350)")
    svg_path = f"{OUT}/linkedin_card_{lang}.svg"
    png_path = f"{OUT}/linkedin_card_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1080, output_height=1350)
    print(f"Generado: {png_path}")
