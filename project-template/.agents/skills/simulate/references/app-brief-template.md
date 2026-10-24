# App Brief — đầu vào của tester

Brief là thứ giúp scenario giống hành vi thật, và criteria trong brief là chuẩn để phán đúng sai. Cả hai phải đến từ **phía người dùng và chủ app**, không rút ra từ source code: tester không mở code để biết "app đang làm gì" rồi coi đó là đúng. Điền càng cụ thể càng tốt; mục nào chưa biết thì ghi `?` để tester hỏi hoặc ghi giả định. Lưu thành `simulate/app-brief.md`.

Quy ước nhãn cho từng mục: `[known]` do chủ app nói hoặc có trong tài liệu, `[derived]` tester suy ra từ code/tài liệu, `[assumed]` giả định chưa xác nhận.

## Mục lục
1. Nguồn được dùng để điền brief (và nguồn bị cấm)
2. Mẫu brief
3. Cách viết criteria
4. Ví dụ điền sẵn (app học tiếng Việt có chat AI)
5. Câu hỏi gộp khi còn thiếu

---

## 1. Nguồn được dùng để điền brief (và nguồn bị cấm)

**Được dùng:**

- README, tài liệu hướng dẫn, release notes, mô tả trên trang đăng tải.
- Acceptance criteria, user story, ghi chú sản phẩm.
- Phản hồi, câu hỏi, bug report do **người dùng viết** (cho biết họ thật sự làm gì và gặp gì).
- Chính giao diện khi chạy thử: nhãn nút, form, thông báo, luồng điều hướng.
- Quan sát lúc chạy: request thật gửi ra ngoài, dữ liệu được lưu, quyền thiết bị được hỏi.
- Lệnh cài và chạy (README, hoặc riêng phần `scripts` để biết cách chạy).

**Không dùng để thiết kế test:** source code, comment trong code, test sẵn có, commit/diff, tên hàm hay biến, cấu trúc thư mục. Chúng cho biết người viết code đã nghĩ gì, không cho biết người dùng cần gì. Tester chỉ được mở code sau khi scenario đã đóng băng, để chạy và chẩn đoán (xem SKILL.md).

Chỉ hỏi chủ app phần còn trống, gộp một lần, ưu tiên mục 2, 5, 7.

## 2. Mẫu brief

```markdown
# App Brief: <tên app>

## 1. Tổng quan
- App làm gì (1–2 câu):
- Người dùng chính (tuổi, vai trò, trình độ dùng máy):
- Thiết bị/trình duyệt/hệ điều hành phổ biến:
- Bối cảnh dùng (ở nhà, trên lớp, văn phòng, di chuyển; mạng ổn hay yếu):
- Cách app được phân phối (web độc lập, nhúng iframe, cài PWA, plugin trong phần mềm khác):

## 2. Hành trình thật (3–5 luồng, theo thứ tự user thực sự đi)
### Hành trình A: <tên>
- Mục tiêu của user:
- Các bước theo thứ tự thật:
  1.
  2.
- Tần suất / ai hay làm:
- Chỗ user hay dừng, do dự, hay bỏ đi:
- Kết quả thành công trông như thế nào:

## 3. Hành vi thực tế đã biết
- User hay làm sai/làm lạ điều gì:
- Bug/khiếu nại đã gặp (kèm cách tái hiện nếu có):
- Số liệu/log/analytics đáng chú ý:
- Thói quen đặc thù (bấm nhanh, dùng phím tắt, dùng lại link cũ, dùng chung máy):

## 4. Cách chạy
- Lệnh cài và chạy (dev/build):
- URL/port:
- Biến môi trường cần có (liệt kê tên, không dán giá trị bí mật):
- Tài khoản/dữ liệu test:
- Có chế độ mock/offline sẵn không:

## 5. Phụ thuộc ngoài (mỗi dịch vụ một khối)
### <tên dịch vụ>   (ví dụ: API chat AI, TTS, Firebase, GitHub API, localStorage, mic, COM AutoCAD)
- App dùng nó để làm gì cho người dùng, ở bước nào của hành trình:
- Bên đó cần nhận gì, trả về gì (theo tài liệu của dịch vụ hoặc quan sát lúc chạy):
- Giới hạn đã biết (rate limit, kích thước, thời gian chờ, quota):
- Cách nó đã hỏng ngoài đời (lỗi từng gặp):
- Có mẫu phản hồi thật để ghi lại không (recorded) hay chỉ có tài liệu (documented):
- Khi nó lỗi, người dùng **nên** thấy và được giữ lại gì (đây là criteria, không phải điều app đang làm):

## 6. Dữ liệu và phiên bản
- Dữ liệu user lưu ở đâu, dạng gì (key/bảng/file):
- Các phiên bản schema đã từng phát hành và khác nhau thế nào:
- Dữ liệu mẫu thật (đã ẩn danh) dùng được cho test T2:

## 7. Criteria và luật nghiệp vụ (xem mục 3 về cách viết)
- Quy tắc cứng (ví dụ: mỗi bài chỉ tính điểm một lần, tên tối đa 20 ký tự):
- Hành vi cam kết khi ngoại vi lỗi (ví dụ: mất mạng thì giữ nháp, không mất bài):
- Điều app cố ý KHÔNG làm:
- Những chỗ chưa quyết định (sẽ thành GAP):

### Criteria
AC-001  Given ... When ... Then ...   (nguồn: ... ; ưu tiên: ...)

## 8. Phạm vi và rủi ro
- Điều tồi tệ nhất có thể xảy ra với user/dữ liệu:
- Luồng quan trọng nhất cần chắc chắn:
- Phần không cần test lần này:
- Mức "phá" được phép (chỉ local/test? có dữ liệu thật không?):
```

