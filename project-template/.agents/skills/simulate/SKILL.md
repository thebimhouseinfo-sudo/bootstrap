---
name: simulate
description: Đóng vai người dùng thật (bé bấm loạn, người dùng cũ, kẻ cố tình phá) để chạy app qua kịch bản từ đơn giản đến phức hợp, rồi TRACE input kích hoạt handler/guard/state/API nào và so với THIẾT KẾ. Kịch bản và kết quả mong đợi chỉ suy ra từ criteria, README, App Brief và hành vi nhìn thấy từ bên ngoài, KHÔNG suy từ source code, để không tạo ra test vừa vặn với code mà user thật không bao giờ nhập như vậy. Ngoại vi (API, AI, phần mềm chủ như AutoCAD cho add-in) được mock hai nhánh pass/fail rồi mô phỏng tiếp app sau kết quả đó. Là CI hành vi, không phải review code. Make sure to use this skill whenever the user says simulate, giả lập user, đóng vai user, test hành vi, test luồng, UAT, chaos/abuse test, mock API lỗi, "thử phá app", "trace input", hoặc muốn kiểm tra app/webapp/CLI/MCP/add-in bằng chuỗi thao tác thật thay vì đọc code, kể cả khi họ không nói chữ "simulate".
---

# Simulate — đóng vai user để CI hành vi

Unit test kiểm một hàm. Skill này kiểm một **hành trình**: một persona, với một trạng thái ban đầu, làm một chuỗi hành động như người thật, và ta quan sát xem bên dưới cái gì được kích hoạt, cái gì bị chặn, kết quả cuối có đúng thiết kế không.

Ta không hỏi "code này đúng không?" mà hỏi "**với tình huống này, hệ thống có hành xử đúng như đã cam kết với người dùng không?**".

## Quy tắc bất khả xâm phạm: thiết kế test từ criteria, không từ code

Nếu người thiết kế test đọc code trước rồi mới nghĩ ra tình huống, test sẽ có hình dạng của code: nó thử đúng cái `if` đang có, đúng tên trường đang có, đúng thứ tự mà lập trình viên nghĩ tới. User thật không bao giờ nhập như vậy, và những thứ user thật làm mà code không lường tới thì không bao giờ được test. Kết quả mong đợi suy từ code thì còn tệ hơn: test luôn pass dù code sai.

Vì vậy mọi thứ sau đây **chỉ được suy ra từ nguồn phía người dùng**: persona, hành trình, input, trạng thái nền, điều kiện ngoại vi, và kết quả mong đợi.

| Vùng được dùng để thiết kế | Vùng cấm khi thiết kế |
|---|---|
| Acceptance criteria, user story | Source code (handler, component, service, route, schema) |
| README, tài liệu hướng dẫn, release notes | Comment trong code |
| App Brief do chủ app cung cấp | Test sẵn có (chúng mang giả định của người viết code) |
| Phản hồi, bug report, câu hỏi do **người dùng** viết | Commit, diff, tên biến, tên hàm |
| Giao diện quan sát được khi chạy app (nhãn, nút, thông báo) | Cấu trúc thư mục suy ra luồng |
| Quan sát lúc chạy: request thật gửi ra ngoài (HAR), nội dung lưu trữ | Cấu hình nội bộ để đoán validation |
| Lệnh cài đặt/chạy trong README (hoặc phần `scripts` để biết cách chạy) | |

Ngoại lệ duy nhất: tra **cách chạy app** (lệnh, port, biến môi trường) khi README không nói; chỉ đọc đúng phần đó, không đọc logic.

### Hai vai, một bức tường

- **Designer (mù code)**: viết hợp đồng, scenario, profile mock từ vùng được dùng. Không mở file source.
- **Tracer (được đọc code)**: chỉ làm việc **sau khi scenario đã đóng băng**. Chạy scenario, quan sát handler/guard nào được kích hoạt, và khi có FAIL thì đọc code để chỉ ra tầng đầu tiên chệch thiết kế.

