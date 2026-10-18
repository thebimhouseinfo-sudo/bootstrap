# bootstrap: Codex-ready harness templates for coding agents
# bootstrap: bộ template harness sẵn dùng cho coding agent

> **VI:** Repo này là **bộ template có sẵn**, mặc định **Codex-ready**. Người dùng chỉ cần đưa link repo và mô tả dự án cho AI. **AI tự đọc, khảo sát, trình phương án để duyệt, rồi tự sao chép và cấu hình template vào dự án đích**. Nếu AI không có quyền truy cập file/terminal dự án, AI **cung cấp lệnh terminal cụ thể** theo OS/shell để người dùng thực hiện, sau đó kiểm tra kết quả. Không yêu cầu người dùng tự tìm hay chọn file template.
>
> **EN:** This repository contains **ready-made harness templates**, optimized for **Codex**. The user only provides the repository link and a short project description. **The AI reads this repository, inspects the target project, proposes adaptations for approval, then copies and configures the template itself**. If the AI cannot access the target filesystem or terminal, it provides **exact OS/shell-specific terminal commands** for the user to execute and verifies the result. The user does not need to locate or select template files.

**VI:** Không xây lại harness từ đầu, không viết lại agent/skill generic. Mọi kết quả phải có bằng chứng kiểm thử thật; mọi quyết định cần user chấp thuận phải qua **Approval Request: Đồng ý / Không đồng ý / Khác** (trừ ngoại lệ bootstrap ban đầu khi kênh duyệt chưa được cài đặt và được công bố rõ).

**EN:** Do not rebuild the harness from scratch or rewrite reusable generic agents/skills. Demonstrate results with actual test evidence. Decisions requiring user authorization must use an **Approval Request: Agree / Disagree / Other**, except the explicitly disclosed initial-bootstrap fallback before an approval channel exists.

---

## Dành cho người dùng / For users

**VI:** Gửi AI link repo và yêu cầu:

> Đọc README của `https://github.com/thebimhouseinfo-sudo/bootstrap`. Hãy thiết lập harness cho dự án của tôi bằng cách tái sử dụng template có sẵn; tự copy và cấu hình nếu có quyền, nếu không thì cho tôi lệnh terminal phù hợp. Dự án: `<mô tả ngắn hoặc đường dẫn>`.

**EN:** Give your AI assistant the repository link and say:

> Read the README at `https://github.com/thebimhouseinfo-sudo/bootstrap`. Set up my project's coding-agent harness using its ready-made templates. Copy and configure files yourself if you have access; otherwise provide exact terminal commands. Project: `<brief description or path>`.

**VI:** AI sẽ khảo sát dự án, hỏi những điều chưa rõ, trình **bảng thay đổi và trạng thái bảo vệ** để duyệt, rồi mới triển khai. Người dùng chỉ cần cung cấp thông tin/quyền thực sự cần thiết và phê duyệt.

**EN:** The AI inspects your project, asks only for missing information, presents an **adaptation and enforcement table** for approval, then implements the setup. The user only supplies necessary information/access and makes approval decisions.

---

## Dành cho AI — đọc kỹ / For AI agents — required reading

### Vai trò / Your role

**VI:** Bạn là **Environment Architect**. Nhiệm vụ: thiết lập môi trường làm việc của coding agents trong **dự án đích**, không phải viết code sản phẩm hay tự lập lý thuyết sản phẩm. **Không sửa repo bootstrap** khi đang setup dự án khác; chỉ thao tác trong project được user chỉ định.

**EN:** You are the **Environment Architect**. Configure the coding-agent environment in the **target project**. Do not implement product features or invent product theory. **Do not change this bootstrap repository** while setting up another project; operate only in the user-designated project.

**VI:** Planner xử lý nội dung sản phẩm trong hai chế độ: **Discovery** (brainstorm/research cùng user, ghi `OPEN` trong CRITERIA) và **Delivery** (sau khi được duyệt, lập GOALMAP, milestone và task). Bootstrap chỉ thiết lập khả năng hoạt động của Planner.

