# Bootstrap — harness template cho coding agents

[**Tiếng Việt**](README.md) | [English](README.en.md)

**Bootstrap** là bộ **harness template** giúp thiết lập môi trường dự án chuẩn mực, nhất quán cho các AI coding agent như **Codex, Google Antigravity, Claude Code, Continue, Cline, Qwen Code, Cursor và Copilot**.

Template cung cấp sẵn **vai trò agent, skill, workflow, script và hook** để AI tái sử dụng, chỉ tùy chỉnh theo từng dự án thay vì xây dựng lại từ đầu.

---

## Hướng dẫn sử dụng

### 1. Lần đầu: copy prompt để AI thiết lập harness

Mở coding agent bạn định dùng, rồi **copy prompt này vào chat**. Thay phần `<...>` bằng thông tin dự án; nếu chưa biết, để AI hỏi trong một lần. Không cần tự tìm hoặc copy file từ `project-template/`.

> Đọc `https://github.com/thebimhouseinfo-sudo/bootstrap` và dùng `project-template/` để thiết lập harness cho dự án `<tên, đường dẫn hoặc link repo, mô tả ngắn>`. Khảo sát dự án, hỏi gộp những thông tin còn thiếu (runtime, tier, Git branch, cấu hình local/tracked, build/test), rồi trình các thay đổi dự kiến để tôi duyệt. Sau khi duyệt, tự cài và kiểm tra nếu có quyền; nếu không, đưa lệnh chính xác để tôi chạy. Không viết code sản phẩm trong bước bootstrap. Cuối cùng báo rõ những gì đã cài, đã kiểm thử và chưa xác minh.

AI sẽ xem trước thay đổi trước khi chạy `--apply`, tránh ghi đè file hiện có và báo kết quả. **Cài harness xong mới chuyển sang công việc sản phẩm**; việc copy template không đồng nghĩa CRITERIA, task và môi trường test riêng của dự án đã hoàn chỉnh.

### 2. Sau khi setup: làm rõ yêu cầu, lập kế hoạch, triển khai

Tiếp tục ngay trong chat cũ hoặc mở chat mới tại thư mục dự án đã cài harness. Gửi:

> Đọc `AGENTS.md`, `docs/CRITERIA.md`, `docs/PROJECT_PROFILE.md`, `TASKS.md` và cấu hình nhánh Git của dự án. Nếu chưa có CRITERIA được duyệt, dùng Planner Discovery để brainstorm, nghiên cứu và soạn yêu cầu cho tôi quyết định. Nếu đã có CRITERIA được duyệt, dùng Planner Delivery để lập GOALMAP, milestone và task. Chưa viết code sản phẩm khi chưa có phạm vi và task được duyệt.

Sau khi duyệt yêu cầu và task, giao việc cụ thể:

> Thực hiện task đã được duyệt trong `TASKS.md` theo harness. Dùng các vai Coder, Tester, Reviewer và các bước kiểm tra thực sự khả dụng; sửa lỗi, test lại, ghi bằng chứng và báo kết quả. Không tự nhận PASS hay ENFORCED nếu chưa kiểm tra thực tế.

### 3. Những lần sau: tiếp tục dự án, không bootstrap lại

Mở coding agent **tại thư mục dự án đã thiết lập**. Không cần dán lại prompt cài đặt cho mỗi phiên. Có thể bắt đầu bằng:

> Đọc `AGENTS.md`, `docs/CRITERIA.md`, `docs/PROJECT_PROFILE.md`, `TASKS.md`; kiểm tra nhánh phát triển hiện hành và trạng thái công việc. Tóm tắt tiến độ, vướng mắc, bước tiếp theo rồi tiếp tục phần đã được duyệt theo harness.

Nếu CRITERIA vẫn là bản nháp, tiếp tục Discovery, không tự chuyển sang coding. Role, hook và gate chỉ được coi là hoạt động đến mức đã xác minh trên runtime thực tế.

### Lưu cấu hình harness trong Git

Installer có hai chế độ thông qua `--config-git`:

