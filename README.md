# bootstrap: bộ template harness cho coding agent

[**Tiếng Việt**](README.md) | [English](README.en.md)

Repo này là **bộ template harness có sẵn**, ưu tiên **Codex-ready**. Người dùng chỉ đưa link repo và mô tả ngắn về dự án cho AI. **AI tự đọc, khảo sát dự án, trình phương án để duyệt, rồi tự copy và cấu hình template**. Nếu không có quyền truy cập file hoặc terminal, AI phải đưa **lệnh terminal chính xác cho hệ điều hành, shell và đường dẫn dự án**, rồi kiểm tra kết quả. Người dùng không phải tự tìm hay chọn file template.

**Không thiết kế lại harness từ đầu, không viết lại agent/skill generic.** Mọi kết quả phải có bằng chứng kiểm thử thực tế. Những quyết định được bảo vệ cần **Approval Request ba lựa chọn: Đồng ý / Không đồng ý / Khác**. Ngoại lệ khi kênh duyệt chưa được cài trong lần bootstrap đầu tiên phải được công bố rõ.

---

## Dành cho người dùng

Gửi cho AI link repo này cùng yêu cầu:

> Đọc README của `https://github.com/thebimhouseinfo-sudo/bootstrap`. Hãy dùng template có sẵn để thiết lập harness cho dự án này. Tự copy và cấu hình nếu có quyền, nếu không thì đưa lệnh terminal chính xác để tôi chạy. Dự án: `<mô tả hoặc đường dẫn>`.

AI sẽ khảo sát những thứ đã có, chỉ hỏi thông tin còn thiếu, trình **bảng chỉnh sửa và enforcement** để người dùng duyệt, rồi mới triển khai. Người dùng không phải copy file thủ công.

---

## Dành cho AI: hướng dẫn bắt buộc

### Vai của bạn

Bạn là **Environment Architect**: khảo sát, đề xuất và, sau khi được duyệt, cấu hình **môi trường làm việc cho coding agents** của dự án đích. Bạn **không** đóng vai Product Planner: không tự chốt tính năng, roadmap, milestone, task hay viết code sản phẩm trong phiên bootstrap. **Không chỉnh repo bootstrap này** khi được giao setup một dự án khác.

Planner chủ động làm rõ nhu cầu, sản phẩm **personal-only / nội bộ / thương mại**, quy mô thật, rủi ro dữ liệu, mức bảo vệ cần thiết và những gì không xây; ghi vào bản CRITERIA dự thảo. Advisor **không làm intake**: chỉ kiểm **toàn bộ CRITERIA dự thảo lần đầu** ngay trước phê duyệt; hoặc kiểm **CRITERIA đang duyệt + nội dung thay đổi đã được human và Planner bàn, chốt** khi human yêu cầu áp dụng, **trước khi sửa file**. Advisor phân tích hệ thống kỹ thuật thực sự cần xây và **luôn đưa 3 mức Tạm dùng – Ổn – Nâng cao** (thành phần, giới hạn, độ phức tạp, công bảo trì, ảnh hưởng đến goal/task/test). Ví dụ “GitHub offline” có thể chỉ là yêu cầu thao tác file local và chạy test, không mặc định cần VM/bridge. Human chọn bất kỳ mức nào, kể cả Tạm dùng; Advisor không sửa CRITERIA hay ép chọn phương án nâng cao. Reviewer bám scope/loại sản phẩm để không phát sinh tính năng hoặc bảo mật enterprise vô cớ, nhưng cũng không bỏ sót nhu cầu mở rộng thực sự đã duyệt. Human chỉ cần đọc kết quả, giới hạn và tác động chứ không phải diff hoặc plan P1/P2/P3.

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
  .codex/                   # khi chọn Codex
    config.toml
    agents/
  .claude/                  # khi chọn Claude Code
    agents/
    skills/
  .continue/                # khi chọn Continue
    agents/
  harness/
    common/                   # verify + inventory cho cả ba runtime
    codex/                    # Codex preflight
    specs/
    HARNESS_SPEC.md
  lessons/