Bức tường được giữ bằng **đóng băng**: khi Designer xong, lưu scenario vào `simulate/scenarios/` và ghi `simulate/FROZEN.md` (ngày giờ, danh sách ID, hash nội dung khối `design`). Sau mốc này Tracer không sửa khối `design` của scenario nào, không bớt scenario "khó pass", không đổi kết quả mong đợi cho khớp với những gì code làm. Nếu có subagent thì giao hai vai cho hai agent riêng. Nếu chỉ có một agent thì giữ đúng thứ tự và ghi vào báo cáo rằng hai vai do cùng một phiên đảm nhận.

Sau khi đóng băng, chỉ được thêm scenario mới (`origin: followup`) khi nó xuất phát từ một câu hỏi ở mức người dùng ("nếu user làm X sau khi gặp lỗi này thì sao?") hoặc từ câu trả lời mới của chủ app, không bao giờ từ "có một nhánh code chưa được chạm tới". Mỗi scenario mới vẫn phải qua câu hỏi thực tế ở dưới.

### Câu hỏi thực tế (áp cho từng scenario)

> Ai là người thật, trong tình huống nào, vì sao lại làm đúng chuỗi này? Và kết quả họ **được hứa** là gì?

Phải trả lời được bằng ngôn ngữ của người dùng, ghi vào `why_a_user_does_this`. Nếu chỉ trả lời được bằng cách nhắc tên hàm, tên biến hay một nhánh code, bỏ scenario đó. Ngay cả persona "kẻ phá hoại" cũng chỉ dùng những kênh một kẻ phá thật có (ô nhập, URL, devtools, file tải lên, gọi API công khai), không dùng giá trị được chế riêng để trúng một đoạn code cụ thể.

## Đầu vào của tester

1. **Criteria**: những gì app cam kết với người dùng, dạng Given/When/Then hoặc user story (mẫu ở `references/app-brief-template.md`). Đây là oracle.
2. **App Brief**: app là gì, ai dùng, dùng thế nào, hành trình thật, phụ thuộc ngoài (Phase 0).

Thiếu criteria thì không có chuẩn để phán. Khi đó **phỏng vấn chủ app** để cùng viết criteria (Phase 1), không "đọc code để biết app đang làm gì rồi coi đó là đúng".

## Chín nguyên tắc

1. **Mù code khi thiết kế** (mục trên). Đọc code chỉ để thực thi và chẩn đoán, sau khi đóng băng.
2. **Oracle từ criteria.** Thứ tự tin cậy: criteria và tài liệu > điều chủ app xác nhận > quy ước chung mà người dùng nào cũng kỳ vọng (ví dụ lỗi phải có thông báo hiểu được) > không có gì thì `GAP`. Hành vi hiện tại của code **không bao giờ** là nguồn của kết quả mong đợi.
3. **Scenario bắt nguồn từ hành trình thật**, rồi biến đổi (đổi input, chèn gián đoạn, đổi state), mỗi cái có lý do người dùng.
4. **Trace xuyên tầng.** Input → event/handler → guard → state → persistence → ranh giới ngoại vi → output. Trace là **kết quả quan sát khi chạy**, không phải đầu vào của thiết kế.
5. **Ngoại vi luôn có hai nhánh** pass và fail, và trace đi tiếp sau kết quả của ngoại vi.
6. **Bị block cũng là kết quả hợp lệ nhưng phải phân loại** (đúng thiết kế, chặn nhầm, lọt qua, rò rỉ).
7. **Thang T0–T6**, từ đơn giản tới tổ hợp và phá hoại.
8. **Invariant chạy ở mọi bước.**
9. **Trung thực về mức xác thực**: `executed` / `instrumented` / `static-trace`, và độ trung thực của mock `recorded` / `documented` / `guessed`.

## Quy trình

### Phase 0 — Intake: App Brief