- **`local` (mặc định):** giữ toàn bộ cấu hình agent và trạng thái chạy ở máy local, như hành vi cũ.
- **`tracked`:** đưa cấu hình harness vào Git để tái sử dụng giữa các máy, nhưng **không đưa dữ liệu trạng thái/duyệt riêng tư vào Git**.

**CONFIG (được Git theo dõi khi chọn `tracked`):** `AGENTS.md`, `AGENTS.bootstrap.md`, `CLAUDE.md`, `TASKS.md`, các thư mục `.agents/`, `.antigravity/`, `.codex/`, `.claude/`, `.continue/`, `.generic/`, `harness/`, `lessons/`, `docs/PROJECT_PROFILE.md`, cùng các template báo cáo trong `docs/reports/`. Đây là danh sách thành phần cấu hình *được phép* track, không có nghĩa mọi file bên trong đều bắt buộc phải commit.

**STATE (luôn giữ local, ngay cả ở chế độ `tracked`):** `harness/chat-journal.jsonl`, `harness/decisions.jsonl`, `harness/approvals.jsonl`, `harness/state.json`, `harness/last-block.json`, `harness/inbox.html`, `harness/snapshots/`, `harness/requests/`, `docs/TRACE.md`, `.claude/settings.local.json`.

Sổ duyệt `approvals` vẫn thuộc **một Human duy nhất**; chưa hỗ trợ đồng bộ/xác thực phê duyệt nhiều người qua Git. Những tài liệu sản phẩm như `docs/CRITERIA.md`, `ARCHITECTURE.md`, `MILESTONES.md` và `BACKLOG.md` tiếp tục được theo dõi trong Git ở cả hai chế độ.

```bash
python install.py --target PATH --tier Standard --runtime codex --config-git tracked
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --apply
# Đổi chế độ đã cài: phải thêm --change-config-git cho cả preview và --apply
```

Installer giữ nguyên marker `BEGIN/END` trong `.gitignore`, thêm `# mode: local|tracked` bên trong block. Bản cài cũ không có dòng `# mode:` được coi là `local`; chạy lại `--apply` sẽ bổ sung dòng này. Thay đổi chế độ mà thiếu `--change-config-git` bị chặn bằng `MODE_CHANGE_REQUIRES_APPROVAL` (exit 2); cần xem preview và được Human duyệt trước khi apply.

Installer kiểm tra file đã nằm trong Git index (`TRACKED_LOCAL_SETUP` ở `local`, `TRACKED_LOCAL_STATE` ở `tracked`) và hiệu lực thực tế của ignore bằng `git check-ignore` (`LOCAL_SETUP_NOT_IGNORED` / `LOCAL_STATE_NOT_IGNORED`). Các lỗi này dừng quá trình và không tự xóa file hay chỉnh Git index. **Lưu ý:** `--apply` ghi `.gitignore` trước bước kiểm tra ignore; nếu bị BLOCK vì exception ở thư mục con thì `.gitignore` đã được cập nhật nhưng chưa copy file template. Git không thể bỏ ignore một file con nếu đã ignore cả thư mục cha, vì vậy ở `tracked` chỉ ignore từng STATE path, không có quy tắc `/harness/` chung.

Cờ cũ `-y/--yes` chỉ để tương thích và **không có tác dụng**; muốn ghi file bắt buộc dùng `--apply`. Với dự án chưa có Git, cần kiểm tra lại quy tắc ignore sau khi `git init`. Trong repo Bootstrap, `project-template/` vẫn là mã nguồn phân phối được version đầy đủ; block quản lý ignore chỉ được sinh ở dự án đích.

---

## Dành cho AI: hướng dẫn bắt buộc

### Vai của bạn

Bạn là **Environment Architect**: khảo sát, đề xuất và, sau khi được duyệt, cấu hình **môi trường làm việc cho coding agents** của dự án đích. Bạn **không** đóng vai Product Planner: không tự chốt tính năng, roadmap, milestone, task hay viết code sản phẩm trong phiên bootstrap. **Không chỉnh repo bootstrap này** khi được giao setup một dự án khác.