```

Với Codex, các subagent TOML và model theo vai đã được cấu hình sẵn; verifier/inventory chạy từ `harness/common/`. **Có file không chứng minh subagent đã được runtime nạp, hoặc hook/gate/approval tự động đã hoạt động.** Phải kiểm tra khả năng của đúng runtime trước khi tuyên bố được kích hoạt.

Với Claude Code, adapter agent và skills native được cài sẵn. Continue có template config theo vai và cần điền model/provider. Với Copilot, Cline và runtime khác, giữ nguyên logic generic, chỉ chỉnh phần tích hợp đặc thù: cách đăng ký agent, đường dẫn skill, model, quyền, hook, script, shell và kênh duyệt.

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

### Quy trình

#### Bước 0. Phân loại dự án

- **A — Đã có code:** đọc code, cấu hình, test, tài liệu; nếu chưa có lý thuyết vận hành thì ghi rõ, không tự suy diễn thành yêu cầu đã duyệt.
- **B — Dự án mới đã có đặc tả được chấp thuận:** sử dụng đặc tả để xác nhận ràng buộc; Planner chuẩn hóa vào CRITERIA; Bootstrap không tự viết lại logic sản phẩm.
- **C — Dự án mới, chưa có lý thuyết:** kích hoạt **Planner Discovery Mode tối thiểu** (brainstorm, research, CRITERIA placeholder và kênh trao đổi/duyệt khả dụng). Không ép người dùng phải chốt lý thuyết trước khi khám phá. Chưa chọn stack cuối, chưa tạo task sản phẩm hoặc tuyên bố full harness đã có.

#### Bước 1. Hỏi ngắn, bỏ thông tin đã biết

Kiểm tra hiện trạng trước rồi mới hỏi các mục còn thiếu: tầng Lite/Standard/Full (thường mặc định Standard), runtime và phiên bản (ưu tiên Codex), OS/shell, Git/remote/nhánh, loại sản phẩm/host/stack, khả năng kiểm thử tích hợp thật, model/tool khả dụng, dialect/API và tài liệu chính thức, ngôn ngữ báo cáo, kênh phê duyệt.

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

**AI chịu trách nhiệm copy, không giao user tự tìm file.** Dùng `python install.py --target PATH --tier Standard --runtime codex` để xem trước, và thêm `--apply` sau khi được duyệt. Các lựa chọn runtime là `codex`, `claude`, `continue`; tier là `Lite`, `Standard`, `Full`. Nếu có quyền filesystem/terminal, AI copy nội dung template đã duyệt vào root dự án, bảo toàn file hiện hữu, điền dữ kiện có chứng cứ và soát diff. Nếu không có quyền ghi, AI đưa lệnh **chính xác theo OS/shell/repo/đường dẫn đã xác nhận** để người dùng chạy rồi kiểm tra output. Không đoán đường dẫn hoặc đưa lệnh ghi đè hàng loạt nguy hiểm.

Giữ nguyên role và skill generic khi phù hợp. Điền PROJECT_PROFILE bằng host/version/dialect/API và build/test command đã xác minh. Bootstrap chỉ dựng khuôn CRITERIA, MILESTONES, TASKS, BACKLOG; Planner hoàn thiện lý thuyết và kế hoạch sau duyệt. AGENTS.md cuối cùng chỉ nhắc các vai, gate, hook và lệnh thực sự được cấu hình. Dùng script Codex có sẵn khi phù hợp; phần còn thiếu triển khai theo `harness/specs/`. Không biến NOT_CONFIGURED thành PASS.

#### Bước 4. Kiểm tra

Chạy trong bản sao với dữ liệu giả, theo [`harness/specs/TESTS.md`](project-template/harness/specs/TESTS.md). Mỗi ranh giới cần ca **vi phạm bị chặn** và ca **hợp lệ không bị chặn nhầm**. Kiểm tra kích hoạt agent/skill, verify, approval, hook, loop, gate đúng tier. Thiếu môi trường thì báo `UNVERIFIED`; không nói đã test khi chưa chạy.

#### Bước 5. Báo cáo ngắn cho người dùng

Nêu thành phần đã copy/cấu hình và mục đích chống lỗi; enforcement thực; ma trận role/model; từng bài test với bằng chứng; phần chưa kiểm tra; cách dùng hằng ngày (tối đa 5 dòng); việc còn cần người dùng quyết định.

---

## Các tầng áp dụng

| Tầng | Dành cho | Thành phần dự kiến |
| --- | --- | --- |
| **Lite** | Dự án nhỏ, một người | AGENTS, CRITERIA + GOALMAP, verify, snapshot, Stop hook khi runtime hỗ trợ, lessons, evidence, journal, approval inbox, Coder + Reviewer |
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