**EN:** Planner handles product content in two modes: **Discovery** (brainstorm/research with the user and record `OPEN` items in CRITERIA) and **Delivery** (derive GOALMAP, milestones and tasks after approval). Bootstrap only enables the Planner's environment.

### Một cây template duy nhất / Single canonical template tree

**VI:** **Nguồn duy nhất để cài:** [`project-template/`](project-template/). Copy **nội dung** của nó vào project root, không copy thành một thư mục con tên `project-template`. Chỉ lấy các file phù hợp tier và không ghi đè tùy tiện dữ liệu hiện có.

**EN:** **Single installation source:** [`project-template/`](project-template/). Copy its **contents** to the target project root, not as a nested `project-template` directory. Select tier-appropriate files and do not overwrite existing work blindly.

```text
project-template/
  AGENTS.md                         # reusable Codex guidance; tailor project facts
  README.md                         # project-specific content to complete
  SETUP.md / CODEX_READY.md
  TASKS.md                          # Planner derives from approved goals
  docs/
    CRITERIA.md                     # ONLY source of product theory; GOALMAP inside
    PROJECT_PROFILE.md
    ARCHITECTURE.md
    MILESTONES.md / BACKLOG.md / TRACE.md
    reports/
  .agents/
    roles/                          # reusable Planner, Reviewer, Critic, Coder, Tester...
    skills/                         # reusable generic SKILL.md, including brainstorming
    config/                         # optional role, model, skill/knowledge settings
    knowledge/                      # optional project/host/dialect references
  .codex/config.toml                # Codex starter config
  harness/
    codex/                          # doctor.py, verify.py, checks.json, sample tests
    specs/                          # gate, hook, approval, loop, trace, snapshot contracts
    HARNESS_SPEC.md
  lessons/
```

**VI:** Mặc định **Codex-first**: sử dụng ngay nội dung generic `AGENTS.md`, `.agents/roles/`, `.agents/skills/` và script nền `doctor.py`/`verify.py`. Các script nền chưa tương đương một hệ thống hook/gate/approval/loop đầy đủ. Native named subagent vẫn phải được đăng ký/xác minh theo phiên bản Codex.

**EN:** **Codex-first by default**: reuse generic `AGENTS.md`, `.agents/roles/`, `.agents/skills/` and baseline `doctor.py`/`verify.py` scripts. Baseline scripts are **not** a complete hook/gate/approval/loop system. Native named subagents still require version-specific registration and verification.

**VI:** Với Claude Code, GitHub Copilot, Cline hoặc runtime khác, **giữ logic generic** và chỉ chuyển đổi phần đặc thù: entrypoint, agent/skill discovery, model, hook, quyền, shell/script và approval channel.

**EN:** For Claude Code, GitHub Copilot, Cline or another runtime, **preserve reusable logic** and adapt only runtime-specific integration: entrypoints, agent/skill discovery, models, hooks, permissions, shell/scripts and approval channels.

### Nguyên tắc cốt lõi / Non-negotiable principles

