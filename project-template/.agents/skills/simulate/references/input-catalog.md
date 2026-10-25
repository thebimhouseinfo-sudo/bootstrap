# Danh mục điều kiện đầu vào

Đọc file này ở Phase 2 khi sinh scenario. Chọn những mục mà **một người dùng thật (hoặc một kẻ phá thật) có thể tự nhiên tạo ra** qua giao diện và kênh công khai của app, gắn với hành trình và criteria trong brief. Không chọn giá trị vì nó "trúng" một nhánh code nào đó; designer không được mở code khi chọn. Mỗi scenario phải trả lời được: ai làm, trong tình huống nào, vì sao (`why_a_user_does_this`). Không dùng hết danh mục.

## Mục lục
1. Trục input (T1)
2. Trục state (T2)
3. Trục chuỗi & thứ tự (T3)
4. Trục thời gian & môi trường (T4)
5. Cố ý phá (T5)
6. Theo loại app: web, app trẻ em, AI/chat, CLI/MCP/plugin CAD
7. Gợi ý ghép cặp T6

---

## 1. Input (T1)

**Văn bản**
- Rỗng; chỉ khoảng trắng; chỉ xuống dòng; tab; 1 ký tự; đúng bằng max length; max+1; gấp 100 lần max.
- Khoảng trắng đầu/cuối; khoảng trắng kép giữa chữ.
- Tiếng Việt: chữ có dấu dạng **NFC** và **NFD** (cùng một chữ nhưng byte khác nhau, dễ làm so sánh chuỗi, tìm kiếm, đếm độ dài, đối chiếu đáp án bị sai); chữ hoa/thường lẫn dấu ("Đ", "đ"); gõ bằng IME đang composition (sự kiện `compositionstart/end` có thể kích hoạt submit sớm khi bấm Enter).
- Emoji, emoji ghép (ZWJ), ký tự RTL, ký tự độ rộng bằng 0, ký tự điều khiển.
- Chuỗi giống cú pháp: `<b>`, `{{x}}`, `${x}`, `%s`, dấu nháy `' "`, backslash, `null`, `undefined`, `NaN`, `true`.

**Số**
- 0, -0, âm, số thập phân, rất lớn, `1e308`, `Infinity`, `NaN`, chuỗi số có dấu phẩy kiểu Việt ("1.234,5").

**Ngày giờ**
- Ngày không tồn tại (30/02), năm 0, tương lai xa, múi giờ khác, đổi sang 00:00, DST.

**File/dữ liệu nhập vào**
- Rỗng, 0 byte, đuôi sai, đúng đuôi sai nội dung, JSON hỏng, JSON đúng nhưng thiếu trường, thừa trường, sai kiểu, schema phiên bản cũ/mới hơn, rất lớn, tên file có dấu/khoảng trắng/ký tự đặc biệt.

**Lựa chọn**
- Chọn không có gì, chọn tất cả, chọn rồi bỏ chọn, chọn giá trị không còn tồn tại trong danh sách.

## 2. State (T2)

- Lần đầu mở (storage trống) vs quay lại.
- Dữ liệu rỗng / 1 phần tử / rất nhiều phần tử (phân trang, hiệu năng).
- **Dữ liệu từ phiên bản trước** (migration): thiếu trường mới, trường đổi tên, kiểu đổi.
- Dữ liệu hỏng sẵn trong storage (JSON cắt cụt, giá trị sai kiểu).
- Storage đầy (quota), storage bị chặn (chế độ riêng tư), cookie tắt.
- Đã đăng nhập / đăng xuất / phiên hết hạn giữa chừng.
- Quyền: có/không có quyền microphone, camera, thông báo.
- Cài đặt người dùng: ngôn ngữ, cỡ chữ, âm thanh tắt, chế độ tối.
- Trạng thái nghiệp vụ: đã hoàn thành, đang dở, đã huỷ, đã hết hạn, trùng bản ghi.

## 3. Chuỗi & thứ tự (T3)

- Bỏ qua bước giữa bằng cách vào thẳng URL/route của bước sau.
- Nút Back/Forward của trình duyệt giữa luồng; Back sau khi đã submit.
- Refresh giữa luồng (state trong bộ nhớ có sống sót không?).
- Đóng tab rồi mở lại; mở link đã lưu của một bước cũ.
- Làm xong rồi làm lại từ đầu; làm hai luồng khác nhau xen kẽ.
- Huỷ giữa chừng rồi bắt đầu lại; huỷ khi đang loading.
- Hoàn tác (undo)/làm lại (redo) sau thao tác phá dữ liệu.
- Thao tác trên mục vừa bị xoá ở nơi khác.

