CP07.1 RESULT
Status: PASS — checkpoint hardening hoàn tất. CP08 chưa sẵn sàng để chạy diễn giải workflow thật vì ngữ nghĩa vẫn cần con người xác nhận.
Confirmed issues:
- Workflow engine chỉ hỗ trợ valid_paths, chưa biểu diễn prerequisite/partial order.
- Skip logic dùng vị trí của candidate đầu tiên thay vì route được chọn; regression test hai route ở vị trí khác nhau xác nhận lỗi.
- Metric âm thầm cắt chuỗi GT/prediction về cùng độ dài nhỏ hơn.
- Background class bị ngầm gắn với ID 0.
- Event không đủ bằng chứng chưa được giữ trong lịch sử quan sát.
- Framewise và MS-TCN dùng objective huấn luyện khác nhau; kết quả lịch sử không phải so sánh thuần kiến trúc.
Implemented:
- Mở rộng WorkflowEngine hiện có để hỗ trợ cấu hình prerequisite DAG cùng với route mode; validator kiểm tra tham chiếu, required actions và chu trình.
- Sửa skip handling: báo đúng bước bị bỏ qua theo route được chọn và tiếp tục sau action quan sát được.
- Lưu mọi ActionEvent nhận vào observations; chỉ event hợp lệ, đủ bằng chứng mới có thể làm state tiến triển. Confidence, evidence status và workflow acceptance vẫn tách biệt.
- Metric từ chối đầu vào lệch độ dài, không phải chuỗi 1D hoặc có class ID ngoài vocabulary; caller phải chỉ rõ background bằng label hoặc ID.
- Thêm .idea/ vào ignore và sửa một số help text/package/workflow docs cũ.
- Không chỉnh temporal decoder: audit không tìm thấy lỗi cụ thể đủ bằng chứng để thay đổi.
Workflow architecture: Một engine, hai schema đầu vào loại trừ lẫn nhau: route hoặc required_actions + prerequisites. DAG cho phép nhiều thứ tự hợp lệ mà không cần liệt kê từng route. Không tạo prerequisite, route hay quy tắc nào cho Disassembly_A.
Human-dependent: Chủ dự án vẫn cần hoàn thiện worksheet và cung cấp Research Workflow Specification đã xác nhận. Không có factory SOP; process compliance và anomaly metrics vẫn NOT EVALUATED.
Tests:
- Full suite: 63 passed
  .venv-cp05\Scripts\python.exe -m unittest discover -s tests -v
- compileall -q src tools tests: pass.
- Validator trên draft: exit 1 như dự kiến vì workflow chưa được duyệt và thiếu quyết định ngữ nghĩa.
- Không có disassembly_A.yaml executable. Worksheet vẫn nguyên trạng.
Frozen artifacts preserved: Không ghi vào experiments/CP05/, experiments/CP06/ hoặc models/; không retrain, regenerate metrics, đổi test split hay thay checkpoint. HEAD ghi nhận: 2a89bc9355b2f8a8453e831ba6b1a7e1fb0fdedc.
Files changed: src/human_action/workflow.py, src/human_action/metrics.py, src/human_action/pipeline.py, src/human_action/__init__.py, tools/train_baseline.py, tools/analyze_cp06.py, tools/validate_workflow.py, tests/test_cp07_contract_and_aggregation.py, configs/workflows/README.md, .gitignore, CHECKSHEET.md, ROADMAP.md.
Files added:
- [CP07.1 context and audit](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP07.1/CP07.1_context_and_audit.md)
- [CP07.1 workflow design](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP07.1/CP07.1_workflow_design.md)
- [CP07.1 system hardening report](C:/Users/Admin/PycharmProjects/HumanActionRecognition/experiments/CP07.1/CP07.1_system_hardening.md)
Potential regressions: action_metrics giờ yêu cầu caller truyền rõ background label hoặc ID; các caller trong repository đã được cập nhật và kiểm thử. Route skip hiện tiến state qua action bị quan sát, thay vì dừng trước action đó.
CP08 readiness: NOT READY for real Disassembly_A process traces. Phần hạ tầng kỹ thuật đã được mở đường; semantic gate vẫn do con người sở hữu.