1. **VI:** Copy rồi chỉnh; không viết lại các phần generic. Chỉ tạo file mới khi template không đáp ứng và phải nêu lý do. **EN:** Copy and adapt; never rewrite generic components without a demonstrated gap.
2. **VI:** Không sửa repo bootstrap khi setup nơi khác. **EN:** Do not modify the bootstrap source repository while installing into another project.
3. **VI:** `docs/CRITERIA.md` là **nguồn sự thật sản phẩm duy nhất**, GOALMAP ở trong đó. Không tạo bản lý thuyết song song. **EN:** CRITERIA is the sole product-theory source, including GOALMAP; never create parallel specifications.
4. **VI:** Phê duyệt qua request human-only, không qua chat "ok"; agent không tự trả lời hoặc sửa sổ duyệt. **EN:** Human-only approval requests are mandatory for protected decisions; agents cannot authorize themselves or tamper with ledgers.
5. **VI:** Điều cần cưỡng chế dùng guard/script/permission thực, phần cần phán đoán dùng Reviewer/CR; instruction thuần túy là `GUIDED_ONLY`. **EN:** Technical enforcement requires working guards; judgment belongs to reviewers; prompts alone are GUIDED_ONLY.
6. **VI:** Mỗi thành phần phải ngăn một lỗi xác định; tránh thừa. **EN:** Every component must prevent a specific failure; avoid unnecessary scaffolding.
7. **VI:** Không mặc định push hoặc gọi mạng từ script/hook; không destructive Git, cài dependency/MCP hoặc đọc secret khi chưa được phép. **EN:** No default push, networked hook, destructive Git, unapproved dependency/MCP install or secret exposure.
8. **VI:** Không âm thầm đổi model; model không có → `UNAVAILABLE`. **EN:** Never silently substitute unavailable models.
9. **VI:** Kiểm tra docs chính thức của runtime/version/host; không trộn schema Codex với Claude/Copilot/Cline. **EN:** Verify the actual runtime/version/host schemas; never mix tool-specific formats.
10. **VI:** Mâu thuẫn template/dự án phải đưa vào bảng thay đổi, không tự chọn. **EN:** Escalate conflicting template/project instructions in the adaptation table.
11. **VI:** Coder/Tester vẫn chạy với generic skill khi không có knowledge bổ sung; host/dialect bắt buộc vẫn phải tuân thủ. **EN:** Coder/Tester retain generic fallback without optional specialist knowledge while honoring mandatory compatibility.
12. **VI:** Template có file không có nghĩa hệ thống đã chạy. `READY`, `CONFIGURE`, `IMPLEMENT`, `ENFORCED`, `GUIDED_ONLY`, `UNVERIFIED` phải trung thực. **EN:** File presence never proves execution or enforcement; label readiness honestly.

### Quy trình / Setup workflow

#### Bước 0 — Phân loại / Step 0 — Classify

- **A — Existing code / Đã có code:** inspect source, Git, docs, tests and existing configuration; do not invent current behavior as approved theory.
- **B — Approved product specification / Đã có đặc tả duyệt:** use it as context; Planner maps approved theory to CRITERIA; Bootstrap does not rewrite product logic.
- **C — Empty or unapproved theory / Dự án trống:** enable **minimal Planner Discovery Mode** (brainstorm, research, CRITERIA placeholder and an available human decision path). Do not stop exploration or pretend the full harness, stack or product plan is approved.

#### Bước 1 — Thu thập thông tin / Step 1 — Intake

**VI:** Xem thông tin đã có rồi chỉ hỏi phần còn thiếu: tier Lite/Standard/Full; runtime/version (mặc định Codex), OS/shell; Git/remote/branch; loại sản phẩm/host/stack; real integration tests; verified models/tools; dialect/API/nguồn chính thức; ngôn ngữ báo cáo; approval channel. Với C, chỉ hỏi những gì cần cho Discovery tối thiểu.

**EN:** Inspect existing information before asking. Gather only missing facts: tier (Lite/Standard/Full), runtime/version (Codex default), OS/shell, Git/remote/branch, product type/host/stack, real integration tests, available models/tools, mandatory dialect/API and official references, reporting language, and approval channel. For case C, minimize intake to what Discovery needs.

**VI:** Runtime không có hook hoặc đường human-only có thể không thể bảo đảm journal/approval integrity; đánh dấu `GUIDED_ONLY` và đề xuất giải pháp phù hợp. **EN:** Runtimes without hooks or human-only controls may be unable to enforce journal/approval integrity; disclose `GUIDED_ONLY` and a practical alternative.

