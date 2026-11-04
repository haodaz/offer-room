# Interview lines for the recording

Spoken lines for the two fictional applicants, written from their files (`applicants/<name>/cv.md`, `story.md`).
Read them at a normal pace; each block is about 45 to 75 seconds. Nothing here goes beyond their files.

---

## Priya, with offer-interviewer playing Marine Carpuat (UMD)

### Opening (if asked "tell me about yourself")
> Hi, I'm Priya. I'm a final-year computer science student at NIT Trichy in Tamil Nadu.
> I work on evaluation for Indian languages. My grandmother speaks only Tamil, with a few English words for
> medicines and phone menus, and every voice assistant we tried failed her. So I built a Tamil–English
> code-switched test set, about 2,400 sentences, and showed that two open 7B models lose 18 to 26 points of
> accuracy when people switch languages the way my family does. That became my first-author workshop paper.
> This summer at Microsoft Research India I worked on the other side, adaptation: adding six thousand Kannada
> tokens to a tokenizer cut sentence length by 41 percent and raised QA F1 by 3.4 points at the same budget.
> I want to spend a PhD learning to measure multilingual models honestly, and to fix what the measurements show.

### Q1, improved (why a PhD, why this group)
> My grandmother is why I started. Every assistant we tried failed her, so I measured how badly models fail on
> how my family actually talks: two open 7B models lose 18 to 26 points on code-switched Tamil.
> I prefer evaluation because it makes failure visible. Your group asks the next question, whether we can trust
> the measurement itself, as in your work on COMET for under-resourced languages. That is the question I want
> to learn to ask.
> In five years I want to be leading evaluation and adaptation work for Indian languages, in an industry
> research lab or as faculty, and I think that starts with learning to build measurements people can trust.

### Q2 (points of what, and is it really code-switching?)
> It's accuracy on two tasks: three-way sentiment and twelve-way intent. Each code-switched sentence is compared
> with a matched monolingual Tamil sentence with the same label. Two native speakers labelled them, and their
> agreement was a kappa of 0.81.
> You're right to ask about script. The sentences come from public social-media posts, and they mix Tamil script
> with romanized Tamil. I didn't separate the two, so part of the drop could be script, not switching.
> The experiment I'd run first is to transliterate everything into one script and measure again. If most of the
> gap survives, it's the switching. If it shrinks, script is a problem worth its own paper.

---

## Maya, with offer-interviewer playing an advisor she picks

### Opening
> Hi, I'm Maya. I'm a senior in computer science at UTEP, in El Paso, and I'm the first in my family to go to
> college.
> My research started at home. My dad calls a clinic phone line for my grandmother, and the automated system
> keeps mishearing him every time he switches between Spanish and English. So in my undergrad lab I built a set
> of about 1,800 code-switched utterances from community radio call-ins, and fine-tuned an open speech model on
> it. Word error rate on the code-switched turns went from 38 percent to 27.
> Last summer, in an NSF REU, I looked at the same gap in text: open LLMs gave about 15 percent more unsupported
> claims when health questions were asked in Spanish.
> I want a PhD so I can build speech and language technology that works for bilingual families, and measure it
> on real conversations, not clean benchmarks.

### Why a PhD, and what after
> Honestly, I didn't know a PhD was paid until my advisor told me in my second year. Once I knew, it was the
> obvious next step, because the problems I care about need years, not a semester.
> Five years from now I want to be leading speech work for bilingual communities, at a research lab or as a
> professor at a Hispanic-Serving Institution like the one I came from. That's also why I look at where a lab's
> students end up, and whether they finish.

### Likely follow-up: why did the error rate drop?
> I fine-tuned on in-domain code-switched audio, so the model heard the kind of speech it was being tested on.
> I can't yet tell you how much came from the switching itself and how much from the radio domain. My next step
> would be to test on code-switched audio from a different source, and on monolingual call-ins from the same
> station, to pull those two apart.

---

## Recording notes
- Answer as the applicant, in the interview-room, after offer-interviewer asks. Keep the stance line it gives back.
- Priya's Q1 is the "after coaching" version: use it in a second take to show the score move.
- Both applicants are fictional; say so once in the video, not in the interview.
