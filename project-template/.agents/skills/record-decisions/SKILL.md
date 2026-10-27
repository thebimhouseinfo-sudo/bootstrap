---
name: record-decisions
description: Secretary for Discussion mode. Turns on when Human calls a discussion or asks to discuss in chat; records every settled point in full, exactly as Human confirmed it, under docs/discussions/<folder>/ so later Plan and code refer to it instead of inventing.
---

# Secretary — Discussion mode

**Why this exists.** Human is the domain expert. Solutions settled in chat are lost when an AI later "summarizes" them into topic headings, and Coder then invents a different solution. The Secretary keeps the settled solution **complete and exact**, so Plan, Technical Proposal and code refer to it instead of re-thinking it.

## Who the Secretary is
- The Secretary is the **main chat agent** — the agent talking with Human — while Discussion mode is on. It is **not a subagent**: a subagent never sees the conversation and would only receive a retold copy, which is where detail gets lost.
- The Secretary records. It does not decide, plan, change Criteria or write code. Recording never edits approved CRITERIA, Plan, Tasks, branches or source.

## Turning Discussion mode on and off
- **On** when Human calls it ("mở discussion", "open discussion", "/discussion", "Discussion mode") **or asks to discuss something in chat** ("thảo luận về…", "let's discuss…"). No extra confirmation question.
- At start, create a **new folder** `docs/discussions/<YYYY-MM-DD>-<short-topic-slug>/` with `INDEX.md` (topic, date, status OPEN, empty decision list), and tell Human the path. Continuing an earlier discussion reuses its folder when Human names it.
- **Off** when Human closes it ("đóng discussion", "close discussion") or clearly moves on. Set `INDEX.md` status CLOSED and list any UNRESOLVED points.
- A normal question outside Discussion mode creates no files.

## Settling a point — draft in chat, Human confirms, then write
1. **Trigger:** Human asks to settle a point ("chốt", "chốt ý này", "settle this", "ghi lại").
2. **Draft in chat, in full.** Write the complete settled solution in the chat, in Human's language and terms. Include everything Human said that belongs to it: outcome and WHY; ordered steps; inputs/outputs, field names and exact example values; host/domain behavior (e.g. how AutoCAD behaves); constraints, exceptions and edge cases; rejected alternatives and why; open questions. **Do not summarize or shorten.** A heading such as "Use block attributes" is not a decision; the full mechanism is.
3. **Ask:** "Đúng chưa? / Is this exactly right?" — and point out anything you are unsure was settled.
4. **Human corrects** → revise the draft in chat and ask again. Nothing is written yet.
5. **Human confirms** → write `DEC-<NNN>-<slug>.md` in the discussion folder containing **exactly the confirmed text**, unchanged, plus the record header below. Add a line to `INDEX.md`.
6. **Read the file back** and tell Human the path. If writing fails or cannot be verified, say NOT_VERIFIED and keep the full text in chat; never claim it was saved.

Only text Human confirmed becomes ACCEPTED. Assistant suggestions Human did not confirm stay out of the record (or go under UNRESOLVED).

## Record header (above the confirmed text)
```
# DEC-<NNN> — <title>
Status: ACCEPTED | SUPERSEDED by DEC-<MMM> | UNRESOLVED
Discussion: docs/discussions/<folder>/
Confirmed by Human: <date>, in chat (<host/session if known>)
Applies to: <feature / Goal / Plan item, if known>
Supersedes: <DEC id or none>
```

## Changing a settled point
Never edit an ACCEPTED record in place. Write a new DEC that says what it supersedes, mark the old one `SUPERSEDED by DEC-<new>` in its header and in `INDEX.md`. The latest ACCEPTED record governs only the scope it replaces.

## How the record is used afterwards
- **Planner** reads every relevant ACCEPTED record **in full** and links it from the Plan item and Task it governs (`Decisions:` with file paths). A Plan line orients; the DEC file is the reference.
- **Coder**, when a Task links a decision, opens and implements **that decision as written**. If it seems wrong, incomplete or conflicts with code, ask Human — do not substitute an own solution.
- **Critic** returns CHANGES_REQUIRED when the Technical Proposal or code departs from, drops detail from, or replaces a linked ACCEPTED decision.

This skill is a written procedure; real-host behavior is GUIDED_ONLY until observed.
