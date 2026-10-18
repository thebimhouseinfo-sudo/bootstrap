# bootstrap: bộ template harness cho coding agent

[**Tiếng Việt**](README.md) | [English](README.en.md)

> **Trạng thái kiểm thử & phát hành:** Template hiện đã **test pass** khi cấu hình cho **Google Antigravity IDE** và **Codex** (bộ cài đặt, script nền, inventory, verify, snapshot, hooks/roles/skills cho hai runtime này đã được kiểm thử và xác nhận). **Các coding agent khác (Claude Code, Continue, Copilot, Cline...) chưa được Human kiểm thử do chưa có môi trường cài đặt; không tự suy ra là không tương thích.** AI khi thiết lập cần **tự kiểm tra và tự sửa/cấu hình theo hướng dẫn trong template** để phù hợp với platform của mình. Kiểm tra trạng thái bằng `python harness/common/status.py --tier Standard --runtime antigravity` (hoặc `--runtime codex`). Xem chi tiết tại `project-template/harness/specs/READINESS.md`.

Repo này là **bộ template harness có sẵn** cho coding agent. Hiện tại, template đã **test pass** khi cấu hình cho **Google Antigravity IDE** và **Codex**; các coding agent khác hiện chưa được kiểm thử trên máy của Human nên cần AI tự xác minh và điều chỉnh theo runtime tương ứng. Người dùng chỉ đưa link repo và mô tả ngắn về dự án cho AI. **AI tự đọc, khảo sát dự án, trình phương án để duyệt, rồi tự copy và cấu hình template**. Nếu không có quyền truy cập file hoặc terminal, AI phải đưa **lệnh terminal chính xác cho hệ điều hành, shell và đường dẫn dự án**, rồi kiểm tra kết quả. Người dùng không phải tự tìm hay chọn file template.

**Không thiết kế lại harness từ đầu, không viết lại agent/skill generic.** Mọi kết quả phải có bằng chứng kiểm thử thực tế. Những quyết định được bảo vệ cần **Approval Request ba lựa chọn: Đồng ý / Không đồng ý / Khác**. Ngoại lệ khi kênh duyệt chưa được cài trong lần bootstrap đầu tiên phải được công bố rõ.

---

## Dành cho người dùng

Gửi cho AI link repo này cùng yêu cầu:

> Đọc README của `https://github.com/thebimhouseinfo-sudo/bootstrap`. Hãy dùng template có sẵn để thiết lập harness cho dự án này. Tự copy và cấu hình nếu có quyền, nếu không thì đưa lệnh terminal chính xác để tôi chạy. Dự án: `<mô tả hoặc đường dẫn>`.

AI sẽ khảo sát những thứ đã có, chỉ hỏi thông tin còn thiếu, trình **bảng chỉnh sửa và enforcement** để người dùng duyệt, rồi mới triển khai. Người dùng không phải copy file thủ công.

### File local của agent và GitHub

Khi cài vào dự án đích, installer tự thêm/cập nhật một block có đánh dấu ở cuối `.gitignore`, giữ nguyên rule sẵn có. Các thư mục `.agents/`, `.antigravity/`, `.codex/`, `.claude/`, `.continue/`, `harness/`, `lessons/`, file hướng dẫn/task local và profile/trace/template báo cáo của agent được giữ local. Source, README và tài liệu sản phẩm như CRITERIA, ARCHITECTURE, MILESTONES, BACKLOG vẫn được theo dõi; không ignore toàn bộ `docs/`.

Dry-run hiện `UPDATE .gitignore` nếu cần; chỉ `--apply` mới ghi. File local đã tracked được báo `TRACKED_LOCAL_SETUP`, exit 2 để xử lý trước khi publish; installer không tự xóa file, sửa index hoặc lịch sử Git. Ignore bảo vệ các lần `git add` thông thường, không thay thế kiểm tra diff trước push. Riêng trong repo bootstrap, `project-template/` là source phân phối nên vẫn được version đầy đủ; block local-only chỉ được sinh ở dự án đích.

Trong dự án Git, sau khi cập nhật rule, installer dùng `git check-ignore` kiểm tra hiệu lực thật. Nếu `.gitignore` ở thư mục con mở lại file local, installer báo `LOCAL_SETUP_NOT_IGNORED` và dừng trước khi copy setup. Lỗi quyền/index/metadata Git không bị coi là “chưa có Git”. Với dự án chưa `git init` hoặc chưa có Git, cần chạy lại kiểm tra sau khi tạo repository.

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
  harness/
    common/                   # verify + inventory cho mọi runtime
    codex/                    # Codex preflight
    claude/                   # Claude Code adapter
    specs/
    HARNESS_SPEC.md
  lessons/