#### Bước 2 — Đề xuất trước khi sửa / Step 2 — Propose before modifying

**VI:** Kiểm kê template và project hiện hữu. Trình bảng:

**EN:** Inventory templates and the existing project. Present this table:

| Template | Target path / Đường dẫn đích | Action / Hành động | Reason / Vì sao | Required adaptation / Cần sửa |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | `AGENTS.md` | reuse / tailor | agent workflow | verified commands |
| `.agents/skills/*` | runtime-native path | reuse / adapt | generic expertise | discovery/config if needed |
| `harness/specs/*` | `harness/specs/` | use as contract | guard/loop behavior | runtime implementation |

**VI:** Đính kèm tier, ma trận vai → model/reasoning/quyền, bảng `ENFORCED/GUIDED_ONLY/UNVERIFIED/NOT_CONFIGURED`, xung đột, rollback, và các ca kiểm thử. Gửi Approval Request loại `HARNESS_PATCH` rồi dừng trước khi thay đổi. Khi chính kênh duyệt chưa được cài, trình bảng trong chat để user quyết định setup ban đầu, **công bố rõ đây chưa phải approval được cưỡng chế**.

**EN:** Include tier, role/model/reasoning/permissions matrix, enforcement status, conflicts, rollback and test cases. Submit a `HARNESS_PATCH` Approval Request before changes. If the approval channel itself does not yet exist, present the initial plan in chat and explicitly disclose that this is **not technically enforced approval**.

#### Bước 3 — AI triển khai / Step 3 — AI installs and adapts

**VI:** **AI thực hiện copy/cấu hình, không giao người dùng tự tìm file.** Nếu có filesystem/terminal phù hợp, AI copy những file đã duyệt vào project root, merge cẩn thận phần đang có, chỉnh các dữ kiện dự án và kiểm tra diff. Nếu không có quyền ghi, AI cung cấp lệnh terminal **đúng OS/shell, repo/path/branch đích** để user chạy và yêu cầu kết quả thực tế nhằm tiếp tục xác minh; không đưa lệnh nguy hiểm hoặc giả định đường dẫn.

**EN:** **The AI handles copying/configuration rather than asking the user to locate template files.** With filesystem/terminal access, the AI installs approved files into the project root, preserves existing work, fills verified project facts and reviews the diff. Without write access, the AI supplies **exact OS/shell- and path-specific terminal commands** for the user, then checks the resulting output. Never guess paths or provide unsafe blanket overwrite commands.

**VI:** Giữ nguyên reusable agents/skills khi dùng được. Điền `PROJECT_PROFILE` bằng host, version, dialect/API và lệnh test có thật. Bootstrap chỉ tạo khuôn CRITERIA, MILESTONES, TASKS, BACKLOG; Planner điền lý thuyết/plan sau khi được duyệt. `AGENTS.md` cuối cùng chỉ đề cập vai, gate, hook và lệnh đã thực sự cấu hình. Dùng script Codex có sẵn khi phù hợp, bổ sung phần runtime thiếu theo `harness/specs/`. Không biến `NOT_CONFIGURED` thành PASS.

**EN:** Reuse agents/skills unchanged whenever applicable. Populate `PROJECT_PROFILE` with verified host/version/dialect/API and real test commands. Bootstrap prepares product-theory/planning placeholders; Planner fills them after approval. The final `AGENTS.md` references only installed commands, agents, gates and hooks. Use existing Codex scripts where applicable and implement missing runtime integrations from `harness/specs/`. Never report NOT_CONFIGURED as PASS.

#### Bước 4 — Kiểm thử / Step 4 — Validate

**VI:** Thử bằng bản sao với dữ liệu giả; theo [`harness/specs/TESTS.md`](project-template/harness/specs/TESTS.md). Với mỗi guard, chứng minh cả ca **vi phạm bị chặn** và ca **hợp lệ được phép**. Kiểm tra role/skill activation, verify, approval và loop/gate đúng tier. Thiếu môi trường → `UNVERIFIED`, không báo đã chạy.

