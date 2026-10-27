# Bootstrap — Coding agent setup

[**Tiếng Việt**](README.md) | [English](docs/user-guide.en.md) | [For AI](docs/FOR_AI.md)

Bootstrap giúp **Codex, Claude Code, Antigravity** và các coding agent tương thích thiết lập môi trường phát triển (agents, skills, hooks, scripts và workflow) cho một dự án.

**Cách dùng:** mở coding agent có quyền truy cập thư mục dự án và công cụ thực thi lệnh. Chọn **một** prompt dưới đây, chỉ thay đường dẫn thư mục. Không cần tự clone Bootstrap, copy template hay chạy installer; agent sẽ làm các việc đó sau khi được cấp quyền cần thiết.

## Hai cách sử dụng Bootstrap: Lead là luồng chính

**Lead profile là cách dùng mặc định** cho một dự án mới hoặc dự án đã có code. Lead vận hành toàn bộ quy trình Bootstrap: tìm hiểu dự án, xây dựng/duy trì Criteria, Plan và milestones, chuẩn bị Technical Proposal, tổ chức **Critic Review** trước khi code, rồi trực tiếp thực hiện hoặc giao việc. Hai prompt Greenfield và Brownfield bên dưới đều khởi động **Lead**, không phải Worker.

**Worker profile là gì?** Worker là phiên thực thi công việc *do một Lead đang quản lý dự án giao xuống*, nhằm chia nhỏ phần triển khai cụ thể, giảm context phải đọc và giúp Lead tập trung vào thiết kế, điều phối, tích hợp. Worker **không** khởi tạo hoặc quản lý dự án độc lập. Trong **luồng thiết kế chuẩn**, Worker **chỉ nhận Technical Proposal đã Critic Review PASS làm Criteria**. Technical Proposal phải đủ cụ thể để thể hiện phạm vi code, dependency, đầu ra, điều kiện nghiệm thu và những giới hạn cần thiết; không tạo một Criteria thứ hai hay coi bảng giao việc riêng là Criteria. Thông tin truy cập source/branch có thể được cung cấp để thực thi, nhưng không thay thế hoặc mở rộng Criteria của Worker. Người dùng có quyền sử dụng Bootstrap theo cách khác; đó không phải luồng khuyến nghị nhằm đạt hiệu quả tốt nhất. Worker dùng **cùng Bootstrap, roles, skills và các khả năng kỹ thuật** như Lead; không có installer, tier hay loại model riêng.

**Worker sẽ làm gì?** Đọc assignment và đúng những tài liệu/source cần thiết; thực hiện thay đổi đã được duyệt; tự kiểm tra, sửa lỗi trong phạm vi giao việc; trả lại cho Lead source/diff, bằng chứng test, phần chưa xác minh và những lệch phạm vi cần quyết định. Worker **bỏ qua toàn bộ project bootstrap**: không khám phá lại Criteria cấp dự án, không gọi Technical Advisor để duyệt lại Criteria, không tạo lại Plan/milestones và **không bắt chạy lại Pre-Code CR** cho proposal đã PASS. Nếu thiết kế cần thay đổi đáng kể, báo Lead xử lý thay vì tự mở rộng phạm vi.

**Quan hệ Lead–Worker:** Worker chỉ có ý nghĩa **sau khi tồn tại Lead và assignment đã duyệt**. Lead có thể tự code, tự test và hoàn tất dự án mà không tạo Worker nào. Không giả định model local khoảng 27B đủ năng lực làm Lead dự án; nó chỉ là ứng viên cho công việc triển khai được giao và cần đánh giá bằng kết quả thực tế. Nếu model local thực sự đủ năng lực điều hành cả dự án, sử dụng **Lead profile** với model đó — và Lead có thể tự thực hiện luôn công việc của Worker.

