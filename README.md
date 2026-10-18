# Bootstrap — bộ template môi trường cho coding agents

Repository này cung cấp **cây dự án có sẵn** tại [`project-template/`](project-template/). Khi được giao thiết lập môi trường agent cho một dự án, **sao chép các file phù hợp vào đúng vị trí rồi điều chỉnh theo dự án**, không xây lại harness từ đầu và không thay nội dung lý thuyết sản phẩm theo suy đoán.

Người dùng có thể không đọc code: kết quả cần bằng chứng kiểm thử thực tế và diễn giải ngôn ngữ thường. Những hành động bắt buộc có phê duyệt phải đi qua kênh Approval Request đã được xác minh, không giả mạo quyền đồng ý.

## Bắt đầu nhanh

Cho AI repo này và yêu cầu: “Đọc README bootstrap, khảo sát dự án của tôi, đề xuất cấu hình cần thiết; sau khi tôi duyệt thì sao chép và tùy chỉnh `project-template/`.”

- **Dự án đã có code (A):** khảo sát code, cấu hình, khả năng kiểm thử và các hướng dẫn đang có; giữ lại dữ liệu/cấu hình hợp lệ, không overwrite mù quáng.
- **Dự án mới có lý thuyết đã duyệt (B):** Bootstrap triển khai môi trường dựa trên các ràng buộc đã xác nhận, còn Planner chuẩn hóa lý thuyết vào CRITERIA.
- **Dự án trống/chưa có lý thuyết (C):** không buộc dừng hoàn toàn. Dựng *Discovery Mode tối thiểu* (Planner + brainstorm/research + CRITERIA placeholder + phương thức trao đổi/duyệt khả dụng). Planner cùng người dùng hoàn thiện lý thuyết; chưa chốt stack, chưa tạo milestone/task sản phẩm hay tuyên bố full harness sẵn sàng.

Không làm việc ở repo bootstrap khi đang thiết lập một dự án khác. Chỉ chỉnh chính repo bootstrap nếu người dùng yêu cầu cập nhật bộ template.

## Cây thư mục nguồn

```text
README.md                         # entrypoint cho người và AI
harness-bootstrap-prompt-v9.md    # tham chiếu đầy đủ: bất biến, vai trò, gates, test
project-template/                 # CÂY THƯ MỤC THỰC TẾ cần copy nội dung vào project root
  SETUP.md                        # chỉ dẫn trạng thái và thứ tự cấu hình
  AGENTS.md                       # placeholder: Planner viết hướng dẫn dự án
  README.md                       # placeholder: Planner viết tài liệu dự án
  TASKS.md                        # placeholder: Planner quản lý các task
  docs/
    CRITERIA.md                   # nguồn lý thuyết sản phẩm DUY NHẤT; GOALMAP nằm ở đây
    ARCHITECTURE.md
    PROJECT_PROFILE.md
    MILESTONES.md
    BACKLOG.md
    TRACE.md                      # placeholder; script sinh khi đã cấu hình
    reports/
  .agents/
    roles/                        # Planner, Reviewer, Critic/CR, Coder, Tester...
    skills/                       # generic SKILL.md, gồm brainstorm/research
    config/                       # model & worker-context placeholders
    knowledge/                    # optional knowledge theo host/dialect
  harness/
    README.md                     # triển khai harness theo nền tảng
    HARNESS_SPEC.md               # ý định guard sau khi được duyệt
    specs/                        # VERIFY, HOOKS, GATES, REVIEW_LOOP, APPROVAL, TESTS...
  lessons/
```

**Không copy nguyên thư mục `project-template` thành thư mục con** của dự án. Copy *nội dung* vào root sau khi đã kiểm tra xung đột và được duyệt. Thư mục `templates/` cũ chỉ còn file chỉ hướng sang cây canonical; ZIP Claude là nguồn tham khảo đã được đối chiếu, không phải cây cài đặt thứ hai.

## Vai trò và quyền

**Bootstrap / Environment Architect:** khảo sát môi trường, xác nhận runtime/OS/host/model, lựa chọn các thành phần, đề xuất bản chỉnh và triển khai kỹ thuật sau phê duyệt. Không quyết định tính năng, roadmap hoặc viết code sản phẩm trong phiên bootstrap.

