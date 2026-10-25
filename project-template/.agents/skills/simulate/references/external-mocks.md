# Mock ranh giới ngoại vi: hai nhánh pass và fail

Đọc file này ở Phase 3 (ranh giới và mock) và Phase 4 (nối mock vào lúc chạy). Mã trong file là **mẫu khởi đầu, chưa kiểm chạy trên app cụ thể**; chạy thử một profile pass trước khi tin kết quả của các profile fail.

## Mục lục
1. Boundary card
2. Danh mục profile pass và fail
3. Mock web bằng Playwright (profile, ghi lại chiều đi ra, chạy mọi profile)
4. Lỗi của API trình duyệt (storage, quyền, đồng hồ, offline)
5. Mock trong Vitest/Jest
6. Mock CLI / MCP / COM (AutoCAD)
7. Mock tính năng AI
8. Static-trace: đi hai nhánh bằng tay
9. Vệ sinh mock

---

## 1. Boundary card

Mỗi ranh giới ngoại vi một card, đặt trong `simulate/boundaries.md`. Card được viết ở mức hợp đồng, **từ brief, tài liệu của dịch vụ và quan sát lúc chạy (HAR, lệnh gửi sang phần mềm chủ), không từ source code**:

```yaml
boundary: chat_api
kind: http                       # http | sdk | browser-api | storage | cli | com | file
purpose: "trả lời tin nhắn của người học trong Story Chat"      # theo brief
observed_at_runtime: { method: POST, url: /api/chat }           # ghi từ HAR khi chạy thử app
sends:     "lịch sử hội thoại + tin mới"                         # mô tả nghiệp vụ
expects:   "một câu trả lời văn bản"
criteria: [AC-013, AC-014]       # cam kết với người dùng khi nó thành công và khi nó lỗi
fidelity: documented             # recorded | documented | guessed
profiles:
  pass: [ok-typical, ok-edge-empty-reply, ok-edge-long-reply, ok-slow-3s]
  fail: [fail-network, fail-timeout, fail-401, fail-429, fail-500, fail-malformed-200, fail-stream-cut, fail-late-out-of-order]
# Tracer điền SAU khi chạy (không điền ở bước thiết kế):
observed_handling: { when_fail: "...", where: "file:dòng" }
```

Nếu sau khi chạy thấy app không có xử lý nào khi ngoại vi lỗi, đó là `FAIL-UNHANDLED-EXTERNAL` (khi criteria yêu cầu xử lý) hoặc `GAP` (khi criteria im lặng).

## 2. Danh mục profile

### Nhánh pass
| Profile | Mô tả | Kiểm điều gì |
|---|---|---|
| `ok-typical` | Phản hồi đúng như tài liệu | Luồng chính |
| `ok-edge-empty` | Hợp lệ nhưng rỗng (mảng rỗng, chuỗi rỗng) | App có coi rỗng là lỗi hay hiển thị trống đẹp |
| `ok-edge-long` | Rất dài, nhiều dòng, nhiều ký tự đặc biệt | Tràn layout, cắt chuỗi, lưu quá quota |
| `ok-edge-unicode` | Tiếng Việt NFC/NFD, emoji, RTL | So khớp, hiển thị, đo độ dài |
| `ok-slow` | Thành công sau 3–10 giây | Loading, double submit, người dùng bỏ đi giữa chừng |
| `ok-extra-fields` | Thêm trường lạ | Parser có chịu được không |

### Nhánh fail
| Profile | Mô tả | Kiểm điều gì |
|---|---|---|
| `fail-network` | Mất kết nối ngay | Offline, thông báo, giữ dữ liệu nhập |
| `fail-timeout` | Treo rồi hết giờ | Có timeout không, UI có kẹt loading vô hạn |
| `fail-401/403` | Hết phiên/không quyền | Điều hướng đăng nhập, không mất dữ liệu |
| `fail-404` | Tài nguyên không còn | Mục đã bị xoá ở nơi khác |
| `fail-429` | Quá giới hạn (có/không `Retry-After`) | Có tự retry dồn dập không, có báo user |
| `fail-500/503` | Lỗi phía dịch vụ | Retry hợp lý, không ghi dở |
| `fail-malformed-200` | Mã 200 nhưng sai schema/JSON hỏng/rỗng | Parser, null-check, không crash |
| `fail-stream-cut` | Đứt giữa chừng khi stream | Nội dung nửa vời có được lưu như hoàn chỉnh không |
| `fail-late-out-of-order` | Response cũ đến sau response mới | Race condition, ghi đè sai |
| `fail-duplicate` | Trả/giao hai lần | Idempotent, không tạo bản ghi trùng |
| `fail-permission-denied` | Bị từ chối quyền thiết bị | Đường lui khi không có mic/camera |
| `fail-quota` | Hết quota/đầy dung lượng | Thông báo, không mất dữ liệu cũ |
| `fail-hostile-body` | Phản hồi chứa canary XSS hoặc chỉ thị injection | App có tin nội dung ngoại vi không |