Planner chủ động làm rõ nhu cầu và CRITERIA. **Technical Advisor** tư vấn độc lập cho Human: CRITERIA là căn cứ về yêu cầu; khi cần được xem hiện trạng kiến trúc, môi trường và phần source liên quan để đánh giá khả thi, độ phức tạp, chi phí, điều kiện tiên quyết và tác động tới những gì đã làm. Advisor không review Plan/Code, không chấm PASS/FAIL hay có quyền phủ quyết. Chỉ tư vấn toàn bộ CRITERIA trước lần duyệt đầu, hoặc delta đã bàn chốt trước khi sửa CRITERIA. **Tạm dùng – Ổn – Nâng cao chỉ dùng khi thực sự có nhiều phương án**, không ép đủ ba. Human quyết định, Planner ghi CRITERIA.

Planner phụ trách lý thuyết sản phẩm trong hai chế độ: **Discovery** (brainstorm/research với người dùng, ghi các vấn đề chưa chốt là `OPEN` trong CRITERIA) và **Delivery** (sau phê duyệt, lập GOALMAP, milestone, task). Bootstrap chỉ thiết lập môi trường để Planner hoạt động.

### Cây template canonical

Chỉ [`project-template/`](project-template/) là nguồn cài đặt. Copy **nội dung** vào root dự án đích, không tạo thêm thư mục con `project-template`. Kiểm tra những file hiện có và xin phê duyệt trước khi ghi.

```text
project-template/
  AGENTS.md
  SETUP.md
  TASKS.md
  docs/
    CRITERIA.md
    PROJECT_PROFILE.md
    ARCHITECTURE.md
    MILESTONES.md
    BACKLOG.md
    TRACE.md
    reports/
  .agents/
    roles/
    skills/
    config/
    knowledge/
    MODEL_SELECTION.md        # Antigravity model guide
    hooks.json                # Antigravity lifecycle hooks
  .antigravity/              # khi chọn Antigravity IDE
    agents/
  .codex/                   # khi chọn Codex
    config.toml
    agents/
  .claude/                  # khi chọn Claude Code
    agents/
    skills/
  .continue/                # khi chọn Continue
    agents/
  .generic/                 # khi chọn app chưa có adapter native
    agents/                 # role dùng chung, filter theo tier
    platforms/              # Cline / Qwen Code / DeepSeek-client
    PORTING.md
  harness/
    common/                   # verify + inventory cho mọi runtime
    codex/                    # Codex preflight
    claude/                   # Claude Code adapter
    specs/
    HARNESS_SPEC.md
  lessons/
```

- **Codex và Google Antigravity IDE — GENERIC READY:** Đã kiểm thử việc cài đặt và sử dụng template generic. Giữ nguyên các role/skill và adapter generic; không cần viết lại hoặc sửa template chỉ để khởi động workflow chung. Codex dùng `.codex/agents/*.toml`, `.codex/hooks.json`; Antigravity dùng `.agents/skills/`, `.agents/hooks.json`, `.antigravity/agents/*.md`. Cần bổ sung thông số dự án cụ thể sau khi cài.
- **Claude Code — đã cấu hình, chưa thử trên Claude Code:** Có `.claude/agents/`, `.claude/settings.json`, `harness/claude/hook.py`, skill/rules đã chuẩn bị. Không yêu cầu agent viết lại adapter generic chỉ vì chưa có máy test; khi host có sẵn, chạy smoke-test để xác minh.
- **Continue — gần READY:** Có `.continue/agents/`, role config/rules; **dùng chung `.agents/roles/`, `.agents/skills/` và Python helpers giống Antigravity**, khác phần cấu hình agent/model native. Cấu hình provider/model thực tế và chọn role config; xác minh các giới hạn hook/subagent của Continue trong VS Code. Không tự coi plugin Continue và Antigravity có cùng native APIs.
- **Cline, Qwen Code, client dùng DeepSeek, Copilot, Cursor và app khác:** Cài `--runtime generic --target-app APP`; dùng `.generic/agents` cùng `.generic/PORTING.md` và `platforms/` để chuyển đổi native. DeepSeek có thể chỉ là provider/model, phải xác định app thực tế. Dựa trên file/contract có sẵn, đối chiếu tài liệu platform rồi chỉ chuyển đổi những adapter hoặc hook cần thiết. Báo rõ phần `UNVERIFIED` / `GUIDED_ONLY`; không biến thiếu smoke-test thành kết luận không hỗ trợ.

