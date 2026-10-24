# M4 — Code Structure Proposal: Coder solution clarification, user artifact knowledge, descriptive source design

**Status:** PRE-CODE / GUIDED_ONLY. Authority: Unified v7 Functional-First Plan M4 and operational Sections E4–E7, I1–I5. Native independent Reviewer remains UNVERIFIED.

## Goal

Coder reads the full relevant accepted Human professional decision and existing host/source, asks only about genuinely missing user/operational/domain facts and creates ONE Markdown per-Task Code Structure Proposal with intended file paths, functions, callers, contracts and tests **before writing application code**. Coder is software engineer not professional Domain Expert; internal implementation details do not become new Human questionnaires.

## Proposed code and caller map

| Path | Action | Responsibility and callers |
| --- | --- | --- |
| project-template/.agents/roles/coder.md | MODIFY | Read full decision/Goal/host facts, distinguish domain unknown vs normal technical choice; pre-code proposal with no source files before review; phase/purpose-based artifact lifecycle; existing branch authority unchanged. Existing host Coder role consumes. |
| project-template/.agents/skills/implement-task/SKILL.md | MODIFY | Split Pre-Code descriptive proposal → whole relevant Reviewer review → implementation after PASS → evidence/test/repair. Existing Coder invokes; no new approval engine. |
| project-template/.agents/skills/solution-clarification/SKILL.md | CREATE | Focused one-time Goal/Job-Pack domain/host question method, asks Human only if consequential missing information; no duplicate form/gate. |
| project-template/.agents/knowledge/operational-file-lifecycle.md | CREATE | On-demand Coder knowledge: DEV internal vs user-directed OPERATION documents/code vs app-generated support/recovery. Word DOCX, AutoCAD DWG/BAK/DWL/DWL2, same-name LISP reload, CadGPT Temp/Custom Job export/import. |
| Existing seven Coder host mirror paths | MODIFY | Mirror full canonical Coder role, keeping native TOML/YAML/Markdown wrappers, Generic byte-equal; no installer rewrite. |
| tests/test_installer.py | MODIFY | Ensure focused skill/knowledge packaged in current host layouts and canonical role mirrors; scripts do not claim a live agent used skill. |
| install.py, Task runner, Criteria, Job runtime | REUSE_AS_IS | No new registries, file version service, identity manager, native host logic or installer architecture. |

## Workflow and tests

Pre-Code input: Goal + Task IDs, actual Plan, full accepted DEC refs or directly provided settled instructions, current source/callers, verified host. Output: ONE descriptive proposal with explicit status VERIFIED vs PROPOSED symbols. Reviewer reads ALL interacting Task proposals and checks smallest solution, duplicate gates, system impact, operational file lifecycle. PASS permits existing authorized source writes; CHANGES_REQUIRED updates proposal only; HUMAN_ESCALATION only for actual missing user choice or disproportionate risk, including manual alternative.

Test cases: Word document external rename/version unchanged content can be opened; CadGPT User-produced Job is CODE but may be edited/exported/imported/run without mandatory SHA or GUID identity; new same-name LISP LOAD not refused merely because content changed; host BAK is recovery not disposable, DWL/DWL2 ordinary temp and not user Job products. A complete accepted Goal should yield no repeat questions. Pre-Code does not create empty compilable application source. Native CAD/IDE host success requires real-host evidence; static tests must not call it PASSED.

## Guided Reviewer findings
- Minimal reusable host roles and existing skill loader are sufficient. A new file-management service or universal schema is disproportionate.
- Do not conflate internal Git blob SHA/CAS used to write DEV source with the User's file naming/version or operational reload contract.
- Independent Reviewer PASS is not available in this current GitHub-only control path; record UNVERIFIED rather than invent signature.
- This document is temporary dogfood evidence and deleted from release HEAD when ship acceptance is complete.