**Planner:** chịu trách nhiệm nội dung tùy theo giai đoạn. Trong Discovery Mode, dùng `brainstorm-theory` + `research-evidence` để trao đổi phương án với người dùng; giả thuyết và vấn đề chưa chốt ghi `OPEN` trong CRITERIA. Trong Delivery Mode, dựa vào CRITERIA được duyệt để lập GOALMAP, milestone, task. Viết lại root `AGENTS.md` và tài liệu dự án cho đúng ngữ cảnh đã xác nhận, nhưng không tự sửa chính sách bảo vệ hay phê duyệt.

**Reviewer / Critic (CR):** sử dụng contract generic qua nhiều dự án. Reviewer có ngữ cảnh để đối chiếu goal và evidence; Critic quan sát độc lập theo ranh giới đọc đã xác minh.

**Coder / Tester:** chạy được với generic skill ngay cả khi chưa có bộ knowledge theo dự án. Có thể nạp lại skill/knowledge đã kiểm chứng theo session/task hoặc thay đổi profile để hạn chế sai dialect/API và giảm vòng test. Thiếu *tài liệu bổ trợ tùy chọn* không đồng nghĩa với thất bại; nhưng ràng buộc compatibility bắt buộc trong PROJECT_PROFILE vẫn có hiệu lực.

Role contract hoặc file SKILL.md **không tự động đăng ký thành subagent/skill**. Bootstrap phải chuyển chúng sang định dạng native của runtime, kích hoạt và test thật; nếu không thể chứng minh thì ghi `UNVERIFIED`/`GUIDED_ONLY`.

## Quy trình bắt buộc cho agent

### 0. Khảo sát và chọn chế độ

Đọc những gì đã có trước khi hỏi. Chỉ hỏi thông tin chưa xác minh: dự án A/B/C, tầng Lite/Standard/Full (mặc định Standard khi phù hợp), runtime/phiên bản, OS/shell, Git/remote, host/stack, khả năng chạy test thật, model khả dụng, API/dialect bắt buộc và kênh duyệt của người dùng.

Với dự án C, hỏi ít thông tin cần thiết để kích hoạt Discovery Mode. **Không yêu cầu đặc tả hoàn chỉnh trước khi bắt đầu brainstorm/research.**

### 1. Khảo sát runtime và reuse

Xác minh khả năng thực của runtime: subagent, skill discovery, hooks, context reload, MCP, permissions, model/reasoning, tools và tài liệu chính thức phù hợp phiên bản. Kiểm kê script/test/CI/harness đã tồn tại; không tạo bản trùng.

Mỗi thành phần đưa vào cần trả lời được: **“Nó ngăn lỗi nào?”** Cái chưa cần thì bỏ. Không giả định cú pháp hook của Claude Code áp dụng được cho Codex, hay ngược lại.

### 2. Trình kế hoạch thay đổi harness để người dùng duyệt

Trước khi ghi vào dự án đích, trình bảng sau (không lập product plan):

| File/thành phần | Đường dẫn đích | Giữ/copy/sửa/bỏ | Vì sao | Trạng thái |
|---|---|---|---|---|
| `project-template/AGENTS.md` | `AGENTS.md` | Planner viết lại | hướng dẫn đúng dự án | chưa điền |
| `.agents/roles/*` | theo native runtime | cấu hình và test | cho agent gọi được | UNVERIFIED |
| `harness/specs/HOOKS.md` | contract ở `harness/specs/` | hiện thực khi hỗ trợ | guard theo lifecycle | NOT_CONFIGURED |

Kèm ma trận vai → model/reasoning/permissions/skills, bảng `ENFORCED` / `GUIDED_ONLY` / `UNVERIFIED`, danh sách mâu thuẫn và kế hoạch backup/rollback. Phê duyệt qua request `HARNESS_PATCH`; khi chưa có approval channel, nêu rõ ngoại lệ bootstrap ban đầu và giới hạn thực tế, không tự ghi approvals.

### 3. Copy → cấu hình → Planner hoàn thiện

