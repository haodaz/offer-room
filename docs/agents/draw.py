"""Flat illustrated portraits for the six agents (same style as the applicant portraits). Writes <name>.svg here.
They are job archetypes, not real people."""
from pathlib import Path

here = Path(__file__).parent

def face(skin, shade):
    return f'''<path d="M178 330 L178 376 C190 390 210 390 222 376 L222 330Z" fill="{shade}"/>
<ellipse cx="200" cy="262" rx="64" ry="78" fill="{skin}"/>
<ellipse cx="136" cy="268" rx="10" ry="16" fill="{shade}"/><ellipse cx="264" cy="268" rx="10" ry="16" fill="{shade}"/>'''

def eyes(glasses=False, frame="#2b1d17", happy=False):
    e = ('<path d="M166 264 Q176 256 186 264" stroke="#1d1410" stroke-width="5" fill="none" stroke-linecap="round"/>'
         '<path d="M214 264 Q224 256 234 264" stroke="#1d1410" stroke-width="5" fill="none" stroke-linecap="round"/>') if happy else \
        '<circle cx="176" cy="264" r="4.5" fill="#1d1410"/><circle cx="224" cy="264" r="4.5" fill="#1d1410"/>'
    g = (f'<circle cx="176" cy="263" r="18" fill="none" stroke="{frame}" stroke-width="4"/>'
         f'<circle cx="224" cy="263" r="18" fill="none" stroke="{frame}" stroke-width="4"/>'
         f'<path d="M194 261 L206 261" stroke="{frame}" stroke-width="4"/>') if glasses else ""
    return e + g

def brows(c):
    return (f'<path d="M160 236 Q176 230 190 236" stroke="{c}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M210 236 Q224 230 240 236" stroke="{c}" stroke-width="4.5" fill="none" stroke-linecap="round"/>')

def mouth(kind="smile", lip="#5a2f1e"):
    if kind == "grin":
        return '<path d="M180 302 Q200 322 220 302 Z" fill="#7a2e2a"/><path d="M184 304 Q200 311 216 304" stroke="#fff" stroke-width="4" fill="none"/>'
    if kind == "flat":
        return f'<path d="M186 308 Q200 312 214 308" stroke="{lip}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    return f'<path d="M184 304 Q200 316 216 304" stroke="{lip}" stroke-width="4" fill="none" stroke-linecap="round"/>'

def nose(c):
    return f'<path d="M196 282 Q200 290 204 282" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round"/>'