**Thiết kế tối thiểu:** Lead/Worker là **điểm vào và phạm vi Criteria**, không phải hai bản Bootstrap. Giữ nguyên Lite/Standard/Full (cấp tính năng cài đặt). Không cần công tắc installer `--profile lead/worker` hay hệ thống điều phối mới chỉ để đặt tên hai luồng. Worker handoff và giới hạn context được triển khai trong giai đoạn B3 theo hợp đồng công việc; việc chép role/skill không tự chứng minh host-native agent hoặc quyền ghi được cưỡng chế.

## 1. Greenfield — dự án mới

> Thiết lập Bootstrap cho **dự án greenfield (mới, chưa có code)** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Trước khi gọi tool xin quyền, thông báo trước rằng sẽ có câu hỏi cấu hình riêng. Tự setup và chỉ hỏi khi cần duyệt.

## 2. Brownfield — dự án đã có code

> Thiết lập Bootstrap cho **dự án brownfield (đã có code)** tại `<ĐƯỜNG_DẪN_DỰ_ÁN>`. Đọc và làm theo https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Trước khi gọi tool xin quyền, thông báo trước rằng sẽ có câu hỏi cấu hình riêng. Bảo toàn code và tự setup; chỉ hỏi khi cần duyệt.

**Phân biệt cấp quyền và câu hỏi setup:** Trước khi chạy installer, AI sẽ gửi một tin nhắn báo trước. Sau khi bạn cho phép lệnh cần thiết, **IDE hiển thị dialog lựa chọn**, còn **CLI hiển thị các dòng câu hỏi và lựa chọn đánh số ngay trong terminal**. Hãy đọc kỹ trước khi chọn 1/2: đây là lựa chọn cấu hình, **không phải một yêu cầu cấp quyền mới**. Câu trả lời được lưu để truy vết; không chuyển bảng câu hỏi sang chat.

**Nhiều coding host trong một dự án:** chọn một host chính để quản lý vòng đời staged/hook-lock, rồi chọn thêm các host như Codex và Claude Code. Installer hỗ trợ lặp `--runtime` (ví dụ `--runtime codex --runtime claude`); thứ tự có ý nghĩa: host đầu tiên là host chính và phải giữ nguyên khi nâng cấp. Tệp dùng chung chỉ được cài một lần; mỗi host có adapter riêng. Cài đặt không đồng nghĩa native hooks của tất cả host đều PASS — cần kiểm thử thực tế riêng trên từng host trước khi tuyên bố tương đương. Không tự chuyển primary host hoặc bỏ qua human approval.

**Continue CLI / IDE:** Bootstrap installs `.continue/settings.json`, native CLI Criteria hooks and always-on `.continue/rules/` for `--runtime continue`. `cn` CLI must be verified with actual TUI allow/deny events; **Continue VS Code extension does not inherit the CLI hook automatically**, and remains guided-only for protected writes unless separate native interception is proven. See `.continue/HOOKS_SETUP.md`.

**Codex lập kế hoạch, Continue viết code bằng model local:** cài cùng lúc bằng `--runtime codex --runtime continue` (có thể thêm `--runtime copilot`), rồi bàn giao qua Plan và Tasks đã duyệt trong cùng dự án. Chọn Continue Coder config và cấu hình model local thật trong config đó; các role không tự chia sẻ lịch sử chat hay tự chạy thành subagent. Dùng một agent ghi code tại một thời điểm trong cùng checkout. Xem [hướng dẫn nhiều harness và bàn giao](project-template/harness/MULTI_HARNESS.md).

**VS Code Copilot:** chọn `--runtime copilot` để cài **native** `.github/agents/*.agent.md` và `.github/hooks/criteria.json`, không chọn `generic --target-app copilot` cho dự án mới. Planner trình Criteria draft/delta trên chat, chỉ khi Human đồng ý ghi mới gọi Technical Advisor, Human xác nhận **sau tư vấn** rồi hook mới cho chạy lệnh ghi một lần (xem `.github/COPILOT_SETUP.md`). Trong VS Code phải chọn **Copilot Session Target**, không phải Local/Claude/Codex.

