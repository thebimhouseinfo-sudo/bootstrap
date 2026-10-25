# Ví dụ đầy đủ: add-in / công cụ cho AutoCAD

Minh hoạ cách mô phỏng một app nằm trong hoặc điều khiển phần mềm chủ. Khi lệnh đã gửi vào CAD thì nó nằm ngoài app: ta thay CAD bằng **host giả**, cho host trả thành công hoặc fail ở nhiều pha (load, chạy lệnh, xác nhận), rồi **mô phỏng tiếp** hành vi của app và của user sau kết quả đó.

Lưu ý về nguồn: tên lệnh, thao tác và kết quả mong đợi của add-in lấy từ **hướng dẫn sử dụng, criteria và quan sát khi chạy** (ví dụ xem danh sách lệnh trên dòng lệnh CAD), không từ việc đọc mã add-in. Phần "Trace có nhánh" ở mục 5 là sản phẩm của vai Tracer sau khi đóng băng.

Mã trong file là mẫu khởi đầu, chưa kiểm chạy với AutoCAD thật. Tên biến hệ thống và cơ chế nạp nêu dưới đây là loại thường gặp; đối chiếu tài liệu của đúng phiên bản AutoCAD đang dùng trước khi dựa vào chi tiết.

## Mục lục
1. Xác định loại app và ranh giới
2. Boundary cards cho add-in CAD
3. Danh mục outcome: pha load, pha lệnh, sự kiện host chủ động
4. Host giả có trạng thái (mẫu Python)
5. Scenario mẫu và trace có nhánh
6. Bộ kiểm riêng cho công cụ CAD

---

## 1. Xác định loại app và ranh giới

| Loại | Cách tới CAD | Ranh giới chính |
|---|---|---|
| Add-in .NET (DLL nạp vào CAD) | CAD gọi vào command của add-in; add-in gọi API của CAD | Hai chiều: nạp add-in, lệnh được gọi, API đọc/ghi bản vẽ, sự kiện của CAD |
| AutoLISP (`.lsp`/`.fas`) | CAD nạp file, lệnh `c:XXX` chạy trong CAD | Nạp file (có thể nạp dở), lệnh, `*error*`, biến hệ thống |
| Điều khiển từ ngoài (COM, MCP server, script) | Tiến trình ngoài gửi lệnh/gọi API qua COM | Kết nối COM, gửi lệnh, đọc kết quả, CAD bận hoặc bị đóng |

Với add-in chạy **bên trong** CAD, CAD vừa là nơi app gọi vào, vừa là bên gọi ngược vào app. Mock cần điều khiển cả hai chiều: kết quả trả lời lẫn các sự kiện CAD chủ động bắn (lệnh bị huỷ, tài liệu đóng, CAD tắt).

## 2. Boundary cards cho add-in CAD

```yaml
- boundary: cad_load
  kind: host-load
  sends: "nạp add-in/LISP vào phiên CAD"          # theo hướng dẫn cài đặt
  expects: "các lệnh trong hướng dẫn dùng được"
  criteria: [AC-001]

- boundary: cad_command
  kind: host-command
  sends: "tên lệnh + tham số (vd. SETLAYER_BULK, layer đích, bộ chọn)"   # tên lệnh theo tài liệu
  expects: "kết quả hoàn tất + số đối tượng đã đổi"
  criteria: [AC-031, AC-032]

- boundary: cad_drawing_state
  kind: host-api
  sends: "đọc/ghi đối tượng, layer, biến hệ thống"
  expects: "dữ liệu bản vẽ hợp lệ"

- boundary: cad_user_prompt
  kind: host-ui
  sends: "yêu cầu người dùng chọn đối tượng/điểm"
  expects: "lựa chọn, hoặc ESC (huỷ)"
```

## 3. Danh mục outcome

### Pha load (nạp add-in)
| Profile | Nhánh | Kiểm điều gì |
|---|---|---|
| `ok-load` | pass | Lệnh đăng ký đủ, app biết đã sẵn sàng |
| `ok-already-loaded` | pass | Nạp lần hai không nhân đôi lệnh/sự kiện |
| `fail-file-not-found` | fail | Đường dẫn sai, tên có dấu/khoảng trắng |
| `fail-wrong-host-version` | fail | Add-in build cho phiên bản/kiến trúc CAD khác |
| `fail-missing-dependency` | fail | Thiếu thư viện đi kèm |
| `fail-blocked-untrusted` | fail | CAD chặn nạp từ thư mục không tin cậy (cơ chế bảo mật nạp mã của CAD) |
| `fail-exception-in-init` | fail | Lỗi khi khởi tạo: add-in nạp một nửa, một số lệnh có, một số không |
| `fail-partial-lisp-load` | fail | File LISP lỗi cú pháp giữa chừng: hàm phía trước đã định nghĩa, phía sau thì không |