## 3. Cách viết criteria

Criteria là cam kết với người dùng, nói bằng điều **nhìn thấy và lưu lại được**. Dạng Given/When/Then:

```
AC-013  Given người dùng đang gõ tin nhắn trong chat
        When mạng bị mất lúc bấm Gửi
        Then họ thấy một thông báo dễ hiểu, chữ đã gõ vẫn còn trong ô nhập, và tin chưa được tính là đã gửi.
        nguồn: chủ app xác nhận     ưu tiên: cao (mất dữ liệu người dùng)
```

Nguyên tắc:

- Không nhắc tên hàm, component, biến, API nội bộ. Nếu muốn nói "gọi hàm X", hãy hỏi: người dùng thấy gì khi X lỗi?
- Mỗi criterion kiểm được bằng quan sát từ ngoài.
- Có criteria cho cả **khi ngoại vi lỗi**, không chỉ khi thành công.
- Không có sẵn thì tester phỏng vấn chủ app, viết nháp theo ngôn ngữ người dùng, và để chủ app xác nhận. Chỗ chủ app chưa quyết thì để `GAP`.
- Được phép dùng quy ước chung mà người dùng nào cũng kỳ vọng (lỗi phải có thông báo hiểu được, không mất dữ liệu đã nhập, nút không bấm đúp ra hai bản ghi), gắn nguồn `convention`.

## 4. Ví dụ điền sẵn (minh hoạ)

Ví dụ giả định để thấy mức chi tiết cần có, không phải thông tin của app thật nào.

```markdown
# App Brief: Học tiếng Việt theo cụm (ví dụ)

## 1. Tổng quan
- App làm gì: người học ghi nhật ký theo cụm từ, có tính năng chat với nhân vật truyện để luyện nói. [known]
- Người dùng chính: người học tiếng Việt, 10–40 tuổi, phần lớn dùng điện thoại. [assumed]
- Phân phối: web tĩnh, nhúng iframe trong blog. [known]

## 2. Hành trình thật
### Hành trình A: Học một cụm mới
  1. Mở app (lần đầu hoặc quay lại)
  2. Chọn chủ đề → xem cụm từ
  3. Nghe phát âm → tự đặt câu → lưu vào nhật ký
- Chỗ hay bỏ đi: bước tự đặt câu (hay để trống, hay gõ không dấu). [assumed]

### Hành trình B: Chat với nhân vật
  1. Mở Story Chat → chọn nhân vật
  2. Gõ tin → chờ phản hồi → gõ tiếp
  3. Thoát giữa chừng, quay lại sau vài giờ

## 5. Phụ thuộc ngoài
### API chat AI
- Gọi ở: gửi tin trong Story Chat.
- Gửi: lịch sử hội thoại + system prompt nhân vật.
- Nhận: văn bản trả lời (có thể stream).
- Giới hạn: có rate limit (theo tài liệu của nhà cung cấp). [derived-from-docs]
- Khi lỗi, người dùng nên thấy gì: chưa có criteria. → GAP, hỏi chủ app.
### localStorage trong iframe
- Lưu nhật ký và lịch sử chat.
- Từng hỏng: trình duyệt chặn storage bên thứ ba trong iframe (Safari). [assumed]
### Phát âm (Web Speech/TTS)
- Có thể bị chặn tới khi user tương tác lần đầu.

## 7. Luật nghiệp vụ
- Lịch sử chat giữ tối đa N tin (N: ?). → cần xác nhận.
- Đáp án so khớp có/không phân biệt dấu: ? → cần xác nhận.
```

## 5. Câu hỏi gộp khi còn thiếu

Hỏi một lần, đánh số, ưu tiên những câu làm thay đổi scenario nhiều nhất:

1. Hành trình nào user dùng nhiều nhất, và họ hay bỏ ở bước nào?
2. App gọi ra ngoài những dịch vụ nào? Dịch vụ nào từng lỗi ngoài đời và lỗi ra sao?
3. Khi dịch vụ đó lỗi, người dùng **nên** thấy gì và được giữ lại gì (không phải code đang làm gì)?
4. Có dữ liệu hoặc phiên bản cũ đang nằm ở user không?
5. Quy tắc cứng nào không được vi phạm (điểm, tiền, dữ liệu học)?
6. Môi trường nào được phép phá?

Nếu người dùng không trả lời một câu, ghi `[assumed]` kèm giả định cụ thể và tiếp tục.