Chọn profile theo **lớp lỗi mà criteria phân biệt** cộng vài lỗi phổ biến ngoài đời (mạng, timeout, 5xx) dù criteria chưa nói tới; khi đó verdict là `GAP`. Không chọn profile vì biết code có nhánh xử lý riêng cho nó. Không cần đủ danh mục cho mọi ranh giới.

## 3. Mock web bằng Playwright

`simulate/harness/boundary.ts`

```ts
import type { Page, Route } from '@playwright/test';

export type Received = { method: string; url: string; body: string | null; t: number };
export type BoundaryState = { calls: number };

export type Profile = {
  name: string;
  branch: 'pass' | 'fail';
  respond: (route: Route, state: BoundaryState) => Promise<void>;
};

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
const json = (body: unknown) => ({ contentType: 'application/json', body: JSON.stringify(body) });

export const profiles = {
  okTypical: (body: unknown): Profile => ({
    name: 'ok-typical', branch: 'pass',
    respond: async (route) => route.fulfill({ status: 200, ...json(body) }),
  }),
  okSlow: (ms: number, body: unknown): Profile => ({
    name: `ok-slow-${ms}ms`, branch: 'pass',
    respond: async (route) => { await sleep(ms); await route.fulfill({ status: 200, ...json(body) }); },
  }),
  failNetwork: (): Profile => ({
    name: 'fail-network', branch: 'fail',
    respond: async (route) => route.abort('failed'),
  }),
  // Treo lâu hơn timeout của app rồi mới đứt. Chỉnh `hangMs` lớn hơn timeout app đặt.
  failTimeout: (hangMs = 15000): Profile => ({
    name: 'fail-timeout', branch: 'fail',
    respond: async (route) => { await sleep(hangMs); await route.abort('timedout').catch(() => {}); },
  }),
  failStatus: (status: number, headers: Record<string, string> = {}): Profile => ({
    name: `fail-${status}`, branch: 'fail',
    respond: async (route) =>
      route.fulfill({ status, headers, ...json({ error: 'mock-error' }) }),
  }),
  failMalformed200: (rawBody = '{"reply":'): Profile => ({
    name: 'fail-malformed-200', branch: 'fail',
    respond: async (route) => route.fulfill({ status: 200, contentType: 'application/json', body: rawBody }),
  }),
  // Lần gọi đầu trả muộn với nội dung CŨ, lần gọi sau trả nhanh với nội dung MỚI.
  failLateOutOfOrder: (oldBody: unknown, newBody: unknown): Profile => ({
    name: 'fail-late-out-of-order', branch: 'fail',
    respond: async (route, state) => {
      if (state.calls === 1) { await sleep(3000); await route.fulfill({ status: 200, ...json(oldBody) }); }
      else { await route.fulfill({ status: 200, ...json(newBody) }); }
    },
  }),
  failHostileBody: (): Profile => ({
    name: 'fail-hostile-body', branch: 'fail',
    respond: async (route) =>
      route.fulfill({ status: 200, ...json({ reply: '<img src=x onerror="window.__pwned=1">' }) }),
  }),
};

// Gắn mock vào một ranh giới và ghi lại mọi thứ app GỬI ĐI (kiểm chiều đi ra).
export async function mockBoundary(page: Page, urlGlob: string, profile: Profile) {
  const received: Received[] = [];
  const state: BoundaryState = { calls: 0 };
  await page.route(urlGlob, async (route) => {
    const req = route.request();
    state.calls++;
    received.push({ method: req.method(), url: req.url(), body: req.postData(), t: Date.now() });
    await profile.respond(route, state);
  });
  return { received, state };
}
```

Chạy mọi profile của một scenario, mỗi profile một test con có ID `@boundary=profile`:

```ts
import { test, expect } from '@playwright/test';
import { makeSimulator } from '../harness/step';
import { mockBoundary, profiles } from '../harness/boundary';

const chatProfiles = [
  profiles.okTypical({ reply: 'xin chào' }),
  profiles.okSlow(3000, { reply: 'xin chào' }),
  profiles.failNetwork(),
  profiles.failStatus(429, { 'Retry-After': '5' }),
  profiles.failStatus(500),
  profiles.failMalformed200(),
  profiles.failHostileBody(),
];

for (const profile of chatProfiles) {
  test(`T4-007@chat_api=${profile.name}`, async ({ page }) => {
    const sim = await makeSimulator(page, { allowedHosts: ['localhost:5173'] });
    const chat = await mockBoundary(page, '**/api/chat', profile);

    await page.goto('http://localhost:5173/');
    const rec = await sim.step('gõ và gửi', async () => {
      await page.getByRole('textbox').fill('xin chào');
      await page.getByRole('button', { name: /gửi/i }).click();
    });

    // Chiều đi ra: app gửi đúng 1 request, nội dung có đủ những gì tài liệu/HAR cho thấy dịch vụ cần.
    expect(chat.received.length).toBe(1);
    expect(JSON.parse(chat.received[0].body ?? '{}')).toHaveProperty('messages');

    // Invariant luôn kiểm; kết quả riêng cho từng nhánh đọc ở bước verdict, so với khối `after_boundary` của scenario.
    expect(rec.invariantViolations).toEqual([]);
    // Các assert theo nhánh (thông báo lỗi, nội dung hội thoại, ô nhập) thêm theo `after_boundary` của scenario.
  });
}
```

Tên test chứa hậu tố `@chat_api=<profile>` để báo cáo gom thành ma trận ngoại vi × profile.

Mock của các nền tảng dựa trên SDK gọi HTTP vẫn chặn được ở tầng mạng bằng `page.route` theo URL của nhà cung cấp; nếu SDK dùng WebSocket hoặc kênh khác, chuyển sang mock mức module (mục 5).

## 4. Lỗi của API trình duyệt

Chèn bằng `page.addInitScript` **trước** khi trang tải:

```ts
// localStorage đầy sau N lần ghi
await page.addInitScript((limit) => {
  let n = 0;
  const orig = Storage.prototype.setItem;
  Storage.prototype.setItem = function (k: string, v: string) {
    if (++n > limit) throw new DOMException('quota', 'QuotaExceededError');
    return orig.call(this, k, v);
  };
}, 3);

// storage bị chặn hoàn toàn (kiểu iframe bên thứ ba/chế độ riêng tư)
await page.addInitScript(() => {
  Object.defineProperty(window, 'localStorage', {
    get() { throw new DOMException('denied', 'SecurityError'); },
  });
});

// từ chối quyền micro
await page.addInitScript(() => {
  navigator.mediaDevices.getUserMedia = () =>
    Promise.reject(new DOMException('denied', 'NotAllowedError'));
});
```

Ngoài ra:

- Offline: `await page.context().setOffline(true)` và bật lại giữa chừng để mô phỏng mạng chập chờn.
- Đồng hồ: `page.clock` của Playwright (bản có hỗ trợ clock) để tua nhanh timeout, đổi ngày qua nửa đêm. Kiểm phiên bản Playwright đang dùng trước.
- Âm thanh/TTS: ghi đè `speechSynthesis.speak` để báo thành công hoặc phát sự kiện `error`.
- Iframe: cho app chạy trong một trang bọc bằng iframe khác origin để thấy storage/cookie bị phân vùng.

## 5. Mock trong Vitest/Jest

```ts
import { vi } from 'vitest';

// Mock fetch toàn cục theo profile
function mockFetch(profile: 'ok' | 'network' | '500' | 'malformed') {
  vi.stubGlobal('fetch', vi.fn(async () => {
    if (profile === 'network') throw new TypeError('Failed to fetch');
    if (profile === '500') return new Response('{"error":"x"}', { status: 500 });
    if (profile === 'malformed') return new Response('{"reply":', { status: 200 });
    return new Response(JSON.stringify({ reply: 'ok' }), { status: 200 });
  }));
}
```

Với SDK hoặc service module, `vi.mock('./services/chat', ...)` trả về hoặc ném lỗi theo profile. Mock ở mức module bỏ qua tầng mạng nên không kiểm được timeout thật; ghi rõ giới hạn đó trong báo cáo.

## 6. Mock CLI / MCP / COM (AutoCAD)

Nguyên tắc giống nhau: thay phía bên kia bằng một stub có thể lập trình để trả pass hoặc fail, và ghi lại lệnh nó nhận.