- Copy đúng cây và file cần thiết theo tầng; với dự án hiện hữu so diff và giữ phần không liên quan.
- File **dùng làm nguồn trực tiếp**: generic role prompts, generic SKILL.md, report/lesson formats.
- File **placeholder**: AGENTS, project README, CRITERIA, PROJECT_PROFILE, ARCHITECTURE, GOALMAP/MILESTONES/TASKS; Planner điền lý thuyết đã duyệt và nội dung dự án, Bootstrap cung cấp dữ liệu môi trường đã xác minh.
- File **contract để hiện thực**: `harness/specs/*`; xác định script/hook/loop/gate/approval hợp với runtime thật và tầng đã chọn. Không tạo executable giả, không coi tài liệu là ENFORCED.
- Model ID, command, API/host version không biết phải ghi `UNVERIFIED`; không tự chọn model fallback hay bịa cú pháp.
- Dự án mới chưa có lý thuyết chỉ cấu hình đủ Discovery Mode trước. Hoàn thiện full harness và planning sau khi có lý thuyết được duyệt.

### 4. Tự kiểm thử trước khi tuyên bố hoạt động

Theo `project-template/harness/specs/TESTS.md`, kiểm thử trên bản sao với dữ liệu giả: mỗi ranh giới cần ít nhất một ca hợp lệ không bị chặn nhầm và một ca vi phạm bị chặn đúng. Thử role/skill activation, cả Coder/Tester không có knowledge bổ sung, context isolation, approval authorization, Stop/verify/loop/gates, stale dependencies theo tầng. Không test được → `UNVERIFIED`, không gọi là PASS.

### 5. Báo cáo ngắn cho người dùng

Nêu tầng và môi trường đã xác nhận; thứ gì được copy, cái gì đã được tùy biến/triển khai thật; ma trận agent-model; bảng quyền cưỡng chế và phần chỉ được hướng dẫn; kết quả test và bằng chứng; các yêu cầu đang chờ, cách khôi phục, cách giao việc hằng ngày. Không dùng thuật ngữ PASS cho khả năng chưa thử.

## Bất biến và giới hạn quyền

1. `docs/CRITERIA.md` là nguồn sự thật duy nhất về lý thuyết sản phẩm; GOALMAP dẫn xuất nằm bên trong. Các file khác chỉ trỏ ID, không tạo draft spec song song. Mơ hồ → `OPEN` / `THEORY_GAP`.
2. CRITERIA đã duyệt > GOALMAP > milestones > tasks > code/tests > chat chưa xác minh. Thay đổi ID làm phần phụ thuộc STALE, không bắt toàn hệ thống chạy lại khi không liên quan.
3. Phê duyệt chính thức bằng request **Đồng ý / Không đồng ý / Khác** không hết hạn; agents không được tự trả lời, và chat “ok” không phải chứng cứ authorization khi yêu cầu request.
4. Script/hook là đường cưỡng chế; role prompt và quy ước chỉ là `GUIDED_ONLY` nếu runtime chưa chứng minh được quyền. Runtimes không có hook/user-only input không được nhận vơ journal/approval integrity.
5. Không raw push, force push, rewrite history, destructive reset, xóa nhánh không rõ, cài plugin/MCP ngoài, đọc/chia sẻ secret hay đổi cấu hình nhạy cảm mà không có phê duyệt phù hợp.
6. Role ≠ model ≠ project profile ≠ skill. Không lặng lẽ đổi model hoặc biến research thành lý thuyết đã duyệt.
7. Mỗi BLOCK phải giải thích mã, luật, nguyên nhân, file định nghĩa và cách khôi phục hợp lệ. Fixer sửa lỗi cấu hình theo HARNESS_SPEC, không nới guard cho qua chặn.
8. Đúng phạm vi tầng Lite/Standard/Full; gate chưa cấu hình phải là `NOT_CONFIGURED`, không dựng milestone hay trạng thái PASS giả.

Tham chiếu: [SETUP](project-template/SETUP.md), [Harness guides](project-template/harness/README.md), [bộ test](project-template/harness/specs/TESTS.md), [prompt đầy đủ](harness-bootstrap-prompt-v9.md).

## License

MIT — xem `LICENSE`.
