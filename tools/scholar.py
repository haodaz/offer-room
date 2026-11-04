"""Command-line front for hioffer.tools.scholar. Prints JSON. Reads only the OPENALEX_* lines of hioffer's .env."""
import json
import os
import sys
from pathlib import Path

env = Path(os.environ.get("HIOFFER_DIR", Path.home() / "Documents/hioffer")) / ".env"
if env.exists():
    for line in env.read_text().splitlines():
        if line.startswith("OPENALEX_") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

sys.path.insert(0, str(env.parent))
from hioffer.tools import scholar  # noqa: E402

cmd, *args = sys.argv[1:] or ["help"]
if cmd == "find":
    out = scholar.find_author(args[0], args[1] if len(args) > 1 else "")
elif cmd == "works":
    out = scholar.recent_works(args[0], int(args[1]) if len(args) > 1 else 2023, 8)
elif cmd == "coauthors":
    out = scholar.coauthors(args[0], int(args[1]) if len(args) > 1 else 2021)
elif cmd == "topic":
    # Who at an institution recently published on a topic, ranked by matching papers (not by citations).
    topic, inst = args[0], args[1]
    since = int(args[2]) if len(args) > 2 else 2023
    found = scholar._get("/institutions", search=inst, per_page=1)["results"]
    if not found:
        sys.exit(f"no institution matches {inst!r}")
    iid = found[0]["id"].rsplit("/", 1)[-1]
    works = scholar._get("/works", search=topic, per_page=100, select="id,title,publication_year,authorships",
                         filter=f"institutions.id:{iid},from_publication_date:{since}-01-01")["results"]
    people = {}
    for w in works:
        for au in w.get("authorships", []):
            if not any((i.get("id") or "").endswith(iid) for i in au.get("institutions", [])):
                continue
            a = au.get("author") or {}
            if not a.get("id"):
                continue
            p_ = people.setdefault(a["id"].rsplit("/", 1)[-1], {"id": a["id"].rsplit("/", 1)[-1], "name": a.get("display_name"), "papers": []})
            p_["papers"].append({"id": w["id"].rsplit("/", 1)[-1], "title": w.get("title"), "year": w.get("publication_year"), "position": au.get("author_position")})
    ranked = sorted(people.values(), key=lambda x: -len(x["papers"]))[:12]
    out = {"institution": found[0]["display_name"], "topic": topic, "since": since, "works_scanned": len(works),
           "note": "Students and faculty both appear; check the faculty directory before calling anyone an advisor.",
           "people": ranked}
elif cmd == "profile":
    out = scholar.author_profile(args[0])
else:
    sys.exit(__doc__ + "\nusage: scholar find NAME [INSTITUTION] | works ID [SINCE] | topic TOPIC INSTITUTION [SINCE] | coauthors ID [SINCE] | profile ID")
print(json.dumps(out, indent=1, ensure_ascii=False))
