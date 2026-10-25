# Mẫu harness để chạy thật và ghi trace

Đây là **mẫu khởi đầu**, chưa được kiểm chạy trên app cụ thể nào. Khi dùng, chạy thử một scenario T0 trước để chắc harness bắt đúng sự kiện, rồi mới mở rộng. Điều chỉnh theo stack của app.

## Mục lục
1. Chọn công cụ
2. Trace recorder (Playwright)
3. Helper `step()` ghi diff state
4. Ví dụ một scenario T4 và một scenario T5
5. Chèn instrumentation tạm cho handler
6. Xuất trace thành bảng

---

Harness chạy **sau khi scenario đã đóng băng** (vai Tracer). Hành động của user trong test dùng thứ người dùng nhìn thấy (vai trò và nhãn trên màn hình như `getByRole('button', { name: /gửi/i })`), không dùng selector hay tên nội bộ lấy từ code; URL của ngoại vi lấy từ quan sát lúc chạy thử (HAR). Các giá trị `/api/chat`, `localhost:5173` trong ví dụ chỉ minh hoạ.

Ngoại vi (API, AI, storage, quyền thiết bị) được mock bằng profile pass/fail theo `external-mocks.md`; harness dưới đây chỉ lo phần trace và invariant.

## 1. Chọn công cụ

| Cần kiểm | Công cụ | Ghi chú |
|---|---|---|
| Hành trình thật trên trình duyệt, mạng, storage, iframe | Playwright | Mặc định cho web |
| Logic UI nhanh, không cần trình duyệt thật | Vitest/Jest + Testing Library + `userEvent` | Không có mạng/iframe thật; mock fetch |
| CLI / MCP / script | `subprocess` hoặc client MCP trong test | Ghi stdin/stdout/exit code, file thay đổi |
| Không chạy được | Static-trace | Gắn nhãn `static-trace` |

Khởi tạo Playwright nếu chưa có (cần mạng npm):

```bash
npm i -D @playwright/test && npx playwright install chromium
```

Nếu sandbox không tải được trình duyệt, chuyển sang Vitest + jsdom hoặc static-trace và nói rõ.

## 2. Trace recorder (Playwright)

`simulate/harness/trace.ts`

```ts
import type { Page } from '@playwright/test';

export type TraceEvent = {
  t: number;                 // ms kể từ lúc bắt đầu
  kind: 'step' | 'console' | 'pageerror' | 'request' | 'response' | 'dialog';
  data: Record<string, unknown>;
};

export type Snapshot = {
  local: Record<string, string>;
  session: Record<string, string>;
  url: string;
};

export async function snapshot(page: Page): Promise<Snapshot> {
  return page.evaluate(() => ({
    local: Object.fromEntries(Object.entries(localStorage)),
    session: Object.fromEntries(Object.entries(sessionStorage)),
    url: location.href,
  }));
}

export function diffStorage(a: Snapshot, b: Snapshot) {
  const out: string[] = [];
  for (const area of ['local', 'session'] as const) {
    const keys = new Set([...Object.keys(a[area]), ...Object.keys(b[area])]);
    for (const k of keys) {
      if (a[area][k] !== b[area][k]) {
        out.push(`${area}.${k}: ${trunc(a[area][k])} → ${trunc(b[area][k])}`);
      }
    }
  }
  if (a.url !== b.url) out.push(`url: ${a.url} → ${b.url}`);
  return out;
}

const trunc = (v: unknown, n = 80) =>
  v === undefined ? '∅' : String(v).length > n ? String(v).slice(0, n) + '…' : String(v);

export function attachTrace(page: Page) {
  const events: TraceEvent[] = [];
  const t0 = Date.now();
  const push = (kind: TraceEvent['kind'], data: Record<string, unknown>) =>
    events.push({ t: Date.now() - t0, kind, data });

  page.on('console', (m) => push('console', { type: m.type(), text: m.text() }));
  page.on('pageerror', (e) => push('pageerror', { message: e.message, stack: e.stack }));
  page.on('request', (r) => push('request', { method: r.method(), url: r.url() }));
  page.on('response', (r) => push('response', { status: r.status(), url: r.url() }));
  page.on('dialog', async (d) => {
    push('dialog', { type: d.type(), message: d.message() });
    await d.dismiss();
  });

  return { events, mark: (label: string) => push('step', { label }) };
}
```

## 3. Helper `step()` ghi diff state và kiểm invariant

`simulate/harness/step.ts`

```ts
import type { Page } from '@playwright/test';
import { attachTrace, snapshot, diffStorage, type TraceEvent } from './trace';

export type StepRecord = {
  label: string;
  storageDiff: string[];
  events: TraceEvent[];
  invariantViolations: string[];
};

export async function makeSimulator(page: Page, opts: { allowedHosts?: string[] } = {}) {
  // Canary: nếu nội dung user chạy được script, giá trị này tăng.
  await page.addInitScript(() => { (window as any).__pwned = 0; });

  const trace = attachTrace(page);
  const records: StepRecord[] = [];

  async function step(label: string, action: () => Promise<void>): Promise<StepRecord> {
    const before = await snapshot(page);
    const from = trace.events.length;
    trace.mark(label);

    let thrown: string | undefined;
    try { await action(); } catch (e) { thrown = String(e); }

    await page.waitForTimeout(200); // cho handler bất đồng bộ kịp chạy
    const after = await snapshot(page);
    const events = trace.events.slice(from);

    const violations: string[] = [];
    if (thrown) violations.push(`action ném lỗi (selector/timeout?): ${thrown}`);
    if (events.some((e) => e.kind === 'pageerror')) violations.push('INV1: pageerror');
    if ((await page.evaluate(() => (window as any).__pwned)) !== 0) violations.push('INV6: canary XSS đã chạy');
    if (opts.allowedHosts) {
      for (const e of events) {
        if (e.kind !== 'request') continue;
        const host = new URL(String(e.data.url)).host;
        if (!opts.allowedHosts.includes(host)) violations.push(`INV7: request ngoài danh sách: ${host}`);
      }
    }
    // INV2/3/4/5/8 phụ thuộc app: thêm kiểm tra riêng (schema storage, UI kẹt, thông báo lỗi...).

    const rec = { label, storageDiff: diffStorage(before, after), events, invariantViolations: violations };
    records.push(rec);
    return rec;
  }

  return { step, records, trace };
}
```

