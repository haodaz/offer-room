"""Cut the submission video (1920x1080, about 3 minutes) from cards, Discord stills and the live interview frames,
with OpenAI narration and an .srt (not burned in).

    cd ~/Documents/hioffer && uv run python ~/Documents/offer-room/docs/video/assemble.py
"""
import json
import subprocess
from pathlib import Path

here = Path(__file__).parent
out = here / "out"
st = out / "stills"
live = out / "live_q2"
TTS = Path(__file__).parent / "tts-qwen-out" / "tts"
FF = "/Users/aisandbox/Documents/companydata/node_modules/ffmpeg-static/ffmpeg"
CHAT = (766, 372, 2170, 1360)          # the Discord message column in a 2992x1868 window capture


def zoom(y0):
    """A 16:9 band of the full message column (lines wrap at full width, so never crop sideways)."""
    return (CHAT[0], min(max(y0, CHAT[1]), CHAT[1] + CHAT[3] - 1221), CHAT[2], 1221)


def card(name, d):
    return {"img": here / f"{name}.png", "d": d}


def chat(name, d, rect=CHAT, hl=()):
    return {"img": st / f"{name}.png", "d": d, "rect": rect, "hl": hl}


def frame(n, d, rect=CHAT, hl=(), still=True):
    return {"img": live / f"f{n:02d}.png", "d": d, "rect": rect, "still": still, "hl": hl}


def line(y, x=880, w=1990, h=46):
    """A highlighter stroke over one line of a capture, in the capture's own pixels."""
    return (x, y - 4, w, h)


CONSOLE = Path(__file__).parent / "out" / "console" / "agents.png"
SECTIONS = [
    {"n": ["c1"], "lead": 0.5, "shots": [card("cover", 4.5)]},
    {"n": ["c2"], "shots": [card("team", 10.0)]},
    {"n": ["c2b"], "shots": [{"img": st / "team_live.jpg", "d": 7.5, "rect": (383, 82, 1113, 626), "tab": True}]},
    {"n": ["c3"], "shots": [card("template", 4.0), {"img": CONSOLE, "d": 3.5, "rect": (0, 625, 1010, 568)}]},
    {"n": ["p1"], "shots": [card("personas", 4.5)]},
    {"n": ["p2"], "shots": [card("priya", 7.0)]},
    {"n": ["p3"], "shots": [card("maya", 6.5)]},
    {"n": ["r1"], "shots": [chat("r1_ask", 3.5), chat("r1_ask", 7.0, zoom(900), [line(1646, w=1450)])]},
    {"n": ["r2"], "shots": [chat("r2_mentor", 6.0, zoom(900), [line(1316, w=2030, h=92)]), chat("r2_critic", 6.5, zoom(560), [line(874, w=1780)])]},
    {"n": ["r3"], "shots": [chat("r3_correct", 6.0, zoom(620), [line(954, w=800)]), chat("r3_critic", 6.0, zoom(560), [line(798, w=1300), line(1238, w=720)])]},
    {"n": ["m1"], "shots": [chat("m_outcomes", 9.0, zoom(380))]},
    {"n": ["f1"], "shots": [chat("f_maya", 3.5)]},
    {"n": ["f2"], "shots": [chat("f_maya", 7.0, zoom(560), [line(1022, w=1990)])]},
    {"n": ["f3"], "shots": [chat("f_priya", 7.0, zoom(620), [line(1010, x=1170, w=540), line(1614, w=1960)])]},
    {"n": ["i1"], "shots": [chat("i_q1", 6.0, zoom(560)), chat("i_score", 6.5, zoom(640), [line(1262, w=1080), line(1394, w=1100)])]},
    {"n": ["i2"], "shots": [frame(1, 0.7), frame(6, 0.5), frame(12, 0.5), frame(16, 1.0), frame(16, 4.5, zoom(700), [line(1218, w=1160)])]},
    {"n": ["w1"], "shots": [chat("w_draft", 4.5, zoom(560)), chat("w_critic", 5.0, zoom(560))]},
    {"n": ["t1"], "shots": [card("checker", 7.5)]},
    {"n": ["e1"], "lead": 0.4, "shots": [card("end", 6.0)]},
]

lines = {s["id"]: s["text"] for s in json.loads((here / "narration.json").read_text())}
durs = {d["id"]: d["dur"] for d in json.loads((TTS / "durations.json").read_text())}
GAP = 0.3

clips = out / "clips"
clips.mkdir(exist_ok=True)
parts, cues, voice = [], [], []
t = 0.0
k = 0
for sec in SECTIONS:
    lead = sec.get("lead", 0.25)
    talk = sum(durs[n] for n in sec["n"]) + GAP * (len(sec["n"]) - 1)
    extra = max(0.0, lead + talk + 0.4 - sum(sh["d"] for sh in sec["shots"]))
    c = t + lead
    for n in sec["n"]:
        voice.append((n, c))
        sentences = [x.strip() for x in lines[n].replace("? ", "?|").replace(". ", ".|").replace(": ", ":|").split("|") if x.strip()]
        total = sum(len(x) for x in sentences)
        cc = c
        for x in sentences:
            dd = durs[n] * len(x) / total
            cues.append((cc, cc + dd, x))
            cc += dd
        c += durs[n] + GAP
    for i, sh in enumerate(sec["shots"]):
        d = sh["d"] + (extra if i == len(sec["shots"]) - 1 else 0)
        frames = int(round(d * 30))
        marks = "".join(f"drawbox=x={a}:y={b}:w={c}:h={e}:color=0xFFD84D@0.38:t=fill:enable='gte(t,0.8)'," for a, b, c, e in sh.get("hl", ()))
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            if sh["img"] == CONSOLE or sh.get("tab"):
                base = f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos"
            elif sh["rect"] == CHAT:  # whole column: fit inside the frame on white
                base = f"{marks}crop={w}:{h}:{x}:{y},scale=-2:1000:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white"
            else:
                base = f"{marks}crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos"
        elif str(sh["img"]).endswith("agents.png"):
            base = "scale=-2:1000:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white"
        else:
            base = "scale=1920:1080:flags=lanczos"
        move = "" if sh.get("still") else f",scale=3840:2160,zoompan=z='1+0.02*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30"
        clip = clips / f"{k:02d}.mp4"
        subprocess.run([FF, "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", f"{d:.3f}", "-i", str(sh["img"]),
                        "-vf", f"{base}{move},fps=30,format=yuv420p,setsar=1", "-frames:v", str(frames),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(clip)], check=True)
        parts.append(clip)
        k += 1
        t += frames / 30


def ts(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


(out / "offer-room.srt").write_text("\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{s}\n" for i, (a, b, s) in enumerate(cues)))
(out / "clips.txt").write_text("".join(f"file '{p}'\n" for p in parts))
subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(out / "clips.txt"), "-c", "copy", str(out / "video.mp4")], check=True)
inputs, af = [], []
for j, (n, at) in enumerate(voice):
    inputs += ["-i", str(TTS / f"{n}.wav")]
    af.append(f"[{j + 1}:a]adelay={int(at * 1000)}|{int(at * 1000)}[a{j}]")
fc = ";".join(af) + ";" + "".join(f"[a{j}]" for j in range(len(voice))) + f"amix=inputs={len(voice)}:normalize=0,apad,atrim=0:{t:.2f}[aout]"
subprocess.run([FF, "-v", "error", "-y", "-i", str(out / "video.mp4"), *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out / "offer-room.mp4")], check=True)
print(f"done {t:.1f}s -> {out / 'offer-room.mp4'}")
