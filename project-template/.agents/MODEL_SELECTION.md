# Hướng dẫn chọn Model cho Google Antigravity IDE

Tài liệu này xác định cách phân bổ và lựa chọn mô hình cho 7 vai trò chuẩn của coding-agent harness, dựa trên danh sách mô hình thực tế hiện có trong dropdown của Google Antigravity IDE:

1. **Gemini 3.8 Flash High**
2. **Claude Sonnet 4.6 (Thinking)**
3. **Claude Opus 4.6 (Thinking)**
4. **GPT-OSS 120B (Medium)**

---

## 1. Ma trận phân vai & Khuyến nghị mô hình

| Vai trò (Role) | Nhiệm vụ chính | Mô hình khuyến nghị (Antigravity) | Mô hình dự phòng | Lý do kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Planner** | Khám phá nhu cầu, lập luận đa tầng, soạn thảo & bảo vệ `docs/CRITERIA.md`, chia nhỏ task trong `TASKS.md`. | **Claude Opus 4.6 (Thinking)** | **Gemini 3.8 Flash High** | Khả năng suy luận ngữ cảnh sâu (deep thinking), duy trì tính nhất quán lý thuyết, không bỏ sót non-goals và ranh giới an toàn. |
| **Advisor** | Cố vấn độc lập cho người dùng: đánh giá tính khả thi, chi phí, rủi ro kiến trúc trước khi phê duyệt CRITERIA. | **Claude Opus 4.6 (Thinking)** | **Gemini 3.8 Flash High** | Cần tư duy phản biện sắc bén, phân tích tác động dây chuyền khách quan, không bị thiên lệch bởi áp lực code nhanh. |
| **Reviewer** | Soát xét kế hoạch và mã nguồn: đối chiếu chặt chẽ với `docs/CRITERIA.md`; phát hiện overengineering lẫn thiếu sót. | **Claude Sonnet 4.6 (Thinking)** | **Gemini 3.8 Flash High** | Soi chiếu chi tiết diff, kiểm tra quy tắc an toàn, không tự ý nới lỏng các ràng buộc của dự án. |
| **Coder** | Hiện thực hóa task nhỏ nhất đã được duyệt, thực hiện quy trình safe-change (snapshot trước khi sửa, verify sau khi sửa). | **Claude Sonnet 4.6 (Thinking)** | **Gemini 3.8 Flash High** | Sinh mã chính xác, hiểu sâu cấu trúc dự án, ít lỗi cú pháp, tốc độ tốt. |
| **Tester** | Thực thi các kiểm tra thực tế qua `harness/common/verify.py`, đối soát bằng chứng khách quan. | **Gemini 3.8 Flash High** | **Claude Sonnet 4.6 (Thinking)** | Tốc độ phản hồi cực nhanh, chi phí quota thấp, thực thi lệnh và kiểm tra output chính xác. |
| **Critic** | Đóng vai người dùng bên ngoài: chỉ nhìn UI/README, không đọc CRITERIA nội bộ; phản ánh trải nghiệm thực tế. | **GPT-OSS 120B (Medium)** | **Gemini 3.8 Flash High** | Cung cấp góc nhìn độc lập (khác họ mô hình với Claude/Gemini), bảo đảm tính khách quan tách biệt với mã nguồn nội bộ. |
| **Explorer** | Quét cấu trúc repository, đọc tài liệu thư viện, tổng hợp thông tin. | **Gemini 3.8 Flash High** | **Claude Sonnet 4.6 (Thinking)** | Cửa sổ ngữ cảnh (context window) siêu lớn, tốc độ quét và đọc tài liệu nhanh nhất. |

---

## 2. Quy tắc chuyển đổi Model trong Antigravity IDE

1. **Model trò chuyện chính (Main Chat Model):** Do người dùng trực tiếp chọn trên thanh trạng thái góc dưới (Model Picker). Bạn có thể đổi sang **Claude Sonnet 4.6 (Thinking)** khi cần code/refactor sâu, hoặc **Gemini 3.8 Flash High** khi cần tốc độ và tương tác linh hoạt.
2. **Khi hạn mức (Rate Limits) bị giới hạn:**
   - Nếu Claude gặp thông báo quota (`Notice` / `ineligible for higher rate limits`): Bạn có thể chuyển model chính sang **Gemini 3.8 Flash High** mà vẫn giữ nguyên toàn bộ skills trong `.agents/skills/` và các quy tắc `AGENTS.md`.
   - Nếu cần phản biện độc lập mà không tốn quota Claude: Chọn **GPT-OSS 120B (Medium)** cho vai Critic.