## 4. Ví dụ scenario

`simulate/scenarios/T4-007.spec.ts` (double submit khi request đầu chưa xong)

```ts
import { test, expect } from '@playwright/test';
import { makeSimulator } from '../harness/step';
import { writeFileSync } from 'node:fs';

test('T4-007 double submit khi mạng chậm', async ({ page }) => {
  const sim = await makeSimulator(page, { allowedHosts: ['localhost:5173'] });

  // Làm chậm API chat 3s để tạo cửa sổ double-submit.
  await page.route('**/api/chat', async (route) => {
    await new Promise((r) => setTimeout(r, 3000));
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ reply: 'ok' }) });
  });

  await page.goto('http://localhost:5173/');

  await sim.step('gõ "xin chào"', async () => {
    await page.getByRole('textbox').fill('xin chào');
  });

  const first = await sim.step('bấm Gửi lần 1', async () => {
    await page.getByRole('button', { name: /gửi/i }).click();
  });

  const second = await sim.step('bấm Gửi lần 2 khi request 1 chưa xong', async () => {
    await page.getByRole('button', { name: /gửi/i }).click({ force: true });
  });

  // Mong đợi theo criteria AC-014: chỉ 1 request, hội thoại +1 tin
  const chatRequests = sim.trace.events.filter(
    (e) => e.kind === 'request' && String(e.data.url).includes('/api/chat'),
  );
  expect(chatRequests.length, 'FAIL-BEHAVIOR nếu > 1: gửi trùng').toBe(1);
  expect(first.invariantViolations).toEqual([]);
  expect(second.invariantViolations).toEqual([]);

  writeFileSync('simulate/out/T4-007.trace.json', JSON.stringify(sim.records, null, 2));
});
```

`T5` canary XSS qua ô nhập tên (mẫu rút gọn):

```ts
test('T5-002 canary XSS ở tên hiển thị lại', async ({ page }) => {
  const sim = await makeSimulator(page);
  await page.goto('http://localhost:5173/');
  const payload = '<img src=x onerror="window.__pwned=1">';

  const rec = await sim.step('nhập tên chứa canary và lưu', async () => {
    await page.getByLabel(/tên/i).fill(payload);
    await page.getByRole('button', { name: /lưu/i }).click();
  });

  // Hợp lệ: bị chặn (PASS-BLOCKED) hoặc được hiển thị dạng text. Không hợp lệ: canary chạy.
  expect(rec.invariantViolations.filter((v) => v.startsWith('INV6'))).toEqual([]);
});
```

Lưu ý `force: true` bỏ qua kiểm tra "nút đang disabled" của Playwright: nó mô phỏng người dùng bấm cực nhanh hoặc gỡ `disabled` bằng devtools, tức là kiểm xem guard nằm ở handler hay chỉ ở thuộc tính HTML. Muốn mô phỏng người dùng bình thường thì bỏ `force`.

## 5. Chèn instrumentation tạm cho handler (chế độ B)

Khi cần thấy handler/guard nào chạy mà không có sẵn log:

1. Tạo nhánh tạm: `git switch -c simulate/instrument`.
2. Thêm vào đầu mỗi handler và tại mỗi guard một dòng, ví dụ:
   ```ts
   (window as any).__trace?.push({ fn: 'onSend', guard: 'isSending', blocked: isSending });
   ```
3. Trong harness, khởi tạo `window.__trace = []` bằng `addInitScript`, đọc lại sau mỗi `step` bằng `page.evaluate(() => (window as any).__trace.splice(0))`.
4. Xong thì **revert hoàn toàn** (`git switch -` rồi xoá nhánh). Báo cáo ghi chế độ `instrumented`.

Với Chromium có thể dùng thêm `page.coverage.startJSCoverage()` / `stopJSCoverage()` để xem hàm nào đã chạy trong một step; với bản build đã minify thì khó đọc, nên dùng dev server có sourcemap.

## 6. Xuất trace thành bảng

Từ `records` của mỗi scenario, sinh bảng Markdown cho `report.md`:

| # | Hành động | Handler (từ `__trace`) | Guard | Storage diff | Request | Lỗi/invariant | Verdict |
|---|---|---|---|---|---|---|---|

- `Handler` và `Guard` do Tracer quan sát khi chạy (instrumentation), hoặc ghi từ việc lần theo code ở chế độ static-trace. Chúng là kết quả, không phải thứ dùng để thiết kế scenario.
- `Request` lấy từ events kind `request`/`response` trong khoảng của step.
- `Verdict` do bạn phán theo Phase 5, so với criteria (không so với hành vi hiện tại của code), không phải do test pass/fail máy móc: test chỉ xanh khi assertion khớp, còn FAIL-LEAK hay GAP cần đọc trace để thấy.