Thu thập theo thứ tự, chỉ từ vùng được dùng:

1. **Tự điền trước** từ README, tài liệu, release notes, phản hồi của người dùng, và giao diện khi chạy thử. Đánh dấu từng mục `[known]`, `[derived-from-docs]`, hoặc `[assumed]`.
2. **Hỏi phần còn thiếu**, gộp một lần, ưu tiên: hành trình thật, ngoại vi, criteria, điều chủ app lo nhất.
3. Người dùng không trả lời được thì ghi `[assumed]` kèm giả định cụ thể, và scenario dựa trên đó mang nhãn `assumed`.

Tám nhóm (mẫu đầy đủ ở `references/app-brief-template.md`): tổng quan; hành trình thật; hành vi thực tế đã biết (từ người dùng); cách chạy; phụ thuộc ngoài; dữ liệu và phiên bản cũ; criteria/luật nghiệp vụ; phạm vi và rủi ro. Lưu `simulate/app-brief.md`.

Ngưỡng tối thiểu để sinh scenario T3 trở lên: có ít nhất một hành trình, danh sách phụ thuộc ngoài, và criteria cho hành trình đó (kể cả do chủ app nói miệng). Dưới ngưỡng chỉ làm T0–T2 và nói rõ vì sao dừng.

### Phase 1 — Contract: hợp đồng từ criteria

Với mỗi criterion, viết ra hành vi cam kết ở mức người dùng thấy được, kèm nguồn:

```
AC-012  Khi user gửi tin nhắn trống hoặc chỉ khoảng trắng → tin không được gửi, ô nhập giữ nguyên.
        nguồn: README §Chat                        (documented)
AC-013  Khi mất mạng lúc gửi tin → user thấy thông báo dễ hiểu và tin vẫn còn trong ô nhập để gửi lại.
        nguồn: chủ app xác nhận                    (owner-stated)
AC-014  Khi dịch vụ chat hết giờ chờ → ?           (GAP, cần chủ app quyết)
```

Quy tắc:

- Hợp đồng chỉ nói điều **quan sát được từ ngoài**: màn hình, dữ liệu được lưu như đã hứa, thứ gửi ra ngoài ở mức nghiệp vụ (ví dụ "một yêu cầu gửi tới dịch vụ chat", không phải tên hàm). Không ghi tên handler hay guard; chúng là thứ ta **khám phá khi chạy**.
- Nhánh fail của ngoại vi cũng cần criteria. Im lặng nghĩa là `GAP`. **Hỏi chủ app gộp một lần** cho GAP quan trọng nhất; không tự điền bằng cách xem code đang làm gì.
- Chốt invariants (mục dưới).
- Với mỗi criterion, ghi mức ưu tiên (mất dữ liệu, tiền, an toàn trẻ em > trải nghiệm > thẩm mỹ).

### Phase 2 — Scenario theo thang T0–T6 (Designer, mù code)

Danh mục giá trị ở `references/input-catalog.md`. Chỉ chọn giá trị mà persona **có thể tự nhiên tạo ra** qua giao diện hoặc kênh công khai của app.

| Tầng | Tên | Câu hỏi | Ví dụ |
|---|---|---|---|
| T0 | Happy path | Luồng chính có chạy không? | Đăng ký → làm bài → xem kết quả |
| T1 | Biến thể input | Giá trị người ta thật sự nhập có xử lý đúng không? | Rỗng, 1 ký tự, dán đoạn dài, tiếng Việt NFC/NFD, emoji, số âm |
| T2 | Biến thể state | Cùng hành động, khác trạng thái nền? | Lần đầu vs quay lại, dữ liệu rỗng vs đầy, dữ liệu phiên bản cũ, đã đăng xuất |
| T3 | Chuỗi & thứ tự | Đi sai thứ tự/giữa chừng có ổn không? | Back, refresh giữa bước, bỏ qua bước, quay lại bước cũ |
| T4 | Thời gian & môi trường | Nhịp độ và hạ tầng xấu? | Double click, bấm dồn, 2 tab, mạng chậm, ngoại vi lỗi giữa chừng |
| T5 | Cố ý phá | Có thể bị lạm dụng bằng kênh có sẵn không? | Canary XSS qua ô nhập, sửa localStorage, đổi tham số URL, file nhập lỗi |
| T6 | Tổ hợp | Hai điều kiện cùng lúc? | Dữ liệu cũ + double click + ngoại vi lỗi |

