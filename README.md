# Bootstrap — Harness template cho coding agents

[**Tiếng Việt**](README.md) | [English](docs/user-guide.en.md) | [For AI](docs/FOR_AI.md)

**Bootstrap** cung cấp template role, skill, workflow, script và hook cho Codex, Google Antigravity, Claude Code, Continue và các coding agent khác. AI tự khảo sát và cấu hình cho dự án, không yêu cầu bạn tự copy từng file.

## Chọn một trong hai prompt để bắt đầu

Chỉ cần **copy một prompt và thay đường dẫn thư mục dự án**. Các bước thiết lập, đọc code, CRITERIA, skills, smoke test và bàn giao do AI tự điều phối theo [For AI](docs/FOR_AI.md).

### A. Dự án mới — chưa có code

> Thiết lập Bootstrap cho **dự án mới** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo toàn bộ hướng dẫn AI: https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Tự điều phối setup và Discovery; chỉ hỏi tôi về thông tin còn thiếu hoặc quyết định cần duyệt.

### B. Dự án đã có code

> Thiết lập Bootstrap cho **dự án đã có code** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo toàn bộ hướng dẫn AI: https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Khảo sát và bảo toàn code hiện tại; tự điều phối setup, chỉ hỏi tôi về thông tin còn thiếu hoặc quyết định cần duyệt.

**Để AI thực sự chạy installer**, phải có bản clone Bootstrap trên máy, trong thư mục tạm riêng **ngoài dự án đích**: `git clone --depth 1 https://github.com/thebimhouseinfo-sudo/bootstrap.git <thu-muc-tam>`. Nếu agent có quyền shell, sau khi được duyệt nó tự clone và thực hiện; nếu chỉ đọc web, nó phải cung cấp lệnh chính xác cho Human. Link `raw` chỉ giúp đọc tài liệu, không thay thế bản clone.

**Trong cả hai trường hợp:** AI phải dùng lệnh cài có `--staged` cho lần setup đầu, sau khi bạn duyệt preview. Mặc định installer chỉ preview; `--apply` mới ghi file. Runtime/tier và các giới hạn thực tế phải được khai báo rõ; không coi script test là bằng chứng host hook đã hoạt động.

## Quá trình setup sẽ diễn ra thế nào?

1. **Preliminary setup:** cài an toàn, không tự BLOCK thao tác sửa harness khi Git/hooks chưa cấu hình.
2. **CRITERIA:** Planner kiểm tra CRITERIA cũ và/hoặc khảo sát code, làm rõ với bạn rồi xin duyệt.
3. **Technical direction:** đề xuất stack/kiến trúc hoặc hướng refactor để bạn quyết định.
4. **Coder/Tester:** bổ sung skill/knowledge thích hợp; xác minh phiên bản công cụ và phương pháp test.
5. **Audit + smoke test:** AI rà mọi cấu hình bắt buộc, viết và chạy test hợp lệ/bị cấm trên bản sao; sửa lỗi rồi kiểm tra lại.
6. **Live verification:** nếu cần, AI đưa đúng prompt/lệnh cho bạn mở phiên mới kiểm tra hook và script thật.
7. **Final lock + post-lock test:** sau khi xác minh runtime thật, AI chốt trạng thái hook/policy, lưu hash và kiểm tra lại một phiên mới sau khóa. Chỉ khi PASS mới xác nhận handoff và đưa prompt Planner.

### ⚠️ QUAN TRỌNG — KHÔNG ĐÓNG TAB ĐANG SETUP

**Giữ nguyên tab/phiên coding agent đang thiết lập Bootstrap khi được yêu cầu mở tab mới để test.** Tab mới chỉ dùng kiểm thử. Nếu bị BLOCK hoặc hook lỗi, quay về tab setup để sửa; không tự vô hiệu hóa cơ chế bảo vệ. Chỉ đóng tab setup sau khi AI xác nhận bàn giao xong và đã lưu checkpoint/đường recovery.

## Sau khi bàn giao: bắt đầu luồng phát triển

> Gọi Planner theo `AGENTS.md` để đọc CRITERIA đã duyệt, lập/rà soát Implementation Plan (GOALMAP và GOAL ở đầu mỗi mục), sau đó lập Milestones và trình tôi duyệt trước khi tạo Tasks hoặc code.

Sau lần đầu, mở agent trong thư mục dự án và làm việc bình thường theo `AGENTS.md`. Không cần chạy Bootstrap lại.

## Lưu cấu hình harness trong Git

- `--config-git local` (mặc định): giữ cấu hình agent/harness ngoài Git.
- `--config-git tracked`: cho phép commit cấu hình để tái sử dụng; trạng thái private, approvals, snapshots, journal và `docs/TRACE.md` vẫn giữ local.
- Dùng `--change-config-git` nếu chuyển chế độ đã cài (cả preview và apply). Không tự untrack dữ liệu đã nằm trong Git index.

Ví dụ (thay `PATH` và runtime phù hợp):

```bash
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --staged
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --staged --apply
python PATH/harness/common/setup_lifecycle.py audit
python PATH/harness/common/setup_lifecycle.py smoke
python PATH/harness/common/setup_lifecycle.py host-test
```

Các lệnh `audit` và `smoke` nêu vấn đề còn thiếu; `host-test` in hướng dẫn mở phiên mới. AI chuẩn bị bằng chứng; **Human tự chạy** `activate` và `finalize` trong terminal tương tác độc lập sau khi đọc xác nhận. Không dùng lệnh do agent tự gọi để giả duyệt; không tự tạo ra APPROVED CRITERIA hay bằng chứng test trên host. Tham khảo [English](docs/user-guide.en.md) và [For AI](docs/FOR_AI.md).

## Sử dụng bản Lite gọn nhẹ

Với dự án nhỏ không cần luồng đầy đủ, có thể chọn `--tier Lite --staged`. Lite chỉ mang các role/skill của tier Lite, **không có Planner và Tester đầy đủ**; các bước Discovery/Plan/Milestone vẫn phải được Human hoặc agent chính điều phối thủ công. Muốn quy trình setup hoàn chỉnh như phía trên nên dùng Standard.

## Phiên bản và nâng cấp

Installer ghi `harness/.bootstrap-manifest.json` để xác định nguồn và hash các file đã cài. Khi Bootstrap có phiên bản mới, AI có thể preview `--upgrade`, chỉ thay file chưa bị chỉnh sửa kể từ lần cài trước; các file khác phải được duyệt và hợp nhất thủ công. Nếu setup lỗi, đọc kết quả rollback và dùng `harness/common/recover.py` trong terminal độc lập cho sự cố hook. **Không tự tắt guard để thoát BLOCK**.

## License

Xem [LICENSE](LICENSE).
