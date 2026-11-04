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
elif cmd == "profile":
    out = scholar.author_profile(args[0])
else:
    sys.exit(__doc__ + "\nusage: scholar find NAME [INSTITUTION] | works ID [SINCE] | coauthors ID [SINCE] | profile ID")
print(json.dumps(out, indent=1, ensure_ascii=False))