Cách sinh, theo thứ tự:

1. **Mỗi hành trình thật thành một scenario T0**, đúng thứ tự thật, có thời gian suy nghĩ của người (đọc, do dự, gõ), không phải chuỗi lệnh liên tục.
2. **Biến đổi hành trình** để ra T1–T6: đổi input, chèn gián đoạn (refresh, mất mạng, chuyển tab, bỏ đi rồi quay lại), đổi state nền, đổi thiết bị. Một biến đổi cho T1–T4; nhiều biến đổi cho T6.
3. **Persona** lấy từ người dùng thật trong brief, kèm thiết bị và bối cảnh (bé dùng máy bảng của bố mẹ, kỹ sư dùng bản vẽ lớn trên máy cũ).
4. **Criteria coverage** (thay cho "guard coverage"): mỗi criterion có ít nhất một scenario kiểm điều được hứa và ít nhất một scenario đi sát biên của điều được hứa (vừa đủ để còn đúng, và vừa quá để phải bị chặn hoặc báo lỗi).
5. Persona hợp lý theo tình huống: **Newbie** bấm theo trực giác; **Bé nhỏ** bấm loạn, kéo thả sai; **Người dùng cũ** có dữ liệu phiên bản trước; **Người vội** không chờ loading; **Người mạng yếu**; **Người tò mò** mở devtools sửa storage hoặc URL; **Kẻ phá hoại** lạm dụng bằng kênh sẵn có.
6. T6 dùng pairwise trên các trục (loại input, trạng thái user, nhịp độ, ngoại vi, thiết bị/locale, dữ liệu lưu).
7. Giữ vừa phải: 30–60 scenario có chủ đích, chưa tính biến thể mock.

Mỗi scenario viết theo mẫu bên dưới, **chỉ điền khối `design`**.

### Phase 3 — Ranh giới ngoại vi, mock hai nhánh, đóng băng

**Xác định ngoại vi** từ brief, README, tài liệu kiến trúc, và **quan sát lúc chạy** (chạy app một lần, ghi HAR/lưu request, xem quyền thiết bị nào được hỏi, xem lệnh nào gửi sang phần mềm chủ). Không đọc code để tìm "chỗ nào gọi ra ngoài".

Với mỗi ngoại vi, lập **boundary card** ở mức hợp đồng: app gửi gì đi (theo nghiệp vụ), mong nhận gì về, criteria nào liên quan. Chi tiết kỹ thuật và mã mẫu ở `references/external-mocks.md`.

Profile mock chia hai nhánh, chọn theo **lỗi mà đời thật hay gặp** (kể cả khi criteria chưa nói tới; khi đó verdict là `GAP`):

- **Pass**: điển hình, rỗng, rất dài, Unicode, chậm nhưng thành công.
- **Fail**: mất mạng, timeout, 401/429/500, 200 nhưng sai dạng, nửa chừng, trả muộn sai thứ tự, trả trùng, từ chối quyền, hết quota, nội dung độc hại.

Quy tắc:

- Mỗi scenario chạm ngoại vi chạy tối thiểu pass và một đại diện cho mỗi **lớp lỗi mà criteria phân biệt**; ngoài ra chọn vài lỗi phổ biến (mạng, timeout, 5xx) dù criteria im lặng. Biến thể đặt ID `T4-007@chat_api=timeout`.
- Nhánh fail có criteria riêng; im lặng là `GAP`, không phải `PASS`.
- Ghi lại **chiều đi ra** của mock để kiểm app gửi gì, bao nhiêu lần.
- Gắn độ trung thực mock: `recorded`, `documented`, `guessed`.
- Mock tách khỏi app; không sửa app để nhường chỗ cho mock.

