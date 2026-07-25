"""
Genera un grafico de resumen (1080x1350, formato 4:5 vertical) en ES y EN,
con la identidad visual del dashboard del Mundial (cancha nocturna + dorado).
"""
import cairosvg

P = {
    "bg": "#0e2919", "bg2": "#153524", "card": "#1b422e", "border": "#2c5b41",
    "text": "#F2EFE3", "text2": "#A7C4AE", "muted": "#6E8F77",
    "gold": "#E0B23D", "red": "#C4453F", "blue": "#3E90B0", "violet": "#9B7FC4", "lime": "#9BC24A",
}

def build_svg(lang):
    if lang == "es":
        title1, title2 = "Radiografía", "de un Mundial"
        subtitle = "PORTAFOLIO DE DATA SCIENCE · FÚTBOL"
        stats = [
            ("104", "partidos analizados y\nverificados manualmente"),
            ("97.8%", "accuracy prediciendo avance\n(vs. 66.7% del azar)"),
            ("20", "goleadores y equipos en\nrankings con IA"),
        ]
        cta = "Demo interactivo + código completo →"
        cta2 = "link en el post · ES / EN"
    else:
        title1, title2 = "Anatomy of", "a World Cup"
        subtitle = "DATA SCIENCE PORTFOLIO · SOCCER"
        stats = [
            ("104", "matches analyzed and\nmanually verified"),
            ("97.8%", "accuracy predicting advancement\n(vs. 66.7% baseline)"),
            ("20", "scorers and teams in\nAI-powered rankings"),
        ]
        cta = "Interactive demo + full code →"
        cta2 = "link in the post · ES / EN"

    W, H = 1080, 1350
    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{P['gold']}"/>
    <stop offset="100%" stop-color="{P['red']}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{P['bg']}"/>

<!-- pitch arc motif (mismo elemento del dashboard) -->
<circle cx="{W-40}" cy="40" r="210" fill="none" stroke="rgba(242,239,227,0.06)" stroke-width="2"/>
<circle cx="{W-40}" cy="40" r="150" fill="none" stroke="rgba(242,239,227,0.05)" stroke-width="2"/>

<text x="80" y="95" font-family="DejaVu Sans" font-size="24" font-weight="bold" letter-spacing="2.5" fill="{P['gold']}">{subtitle}</text>

<text x="76" y="185" font-family="DejaVu Sans" font-size="82" font-weight="bold" fill="{P['text']}">{title1}</text>
<text x="76" y="270" font-family="DejaVu Sans" font-size="82" font-weight="bold" fill="url(#titleGrad)">{title2}</text>

<!-- scoreboard strip, como el hero del dashboard -->
<g transform="translate(80,330)">
'''
    cell_w = (W - 160) / 4
    cell_labels = [("48", "TEAMS" if lang == "en" else "EQUIPOS"), ("12", "GROUPS" if lang == "en" else "GRUPOS"),
                   ("3", "HOSTS" if lang == "en" else "SEDES"), ("🇪🇸", "CHAMPION" if lang == "en" else "CAMPEÓN")]
    for i, (num, lbl) in enumerate(cell_labels):
        x = i * cell_w
        svg += f'''
  <rect x="{x}" y="0" width="{cell_w-2}" height="90" fill="{P['card']}" stroke="{P['border']}"/>
  <text x="{x+cell_w/2}" y="45" font-family="DejaVu Sans Mono" font-size="28" font-weight="bold" fill="{P['gold']}" text-anchor="middle">{num}</text>
  <text x="{x+cell_w/2}" y="70" font-family="DejaVu Sans" font-size="12" fill="{P['text2']}" text-anchor="middle" letter-spacing="1">{lbl}</text>
'''
    svg += "</g>\n"

    y0 = 470
    block_h = 175
    for i, (num, label) in enumerate(stats):
        by = y0 + i * block_h
        color = [P['gold'], P['red'], P['blue']][i]
        lines = label.split("\n")
        label_svg = "".join(
            f'<tspan x="440" dy="{0 if j==0 else 32}">{ln}</tspan>' for j, ln in enumerate(lines)
        )
        svg += f'''
<rect x="80" y="{by}" width="8" height="130" rx="4" fill="{color}"/>
<text x="115" y="{by+90}" font-family="DejaVu Sans Mono" font-size="60" font-weight="bold" fill="{P['text']}">{num}</text>
<text x="440" y="{by+30}" font-family="DejaVu Sans" font-size="26" fill="{P['text2']}">{label_svg}</text>
'''

    footer_y = y0 + len(stats) * block_h + 10
    svg += f'''
<rect x="80" y="{footer_y}" width="{W-160}" height="1" fill="{P['border']}"/>
<text x="80" y="{footer_y+55}" font-family="DejaVu Sans Mono" font-size="21" fill="{P['muted']}">Python · scikit-learn · SQL · SQLite · Chart.js</text>

<rect x="80" y="{footer_y+90}" width="{W-160}" height="80" rx="12" fill="{P['card']}" stroke="{P['border']}"/>
<text x="{W/2}" y="{footer_y+135}" font-family="DejaVu Sans" font-size="28" font-weight="bold" fill="{P['text']}" text-anchor="middle">{cta}</text>
<text x="{W/2}" y="{footer_y+162}" font-family="DejaVu Sans Mono" font-size="18" fill="{P['gold']}" text-anchor="middle">{cta2}</text>
</svg>'''
    return svg

for lang in ["es", "en"]:
    svg_code = build_svg(lang)
    svg_path = f"/home/claude/worldcup_portfolio/assets_linkedin/linkedin_card_{lang}.svg"
    png_path = f"/home/claude/worldcup_portfolio/assets_linkedin/linkedin_card_{lang}.png"
    import os
    os.makedirs("/home/claude/worldcup_portfolio/assets_linkedin", exist_ok=True)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1080, output_height=1350)
    print(f"Generado: {png_path}")
