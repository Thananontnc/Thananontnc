"""Generate an animated terminal SVG for the GitHub profile README."""
import base64, html, sys

repo = sys.argv[1]
img_b64 = base64.b64encode(open(f"{repo}/hero-terminal.png", "rb").read()).decode()

W, LH = 860, 24
C = dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#c9d1d9", muted="#8b949e",
         green="#7ee787", blue="#79c0ff", purple="#d2a8ff", orange="#ffa657")
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

css, body = [], []
n = 0

def esc(s): return html.escape(s, quote=False)

def prompt(y, cmd, t, dur=None):
    """Prompt line; the command types out starting at t."""
    global n
    n += 1
    dur = dur or max(0.35, len(cmd) * 0.06)
    body.append(f'<g class="f" style="animation-delay:{t:.2f}s">'
                f'<text x="28" y="{y}"><tspan fill="{C["green"]}">pie@github</tspan>'
                f'<tspan fill="{C["blue"]}"> ~</tspan><tspan fill="{C["text"]}"> %</tspan></text></g>')
    body.append(f'<text x="160" y="{y}" fill="{C["text"]}" class="ty{n}">{esc(cmd)}</text>')
    css.append(f'.ty{n}{{clip-path:inset(0 100% 0 0);animation:type {dur:.2f}s steps({len(cmd)}) {t+0.25:.2f}s forwards}}')
    return t + 0.25 + dur

def show(svg, t):
    body.append(f'<g class="f" style="animation-delay:{t:.2f}s">{svg}</g>')

t, y = 0.3, 70
t = prompt(y, "whoami", t)
y += LH
show(f'<text x="28" y="{y}" fill="{C["text"]}">Thananon <tspan fill="{C["orange"]}">"Pie"</tspan> Chounudom'
     f'<tspan fill="{C["muted"]}">  ·  I build data pipelines, ML models and the apps on top</tspan></text>', t + 0.15)
t += 0.6
y += LH + 14
t = prompt(y, "neofetch", t)
t += 0.15

# neofetch block: portrait left, info right
top = y + 18
show(f'<image x="28" y="{top}" width="168" height="210" href="data:image/png;base64,{img_b64}" '
     f'preserveAspectRatio="xMidYMid slice"/>', t)
info_x, key_w = 228, 84
import json
ICONS = json.load(open(f"{repo}/icons.json"))

def icon_color(hexcode):
    r, g, b = (int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5))
    # dark brand colors vanish on the dark terminal; draw them light instead
    return C["text"] if 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.3 else hexcode

def icons_row(x, y, slugs, size=20, gap=14):
    parts = []
    for slug in slugs:
        ic = ICONS[slug]
        parts.append(f'<g transform="translate({x},{y - size + 4}) scale({size / 24})">'
                     f'<title>{ic["title"]}</title><path d="{ic["path"]}" fill="{icon_color(ic["hex"])}"/></g>')
        x += size + gap
    return "".join(parts), x

rows = [
    ("role", "Data Engineer · Bangkok, TH"),
    ("data", ["python", "apacheairflow", "apachespark", "pandas", "postgresql"]),
    ("ml", (["jupyter", "r"], "prediction models · LLM apps")),
    ("web", ["nextdotjs", "react", "typescript", "nodedotjs"]),
    ("cloud", ["googlecloud", "amazonaws", "vercel", "supabase"]),
    ("also", ["swift", "openjdk", "go", "c", "espressif"]),
    ("now", "Portfolio Analytics Pipeline"),
]
ry = top + 16
show(f'<text x="{info_x}" y="{ry}"><tspan fill="{C["green"]}" font-weight="700">pie</tspan>'
     f'<tspan fill="{C["text"]}">@</tspan><tspan fill="{C["green"]}" font-weight="700">github</tspan></text>'
     f'<text x="{info_x}" y="{ry + 20}" fill="{C["border"]}">──────────────────────────────</text>', t)