#### Tiếp tục mô phỏng sau ranh giới

Mock không phải điểm dừng. Kết quả mock là **input của tầng tiếp theo**: trace đi tiếp qua cách app nhận kết quả, cập nhật hiển thị và dữ liệu, rồi tới **hành động kế tiếp của user** (thử lại ngay, làm việc khác, huỷ, đóng, chạy lại sau khi nguyên nhân đã sửa). Ví dụ add-in AutoCAD: lệnh gửi vào CAD là rời khỏi app; thay CAD bằng host giả trả thành công, load fail, bận, bị ESC, làm được một nửa, hoặc im lặng, rồi mô phỏng tiếp.

- **Host có trạng thái và trạng thái sống sót qua lỗi** (lệnh làm một phần để lại đối tượng đã đổi, biến hệ thống chưa khôi phục).
- **Ranh giới có thể bất đồng bộ và hai chiều**: kết quả có thể đến muộn, sai thứ tự hoặc không đến; phần mềm chủ có thể chủ động gọi ngược (tài liệu đóng, lệnh bị huỷ, host tắt).
- **"Đã gửi" khác "đã xác nhận"**: app có báo thành công hoặc ghi dữ liệu trước khi bên kia xác nhận? Có hoàn tác khi bên kia báo fail?
- Mỗi nhánh có 2–3 follow-up tự nhiên của user, tối đa hai lượt sau ranh giới (sâu hơn chỉ ở T6).
- Ví dụ đầy đủ: `references/example-autocad-addin.md`.

#### Đóng băng

Kiểm lại từng scenario qua câu hỏi thực tế, kiểm mọi criterion có scenario, rồi ghi `simulate/FROZEN.md`. Từ đây mới được mở source code.

### Phase 4 — Thực thi và trace (Tracer)

Chọn chế độ mạnh nhất khả thi và nói rõ:

- **A. Executed**: chạy app thật, tương tác qua giao diện như user (nhãn, vai trò nhìn thấy được, không dùng selector nội bộ khi có thể), ngoại vi được mock. Mẫu ở `references/harness-playwright.md`.
- **B. Instrumented**: thêm log/hook tạm vào handler và guard để thấy đường đi; xong thì revert hoàn toàn bằng git.
- **C. Static-trace**: không chạy được. Dùng như **cách thực thi** scenario đã đóng băng: lần theo code, ghi file:dòng, đi cả hai nhánh tại ngoại vi. Không được dùng bước này để thêm, bớt hay sửa scenario. Mọi kết luận gắn `static-trace` và độ tin cậy thấp hơn.

Bảng trace cho mỗi scenario, các cột `Mong đợi` lấy từ khối `design` đã đóng băng; các cột còn lại là quan sát:

| # | Hành động của user | Mong đợi (từ criteria) | Quan sát (màn hình/dữ liệu) | Handler/guard kích hoạt (quan sát) | State trước → sau | Ranh giới (→ gửi / ← kết quả mock) | Verdict |
|---|---|---|---|---|---|---|---|

Tại ranh giới tách hai dòng `→ gửi` và `← kết quả`, rồi ghi tiếp các dòng sau ranh giới tới hết follow-up. Cột "Handler/guard" **do Tracer điền khi chạy**; nếu bước bị chặn, ghi guard nào chặn và lý do.

### Phase 5 — Phán quyết và chẩn đoán

Phán quyết so quan sát với **criteria** (không so với code). Nhãn duy nhất:

- `PASS`: đúng cam kết.
- `PASS-BLOCKED`: bị chặn đúng như cam kết (thông báo đúng, state không đổi).
- `FAIL-BEHAVIOR`: chạy nhưng kết quả sai cam kết.
- `FAIL-BYPASS`: đáng ra phải bị chặn nhưng lọt qua. Nghiêm trọng nhất.
- `FAIL-FALSE-BLOCK`: user hợp lệ bị chặn nhầm.
- `FAIL-LEAK`: lỗi/chặn nhưng đã để lại side effect hoặc state nửa vời.
- `FAIL-DESYNC`: trạng thái app và ngoại vi lệch nhau.
- `FAIL-UNHANDLED-EXTERNAL`: ngoại vi lỗi mà app không xử lý (treo, trắng trang, nuốt lỗi).
- `FAIL-INVARIANT`: vi phạm invariant.
- `GAP`: criteria không nói; ghi lại hệ thống đã làm gì để chủ app quyết đúng hay sai. **Không** tự coi hành vi đó là đúng.
- `UNVERIFIED`: không xác thực được (nêu lý do).

**Chẩn đoán (lúc này mới đọc code)**: với mỗi FAIL, chỉ ra tầng đầu tiên đi chệch (file:dòng) và đề xuất sửa ngắn. Việc đọc code ở đây chỉ để trả lời "chệch ở đâu", không được dẫn tới đổi kết quả mong đợi hay đổi scenario. Không tự sửa code trừ khi người dùng yêu cầu.

### Phase 6 — Báo cáo và lưu regression

`simulate/report.md`:

- **Tóm tắt**: ma trận tầng × verdict, 3–5 phát hiện đáng chú ý.
- **Chi tiết FAIL**: scenario, `why_a_user_does_this`, trace rút gọn tới bước lỗi, tầng chệch đầu tiên, đề xuất.
- **Ma trận ngoại vi**: mỗi ranh giới × profile → verdict.
- **GAP**: câu hỏi cho chủ app.
- **Criteria coverage**: criterion nào chưa có scenario hoặc chưa có scenario sát biên.
- **Code chưa được chạm tới (thông tin, không phải việc cần test)**: nếu khi trace phát hiện code có xử lý mà không scenario nào chạm tới, **không viết thêm test nhắm vào nó**. Biến nó thành câu hỏi cho chủ app ("code có xử lý X, criteria chưa nói; X có phải cam kết với người dùng không?"). Nếu câu trả lời là có, thêm criterion rồi mới sinh scenario theo quy trình thường (`origin: followup`).
- **Mức xác thực**: tỉ lệ executed/instrumented/static-trace và mock recorded/documented/guessed; ghi rõ hai vai Designer/Tracer là agent riêng hay cùng một phiên.
- **Giả định**: các scenario/criteria `assumed` để chủ app xác nhận.

Lần chạy sau so với report trước: mới hỏng, đã sửa, còn nguyên. Trả lời người dùng bằng tóm tắt ngắn kèm đường dẫn tới report.

## Mẫu scenario

Khối `design` được đóng băng. Khối `observed` do Tracer điền sau khi chạy.