**EN:** Test on a disposable copy with fake data, following the tier-specific [test contract](project-template/harness/specs/TESTS.md). For each guard prove both a blocked invalid action and a permitted valid one. Verify role/skill activation and installed gates/loops/approvals. If a check cannot run, mark UNVERIFIED.

#### Bước 5 — Báo cáo / Step 5 — Report

**VI:** Báo cáo ngắn: đã copy/cấu hình gì; mỗi thành phần chống lỗi nào; enforcement thực tế; ma trận vai/model; kết quả script/hook và bằng chứng; thứ chưa test; cách dùng hằng ngày (tối đa năm dòng); bước cần user thực hiện tiếp.

**EN:** Report what was installed/adapted, why it exists, actual enforcement, role/model matrix, observed test evidence, unverified items, daily usage (at most five lines), and any remaining user action.

---

## Các tầng / Tiers

| Tier / Tầng | Intended use / Mục đích | Components / Thành phần |
| --- | --- | --- |
| **Lite** | Small projects / dự án nhỏ | AGENTS, CRITERIA + GOALMAP framework, verify, snapshot, Stop hook where supported, lessons, evidence, journal, approval inbox, Coder + Reviewer |
| **Standard** | Most projects / dự án vừa | Lite + Planner, Tester, Critic, milestones and G0–G11, trigger-based review/repair, G13 trace, decision log |
| **Full** | Larger/higher-risk / dự án lớn | Standard + G14, G12 Git Admin, harness-fixer, doctor/self-test, weakening detector |

**VI:** Chỉ cài cơ chế thuộc tier đã duyệt. Nếu script/hook không được triển khai hoặc không được hỗ trợ, ghi trạng thái thực tế; không coi bảng tier là bằng chứng đã cài. Nâng tier phải qua `HARNESS_PATCH`.

**EN:** Install only the approved tier's mechanisms. If scripts/hooks are unavailable or not implemented, disclose their real state; a tier table is not proof of installation. Tier upgrades require `HARNESS_PATCH`.

---

## Điều chỉnh thường và thay đổi được bảo vệ / Ordinary vs protected changes

| Usually configurable / Được cấu hình theo dự án | Protected; approval required / Phải được duyệt |
| --- | --- |
| Project name/paths and verified build/test/lint commands | Role write permissions, deny-lists, protected paths |
| Host, OS, dialect/API and version references | Gate semantics, escalation thresholds, guard weakening |
| Runtime-specific syntax and integrations | Push policy, approval validation and ledger integrity |
| Applicable optional specialist knowledge | Verified model assignment changes and sensitive hook settings |
| Reporting language and project docs | Removal/weakening of critical protections |

**VI:** Nếu thay đổi làm giảm khả năng chặn hoặc cho agent thêm quyền, không áp dụng dưới danh nghĩa sửa placeholder. **EN:** Any permission expansion or guard weakening is a protected policy change, never a routine placeholder edit.

---

## Khi bị chặn / When blocked

**VI:** Đọc thông báo `BLOCK` gồm mã, rule, nơi định nghĩa, lý do, bằng chứng và điều kiện mở khóa. Nếu harness cấu hình sai, dùng doctor hoặc harness-fixer (Full) và test hồi quy. Sửa đúng ý định đã duyệt, **không nới luật để qua chặn**. Trường hợp đặc biệt chỉ mở khóa một lần qua `BREAK_GLASS`.

**EN:** Read the `BLOCK` code, rule, source location, reason, evidence and authorized unlock path. If a harness defect is suspected, use doctor or Full-tier harness-fixer with regression tests. Repair against approved intent, **never weaken protections to bypass a block**. Exceptional one-time overrides require `BREAK_GLASS`.

---

## License / Giấy phép

MIT — see [LICENSE](LICENSE).
