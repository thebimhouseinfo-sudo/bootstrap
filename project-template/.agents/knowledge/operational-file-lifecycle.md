# Coder knowledge — file lifecycle by phase, intended product and app design

**Use on demand when a Task creates, opens, loads, saves, imports, exports or deletes files.** This is knowledge, NOT a mandatory file-classifier, manager, schema or new approval gate.

## Governing principle
**DEV:** Files used internally to develop the software — product source, test/build materials, internal repository/protocol records — follow accepted developer engineering controls (Git SHA/CAS, internal record IDs, review state) when needed.
**OPERATION / User-intended product:** Files that the Human *intentionally asks the delivered application to create/use* belong to their workflow and native document/host operations. They need not be SHA/GUID/version-registered by the application. Code format, extension, physical author, directory or model writer do NOT turn them into DEV files.
**OPERATION / app-generated support:** Files that application/host produces to serve its own design, not as the intended User deliverable, may follow its designed temporary/cache/backup/recovery lifecycle, including justified internal IDs. Co-location does not make them the same as the User document.

## Three representative journeys
1. **Word:** User creates DOCX, renames and archives personally, opens later to read/edit/save. Word need not know whether User calls it v1 or v20, and a changed SHA is not a normal reason to refuse Open. A user-requested versioning feature is possible, but not assumed.
2. **AutoCAD:** User controls DWG Save/Save As/Export. AutoCAD creates session DWL/DWL2 files normally removed on clean close; crash may leave them. BAK is host-managed *backup/recovery*, generally created on qualifying saves with backup enabled and may persist after close. Never delete BAK as though it were session temp; never build CadGPT's own cleanup daemon without need. Same-folder files can have different lifecycles.
3. **CadGPT:** A User-generated **Temp Job or Custom Job is itself user-created code during OPERATION**, containing JOB.md, LISP/Python etc. User updates it, exports externally, imports again and runs it. The app need not know its version or original SHA/GUID to perform normal authorized work. Same-name revised Lisp LOAD must not be rejected **solely** because file content SHA differs. A separate execution Run ID, if part of real internal runtime, is not the User Job's identity or mandatory version registry. User elects any permanent promotion/publishing, not Coder by default.

## Practical Coder decision test
Ask: (a) what was this file created FOR, (b) who intends to control it and native Save/Load/Import/Export, and (c) what is *already decided by User/host*? Follow existing User workflow for User product and existing app/host design for support. For **consequential unaddressed** User data overwrite, same-name collision, retention or publication, ask once at a workflow level. Do NOT ask for ordinary .dwl lifecycle or internal variable naming. Do not ask again if chosen.

Protect normal permission/path validation, actual file-format checks, executable-source safety and host capability verification. Reject an incomplete/untrusted/imported Job for its **real** reason, never fabricated "hash changed therefore different immutable Job." Two unrelated imported Jobs that collide in name may require a genuine User resolution; do not silently overwrite or assume equal based on names.

## Pre-code Reviewer and Tester checks
For a Task handling operational files, descriptive Code Structure Proposal should state file purpose/owner, intended native operation, User-facing name/path policy source, internal-only metadata if any, conflict/overwrite/update rules and how real host would verify. Do not add this form to unrelated Tasks.

Reviewer challenges default GUID/SHA registry, forced version suffix, publish/promote, draft/checkout, excessive cleanup or new manager with no actual requirement. Tester simulates User Save/Load/Import/Export and same-name changed-content reload as applicable, distinguishing native host evidence from script/mock results. This does NOT forbid necessary DEV Git SHA/CAS on actual developer-controlled source.

**No universal file identity rule** exists for all extension/path/phase combinations. Intent and actual app ownership determine lifecycle; accepted User decisions take priority where they govern the product.