```yaml
id: T4-007
tier: T4
design:
  title: Gửi tin nhắn lần nữa khi tin trước chưa thấy trả lời
  persona: Người vội, điện thoại, mạng chậm
  why_a_user_does_this: "Bấm Gửi mà không thấy gì xảy ra trong vài giây nên bấm lại."
  journey: "Hành trình B: chat với nhân vật (brief §2)"
  criteria: [AC-014]
  oracle_source: documented     # documented | owner-stated | convention
  evidence: assumed             # evidenced | assumed
  origin: design                # design | followup
  precondition: "Đã có 2 tin trong hội thoại"
  think_time: "gõ 3s, bấm gửi, bấm lại sau 1s"
  boundary_mocks:
    chat_api:
      fidelity: documented      # recorded | documented | guessed
      profiles: [ok-typical, ok-slow-3s, fail-timeout, fail-429, fail-malformed-200]
  steps:
    - do: "Gõ 'xin chào' và bấm Gửi"
      expect: "Tin hiện trong hội thoại một lần, có dấu hiệu đang chờ trả lời"
    - do: "Bấm Gửi lần nữa ngay khi chưa có trả lời"
      expect: "Không có tin thứ hai bị gửi đi; user hiểu là đang chờ"
  after_boundary:
    fail-timeout:
      expect: "Thông báo lỗi dễ hiểu; chữ đã gõ không mất; dùng lại được ngay; không còn tin dở trong hội thoại"
      follow_ups:
        - do: "Bấm Gửi lại"
          expect: "Gửi được bình thường"
        - do: "Đóng tab rồi mở lại"
          expect: "Không còn tin dở"
    fail-429:
      expect: "Báo thử lại sau; không tự gửi lại dồn dập"
  invariants_extra: []
# --- Tracer điền sau khi chạy; không sửa khối design ---
observed:
  mode: executed                # executed | instrumented | static-trace
  triggers: []                  # handler quan sát được, theo thứ tự
  guards: []                    # guard đã chạy và kết quả
  state_diff: []
  boundary_sent: []             # app đã gửi gì ra ngoài
  verdict: {}                   # theo từng profile
```

## Invariants mặc định

Kiểm sau **mỗi bước**. Bổ sung invariant riêng ở Phase 1.

1. Không có exception chưa bắt / `pageerror` / unhandled rejection.
2. Không mất dữ liệu người dùng đã lưu.
3. Dữ liệu lưu luôn hợp lệ (không có `undefined`/`NaN` rò vào dữ liệu).
4. UI không kẹt (luôn còn đường đi tiếp hoặc quay lại; không loading vô hạn, kể cả khi ngoại vi không bao giờ trả lời).
5. Mọi lỗi hiện ra user đều có thông báo hiểu được, không lộ stack trace, đường dẫn nội bộ hay nội dung thô của dịch vụ ngoài.
6. Không thực thi nội dung do user nhập hoặc do ngoại vi trả về (canary `window.__pwned` luôn bằng 0).
7. Không có request ra ngoài danh sách cho phép; không lộ secret trong request/response/log.
8. Hành động lặp lại không tạo bản ghi trùng ngoài ý muốn, kể cả khi ngoại vi trả trùng.
9. Trạng thái app phản ánh đúng trạng thái ngoại vi sau mỗi kết quả (không desync), và sau lỗi, trạng thái nền của host (biến hệ thống, lệnh đang chạy, undo) được trả về như trước khi app tác động.

## An toàn khi phá hoại

- Chỉ chạy trên **bản local/test của chính app** của người dùng. Nếu môi trường duy nhất là production hoặc dữ liệu thật, dừng lại và hỏi.
- **Snapshot trước, khôi phục sau**: sao lưu storage/DB/file mẫu; chạy trong profile trình duyệt sạch hoặc thư mục tạm.
- **Mock mọi ngoại vi** mà scenario chạm tới; không dùng khoá API hay tài khoản thật trong kịch bản phá.
- Payload chỉ là **canary vô hại** (ví dụ `<img src=x onerror="window.__pwned=1">`, chuỗi rất dài, JSON hỏng). Phát hiện lỗ hổng thật thì báo cáo mức độ và cách tái hiện tối thiểu, không viết chuỗi khai thác hoàn chỉnh.
- Không vượt phạm vi: không quét mạng, không vét cạn đăng nhập vào dịch vụ thật.

## Khi nào làm nhẹ hơn

Nếu người dùng chỉ muốn thử nhanh một tính năng, rút brief còn vài dòng (app làm gì, người dùng cần gì, kết quả được hứa là gì, gọi ra ngoài những gì), trả kết quả trong chat. Vẫn giữ bốn thứ cốt lõi: không thiết kế test từ code, bảng trace, nhãn verdict, và hai nhánh pass/fail ở ngoại vi.