### Pha lệnh
| Profile | Nhánh | Kiểm điều gì |
|---|---|---|
| `ok-typical` | pass | Luồng chính, số đối tượng đổi đúng |
| `ok-no-change` | pass | Không có đối tượng nào khớp: app có báo rõ, không báo "thành công" mơ hồ |
| `ok-with-skips` | pass | Một số đối tượng bị bỏ qua im lặng (layer khoá, readonly): app có cho user biết |
| `fail-busy` | fail | CAD đang trong lệnh khác hoặc có hộp thoại: lệnh bị từ chối |
| `fail-cancelled` | fail | Người dùng ESC giữa lệnh |
| `fail-no-active-document` | fail | Không có bản vẽ nào đang mở |
| `fail-readonly-or-locked` | fail | Bản vẽ chỉ đọc hoặc đối tượng bị khoá |
| `fail-partial-then-exception` | fail | Xử lý được một phần rồi lỗi; biến hệ thống đã đổi mà chưa khôi phục |
| `fail-timeout-no-ack` | fail | Không có phản hồi: treo hay lệnh vẫn chạy? |
| `fail-late-ack` | fail | Ack của lệnh 1 đến sau khi lệnh 2 đã gửi |
| `fail-duplicate-ack` | fail | Ack giao hai lần |
| `fail-host-crash` | fail | Mất kết nối giữa chừng; CAD đóng |

### Sự kiện host chủ động (host gọi ngược vào app)
`doc-closed-during-command`, `doc-switched-during-command`, `command-will-cancel`, `host-shutting-down`, `sysvar-changed-by-other`.

## 4. Host giả có trạng thái (mẫu Python)

Host giả giữ một mô hình nhỏ của CAD để trạng thái **sống sót qua lỗi**: lệnh fail một nửa vẫn để lại đối tượng đã đổi và biến hệ thống đã đổi, đúng như ngoài đời.

```python
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Entity:
    id: int
    layer: str
    kind: str = "LINE"

@dataclass
class HostState:
    entities: list[Entity]
    locked_layers: set[str] = field(default_factory=set)
    current_layer: str = "0"
    sysvars: dict = field(default_factory=lambda: {"OSMODE": 4133, "CMDECHO": 1})
    command_active: bool = False
    doc_open: bool = True
    undo_marks: list[str] = field(default_factory=list)

class HostError(Exception): ...
class HostBusy(HostError): ...
class HostGone(HostError): ...

# Profile = hàm quyết định host làm gì với lệnh, và CÓ THỂ đổi HostState trước khi lỗi.
Profile = Callable[["FakeCadHost", str, dict], dict]

def ok_typical(host, cmd, args):
    changed = 0
    for e in host.state.entities:
        if e.layer not in host.state.locked_layers:
            e.layer = args["target_layer"]; changed += 1
    return {"ok": True, "changed": changed, "skipped": len(host.state.entities) - changed}

def fail_busy(host, cmd, args):
    raise HostBusy("host đang trong lệnh khác")            # state không đổi

def fail_partial_then_exception(after=3):
    def _p(host, cmd, args):
        host.state.sysvars["OSMODE"] = 0                    # app đã tắt snap, CHƯA khôi phục
        host.state.undo_marks.append("begin")               # đã mở nhóm undo, CHƯA đóng
        for e in host.state.entities[:after]:
            e.layer = args["target_layer"]
        raise HostError("lỗi giữa chừng")                   # state dở dang được giữ lại
    return _p

def fail_timeout_no_ack(host, cmd, args):
    host.state.command_active = True                        # lệnh vẫn chạy trong host
    raise TimeoutError("không có ack")

def fail_host_crash(host, cmd, args):
    host.state.doc_open = False
    raise HostGone("mất kết nối")

class FakeCadHost:
    def __init__(self, state: HostState, profile: Profile):
        self.state, self.profile = state, profile
        self.received: list[tuple[str, dict]] = []          # chiều đi ra: app gửi gì
    def send_command(self, cmd: str, args: dict) -> dict:
        self.received.append((cmd, args))
        return self.profile(self, cmd, args)
```

Driver chạy một scenario với mọi profile, kèm lượt follow-up và kiểm desync (giả sử `MyApp` nhận host qua dependency injection):

