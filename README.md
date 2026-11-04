# offer room

Four AI agents and an applicant in one team chat, built for the Flip the Switch hackathon (Nov 2026).

Each agent starts from a different place and is allowed to disagree:

| Agent | Starts from | Tends to argue for |
|---|---|---|
| offer-scout | programs' official pages | feasibility: deadlines, requirements, funding |
| offer-mentor | advisors' papers and students (OpenAlex) | fit and mentorship over prestige |
| offer-critic | the applicant's own record, read cold | honesty about what the record supports |
| offer-writer | the applicant's materials | one coherent story across programs |

A question runs as a relay: scout, then mentor, then critic. Every reply after the first opens with
agree, building on, or I disagree, and critic closes with where the team agrees, where it splits, and
what only the applicant can decide. The applicant decides and sends; agents never email, submit or pay.

- Room rules: [CLAUDE.md](CLAUDE.md). Each agent's harness: `agents/<name>/AGENT.md`.
- Switch template (paste into Switch Console): [offer-room.template.yaml](offer-room.template.yaml).
- The demo applicant in `applicant/` is fictional (from hioffer). The target programs are real public pages.
- OpenAlex lookups reuse [hioffer](https://github.com/haodaz/hioffer)'s scholar tool through `tools/scholar`.

The same room works for a job search: swap programs for roles, the mentor for someone who reads the team,
and the critic for a hiring manager.