def card(bg, hill, sun, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480">
<defs><clipPath id="c"><rect width="400" height="480" rx="40"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="400" height="480" fill="{bg}"/>
<circle cx="300" cy="110" r="44" fill="{sun}"/>
<path d="M0 320 L90 270 L170 300 L260 250 L400 300 L400 480 L0 480Z" fill="{hill}"/>
{body}</g></svg>'''

P = {}

# scout: the admissions office. Bob with a grey streak, cardigan, lanyard, a wall calendar.
P["scout"] = card("#fde4e4", "#f6c9c9", "#f9b8b8", f'''
<rect x="40" y="70" width="110" height="120" rx="10" fill="#fff"/><rect x="40" y="70" width="110" height="28" rx="10" fill="#e5484d"/>
<g fill="#f2b8b8">{"".join(f'<rect x="{52+i%4*24}" y="{108+i//4*24}" width="16" height="16" rx="3"/>' for i in range(12))}</g>
<rect x="124" y="156" width="16" height="16" rx="3" fill="#e5484d"/>
<path d="M126 210 C122 150 278 150 274 210 L278 330 L122 330Z" fill="#3b2a24"/>
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#8e5bb5"/>
<path d="M172 372 L200 404 L228 372 L228 480 L172 480Z" fill="#f4ecf7"/>
<path d="M176 372 L196 452 M224 372 L204 452" stroke="#1f7ae0" stroke-width="5"/><rect x="186" y="446" width="28" height="34" rx="4" fill="#fff" stroke="#1f7ae0" stroke-width="3"/>
{face("#d9a37e", "#c88f69")}
<path d="M134 250 C134 190 266 190 266 250 C246 214 214 206 170 216 C156 224 142 236 134 250Z" fill="#3b2a24"/>
<path d="M226 200 C246 206 260 222 266 246 C254 230 240 220 224 214Z" fill="#b9aca6"/>
{eyes(glasses=True, frame="#8e5bb5")}{brows("#3b2a24")}{nose("#a9714d")}{mouth()}''')

# mentor: the senior PhD student. Messy short hair, hoodie, coffee cup, laptop stickers.
P["mentor"] = card("#e2f4e6", "#bfe3c7", "#b5dcbf", f'''
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#3f8f5c"/>
<path d="M150 372 C150 410 250 410 250 372" stroke="#2f7049" stroke-width="10" fill="none"/>
<path d="M188 400 L186 446 M212 400 L214 446" stroke="#e7f3ea" stroke-width="5" stroke-linecap="round"/>
<rect x="270" y="388" width="64" height="74" rx="10" fill="#fff"/><rect x="270" y="388" width="64" height="16" rx="6" fill="#6b4a33"/>
<path d="M334 410 C356 410 356 440 334 440" stroke="#fff" stroke-width="8" fill="none"/>
<path d="M290 378 Q296 366 290 354 M306 378 Q312 366 306 354" stroke="#9cc9a9" stroke-width="4" fill="none" stroke-linecap="round"/>
{face("#e8b896", "#d6a27f")}
<path d="M134 248 C128 176 272 170 266 248 C258 222 250 214 238 210 C232 222 214 218 206 206 C196 220 172 222 160 212 C148 222 140 234 134 248Z" fill="#2a2320"/>
{eyes(happy=True)}{brows("#2a2320")}{nose("#b98463")}{mouth("grin")}''')

# critic: the committee reader. Grey hair and beard, half-moon glasses, a stack of files.
P["critic"] = card("#e3ecfb", "#c5d6f3", "#b9cdf0", f'''
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#33415c"/>
<path d="M170 372 L200 430 L230 372" fill="#e9edf5"/><path d="M194 392 L200 440 L206 392Z" fill="#8a2d3b"/>
<g transform="translate(262 392)"><rect width="92" height="16" rx="3" fill="#fff" stroke="#9fb2d6" stroke-width="2"/><rect y="18" width="92" height="16" rx="3" fill="#f3e7c9" stroke="#9fb2d6" stroke-width="2"/><rect y="36" width="92" height="16" rx="3" fill="#fff" stroke="#9fb2d6" stroke-width="2"/><rect y="54" width="92" height="16" rx="3" fill="#dfe8f7" stroke="#9fb2d6" stroke-width="2"/></g>
{face("#f0c9a8", "#ddb08d")}

<path d="M134 254 C130 196 270 196 266 254 C262 226 250 212 236 208 L164 208 C150 214 138 232 134 254Z" fill="#d4d4d4"/>
<path d="M160 270 L192 270 M208 270 L240 270" stroke="#33415c" stroke-width="4" stroke-linecap="round"/>
<circle cx="176" cy="262" r="4" fill="#1d1410"/><circle cx="224" cy="262" r="4" fill="#1d1410"/>
<path d="M142 286 C146 334 172 346 200 346 C228 346 254 334 258 286 C250 312 236 322 222 318 C214 312 186 312 178 318 C164 322 150 312 142 286Z" fill="#bdbdbd"/>
<path d="M178 296 C188 290 212 290 222 296 C214 300 186 300 178 296Z" fill="#a8a8a8"/>
{brows("#9a9a9a")}{nose("#c99573")}<path d="M188 308 Q200 312 212 308" stroke="#7a5a4a" stroke-width="4" fill="none" stroke-linecap="round"/>''')

# writer: the writing-center coach. Curly bun, pen behind the ear, an open notebook.
P["writer"] = card("#fdeedd", "#f8d6b0", "#f6c58f", f'''
<circle cx="200" cy="160" r="34" fill="#4a2c22"/>
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#e2833b"/>
<path d="M168 372 Q200 400 232 372" stroke="#fff3e6" stroke-width="9" fill="none"/>
<g transform="translate(250 384) rotate(-6)"><rect width="104" height="76" rx="6" fill="#fff"/><path d="M52 0 L52 76" stroke="#f0c9a0" stroke-width="3"/>
<path d="M10 18 H44 M10 30 H40 M10 42 H44 M60 18 H94 M60 30 H86" stroke="#c9a27c" stroke-width="3" stroke-linecap="round"/></g>
{face("#a8693f", "#965c37")}
<g fill="#4a2c22"><circle cx="150" cy="214" r="20"/><circle cx="176" cy="198" r="22"/><circle cx="206" cy="194" r="22"/><circle cx="236" cy="204" r="20"/><circle cx="256" cy="226" r="14"/><circle cx="142" cy="236" r="12"/></g>
<rect x="258" y="226" width="7" height="64" rx="3" fill="#2f6fd6" transform="rotate(18 262 258)"/>
{eyes()}{brows("#4a2c22")}{nose("#7a4527")}{mouth()}''')

# funder: the financial-aid counsellor. Neat side part, rolled sleeves, a calculator.
P["funder"] = card("#ddf3f1", "#b8e3df", "#a6dbd5", f'''
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#f2f5f7"/>
<path d="M176 372 L200 398 L224 372" fill="none" stroke="#cfd8de" stroke-width="5"/><path d="M196 398 L190 470 L200 480 L210 470 L204 398Z" fill="#1f8f86"/>
<g transform="translate(270 386)"><rect width="70" height="88" rx="10" fill="#2b3440"/><rect x="10" y="10" width="50" height="18" rx="3" fill="#bfe9c9"/>
<g fill="#e6edf2">{"".join(f'<rect x="{10+i%3*18}" y="{36+i//3*16}" width="12" height="11" rx="2"/>' for i in range(9))}</g></g>
{face("#7a4a2e", "#6a3f27")}
<path d="M136 246 C130 182 270 178 264 244 C250 216 228 206 188 208 C168 212 148 224 136 246Z" fill="#1c1410"/>
<path d="M188 208 C200 216 214 218 230 214" stroke="#3a2a22" stroke-width="3" fill="none"/>
{eyes()}{brows("#1c1410")}{nose("#55301c")}{mouth()}''')

# interviewer: the professor across the table, played for practice. Silver pixie cut, blazer, a PRACTICE card.
P["interviewer"] = card("#fdebdc", "#f6d2b5", "#f4c39b", f'''
<path d="M88 480 C94 400 140 372 200 368 C260 372 306 400 312 480Z" fill="#5a4a7a"/>
<path d="M170 372 L200 420 L230 372 L230 480 L170 480Z" fill="#f6efe7"/>
<path d="M170 372 L150 480 M230 372 L250 480" stroke="#463a62" stroke-width="5"/>
<g transform="translate(252 400) rotate(-5)"><rect width="110" height="44" rx="8" fill="#fff" stroke="#e2833b" stroke-width="3"/>
<text x="55" y="29" font-family="Inter,Arial,sans-serif" font-size="17" font-weight="800" fill="#e2833b" text-anchor="middle" letter-spacing="2">PRACTICE</text></g>
{face("#e3b08c", "#d29d78")}
<path d="M136 248 C128 186 272 180 266 246 C258 230 252 220 240 216 C222 226 186 220 172 210 C156 220 142 232 136 248Z" fill="#cfcfd6"/>
{eyes(glasses=True, frame="#5a4a7a")}{brows("#a9a9b2")}{nose("#b98463")}{mouth()}''')

for k, v in P.items():
    (here / f"{k}.svg").write_text(v)
print("drew", ", ".join(P))
