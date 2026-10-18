# Bootstrap — Coding agent setup

[**Tiếng Việt**](README.md) | [English](docs/user-guide.en.md) | [For AI](docs/FOR_AI.md)

Bootstrap giúp **Codex, Claude Code, Antigravity** và các coding agent tương thích thiết lập môi trường phát triển (agents, skills, hooks, scripts và workflow) cho một dự án.

**Cách dùng:** mở coding agent có quyền truy cập thư mục dự án và công cụ thực thi lệnh. Chọn **một** prompt dưới đây, chỉ thay đường dẫn thư mục. Không cần tự clone Bootstrap, copy template hay chạy installer; agent sẽ làm các việc đó sau khi được cấp quyền cần thiết.

## 1. Dự án mới — chưa có code

> Thiết lập Bootstrap cho **dự án mới** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Tự điều phối toàn bộ setup và Discovery; chỉ hỏi tôi về quyết định cần duyệt hoặc thông tin còn thiếu.

## 2. Dự án đã có code

> Thiết lập Bootstrap cho **dự án đã có code** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Khảo sát, bảo toàn code hiện tại và tự điều phối toàn bộ setup; chỉ hỏi khi cần tôi quyết định hoặc phê duyệt.

## AI sẽ tự làm gì?

Agent xác định runtime, kiểm tra dự án, chuẩn bị và chạy installer ở chế độ **staged**, đưa CRITERIA và phương hướng kỹ thuật cho Human duyệt, cấu hình Coder/Tester, audit và chạy smoke test. Sau khi kiểm thử thực tế, agent hướng dẫn khóa hook và bàn giao. Quy trình chi tiết dành cho agent nằm trong [For AI](docs/FOR_AI.md), không phải các bước người dùng phải tự làm.

**Quyền truy cập:** Codex CLI/App, Claude Code và các coding agent tương thích có thể sử dụng shell/terminal **khi runtime và người dùng cấp quyền**. Nếu bị sandbox, không có mạng hoặc thiếu quyền đọc/ghi dự án, agent phải báo chính xác thao tác cần cho phép; không được giả định đã cài thành công. **Claude Web chỉ đọc trang web không thay thế coding agent có quyền truy cập dự án.**

### ⚠️ Không đóng tab đang setup

Khi agent yêu cầu mở phiên mới để test hook, **giữ nguyên phiên setup** để nhận lỗi và sửa. Các lệnh xác nhận `activate` và `finalize` phải do **Human tự thực hiện trong terminal tương tác độc lập** theo hướng dẫn của agent. Chỉ đóng tab setup sau khi post-lock verification và bàn giao hoàn tất.

## Sau khi bàn giao

Agent sẽ đưa prompt vào luồng phát triển chính. Nếu cần gọi thủ công:

> Gọi **Planner** đọc CRITERIA đã duyệt, lập/rà soát Implementation Plan (GOALMAP trong Plan, GOAL ở đầu mỗi mục) và Milestones; trình tôi phê duyệt trước khi tạo Tasks hoặc viết code.

Cấu hình `local/tracked`, cách nâng cấp, rollback, giới hạn của Lite và các bài test xem trong [hướng dẫn AI](docs/FOR_AI.md) và [hướng dẫn setup kỹ thuật](project-template/SETUP.md). Việc chạy script PASS không tự chứng minh hook đã được host kích hoạt.

[License](LICENSE).
