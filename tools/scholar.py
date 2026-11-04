"""OpenAlex lookups for the agents. Prints JSON. Optional: OPENALEX_API_KEY / OPENALEX_MAILTO in the environment or
in a .env file at the repo root (only OPENALEX_* lines are read)."""
import json
import os
import sys
from pathlib import Path

env = Path(__file__).resolve().parent.parent / ".env"
if env.exists():
    for line in env.read_text().splitlines():
        if line.startswith("OPENALEX_") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openalex as scholar  # noqa: E402

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
elif cmd == "schools":
    # Which universities publish most on a topic recently: where to look, not a ranking of quality.
    topic = args[0]
    country = args[1].upper() if len(args) > 1 else "US"
    since = int(args[2]) if len(args) > 2 else 2023
    data = scholar._get("/works", filter=f"title_and_abstract.search:{topic},from_publication_date:{since}-01-01,institutions.type:education,institutions.country_code:{country},primary_topic.field.id:17",
                        group_by="authorships.institutions.id", per_page=200)
    out = {"topic": topic, "country": country, "since": since,
           "note": "Computer-science papers only. Counts of recent papers by institution (OpenAlex). Where the work is, not how good it is.",
           "schools": [{"id": g["key"].rsplit("/", 1)[-1], "name": g["key_display_name"], "papers": g["count"]}
                       for g in data.get("group_by", [])[:25]]}
elif cmd == "alumni":
    # Where people who published with an advisor early in their careers are now. A proxy for lab outcomes:
    # early-career co-authors (few works before the shared paper) and their latest known institution.
    aid = args[0]
    since = int(args[1]) if len(args) > 1 else 2014
    until = int(args[2]) if len(args) > 2 else 2021
    works = scholar._get("/works", filter=f"authorships.author.id:{aid},from_publication_date:{since}-01-01,to_publication_date:{until}-12-31",
                         per_page=100, select="id,publication_year,authorships")["results"]
    firsts = {}
    for w in works:
        for au in w.get("authorships", []):
            a = au.get("author") or {}
            if au.get("author_position") == "first" and a.get("id") and not a["id"].endswith(aid):
                firsts.setdefault(a["id"].rsplit("/", 1)[-1], {"name": a.get("display_name"), "example": w["id"].rsplit("/", 1)[-1], "year": w.get("publication_year")})
    people = []
    for pid, info in list(firsts.items())[:25]:
        rec = scholar._get(f"/authors/{pid}")
        last = [i.get("display_name") for i in (rec.get("last_known_institutions") or [])]
        people.append({"id": pid, **info, "now": last, "works_count": rec.get("works_count")})
    out = {"advisor": aid, "window": f"{since}-{until}",
           "note": "First authors on the advisor's papers in this window and their latest institution in OpenAlex. "
                   "Not every first author was a student, and records can be stale: a lead, not a placement list.",
           "people": people}
elif cmd == "profile":
    out = scholar.author_profile(args[0])
else:
    sys.exit(__doc__ + "\nusage: scholar find NAME [INSTITUTION] | works ID [SINCE] | topic TOPIC INSTITUTION [SINCE] | alumni ADVISOR_ID [FROM] [TO] | schools TOPIC [COUNTRY=US] [SINCE] | coauthors ID [SINCE] | profile ID")
print(json.dumps(out, indent=1, ensure_ascii=False))