## 4. Thời gian & môi trường (T4)

**Nhịp độ**
- Double click, triple click, bấm giữ, bấm dồn 20 lần/giây, nhấn Enter lặp lại.
- Gửi lần hai khi lần một chưa xong; bấm Huỷ rồi bấm Gửi ngay.
- Gõ trong lúc đang loading; đổi lựa chọn trong lúc đang xử lý.
- Debounce/throttle: dừng đúng ở ngưỡng.

**Mạng**
- Offline từ đầu; offline giữa chừng; mạng chập chờn; rất chậm (3–10s); timeout.
- API trả 400/401/403/404/429/500/502/503; trả 200 nhưng body rỗng hoặc sai schema; trả chậm theo thứ tự đảo (response cũ đến sau response mới: **race condition**).
- Trả về nửa chừng (stream đứt).

**Môi trường**
- Hai tab cùng lúc ghi cùng một storage; tab cũ ghi đè dữ liệu của tab mới.
- Màn hình nhỏ/xoay ngang; cảm ứng vs chuột; bàn phím ảo che ô nhập.
- Trình duyệt khác (Safari/iOS WebView, trình duyệt nhúng trong iframe).
- **App nhúng iframe** (ví dụ nhúng vào Blogger): storage bị phân vùng, cookie bên thứ ba bị chặn, kích thước iframe thay đổi, `window.top` không truy cập được.
- Máy yếu (CPU throttling), tab nền bị throttle timer.
- Đồng hồ hệ thống bị chỉnh; đổi ngày qua nửa đêm.

## 5. Cố ý phá (T5)

Chỉ dùng trên bản local/test, payload canary. Mục tiêu là kiểm guard.

**Bơm nội dung**
- Canary XSS vào mọi chỗ có hiển thị lại nội dung user (tên, ghi chú, tên file, tham số URL, tin nhắn): `<img src=x onerror="window.__pwned=1">`, `"><svg onload=...>`, `javascript:` trong link.
- Chuỗi giống template/format để xem có bị nội suy không.
- Injection vào bất cứ thứ gì đi vào truy vấn, lệnh, đường dẫn: dấu nháy, `../`, ký tự null, xuống dòng giả header.

**Vượt guard phía client**
- Gỡ `disabled`/`maxlength`/`required` bằng devtools rồi submit.
- Gửi trực tiếp request không qua UI (curl/fetch) với giá trị ngoài phạm vi.
- Sửa giá trị trong localStorage/IndexedDB/cookie (điểm, quyền, trạng thái hoàn thành, thời hạn) rồi tải lại.
- Đổi tham số URL/ID để mở dữ liệu không phải của mình.
- Replay một request hợp lệ nhiều lần; đổi thứ tự request.
- Gọi endpoint/handler của bước sau mà chưa qua bước trước.

**Lạm dụng tài nguyên**
- Payload cực lớn; tạo hàng nghìn bản ghi; vòng lặp gửi liên tục; mở rất nhiều tab.
- Input gây regex chậm (chuỗi dài lặp lại).
- Import file nén/nested sâu.

**Logic nghiệp vụ**
- Số âm, 0, số quá lớn trong điểm/tiền/số lượng; tràn số.
- Làm hai việc loại trừ nhau cùng lúc.
- Thử "lấy thưởng" nhiều lần; huỷ sau khi đã nhận.

## 6. Theo loại app

### Web/SPA (React, Vite, nhúng iframe)
- Route không tồn tại (404 có về được không?), route có tham số sai kiểu.
- Reload ở route sâu khi host tĩnh (GitHub Pages không có rewrite → 404): kiểm base path và hash routing.
- Asset/đường dẫn sai base path sau build.
- Service worker/cache cũ phục vụ bản cũ sau khi deploy bản mới.
- Lỗi runtime trong component con có làm trắng cả trang không (error boundary).

