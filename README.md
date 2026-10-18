# Bootstrap — Codex-ready project harness template

**Mục tiêu:** tiết kiệm tối đa quota khi thiết lập dự án. Copy bộ `project-template/` vào root dự án và **dùng nguyên phần lớn nội dung có sẵn**. Mặc định phục vụ **Codex**; chuyển sang Claude Code, Copilot, Cline… chỉ cần sửa lớp cấu hình/tích hợp theo README và kiểm thử lại.

## Trạng thái thực tế

- **READY:** root `AGENTS.md`, role contract `.agents/roles/*`, generic `.agents/skills/*/SKILL.md`, cách làm Discovery/Delivery, biểu mẫu review/evidence và hướng dẫn triage. Không phải viết lại cho mỗi dự án.
- **CONFIGURE:** `docs/CRITERIA.md` (lý thuyết duy nhất, Planner cùng user hoàn thiện), `PROJECT_PROFILE.md`, thông tin sản phẩm, model, API/dialect, lệnh build/test thực tế.
- **IMPLEMENT / VERIFY:** script hooks, loop orchestrator, gates, real approval ledger, snapshot, generated trace và bảo vệ quyền phải được triển khai/test trong môi trường Codex thật. Contract viết sẵn không tự thành mã thực thi.

Codex có hỗ trợ AGENTS.md và repo-local skill SKILL.md; cấu hình dự án `.codex/config.toml` được đọc ở trusted project. Khả năng kích hoạt **named subagent** và lifecycle hook tùy phiên bản: không khẳng định role Markdown hay contract harness tự chạy. Tham chiếu: [Codex configuration](https://developers.openai.com/codex/config-basic), [Agent skills](https://developers.openai.com/api/docs/guides/tools-skills), [Codex usage](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan).

## Cây mẫu cài vào dự án

```
project-template/
  AGENTS.md                  # Codex default workflow dùng ngay
  README.md                  # phần product phải điền
  CODEX_READY.md             # cách dùng/port
  SETUP.md
  TASKS.md                   # Planner cập nhật theo goal
  docs/CRITERIA.md           # single source of product theory
  docs/PROJECT_PROFILE.md
  docs/MILESTONES.md
  .codex/config.toml         # Codex project config bảo thủ
  .agents/roles/             # generic Planner/Reviewer/CR/Coder/Tester
  .agents/skills/            # generic skill đầy đủ
  .agents/config/            # tùy chọn model, skill/knowledge
  harness/specs/             # implementation contracts
  lessons/
```

## Thực hiện

1. Khảo sát dự án. Với dự án chưa có lý thuyết, không dừng: Planner brainstorm/research cùng user và ghi OPEN trong CRITERIA; chưa tự chốt sản phẩm.
2. Chọn tier Lite/Standard/Full phù hợp; kiểm tra runtime Codex đang dùng. Đọc kỹ [SETUP](project-template/SETUP.md) và [Codex README](project-template/.codex/README.md).
3. Trình diff/bảng tùy chỉnh các file thực sự cần sửa, quyền/model/approval để user duyệt. Không viết lại generic workflows chỉ vì bootstrap.
4. Copy template; điền đúng các thông tin không thể biết trước. Giữ generic skills/roles.
5. Phần cơ chế tự động chưa hiện thực: dùng các contract trong `harness/specs/` để viết script/hook đúng runtime, hoặc đánh dấu chưa triển khai.
6. Chạy kiểm tra chức năng và ca vi phạm/hợp lệ trên bản sao. Không có bằng chứng thì UNVERIFIED; không giả mạo approval.
7. Báo cáo ngắn: đã sẵn sàng gì, đã cấu hình gì, đã kiểm thử gì, phần nào còn NOT_CONFIGURED.

## Chuyển sang nền tảng khác

**Giữ** CRITERIA, task/goals, role logic, SKILL.md và các contract. **Thay/kiểm tra** agent discovery, skill path, runtime config, model availability, lifecycle hooks, permissions/approvals, shell scripts và test harness theo tài liệu chính thức của nền tảng đích. Không sao chép cấu hình Codex rồi khẳng định chạy được trên Claude Code/Copilot/Cline.

Xem [harness-bootstrap-prompt-v9.md](harness-bootstrap-prompt-v9.md) cho lý thuyết đầy đủ và [harness/specs/TESTS.md](project-template/harness/specs/TESTS.md) cho selftest.

**Bất biến:** CRITERIA là nguồn sự thật duy nhất; không tự quyết định thay user; không push/động tác phá hủy khi chưa được phép; không nhận nhầm prompt thành guard được cưỡng chế.