**Generic (OpenCode, Qwen Code và các CLI/IDE khác):** installer chỉ chép bộ hợp đồng hành vi và script chung. **Ngay trong quá trình setup, agent phải đọc `.generic/ADAPTER_REQUIREMENTS.md`, chuyển cấu hình `.generic` sang đúng thư mục native của host (ví dụ `.opencode/`, `.qwen/`, `.github/`), tự viết/đăng ký adapter và hook, rồi kiểm thử host thực sự nạp các setting. Không đổi tên cả thư mục một cách máy móc vì mỗi host có schema khác nhau.** Không yêu cầu Human tự viết code và không dừng ở bước `PORT_REQUIRED` nếu host có khả năng hỗ trợ. Các cơ chế host không hỗ trợ phải được chứng minh và thông báo `GUIDED_ONLY`; Tier `Standard` không tự xác nhận hook hoặc quyết định Human.

**Codex Cloud:** nếu không thể mở phiên mới hay chạy Human-terminal độc lập, kiểm thử ở workspace tạm trong **task đang mở** và báo `SCRIPT_TESTED / HOOK_RUNTIME_UNVERIFIED`; không khai `READY` hay giả lập lượt xác nhận của Human. Xem hướng dẫn [For AI](docs/FOR_AI.md).

## AI sẽ tự làm gì?

Agent xác định runtime, kiểm tra dự án, chuẩn bị và chạy installer ở chế độ **staged**. Với greenfield, Planner dùng `brainstorm-theory` để khám phá nhu cầu và giữ nguyên các câu hỏi scope; với brownfield, dùng `write-criteria` để tổng hợp quyết định Human và tái dựng CURRENT từ code (không tự xem code là DESIRED). Khi Human yêu cầu **chốt Criteria lần đầu hoặc sửa Criteria hiện có**, ngay trước khi ghi file Planner phải gọi Technical Advisor tư vấn nếu chưa có tư vấn cho đúng nội dung; Human quyết định **sau tư vấn**, Planner mới ghi. Advisor không phê duyệt hay phủ quyết. Sau đó AI xin duyệt hướng kỹ thuật, cấu hình Coder/Tester, audit và smoke test. Sau khi kiểm thử thực tế, agent hướng dẫn khóa hook và bàn giao. Quy trình chi tiết dành cho agent nằm trong [For AI](docs/FOR_AI.md), không phải các bước người dùng phải tự làm.

**Quyền truy cập:** Codex CLI/App, Claude Code và các coding agent tương thích có thể sử dụng shell/terminal **khi runtime và người dùng cấp quyền**. Nếu bị sandbox, không có mạng hoặc thiếu quyền đọc/ghi dự án, agent phải báo chính xác thao tác cần cho phép; không được giả định đã cài thành công. **Claude Web chỉ đọc trang web không thay thế coding agent có quyền truy cập dự án.**

### ⚠️ Không đóng tab đang setup

Khi agent yêu cầu mở phiên mới để test hook, **giữ nguyên phiên setup** để nhận lỗi và sửa. Các lệnh xác nhận `activate` và `finalize` phải do **Human tự thực hiện trong terminal tương tác độc lập** theo hướng dẫn của agent. Chỉ đóng tab setup sau khi post-lock verification và bàn giao hoàn tất.

## Sau khi bàn giao

Agent sẽ đưa prompt vào luồng phát triển chính. Nếu cần gọi thủ công:

> Gọi **Planner** đọc CRITERIA đã duyệt, lập/rà soát Implementation Plan (GOALMAP trong Plan, GOAL ở đầu mỗi mục) và Milestones; trình tôi phê duyệt trước khi tạo Tasks hoặc viết code.

Cấu hình `local/tracked`, cách nâng cấp, rollback, giới hạn của Lite và các bài test xem trong [hướng dẫn AI](docs/FOR_AI.md) và [hướng dẫn setup kỹ thuật](project-template/SETUP.md). Việc chạy script PASS không tự chứng minh hook đã được host kích hoạt.

[License](LICENSE).
