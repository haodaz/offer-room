# offer room

**Six AI agents and an applicant in one team chat, built with [Switch](https://github.com/sandbox-quantum/switch) for the Flip the Switch hackathon (Nov 2026).**

Applying to a PhD program is a team sport most people play alone. Offer room gives an applicant a team that lives
where they already talk (Discord here; the same template runs on Slack or Teams): agents that each start from a
different place, check each other in the open, and leave every decision and every send to the person.

Getting in is the start, not the finish. The room looks long (the five years after an admit: who you work with,
what you live on, where people from that lab went next), looks real (only what a page, a tool or your own files
show) and connects the steps (school list, materials, money, interviews and offers are one story).

## The team

| Agent | Real-world role | Starts from | Tends to argue for | One to one |
|---|---|---|---|---|
| offer-scout | admissions coordinator | programs' official pages | feasibility: deadlines, letters, small print | the application calendar |
| offer-mentor | senior PhD student | advisors' papers, students, where they went (OpenAlex) | fit and outcomes over prestige | research direction |
| offer-critic | committee reader | the applicant's own record, read cold | honesty about what the record supports | cold reads of every draft |
| offer-writer | writing coach | the applicant's files | one coherent story | SOP, emails, recommender packets |
| offer-funder | financial-aid counsellor | fees, waivers, fellowships, stipends, rent | money is part of fit | a funding plan, offer comparison |
| offer-interviewer | the professor across the table (practice) | one advisor's verified papers and page | depth that survives a follow-up | mock interviews, scored |

Each agent is a Claude Code session with its own harness (`agents/<name>/AGENT.md`: what it knows, its tools,
its bias, its one-to-one work) and its own notebook (`agents/<name>/memory.md`), so it is the same person every
time the applicant comes back.

Portraits of the six agents and both applicants are in `docs/agents/gen/` (Meta Muse Image; invented people).

## How they work together

- **Relay with stances.** A team question goes scout → mentor (→ funder) → critic. Every reply after the first
  opens with *Agree*, *Building on* or *I disagree with X on Y*, with evidence. Critic closes with where the team
  agrees, where it splits, and what only the applicant can decide.
- **Changing minds in public.** When new evidence contradicts an agent, it says "Correction: I was wrong about X"
  first. One rebuttal per point, then it goes back to the person.
- **One-to-one desks.** `interview-room`, `mentor-room`, `funding-desk`, `writing-desk` for long work; a summary
  comes back to the team room only when the applicant says so.
- **Humans act.** No agent emails, submits, pays or contacts anyone.

## Trust, checked by code

- `tools/check_draft`: every sentence of a draft must carry a source tag; file and line tags must resolve; a paper
  id passes only if an OpenAlex call actually returned it. Exit code 1 until it passes.
- `tools/scholar`: OpenAlex lookups with a disk cache (client vendored from [hioffer](https://github.com/haodaz/hioffer)):
  `schools`, `topic`, `find`, `works`, `coauthors`, `alumni`, `profile`.
- `tools/compare_offers`: transparent offer scoring (fit, stipend after rent, signals, years guaranteed) with
  weights the applicant can change.

## The whole application

`CLAUDE.md` maps ten steps (direction, requirements, advisors, calendar, recommenders, materials, outreach, money,
interviews, offers) to an owner and a checker. Shared state lives in `board/<applicant>/` (tracker, plan, decisions,
drafts, interviews, funding).

## License

MIT. Switch itself is licensed separately by SandboxAQ.

## Demo applicants

Both are fictional; the programs and advisors are real public pages and papers.
- **Priya** (`applicants/priya/`): international applicant from India, multilingual NLP.
- **Maya** (`applicants/maya/`): first-generation US applicant and Pell recipient, code-switched speech. Same room,
  different money: fee waivers and fellowships depend on eligibility, and funder quotes the line for each.

## Run it

1. Install [Switch Console](https://github.com/sandbox-quantum/switch) (macOS; it runs the Switch server locally),
   sign in to Claude Code from it, and connect a chat app (Discord here; Mattermost, Slack, Teams or Telegram work too).
2. Install [uv](https://docs.astral.sh/uv/). The tools run through it; nothing else to install.
   Optional: an OpenAlex key in `.env` (`OPENALEX_API_KEY=...`) for a higher daily quota.
3. In Switch Console, import `offer-room.template.yaml` and use it: pick your chat app and keep the default directory.
   Switch creates the six agents, clones this repo into their folder, and opens offer-room plus the four desks.
   (`offer-room-desks.template.yaml` adds the funder, interviewer and desks to an earlier four-agent room.)
4. In offer-room, ask `@offer-scout` a question about one of the applicants, for example:
   `@offer-scout Priya (applicants/priya) can only afford two of UW, UMD and Cornell. Which two, and why?`

The same room works for a job search or college applications: swap programs for roles or colleges, the mentor's
labs for teams, and keep the rest.