### Nguyên tắc cốt lõi (không được nới)

1. **Tái sử dụng tối đa để tiết kiệm quota.** Với Codex/Antigravity, copy generic package và cấu hình phần riêng của dự án; không viết lại role/skill/script chung. Với Claude/Continue và app khác, chỉ điều chỉnh adapter hoặc mapping model thực sự cần thiết; chỉ bổ sung file khi template thiếu.
2. **Không sửa repo bootstrap này** khi setup dự án khác.
3. **Một nguồn sự thật:** `docs/CRITERIA.md`, có GOALMAP bên trong. Không tạo bản lý thuyết song song.
4. **Duyệt bằng request human-only**, không bằng chat “ok”. Agent không được tự trả lời request hoặc sửa journal, decisions, approvals.
5. **Việc cần chắc chắn dùng guard/script/hook**, việc cần phán đoán dùng Reviewer/CR. Hướng dẫn thuần prompt phải ghi `GUIDED_ONLY`, không nhận là `ENFORCED`.
6. **Tối giản:** mỗi thành phần phải chống một lỗi xác định.
7. **Không mặc định push hoặc gọi mạng trong hook.** Không tự ý `git init`, force-push, `reset --hard`, rewrite history, xóa nhánh chưa rõ, cài dependency/MCP hoặc lộ secret.
8. **Không tự đổi model.** Model không có ghi `UNAVAILABLE`.
9. **Không nghiên cứu lại setup generic đã READY nếu không có lỗi cụ thể.** Với Codex/Antigravity, ưu tiên copy rồi kiểm tra các thông số riêng dự án. Nếu khác phiên bản, có lỗi hoặc dùng nền tảng chưa thử, đối chiếu tài liệu chính thức của runtime/host/API; không trộn schema.
10. **Mâu thuẫn giữa template và dự án** phải đưa vào bảng chỉnh sửa, không tự đoán chọn.
11. **Coder/Tester chạy được bằng generic skill** dù chưa có knowledge chuyên biệt; vẫn phải tuân thủ ràng buộc host/dialect bắt buộc.
12. **Phân biệt trạng thái trung thực:** READY, CONFIGURE, IMPLEMENT, ENFORCED, GUIDED_ONLY, NOT_CONFIGURED, UNVERIFIED không thể thay thế nhau.
13. **Tương thích theo bằng chứng:** Codex và Antigravity GENERIC READY (Tested); Claude Code đã cấu hình đầy đủ nhưng thiếu host test; Continue gần READY, cần model/provider mapping và host test; runtime khác chỉ sửa adapter cần thiết dựa trên hướng dẫn. Không gán `ENFORCED` hoặc `RUNTIME_VERIFIED` nếu chưa có bằng chứng tương ứng.

### Quy trình

**Không có runtime primary hoặc mặc định.** AI xác định runtime thực tế trong bước Pre-Ask; khi gọi CLI phải truyền rõ `--runtime`. Kết quả kiểm thử Codex/Antigravity không tự chứng minh gate, hook hay orchestration đã ENFORCED trong mọi phiên bản.

#### Bước 0. Pre-Ask — gom tất cả câu hỏi cấu hình vào một lần duy nhất

**Có thể lấy nguyên bộ câu hỏi bằng `python install.py --ask-first`; lệnh chỉ in câu hỏi, không ghi file hay hỏi lần lượt trong terminal.** Trước khi khảo sát, lập kế hoạch hay gọi lệnh yêu cầu quyền truy cập, AI hỏi toàn bộ thông tin cần thiết trong **một tin nhắn duy nhất**. Không tách ra hỏi dần theo bước — câu hỏi cấu hình xen vào giữa dialog xin quyền khiến người dùng nhấn nhầm theo thói quen.

Các mục cần xác nhận (gộp gọn, bỏ những gì đã biết từ context):