### App trẻ em / học tập
- Bấm loạn nhiều nút cùng lúc, kéo thả sai chỗ, thả ngoài vùng.
- Chạm hai ngón; chạm giữ; trượt nhầm khỏi vùng.
- Âm thanh bị chặn bởi trình duyệt cho tới khi có tương tác đầu tiên; chuyển tab khi đang phát.
- Làm xong bài rồi lùi lại làm lại: điểm/phần thưởng có bị tính lặp không.
- Trả lời đúng bằng cách viết khác (hoa/thường, dấu cách, NFC/NFD): có được chấp nhận không, đúng như thiết kế?
- Nội dung phù hợp độ tuổi: input người lớn/tục tĩu đi vào đâu, có bị lọc trước khi hiển thị lại cho bé?
- Bố mẹ/trẻ dùng chung một thiết bị: dữ liệu hai hồ sơ có lẫn nhau không.

### Tính năng AI/chat
- Rỗng; chỉ khoảng trắng; rất dài; sai ngôn ngữ so với bài học.
- **Prompt injection**: "bỏ qua mọi hướng dẫn trước đó", yêu cầu lộ system prompt, yêu cầu đổi vai, yêu cầu làm việc ngoài phạm vi, nhúng chỉ thị trong nội dung bài/dữ liệu mà app đưa vào prompt.
- Nội dung không phù hợp cho trẻ; chủ đề nhạy cảm; yêu cầu thông tin cá nhân.
- Model trả về sai định dạng (JSON hỏng, thiếu trường, markdown bất ngờ) → parser có chịu được không.
- Lỗi/timeout/429 từ API; stream đứt giữa chừng; trả lời rỗng.
- Gửi tin khi tin trước chưa trả về; reset hội thoại khi đang chờ.
- Lịch sử hội thoại quá dài (vượt giới hạn context): cắt tỉa có làm hỏng định dạng không.
- Khoá API bị thiếu/sai: thông báo gì, có lộ khoá không.

### CLI / MCP server / plugin CAD (AutoCAD, AutoLISP, COM)
- Thiếu tham số, thừa tham số, sai kiểu, sai thứ tự, tham số rỗng.
- Đường dẫn: không tồn tại, không quyền ghi, chứa dấu cách/tiếng Việt, rất dài, UNC.
- Bản vẽ: không mở, đang bị khoá, chưa lưu, chỉ đọc, không có đối tượng nào được chọn, chọn quá nhiều đối tượng, layer bị khoá/đóng băng/off, Xref bị thiếu hoặc unload.
- Thoát giữa lệnh (ESC), lệnh bị huỷ nửa chừng: bản vẽ có kẹt ở trạng thái dở (biến hệ thống như OSMODE, CMDECHO, layer hiện hành chưa được khôi phục)?
- Undo sau lệnh: một lần undo có quay về đúng trạng thái trước lệnh không (undo group/marker)?
- Chạy lệnh hai lần liên tiếp; chạy khi lệnh khác đang chạy; hai client cùng gọi MCP.
- Giá trị tool/MCP: trả lỗi có cấu trúc hay chỉ throw; timeout COM; AutoCAD bị treo/đóng giữa chừng; kết nối lại.
- Đơn vị bản vẽ (mm/m/inch), tỉ lệ, hệ toạ độ UCS khác WCS.
- Khối lượng/export: bản vẽ rỗng, đối tượng thiếu thuộc tính, tên layer lạ, trùng tên, ký tự đặc biệt.

## 7. Gợi ý ghép cặp T6

Cặp có tương tác thật giữa các tầng xử lý thường cho lỗi nhiều nhất:

- State cũ (schema cũ) × bất kỳ thao tác ghi nào → migration thiếu.
- Double submit × mạng chậm → bản ghi trùng, hoặc response cũ ghi đè response mới.
- Unicode NFD × so sánh/đáp án/tìm kiếm × import file.
- Refresh giữa luồng × state chỉ ở bộ nhớ.
- Hai tab × ghi storage × đăng xuất ở tab kia.
- Offline × thao tác cần đồng bộ × đóng tab.
- Input dài × lưu storage (quota) × hiển thị lại (tràn layout).
- Sửa storage × tải lại × logic tin tưởng dữ liệu local (điểm, quyền).
- Prompt injection nằm trong dữ liệu đã lưu × tính năng AI đọc lại dữ liệu đó.
- ESC giữa lệnh × biến hệ thống đã đổi × lệnh tiếp theo chạy trên trạng thái hỏng.
