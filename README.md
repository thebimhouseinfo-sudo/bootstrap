# Bootstrap — Harness template cho coding agents

[**Tiếng Việt**](README.md) | [English](docs/user-guide.en.md) | [For AI](docs/FOR_AI.md)

**Bootstrap** cung cấp template role, skill, workflow, script và hook cho Codex, Google Antigravity, Claude Code, Continue và các coding agent khác. AI tự khảo sát và cấu hình cho dự án, không yêu cầu bạn tự copy từng file.

## Chọn loại dự án và copy một prompt

### A. Dự án mới — chưa có code

> Đọc hướng dẫn **For AI** tại https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md và nguồn `project-template/`. Dự án của tôi: `<ý tưởng, mục đích, thư mục dự án>` (chưa có code). Hãy setup Bootstrap theo quy trình staged: khảo sát và cài sơ bộ an toàn, rồi gọi Planner cùng tôi brainstorm và chốt CRITERIA trước khi đề xuất ngôn ngữ/framework/kiến trúc. Sau khi tôi duyệt phương hướng kỹ thuật, cấu hình skill/knowledge chuyên ngành cho Coder và Tester; kiểm tra hết placeholder cần thiết; tự tạo smoke test hai chiều và nhờ tôi xác minh host thực tế nếu cần. Chỉ khóa hook sau khi test PASS, rồi bàn giao. Đề xuất và xin duyệt các thao tác ghi file trước khi thực hiện. Không tự viết sản phẩm trong lúc setup.

### B. Dự án đã có code — tích hợp vào codebase

> Đọc hướng dẫn **For AI** tại https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md và nguồn `project-template/`. Dự án hiện có: `<thư mục/link repo và mô tả>`. Hãy khảo sát source, tài liệu, cấu hình build/test, Git và các chức năng đang hoạt động; tuyệt đối không ghi đè hoặc refactor code sản phẩm trong bước setup. Cài harness sơ bộ an toàn, kiểm tra trạng thái CRITERIA; nếu chưa được duyệt, Planner tái dựng hiện trạng từ code, hỏi mong muốn của tôi, soạn CRITERIA và xin duyệt. Sau đó đề xuất hướng phát triển/refactor; chỉ khi tôi duyệt mới cấu hình skill/knowledge Coder/Tester, hoàn thiện audit, test hook/script hai chiều trên runtime thực, khóa hook và bàn giao. Hỏi gộp thông tin còn thiếu, trình preview trước khi ghi file.

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

## Sau khi bàn giao: prompt khởi đầu luồng chính

> Hãy gọi **Planner** theo harness vừa được bàn giao. Đọc CRITERIA đã duyệt, ARCHITECTURE, PROJECT_PROFILE và codebase. Tạo hoặc rà soát **Implementation Plan** và **GOALMAP trong Plan**: ở đầu **mỗi mục Plan** phải ghi rõ GOAL — sửa/viết phần code đó để sản phẩm đạt được kết quả gì, liên kết yêu cầu CRITERIA nào, chấp nhận và kiểm thử ra sao. Dựa trên Plan, lập Milestones theo quan hệ phụ thuộc và tiêu chí nghiệm thu. Thực hiện review theo workflow, trình tôi duyệt trước khi lập Tasks hay code. Không tự sửa CRITERIA đã duyệt.

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

## Phiên bản và nâng cấp

Installer ghi `harness/.bootstrap-manifest.json` để xác định nguồn và hash các file đã cài. Khi Bootstrap có phiên bản mới, AI có thể preview `--upgrade`, chỉ thay file chưa bị chỉnh sửa kể từ lần cài trước; các file khác phải được duyệt và hợp nhất thủ công. Nếu setup lỗi, đọc kết quả rollback và dùng `harness/common/recover.py` trong terminal độc lập cho sự cố hook. **Không tự tắt guard để thoát BLOCK**.

## License

Xem [LICENSE](LICENSE).