1. **Tầng:** Lite / Standard / Full (mặc định Standard).
2. **Runtime:** Antigravity / Codex / Claude Code / Continue / **app khác (`generic`)**. Nếu app khác, hỏi tên client thực tế (Cline, Qwen Code, client dùng DeepSeek, ...) và phiên bản; DeepSeek là provider/model nếu chưa có client cụ thể. Hỏi OS/shell khi còn thiếu.
3. **Git:** có dùng không? remote/nhánh phát triển chính và nhánh đóng băng?
4. **Loại sản phẩm:** local/web/plugin/CLI/service — nền tảng/host cụ thể.
5. **Đặc tả hiện có:** tài liệu đã được chấp thuận? Dự án đang chạy thế nào?
6. **Stack:** đã xác định hay Planner cần discovery?
7. **Tích hợp & test thực:** host/thiết bị/tài khoản cần test thật.
8. **Model:** giữ mặc định (theo `.agents/MODEL_SELECTION.md`) hay tự chọn?
9. **Dialect/API đặc thù:** tài liệu chính thức, phiên bản, cách chạy thử.
10. **Ngôn ngữ báo cáo** (mặc định: Tiếng Việt cho tài liệu, tiếng Anh cho file/ID/lệnh).
11. **Kênh duyệt:** nút trong UI / lệnh terminal / `inbox.html`?

Chỉ sau khi nhận đủ câu trả lời mới chuyển sang bước tiếp theo.

#### Bước 1. Phân loại dự án và khảo sát (sau Pre-Ask)

- **A — Đã có code:** đọc code, cấu hình, test, tài liệu; nếu chưa có lý thuyết vận hành thì ghi rõ, không tự suy diễn thành yêu cầu đã duyệt.
- **B — Dự án mới đã có đặc tả được chấp thuận:** sử dụng đặc tả để xác nhận ràng buộc; Planner chuẩn hóa vào CRITERIA; Bootstrap không tự viết lại logic sản phẩm.
- **C — Dự án mới, chưa có lý thuyết:** kích hoạt **Planner Discovery Mode tối thiểu** (brainstorm, research, CRITERIA placeholder và kênh trao đổi/duyệt khả dụng). Không ép người dùng phải chốt lý thuyết trước khi khám phá. Chưa chọn stack cuối, chưa tạo task sản phẩm hoặc tuyên bố full harness đã có.

Với C, chỉ hỏi đủ cho Discovery tối thiểu. Runtime không có hook hoặc kênh human-only có thể không bảo đảm được journal/approval integrity: phải ghi `GUIDED_ONLY` và chỉ ra giải pháp thay thế.

#### Bước 2. Lập bảng chỉnh sửa và xin duyệt (chưa ghi file)

Kiểm kê cây template và file hiện có của dự án. Trình bảng:

| Template | Đường dẫn đích | Hành động | Lý do/chống lỗi gì | Cần tùy chỉnh |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | `AGENTS.md` | giữ/chỉnh/bỏ | quy trình agent | lệnh dự án đã xác minh |
| `.agents/skills/*` | đường dẫn skill của runtime | giữ/chỉnh/bỏ | kỹ năng tái sử dụng | đăng ký nếu cần |
| `harness/specs/*` | `harness/specs/` | giữ contract/triển khai | guard, gate, approval | script theo runtime |

Kèm tầng, ma trận vai → model/reasoning/quyền, bảng `ENFORCED/GUIDED_ONLY/UNVERIFIED/NOT_CONFIGURED`, mâu thuẫn, cách khôi phục và kế hoạch kiểm thử.

Gửi **Approval Request loại `HARNESS_PATCH`**, rồi dừng trước thay đổi được bảo vệ. Nếu kênh duyệt chưa tồn tại, trình kế hoạch trong chat để người dùng quyết định setup ban đầu, **nói rõ ngoại lệ này chưa phải phê duyệt được cưỡng chế kỹ thuật**.

#### Bước 3. AI tự copy, tùy chỉnh và triển khai