ry += 20
for k, v in rows:
    ry += 24
    t += 0.09
    key = f'<text x="{info_x}" y="{ry}" fill="{C["purple"]}" font-weight="700">{k}</text>'
    vx = info_x + key_w
    if isinstance(v, str):
        val = f'<text x="{vx}" y="{ry}" fill="{C["text"]}">{esc(v)}</text>'
    else:
        slugs, extra = v if isinstance(v, tuple) else (v, "")
        val, end = icons_row(vx, ry, slugs)
        if extra:
            val += f'<text x="{end + 4}" y="{ry}" fill="{C["muted"]}">{esc(extra)}</text>'
    show(key + val, t)
ry += 18
t += 0.09
palette = ["#484f58", "#ff7b72", "#7ee787", "#d29922", "#79c0ff", "#d2a8ff", "#56d4dd", "#e6edf3"]
show("".join(f'<rect x="{info_x + i*26}" y="{ry}" width="22" height="12" rx="2" fill="{c}"/>'
             for i, c in enumerate(palette)), t)

y = max(top + 210, ry + 12) + 36
t += 0.5
t = prompt(y, "ls ~/projects", t)
projects = [
    ("data", C["green"],  "superstore-etl-airflow-gcp"),
    ("data", C["green"],  "real-estate-etl-airflow-gcp"),
    ("data", C["green"],  "ecommerce-transaction-etl"),
    ("ai",   C["purple"], "llm-resume-analyzer"),
    ("ml",   C["purple"], "bank-churn-prediction"),
    ("web",  C["blue"],   "simba-spark"),
    ("web",  C["blue"],   "apartment-management"),
    ("iot",  C["orange"], "esp32-homelab-monitor"),
]
t += 0.15
for i, (tag, col, name) in enumerate(projects):
    cx = 28 + (i % 2) * 420
    if i % 2 == 0:
        y += LH
    show(f'<text x="{cx}" y="{y}"><tspan fill="{col}">[{tag:<4}]</tspan>'
         f'<tspan fill="{C["text"]}" x="{cx + 70}">{esc(name)}/</tspan></text>', t)
    t += 0.07
y += LH + 14
t += 0.4
t = prompt(y, "cat contact.txt", t)
y += LH
show(f'<text x="28" y="{y}"><tspan fill="{C["muted"]}">web   </tspan><tspan fill="{C["blue"]}">thananon.dev</tspan>'
     f'<tspan fill="{C["muted"]}">          mail  </tspan><tspan fill="{C["blue"]}">chounudomthananon@gmail.com</tspan></text>', t + 0.15)
t += 0.6
y += LH + 14
show(f'<text x="28" y="{y}"><tspan fill="{C["green"]}">pie@github</tspan>'
     f'<tspan fill="{C["blue"]}"> ~</tspan><tspan fill="{C["text"]}"> %</tspan></text>'
     f'<rect class="cur" x="160" y="{y - 14}" width="9" height="18" fill="{C["text"]}"/>', t)

H = y + 28
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thananon Chounudom - Data Engineer terminal profile">
<style>
text{{font-family:{FONT};font-size:14px;white-space:pre}}
.f{{opacity:0;animation:fade .01s linear forwards}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes type{{to{{clip-path:inset(0 0 0 0)}}}}
@keyframes blink{{50%{{opacity:0}}}}
{chr(10).join(css)}
</style>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{C["bg"]}" stroke="{C["border"]}"/>
<path d="M0.5 36V10.5a10 10 0 0 1 10-10h{W-21}a10 10 0 0 1 10 10V36z" fill="{C["bar"]}"/>
<line x1="0" y1="36" x2="{W}" y2="36" stroke="{C["border"]}"/>
<circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>
<text x="{W/2}" y="23" text-anchor="middle" fill="{C["muted"]}" style="font-size:13px">pie@github: ~ — zsh</text>
{chr(10).join(body)}
</svg>'''
open(f"{repo}/terminal.svg", "w").write(svg)
print(W, H, round(t, 2), len(svg))