```

- **Google Antigravity IDE (đã được Human test trên máy):** skills và roles được nạp native từ `.agents/skills/` và `.agents/roles/`; model assignment theo vai nằm ở `.antigravity/agents/*.md` (với fallback Gemini 3.8 Flash High); lifecycle hooks ở `.agents/hooks.json` (Stop dispatch tới `harness/common/verify.py`).
- **Codex (đã test pass):** các subagent TOML tại `.codex/agents/*.toml` và model theo vai đã được cấu hình sẵn; native hook adapter tại `.codex/hooks.json` gọi `harness/codex/hook.py`; verifier/inventory chạy từ `harness/common/`.
- **Các coding agent khác (chưa được Human kiểm thử thực tế):** Claude Code (adapter `.claude/` và `harness/claude/hook.py`), Continue (`.continue/agents/`), GitHub Copilot, Cline... hiện **chưa có kết quả kiểm thử thực tế của Human**. **AI nhận nhiệm vụ trên các platform này phải tự kiểm tra khả năng thực tế của platform và tự sửa/hoàn thiện cấu hình theo hướng dẫn có sẵn trong template** (xem `project-template/SETUP.md`, `project-template/AGENTS.md`, `project-template/harness/specs/READINESS.md`): điều chỉnh cách đăng ký agent, định dạng cấu hình, đường dẫn skill, mapping model khả dụng, native lifecycle hooks (hoặc ghi rõ `GUIDED_ONLY` nếu platform không hỗ trợ hook cưỡng chế) và kênh duyệt. **Có file trong thư mục không chứng minh subagent đã được runtime nạp hay hook đã hoạt động.** Phải chạy kiểm tra thực tế trước khi tuyên bố kích hoạt.

### Nguyên tắc cốt lõi (không được nới)

1. **Sao chép rồi chỉnh, không viết lại.** Chỉ bổ sung file khi template thật sự thiếu, và giải thích lý do.
2. **Không sửa repo bootstrap này** khi setup dự án khác.
3. **Một nguồn sự thật:** `docs/CRITERIA.md`, có GOALMAP bên trong. Không tạo bản lý thuyết song song.
4. **Duyệt bằng request human-only**, không bằng chat “ok”. Agent không được tự trả lời request hoặc sửa journal, decisions, approvals.
5. **Việc cần chắc chắn dùng guard/script/hook**, việc cần phán đoán dùng Reviewer/CR. Hướng dẫn thuần prompt phải ghi `GUIDED_ONLY`, không nhận là `ENFORCED`.
6. **Tối giản:** mỗi thành phần phải chống một lỗi xác định.
7. **Không mặc định push hoặc gọi mạng trong hook.** Không tự ý `git init`, force-push, `reset --hard`, rewrite history, xóa nhánh chưa rõ, cài dependency/MCP hoặc lộ secret.
8. **Không tự đổi model.** Model không có ghi `UNAVAILABLE`.
9. **Đọc tài liệu chính thức** của runtime, hệ điều hành, host và phiên bản; không trộn schema Codex/Claude/Copilot/Cline.
10. **Mâu thuẫn giữa template và dự án** phải đưa vào bảng chỉnh sửa, không tự đoán chọn.
11. **Coder/Tester chạy được bằng generic skill** dù chưa có knowledge chuyên biệt; vẫn phải tuân thủ ràng buộc host/dialect bắt buộc.
12. **Phân biệt trạng thái trung thực:** READY, CONFIGURE, IMPLEMENT, ENFORCED, GUIDED_ONLY, NOT_CONFIGURED, UNVERIFIED không thể thay thế nhau.
13. **AI tự kiểm tra và điều chỉnh theo platform của mình:** Template đã test pass cho Antigravity IDE và Codex. Với các platform khác (chưa được Human test trên máy), AI có trách nhiệm tự đọc hướng dẫn trong template, khảo sát cơ chế của runtime mình đang chạy, tự sửa và hoàn thiện cấu hình phù hợp, không chuyển gánh nặng cấu hình kỹ thuật sang người dùng.

### Quy trình

**Không có runtime primary hoặc mặc định.** AI xác định runtime thực tế trong bước Pre-Ask; khi gọi CLI phải truyền rõ `--runtime`. Kết quả Human test Codex/Antigravity không tự chứng minh gate, hook hay orchestration đã ENFORCED trong mọi phiên bản.

#### Bước 0. Pre-Ask — gom tất cả câu hỏi cấu hình vào một lần duy nhất

**Trước khi khảo sát, lập kế hoạch hay hiển thị bất kỳ dialog nào**, AI hỏi toàn bộ thông tin cần thiết trong **một tin nhắn duy nhất**. Không tách ra hỏi dần theo bước — câu hỏi cấu hình xen vào giữa dialog xin quyền khiến người dùng nhấn nhầm theo thói quen.

Các mục cần xác nhận (gộp gọn, bỏ những gì đã biết từ context):

1. **Tầng:** Lite / Standard / Full (mặc định Standard).
2. **Runtime:** Antigravity IDE / Codex / Claude Code / Continue — phiên bản, OS và shell (vd. PowerShell trên Windows).
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

**AI chịu trách nhiệm copy, không giao user tự tìm file.** Dùng `python install.py --target PATH --tier Standard --runtime RUNTIME` (chọn rõ `antigravity`, `codex`, `claude` hoặc `continue`) để xem trước, và thêm `--apply` sau khi được duyệt. Các lựa chọn runtime là `antigravity`, `codex`, `claude`, `continue`; tier là `Lite`, `Standard`, `Full`. Nếu có quyền filesystem/terminal, AI copy nội dung template đã duyệt vào root dự án, bảo toàn file hiện hữu, điền dữ kiện có chứng cứ và soát diff. Nếu không có quyền ghi, AI đưa lệnh **chính xác theo OS/shell/repo/đường dẫn đã xác nhận** để người dùng chạy rồi kiểm tra output. Không đoán đường dẫn hoặc đưa lệnh ghi đè hàng loạt nguy hiểm.

Giữ nguyên role và skill generic khi phù hợp. Điền PROJECT_PROFILE bằng host/version/dialect/API và build/test command đã xác minh. Với Antigravity IDE và Codex, cấu hình đã test pass nên có thể dùng ngay sau khi điền thông số dự án. Với các coding agent khác chưa được Human kiểm thử, AI phải tự kiểm tra và sửa cấu hình theo hướng dẫn trong `project-template/SETUP.md` và `harness/specs/` để tương thích với platform của mình. Bootstrap chỉ dựng khuôn CRITERIA, MILESTONES, TASKS, BACKLOG; Planner hoàn thiện lý thuyết và kế hoạch sau duyệt. AGENTS.md cuối cùng chỉ nhắc các vai, gate, hook và lệnh thực sự được cấu hình. Không biến NOT_CONFIGURED thành PASS.

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

**Codex và Google Antigravity IDE (đã được Human test trên máy):**
- **Antigravity IDE:** `.agents/hooks.json` khai báo Stop hook → `harness/common/verify.py`; roles và skills được nạp native từ `.agents/roles/` và `.agents/skills/`; model assignment theo vai ở `.antigravity/agents/*.md` (Gemini 3.8 Flash High fallback).
- **Codex:** `.codex/hooks.json` gọi `harness/codex/hook.py`; subagents nạp từ `.codex/agents/*.toml`.
- Python chung nằm tại `harness/common/` (inventory, status, verify, snapshot, task, branch_authority).

**Các coding agent khác (chưa được Human kiểm thử trên máy):**
- **Claude Code:** `.claude/settings.json` + `harness/claude/hook.py` (adapter sơ bộ).
- **Continue, Copilot, Cline, Cursor...:** chưa hoàn thiện cấu hình native hoặc chưa smoke-test thực tế.
- **Yêu cầu đối với AI:** Khi triển khai trên các platform này, AI cần tự kiểm tra và sửa đổi cấu hình theo hướng dẫn trong template (`project-template/SETUP.md`, `project-template/harness/README.md`, `project-template/harness/specs/READINESS.md`) để thích ứng với nền tảng của mình, sau đó chạy smoke-test xác minh trước khi tuyên bố READY.

### Nhánh phát triển chính và đóng băng main

Bootstrap cung cấp `harness/common/branch_authority.py` cho **mọi tier có Git**. Human chọn nhánh phát triển chính (ví dụ `v5`), các nhánh đóng băng (như `main`) và work branch được phép; policy sống trong Git common directory nên không bị đổi theo checkout. Planner/Coder phải kiểm tra trước khi lập kế hoạch/sửa code và trước khi merge/push; không được tự suy luận `main`. Trong Codex, `PreToolUse` chặn direct apply_patch khi checkout không hợp lệ. Không bao phủ mọi shell/MCP/GitHub API hoặc ngăn push phía server; cần branch protection thực để khóa remote. Xem [BRANCH_AUTHORITY.md](project-template/harness/specs/BRANCH_AUTHORITY.md).