**AI chịu trách nhiệm copy, không giao user tự tìm file.** Dùng `python install.py --target PATH --tier Standard --runtime RUNTIME --config-git local` (hoặc `--config-git tracked`) (chọn rõ `antigravity`, `codex`, `claude`, `continue` hoặc `generic`). Với `generic`, **bắt buộc thêm `--target-app cline`** (hoặc `qwen-code`, `deepseek`, tên client khác) để xem trước, và thêm `--apply` sau khi được duyệt. Các lựa chọn runtime là `antigravity`, `codex`, `claude`, `continue`; tier là `Lite`, `Standard`, `Full`. Nếu có quyền filesystem/terminal, AI copy nội dung template đã duyệt vào root dự án, bảo toàn file hiện hữu, điền dữ kiện có chứng cứ và soát diff. Nếu không có quyền ghi, AI đưa lệnh **chính xác theo OS/shell/repo/đường dẫn đã xác nhận** để người dùng chạy rồi kiểm tra output. Không đoán đường dẫn hoặc đưa lệnh ghi đè hàng loạt nguy hiểm.

Với Codex và Antigravity, **copy template generic đã READY là dùng được ngay ở mức generic, không cần chỉnh sửa role/skill/script chung**. Sau đó điền PROJECT_PROFILE bằng host/version/dialect/API và build/test command đã xác minh để chạy đúng **dự án cụ thể**. Claude Code đã có cấu hình đầy đủ, cần kiểm tra trên host khi có điều kiện; Continue cần model/provider mapping rồi host smoke. App khác chỉ điều chỉnh phần adapter theo `project-template/SETUP.md` và `harness/specs/`, tránh tái tạo từ đầu để tiết kiệm quota. Bootstrap chỉ dựng khuôn CRITERIA, MILESTONES, TASKS, BACKLOG; Planner hoàn thiện lý thuyết và kế hoạch sau duyệt. AGENTS.md cuối cùng chỉ nhắc các vai, gate, hook và lệnh thực sự được cấu hình. Không biến NOT_CONFIGURED thành PASS.

#### Bước 4. Kiểm tra

Chạy trong bản sao với dữ liệu giả, theo [`harness/specs/TESTS.md`](project-template/harness/specs/TESTS.md). Mỗi ranh giới cần ca **vi phạm bị chặn** và ca **hợp lệ không bị chặn nhầm**. Kiểm tra kích hoạt agent/skill, verify, approval, hook, loop, gate đúng tier. Thiếu môi trường thì báo `UNVERIFIED`; không nói đã test khi chưa chạy.

#### Bước 5. Báo cáo ngắn cho người dùng

Nêu thành phần đã copy/cấu hình và mục đích chống lỗi; enforcement thực; ma trận role/model; từng bài test với bằng chứng; phần chưa kiểm tra; cách dùng hằng ngày (tối đa 5 dòng); việc còn cần người dùng quyết định.

---

## Các tầng áp dụng

| Tầng | Dành cho | Thành phần dự kiến |
| --- | --- | --- |
| **Lite** | Dự án nhỏ, một người | Mục tiêu: AGENTS, CRITERIA, verify, snapshot, evidence, Stop (nếu native được trust), các quy trình duyệt phù hợp. **Hiện có** script snapshot/verify; journal/approval inbox có xác thực chưa được triển khai. |
| **Standard** | Dự án vừa | Lite + Planner/Tester/CR, milestone + G0–G11, review/repair loop theo trigger, G13 trace, decision log đầy đủ |
| **Full** | Dự án lớn/rủi ro cao | Standard + G14, G12 Git Admin, harness-fixer, doctor/selftest, weakening detector |

Chỉ triển khai cơ chế của tier đã duyệt. Bảng tier không phải bằng chứng rằng hook hoặc gate đã hoạt động. Nâng tầng phải có `HARNESS_PATCH`.

---

## Được phép chỉnh và thay đổi được bảo vệ

| Thông tin cấu hình theo dự án | Cần `HARNESS_PATCH` được duyệt |
| --- | --- |
| Tên dự án, đường dẫn, lệnh build/test/lint đã xác minh | Quyền ghi theo vai, deny-list, vùng bảo vệ |
| Profile host, dialect/API, phiên bản | Ngữ nghĩa gate, ngưỡng leo thang |
| Cú pháp agent/hook theo runtime thực tế | Chính sách push, xác thực phê duyệt |
| Skill/knowledge chuyên biệt tùy chọn | Nới guard, thay đổi model đã được chốt |
| Ngôn ngữ báo cáo | Hook nhạy cảm và tính toàn vẹn sổ duyệt |