- **CLI**: chạy lệnh với `PATH` trỏ tới thư mục chứa script giả của công cụ ngoài (git, ffmpeg...), script này trả exit code và stdout theo profile.
- **MCP server**: viết client giả gọi tool, hoặc server giả cho phía client; profile gồm: trả lỗi có cấu trúc, ném exception, không trả lời (treo), trả kết quả sai schema, đóng kết nối giữa chừng.
- **COM/AutoCAD và add-in chạy trong CAD**: xem ví dụ đầy đủ ở `example-autocad-addin.md` (host giả có trạng thái, profile load fail/lệnh fail, mô phỏng tiếp sau kết quả). Tóm tắt: bọc đối tượng COM sau một interface mỏng để thay bằng stub. Profile fail gợi ý: AutoCAD bận từ chối cuộc gọi, máy chủ COM không còn (AutoCAD bị đóng giữa chừng), bản vẽ chỉ đọc hoặc đang bị khoá, không có đối tượng nào được chọn, đối tượng thiếu thuộc tính, layer bị khoá/đóng băng, lệnh bị huỷ giữa chừng (ESC). Với các mã lỗi HRESULT cụ thể, đối chiếu tài liệu COM/AutoCAD thay vì tin trí nhớ; ghi `fidelity: guessed` nếu chưa có mẫu lỗi thật.
- Nếu không thể stub (phải chạy trên AutoCAD thật): chạy trên bản vẽ test, chụp trạng thái biến hệ thống trước và sau mỗi lệnh (`OSMODE`, `CMDECHO`, layer hiện hành, `UNDO` marker), và ghi chế độ là `executed` kèm cảnh báo không mô phỏng được lỗi COM.

## 7. Mock tính năng AI

Phản hồi của model cũng là ranh giới ngoại vi, và dễ sai theo cách khó đoán. Profile nên có:

- `ok-typical`: câu trả lời bình thường đúng ngôn ngữ.
- `ok-edge`: rất dài, nhiều dòng, có markdown/bảng/code block, có emoji.
- `fail-empty`: chuỗi rỗng hoặc chỉ khoảng trắng.
- `fail-wrong-format`: yêu cầu JSON nhưng trả văn xuôi, JSON bọc trong ```json```, JSON thiếu trường, JSON cắt cụt.
- `fail-wrong-language`: trả sai ngôn ngữ so với bài học.
- `fail-refusal`: từ chối trả lời.
- `fail-off-topic-or-unsafe`: lạc đề hoặc nội dung không phù hợp lứa tuổi (với app trẻ em, kiểm bộ lọc trước khi hiển thị).
- `fail-hostile-body`: chứa canary XSS hoặc chỉ thị "bỏ qua hướng dẫn trước", để xem app có tin và thực thi nội dung do model trả về không.
- `fail-stream-cut`, `fail-timeout`, `fail-429`: như mục 2.

Kiểm cả chiều đi: prompt app gửi lên có chèn nguyên văn input của user vào chỗ chỉ thị không, có kèm dữ liệu riêng tư không cần thiết không, có cắt lịch sử đúng khi quá dài không.

## 8. Static-trace: đi hai nhánh bằng tay

Chỉ dùng ở vai Tracer, sau khi scenario đã đóng băng, và chỉ để **thực thi** scenario đã có. Khi không chạy được, tại mỗi ranh giới ghi hai dòng trace song song:

```
T4-007 bước 2  src/chat/send.ts:42  await fetch('/api/chat')
  ├─ nhánh PASS (giả định: 200 {reply}):  :47 setHistory([...h, reply])           → khớp C-014
  └─ nhánh FAIL (giả định: throw/timeout): :58 catch → setError('Có lỗi')
        ⚠ :44 đã setHistory([...h, userMsg]) TRƯỚC khi gọi API → tin nằm lại history → FAIL-LEAK (C-013)
        ⚠ không có timeout → treo vô hạn → FAIL-UNHANDLED-EXTERNAL
```

Mọi kết quả của kiểu này gắn `static-trace` và `fidelity: guessed`.

## 9. Vệ sinh mock

- **Giữ mock mỏng**: chỉ thay phía ngoài; không viết lại logic của app trong mock.
- **Bám thực tế**: dựng hình dạng phản hồi từ mẫu đã ghi lại hoặc từ tài liệu/type của nhà cung cấp; nếu phải đoán thì gắn `guessed`.
- **Mỗi nhánh có kết quả mong đợi riêng** lấy từ criteria, không từ cách code đang xử lý. Nhánh fail mà criteria im lặng thì verdict là `GAP`, không phải `PASS`.
- **Ghi lại chiều đi ra** của mọi mock để kiểm payload, số lần gọi, retry.
- **Không có cuộc gọi thật lọt ra ngoài**: bật chế độ chặn mọi request không khớp mock (allowlist) và coi request lạ là vi phạm INV7.
- **Không dùng khoá/tài khoản thật** trong kịch bản phá.
- **Một nguồn sự thật cho profile**: định nghĩa profile ở `boundaries.md` và `harness/boundary.ts`, để các scenario tái dùng thay vì mỗi scenario tự chế lỗi riêng.