```python
import copy, pytest

def fresh_state():
    return HostState(entities=[Entity(i, "A") for i in range(10)], locked_layers={"LOCKED"})

PROFILES = {
    "ok-typical": ok_typical,
    "fail-busy": fail_busy,
    "fail-partial-then-exception": fail_partial_then_exception(3),
    "fail-timeout-no-ack": fail_timeout_no_ack,
    "fail-host-crash": fail_host_crash,
}

@pytest.mark.parametrize("name", PROFILES)
def test_T4_020_bulk_layer(name):
    host = FakeCadHost(fresh_state(), PROFILES[name])
    app = MyApp(host)
    before = copy.deepcopy(host.state)

    result = app.run_bulk_layer("B")            # lượt 1: user bấm chạy
    follow = app.run_bulk_layer("B")            # follow-up: user bấm thử lại ngay

    # Chiều đi ra: app gửi đúng tham số, và số lần gọi hợp lý (không retry dồn dập)
    assert all(args.get("target_layer") == "B" for _, args in host.received)

    # Không desync: UI app khớp với host
    assert_no_desync(app, host)

    # Host được trả về trạng thái nền sau lỗi (biến hệ thống, nhóm undo)
    if name.startswith("fail"):
        assert host.state.sysvars == before.sysvars, "FAIL-LEAK: biến hệ thống chưa khôi phục"
        assert host.state.undo_marks.count("begin") == host.state.undo_marks.count("end"), \
            "FAIL-LEAK: nhóm undo mở mà không đóng"
```

`assert_no_desync` là phần riêng của app: so cái UI/state của app đang nói (đã xong, đang chạy, lỗi) với `host.state` (đối tượng thực sự đã đổi, `command_active`, `doc_open`). Verdict cuối vẫn do bạn phán theo hợp đồng thiết kế; test xanh chưa chắc là PASS, test đỏ chưa chắc là FAIL nếu hợp đồng cho phép hành vi đó.

Nếu app là add-in .NET chạy trong CAD thật, không stub được host trong tiến trình. Hai hướng: (a) bọc API CAD sau một interface mỏng và viết host giả cho interface đó để test logic; (b) chạy trên CAD thật với bản vẽ test, chụp biến hệ thống/đối tượng trước và sau mỗi lệnh, và ghi chế độ `executed` kèm cảnh báo rằng không ép được các lỗi hiếm của host.

## 5. Scenario mẫu và trace có nhánh

```yaml
id: T4-020
tier: T4
design:                                  # đóng băng, viết từ criteria và hướng dẫn dùng
  title: Chạy lệnh đổi layer hàng loạt, CAD trả các kết quả khác nhau, rồi user bấm lại
  persona: Kỹ sư vội, bản vẽ lớn, vừa mở file
  why_a_user_does_this: "Cuối ngày cần chỉnh layer cho cả bản vẽ; thấy lệnh chạy lâu nên bấm lại hoặc nhấn ESC."
  journey: "Hành trình A: chỉnh layer cuối ngày (brief §2)"
  criteria: [AC-031, AC-032]
  oracle_source: owner-stated
  evidence: assumed
  origin: design
  boundary_mocks:
    cad_command:
      fidelity: guessed
      profiles: [ok-typical, ok-with-skips, fail-busy, fail-partial-then-exception, fail-timeout-no-ack, fail-host-crash]
  steps:
    - do: "Chọn đối tượng, chạy lệnh đổi layer sang 'B'"
      expect: "Lệnh chạy; người dùng thấy lệnh đang được xử lý"
  after_boundary:
    ok-typical:
      expect: "Báo xong N đối tượng; số liệu khớp bản vẽ"
    ok-with-skips:
      expect: "Báo xong N và nói rõ M đối tượng bị bỏ qua (layer khoá), không báo 'xong tất cả'"
    fail-busy:
      expect: "Báo CAD đang bận; không có đối tượng nào đổi; dùng lại được"
      follow_ups:
        - { do: "Bấm chạy lại ngay", expect: "Không chạy chồng lên lệnh đang dang dở; hoặc xếp hàng đợi đúng cam kết" }
    fail-partial-then-exception:
      expect: "Báo lỗi; cho user biết bản vẽ đã đổi một phần; các thiết lập CAD của user (chế độ bắt điểm...) về như trước khi chạy"
      follow_ups:
        - { do: "Bấm Undo của CAD", expect: "Một lần Undo đưa bản vẽ về đúng trước lệnh" }
        - { do: "Chạy lại lệnh", expect: "Chạy bình thường, kết quả không cộng dồn từ lần lỗi" }
    fail-timeout-no-ack:
      expect: "Không báo thành công; nói thật là chưa rõ kết quả; không cho chạy chồng lệnh thứ hai"
    fail-host-crash:
      expect: "Báo mất kết nối; giao diện không treo; có đường quay lại"
# observed: do Tracer điền sau khi chạy (triggers, guards, state_diff, boundary_sent, verdict)
```