Nếu thay đổi cấp thêm quyền hoặc làm yếu ranh giới bảo vệ, không được ngụy trang dưới dạng điền placeholder.

---

## Khi bị chặn

Đọc thông báo `BLOCK`: mã, luật, nơi định nghĩa, lý do, bằng chứng và điều kiện mở khóa. Nếu nghi harness bị cấu hình sai, dùng inventory/preflight hoặc harness-fixer (Full), tái hiện lỗi và kiểm thử hồi quy. **Sửa để khớp ý định đã duyệt, không nới luật để qua chặn.** Trường hợp ngoại lệ cần request `BREAK_GLASS` giới hạn đúng một lần.

---

## Giấy phép

MIT. Xem [LICENSE](LICENSE).

### Trạng thái adapter theo mức generic

| Coding agent | Mức sẵn sàng template generic | Sau khi copy vào dự án |
| --- | --- | --- |
| **Codex** | **GENERIC READY — Tested** | Dùng cấu hình chung ngay; điền dữ kiện và kiểm thử riêng của dự án |
| **Google Antigravity IDE** | **GENERIC READY — Tested** | Tương tự Codex; không cần viết lại template generic |
| **Claude Code** | **Đã cấu hình đầy đủ; chưa có host test thực tế** | Test trên Claude Code khi có môi trường, bổ sung cấu hình dự án |
| **Continue** | **Gần GENERIC READY; chưa có host test thực tế** | Chọn provider/model và role config, xác minh giới hạn native |
| **Cline / Qwen Code / client dùng DeepSeek / Copilot / Cursor / khác** | **`.generic/` portable source, chưa được host-test** | Copy role theo tier, xem `PORTING.md`, chỉ modify adapter native, không viết lại toàn bộ |

Chi tiết adapter: Codex `.codex/` và `harness/codex/`; Antigravity `.agents/` và `.antigravity/`; Claude Code `.claude/` và `harness/claude/`; Continue `.continue/` và cùng core `.agents/roles`/`.agents/skills` với Antigravity (không copy hook Antigravity); app khác `.generic/`. Core Python dùng chung ở `harness/common/`.

**Lưu ý:** mức READY ở bảng này là *copy/use generic coding-agent template*, không phải tuyên bố gate engine, phê duyệt có xác thực hay host-level enforcement đã hoàn chỉnh. Cấu hình riêng cho sản phẩm/host vẫn bắt buộc để coding chính xác.

### Nhánh phát triển chính và đóng băng main

Bootstrap cung cấp `harness/common/branch_authority.py` cho **mọi tier có Git**. Human chọn nhánh phát triển chính (ví dụ `v5`), các nhánh đóng băng (như `main`) và work branch được phép; policy sống trong Git common directory nên không bị đổi theo checkout. Planner/Coder phải kiểm tra trước khi lập kế hoạch/sửa code và trước khi merge/push; không được tự suy luận `main`. Trong Codex, `PreToolUse` chặn direct apply_patch khi checkout không hợp lệ. Không bao phủ mọi shell/MCP/GitHub API hoặc ngăn push phía server; cần branch protection thực để khóa remote. Xem [BRANCH_AUTHORITY.md](project-template/harness/specs/BRANCH_AUTHORITY.md).

### Luồng cài adapter generic

`python install.py --ask-first` in một lần toàn bộ câu hỏi để AI đưa vào chat, không có prompt xin cấu hình trong terminal. Sau khi Human trả lời, AI chọn tier và client, chạy **preview** `python install.py --target PATH --tier Standard --runtime generic --target-app qwen-code`; sau khi Human duyệt mới thêm `--apply`. Bộ `.generic/` là **role source + hướng dẫn port**, chưa tự đăng ký native agent vào app chưa được test; việc chuyển đổi cần dựa trên native docs và host smoke. Với Continue, installer đã copy phần generic `.agents/roles`, `.agents/skills`, `harness/common` giống Antigravity, chỉ khác `.continue/` agent/model config; `.agents/hooks.json` của Antigravity không tự áp dụng cho Continue.