Trace có nhánh do Tracer ghi **sau khi chạy** (mô tả; ghi đủ file:dòng khi thực hiện). Handler, guard và dòng code ở đây là kết quả quan sát/chẩn đoán, chưa từng là đầu vào của việc thiết kế scenario:

```
T4-020 bước 1  [user] chọn 10 đối tượng, bấm Chạy
  → onRun (src/run.ts:21) → validateSelection (:25) guard: selection != empty → pass
  → app: setStatus('running') (:30)               ← ghi state TRƯỚC khi host xác nhận
  → [→ gửi] cad_command SETLAYER_BULK {target_layer:"B", ids:[...10]}
  ┌ ok-typical       [← 10 đổi]  → :44 setStatus('done', 10)                      PASS
  ├ ok-with-skips    [← 7 đổi, 3 bỏ qua] → :44 setStatus('done', 10)
  │                     ⚠ hiển thị 10 trong khi host chỉ đổi 7                    FAIL-DESYNC
  ├ fail-busy        [← HostBusy] → catch (:52) setStatus('error')
  │     follow-up: bấm lại ngay → onRun gửi lệnh thứ hai khi host còn bận         FAIL-BEHAVIOR (AC-031)
  ├ fail-partial     [← 3 đổi, OSMODE=0, nhóm undo mở, rồi HostError]
  │                  → catch (:52) setStatus('error')
  │                     ⚠ không có finally: OSMODE vẫn 0, nhóm undo không đóng     FAIL-LEAK
  ├ fail-timeout     [← không ack] → không timeout trong code, status mãi 'running'
  │                     ⚠ UI kẹt, nút bị khoá                                      FAIL-UNHANDLED-EXTERNAL / INV4
  └ fail-host-crash  [← HostGone] → catch (:52) 'error' nhưng không đặt lại kết nối
                        follow-up: bấm lại → ném lỗi chưa bắt                       FAIL-INVARIANT (INV1)
```

Mỗi dòng nhánh cho thấy chính xác tầng đầu tiên chệch khỏi criteria (ví dụ ghi `running` trước khi xác nhận, thiếu `finally`, thiếu timeout), điều mà chỉ test happy path không thấy.

## 6. Bộ kiểm riêng cho công cụ CAD

Dùng để sinh thêm scenario theo mỗi lệnh của công cụ:

- **ESC giữa lệnh** ở từng điểm có thể dừng (chọn đối tượng, nhập điểm, trong lúc vòng lặp chạy): biến hệ thống và layer hiện hành có được khôi phục không?
- **Undo**: một lần Undo có hoàn tác cả lệnh không (nhóm undo mở/đóng đúng, kể cả khi lỗi giữa chừng)?
- **Chạy hai lần liên tiếp**: kết quả giống một lần (idempotent) hay cộng dồn/trùng?
- **Nhiều bản vẽ**: chuyển tài liệu giữa lệnh; lệnh chạy trên bản vẽ nào?
- **Dữ liệu bản vẽ khó**: rỗng, chọn quá nhiều đối tượng, layer khoá/đóng băng/tắt, Xref bị thiếu hoặc unload, tên layer có dấu hoặc ký tự đặc biệt, đơn vị khác, UCS khác WCS.
- **Vòng đời add-in**: nạp lại khi đã nạp, gỡ nạp rồi gọi lệnh, sự kiện bị đăng ký trùng sau khi nạp lại.
- **Khôi phục sau lỗi**: sau mọi nhánh fail, một lệnh bình thường tiếp theo có chạy đúng không (host không bị bỏ lại ở trạng thái hỏng do app).
- **Thông báo cho người dùng**: lỗi từ CAD có được dịch ra câu hiểu được, không lộ stack hay đường dẫn nội bộ.
- **Công cụ điều khiển từ ngoài (MCP/COM)**: kết nối lại sau khi CAD khởi động lại; hai client gọi cùng lúc; kết quả trả về cho agent có cấu trúc lỗi rõ ràng để agent quyết định thử lại hay dừng.
