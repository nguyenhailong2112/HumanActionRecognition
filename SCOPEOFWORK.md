# SCOPE OF WORK (SOW)

## HUMAN ACTION & PROCEDURE UNDERSTANDING FOR INDUSTRIAL VISION

**Tên dự án:** HumanActionRecognition - Human Action Recognition System
**Mục đích:** Nghiên cứu và xây dựng nền tảng Vision AI có khả năng quan sát, nhận biết, theo dõi và hiểu các thao tác của con người trong môi trường công nghiệp; từ đó đánh giá việc thực hiện công việc theo quy trình và phát hiện các sai lệch về hành động, trình tự, thời gian và trạng thái thực hiện.

---

# 1. PROJECT OBJECTIVE

Dự án nhằm nghiên cứu và xây dựng một giải pháp Vision AI có khả năng chuyển dữ liệu video/CCTV thành thông tin có cấu trúc về:

* Con người đang thực hiện hành động gì.
* Hành động diễn ra khi nào và trong bao lâu.
* Người nào đang thực hiện hành động.
* Người đang tương tác với vật thể, dụng cụ hoặc thiết bị nào.
* Hành động đang diễn ra ở khu vực nào.
* Hành động đó thuộc bước nào của một quy trình.
* Chuỗi thực tế có tuân thủ quy trình mong muốn hay không.
* Có xảy ra sai trình tự, bỏ bước, lặp bước, thao tác bất thường, quá lâu, quá nhanh, timeout hoặc không hoàn thành hay không.
* Cung cấp bằng chứng hình ảnh/video để kiểm tra lại kết quả AI.

Mục tiêu cuối cùng không phải chỉ xây dựng một mô hình **Human Action Recognition**, mà là xây dựng một pipeline:

**Video → Perception → Action → Temporal Event → Process State → Workflow → Compliance/Anomaly → Evidence**

---

# 2. SYSTEM SCOPE

Phạm vi nghiên cứu gồm hai miền quan sát chính.

## 2.1. Profile A — Fine-Grained / Small-FOV Human Action

Áp dụng cho các công đoạn có không gian thao tác nhỏ, yêu cầu quan sát chi tiết:

* Kiểm tra linh kiện điện tử.
* Lắp ráp linh kiện.
* Thao tác tay trên bàn thao tác.
* Thao tác với connector, screw, PCB, jig, tray, tool.
* Pick / place / insert / remove / press / scan / tighten / inspect.
* Các thao tác có yêu cầu phân biệt tương tác người–vật thể.

Trọng tâm:

**Hand + Object + Tool + Pose + Interaction + Temporal**

---

## 2.2. Profile B — Large-Scale / Large-FOV Human Activity

Áp dụng cho không gian làm việc lớn:

* Lắp ráp thiết bị.
* Bảo trì máy móc.
* Sửa chữa.
* Kiểm tra thiết bị.
* Thao tác trong workstation lớn.
* Di chuyển giữa các khu vực trong quá trình thực hiện công việc.

Trọng tâm:

**Person + Tracking + Pose + Object/Equipment + Zone + Spatial/Temporal Activity**

---

## 2.3. Hybrid / Medium-Scale

Cho các bài toán nằm giữa hai profile trên.

Không xây dựng một hệ thống thứ ba độc lập; sử dụng kiến trúc chung với cấu hình perception phù hợp.

---

# 3. FUNCTIONAL SCOPE

## WP01 — Problem Definition & Industrial Requirement

### Công việc

* Xác định use case thực tế.
* Xác định đối tượng cần nhận biết.
* Xác định action cần nhận biết.
* Xác định workflow/procedure.
* Xác định anomaly cần phát hiện.
* Xác định điều kiện quan sát cần thiết.
* Xác định các tình huống Vision có thể và không thể giải quyết.

### Kết quả

* Problem Definition.
* System Scope / Non-Scope.
* Requirement Specification.
* Success Criteria.

---

# 4. WP02 — Human Action Taxonomy

Xây dựng hệ thống phân cấp hành động.

## Level 1 — Motion / Gesture

Ví dụ:

* Walk
* Reach
* Bend
* Turn
* Move
* Wait

## Level 2 — Interaction

Ví dụ:

* Touch
* Grab
* Release
* Contact
* Operate

## Level 3 — Atomic Action

Ví dụ:

* Pick
* Place
* Insert
* Remove
* Press
* Scan
* Tighten
* Inspect

## Level 4 — Task

Ví dụ:

* Assembly
* Inspection
* Packing
* Maintenance
* Repair

## Level 5 — Procedure / Workflow

Ví dụ:

* Assembly Procedure A
* Inspection Procedure B
* Maintenance Procedure C

### Kết quả

**Human Action Dictionary / Taxonomy**

Mỗi action nên được định nghĩa tối thiểu bởi:

* Action name.
* Ý nghĩa.
* Điều kiện bắt đầu.
* Điều kiện kết thúc.
* Đối tượng liên quan.
* Tool liên quan nếu có.
* Zone liên quan nếu có.
* Khoảng thời gian kỳ vọng.
* Action trước/sau nếu có.

---

# 5. WP03 — Literature & State-of-the-Art Research

Nghiên cứu các hướng liên quan trực tiếp:

* Human Action Recognition.
* Temporal Action Segmentation.
* Temporal Action Localization.
* Human-Object Interaction.
* Hand/Pose Understanding.
* Procedural Activity Understanding.
* Procedure Step Recognition.
* Mistake / Error Detection.
* Action Quality Assessment.
* Industrial Assembly / Manufacturing Vision.
* Multi-view / multi-camera.
* Real-time deployment.

### Core reference set

Ưu tiên nghiên cứu:

* IMPACT.
* IndustReal.
* Assembly101.
* Every Mistake Counts.
* HA4M.
* MS-TCN / MS-TCN++.
* ASFormer.
* ActionFormer.
* IKEA ASM.
* HoloAssist.
* EPIC-KITCHENS.
* COIN.
* CrossTask.
* FineGym.
* Literature review về vision-based procedural mistake analysis.

### Không yêu cầu

Không triển khai hàng loạt mô hình chỉ để “so model”.

Chỉ benchmark các phương pháp có khả năng trả lời một câu hỏi kỹ thuật cụ thể của dự án.

### Kết quả

**Research Matrix + Technology Selection Report**

---

# 6. WP04 — Camera & Observation Design

Nghiên cứu khả năng quan sát cần thiết trước khi lựa chọn mô hình.

## Fine-Grained

Xác định:

* Camera position.
* Height.
* Angle.
* FOV.
* Working distance.
* Resolution.
* FPS.
* Lighting.
* Hand visibility.
* Object visibility.
* Occlusion.

## Large-Scale

Xác định:

* Whole-body visibility.
* Machine/equipment visibility.
* Workspace coverage.
* Zone coverage.
* Trajectory visibility.
* Multi-person visibility.

### Kết quả

* Camera View Design.
* Observation Requirement.
* Visibility Checklist.
* Recommended capture configuration cho từng use case.

---

# 7. WP05 — Dataset Strategy

Thiết kế chiến lược dữ liệu:

**Public Dataset + Internal Industrial Dataset**

## Public Dataset

Dùng cho:

* Benchmark.
* Algorithm study.
* Pretraining/fine-tuning.
* Comparison.

## Internal Dataset

Dùng để:

* Kiểm chứng factory domain.
* Đánh giá domain gap.
* Tạo model thực tế.
* Phân tích failure case.

### Kết quả

**Dataset Strategy**

bao gồm:

* Data source.
* Data format.
* Train/val/test split.
* Cross-worker split.
* Cross-location split khi cần.
* Data quality criteria.

---

# 8. WP06 — Annotation Specification

Xây dựng chuẩn annotation thống nhất.

## Spatial Annotation

* Person.
* Object.
* Tool.
* Hand.
* Zone.

## Temporal Annotation

* Action start.
* Action end.
* Temporal segment.

## Semantic Annotation

* Action.
* Object.
* Tool.
* Interaction.

## Process Annotation

* Workflow.
* Step.
* Expected sequence.
* Valid branch.
* Completion state.

## Anomaly Annotation

* Wrong sequence.
* Missing step.
* Repeated step.
* Unexpected action.
* Wrong object.
* Wrong zone.
* Too slow.
* Too fast.
* Idle.
* Timeout.
* Incomplete.

### Kết quả

**Annotation Guideline v1**

---

# 9. WP07 — Scene & Human Perception

Xây dựng lớp perception nền tảng.

## Core

* Person detection.
* Person tracking.
* Object detection.
* Tool detection.
* Zone detection/definition.

## Fine-Grained branch

* Hand detection.
* Hand pose khi cần.
* Hand-object association.
* Object state/change observation.

## Large-Scale branch

* Whole-body pose.
* Spatial relation.
* Zone occupancy.
* Human-object/equipment relation.

### Kết quả

Một observation representation thống nhất, ví dụ:

```text
timestamp
worker_id
person
hands
objects
tools
zones
pose
relationships
```

### Acceptance

Video đầu vào phải tạo ra được observation ổn định theo thời gian, có identity association và không phụ thuộc vào action model.

---

# 10. WP08 — Human Action Understanding

Nghiên cứu và triển khai khả năng nhận diện hành động.

## Fine-Grained

Tập trung vào:

* Pick.
* Place.
* Insert.
* Remove.
* Press.
* Scan.
* Tighten.
* Inspect.
* Manipulation primitives.

## Large-Scale

Tập trung vào:

* Walk.
* Approach.
* Enter zone.
* Operate machine.
* Open/close.
* Maintenance.
* Assembly.
* Inspect.
* Move between areas.

### Phương pháp

Triển khai theo baseline tăng dần:

**Simple temporal baseline → Temporal model → Advanced model khi cần**

Các model như MS-TCN++, ASFormer hoặc ActionFormer chỉ được đưa vào khi baseline đơn giản không đạt yêu cầu.

### Kết quả

Action Event:

```text
worker_id
action
start_time
end_time
confidence
object
tool
zone
```

---

# 11. WP09 — Temporal Understanding

Đây là thành phần cốt lõi để biến recognition thành understanding.

Hệ thống phải xác định:

* Action start.
* Action end.
* Action duration.
* Action transition.
* Current action.
* Previous action.
* Next action.
* Idle period.
* Unknown/ambiguous period.

### Yêu cầu

Giảm hiện tượng:

```text
PICK
PICK
UNKNOWN
PICK
```

trở thành nhiều action giả.

### Kết quả

**Action Timeline**

Ví dụ:

```text
10:21:03 – 10:21:05  PICK
10:21:05 – 10:21:07  PLACE
10:21:08 – 10:21:10  SCAN
10:21:11 – 10:21:28  ASSEMBLE
```

---

# 12. WP10 — Process State & Workflow Engine

Đây là lớp business/process logic, tách khỏi AI perception.

## Chức năng

* Current process state.
* Expected next step.
* Valid transition.
* Workflow branching.
* Workflow completion.
* Restart/rework.
* Timeout.
* Process reset.

## Workflow phải cấu hình được

Ví dụ:

```yaml
workflow: assembly_A

steps:
  - S1: PICK
  - S2: PLACE
  - S3: SCAN
  - S4: ASSEMBLE
  - S5: INSPECT
```

Không hard-code workflow vào model.

### Kết quả

**Configurable Workflow Engine**

---

# 13. WP11 — Procedure Compliance & Anomaly Detection

Xây dựng engine đánh giá hành vi thực tế so với quy trình.

## Nhóm 1 — Sequence

* Wrong order.
* Skipped step.
* Repeated step.
* Unexpected step.
* Backward transition.

## Nhóm 2 — Temporal

* Too slow.
* Too fast.
* Timeout.
* Excessive idle.

## Nhóm 3 — Semantic

* Wrong object.
* Wrong tool.
* Wrong zone.
* Wrong interaction.

## Nhóm 4 — Completion

* Incomplete procedure.
* Premature completion.
* Abnormal termination.

### Đặc biệt

Hỗ trợ workflow có nhiều execution path hợp lệ.

Không mặc định:

**Deviation = Mistake**

### Kết quả

```text
Compliance = PASS / WARNING / VIOLATION
Violation Type
Expected
Observed
Timestamp
Confidence
Reason
```

---

# 14. WP12 — Evidence & Explainability

Mỗi cảnh báo quan trọng phải có thể truy nguyên.

Lưu tối thiểu:

* Worker ID.
* Workflow.
* Expected step.
* Observed action.
* Timestamp.
* Duration.
* Confidence.
* Snapshot/frame.
* Short video evidence khi phù hợp.
* Violation reason.

Ví dụ:

```text
Expected: SCAN
Observed: ASSEMBLE
Violation: WRONG_SEQUENCE
Time: 14:32:17
Evidence: 14:32:14–14:32:20
```

### Mục tiêu

Supervisor phải hiểu được kết quả mà không cần biết chi tiết model AI.

---

# 15. WP13 — Evaluation & Benchmark

Đánh giá ở ba tầng.

## AI Level

* Precision.
* Recall.
* F1.
* Temporal IoU.
* Boundary error.
* Detection/localization performance.

## Process Level

* Sequence accuracy.
* Step recognition accuracy.
* Skip detection.
* Wrong-order detection.
* Duration anomaly detection.
* False alarm.
* Missed violation.

## System Level

* FPS.
* End-to-end latency.
* GPU usage.
* CPU usage.
* Memory.
* Frame drop.
* Tracking stability.
* Camera failure recovery.

### Đặc biệt

Phải có **Error Analysis**:

* False positive.
* False negative.
* Occlusion.
* Motion blur.
* Similar action.
* Small object.
* Wrong tracking.
* Ambiguous action.
* Out-of-view.
* Lighting issue.

---

# 16. WP14 — Real-Time Prototype

Tích hợp pipeline end-to-end:

```text
Camera / Video
      ↓
Frame Acquisition
      ↓
Perception
      ↓
Tracking
      ↓
Action Understanding
      ↓
Temporal Engine
      ↓
Workflow Engine
      ↓
Anomaly Engine
      ↓
Evidence
      ↓
UI / API / Log
```

### Yêu cầu

Prototype phải có khả năng:

* Chạy video real-time hoặc near real-time.
* Theo dõi worker.
* Sinh action event.
* Theo dõi process state.
* Phát hiện violation.
* Ghi evidence.
* Hiển thị kết quả.

---

# 17. WP15 — Industrialization Foundation

Chỉ triển khai những thành phần thực sự cần cho prototype production:

## Input

* RTSP.
* Video file.
* Multi-camera khi use case yêu cầu.

## Runtime

* Config management.
* Model version.
* Workflow version.
* Logging.
* Health status.
* Error handling.
* Watchdog/recovery.

## Data

* Event log.
* Result storage.
* Evidence storage.

## Interface

* UI.
* REST/API khi cần tích hợp hệ thống khác.

### Không mặc định triển khai

* Kubernetes.
* Microservice architecture.
* Distributed inference.
* Complex cloud architecture.

Chỉ sử dụng khi yêu cầu thực tế chứng minh cần thiết.

---

# 18. WP16 — Human-in-the-Loop & Continuous Improvement

Cho phép:

```text
AI Detection
      ↓
Human Review
      ↓
Confirm / Reject
      ↓
Error Dataset
      ↓
Model Improvement
```

Mục tiêu:

* Thu thập false positive.
* Thu thập false negative.
* Phát hiện action mới.
* Cải thiện workflow.
* Cải thiện annotation.
* Versioning model.

---

# 19. WP17 — Multimodal Integration Boundary

Xác định những thông tin Vision không nên cố đoán.

Ví dụ:

* PLC status.
* Scanner result.
* Sensor state.
* Machine state.
* Tester result.
* MES/traceability.

Kiến trúc:

```text
Vision
+
Sensor / PLC
+
Scanner
+
Machine Data
+
MES
```

Vision chịu trách nhiệm phần quan sát mà camera có bằng chứng tốt.

---

# 20. RESEARCH OUTPUTS / DELIVERABLES

Dự án phải tạo ra tối thiểu các deliverable sau:

### D01 — Problem Specification

Định nghĩa chính thức phạm vi bài toán.

### D02 — Research Matrix

Bản đồ literature và state-of-the-art.

### D03 — Human Action Taxonomy

Action hierarchy + action dictionary.

### D04 — Workflow Specification

Cách biểu diễn procedure, state, transition và branch.

### D05 — Camera/Observation Specification

View design cho Small-FOV và Large-FOV.

### D06 — Dataset Specification

Dataset strategy + data split + data quality.

### D07 — Annotation Guideline

Chuẩn annotation.

### D08 — Perception Baseline

Person/Object/Hand/Tool/Tracking/Pose.

### D09 — Action Understanding Baseline

Action recognition + temporal localization/segmentation.

### D10 — Temporal Engine

Action timeline + state tracking.

### D11 — Workflow Engine

Configurable procedure state machine.

### D12 — Compliance/Anomaly Engine

Sequence/time/semantic violation detection.

### D13 — Evidence System

Frame/clip/event traceability.

### D14 — Evaluation Report

AI + process + system KPI.

### D15 — End-to-End Prototype

Camera → AI → Workflow → Anomaly → Evidence.

### D16 — R&D Technical Report

Tổng hợp phương pháp, thí nghiệm, limitation, kết quả và hướng tiếp theo.

---

# 21. DEFINITION OF DONE

Dự án được xem là hoàn thành Core Scope khi hệ thống có thể thực hiện được chuỗi:

```text
VIDEO
  ↓
DETECT HUMAN
  ↓
TRACK HUMAN
  ↓
UNDERSTAND ACTION
  ↓
GENERATE TEMPORAL EVENTS
  ↓
MAP EVENT TO PROCESS STEP
  ↓
TRACK WORKFLOW STATE
  ↓
CHECK COMPLIANCE
  ↓
DETECT ANOMALY
  ↓
PROVIDE EVIDENCE
```

và xử lý được tối thiểu:

```text
✓ Correct Sequence
✓ Wrong Sequence
✓ Skipped Step
✓ Repeated Step
✓ Unexpected Action
✓ Too Slow
✓ Too Fast
✓ Idle / Timeout
✓ Incomplete Procedure
```

trên ít nhất:

```text
1 Fine-Grained / Small-FOV use case
+
1 Large-Scale / Large-FOV use case
```

---

# 22. NON-SCOPE / KHÔNG PHẢI CORE

Những hạng mục sau không thuộc Core Scope ban đầu:

* End-to-end universal foundation model.
* VLM/LLM làm bộ quyết định cho toàn bộ hệ thống.
* World model.
* Reinforcement learning.
* Zero-shot universal action recognition.
* Fully autonomous workflow discovery.
* General-purpose AGI-like scene understanding.
* Distributed cloud architecture.
* Massive multi-camera deployment ngay ở phase R&D đầu tiên.

Các hướng này chỉ được nghiên cứu khi một limitation thực tế chứng minh rằng kiến trúc hiện tại không đủ.

---

# 23. CORE vs ADVANCED

## CORE

```text
Problem Definition
Action Taxonomy
Camera Design
Dataset
Annotation
Person/Object/Hand/Tool
Tracking
Action Recognition
Temporal Understanding
Workflow
Compliance
Anomaly
Evidence
Evaluation
Real-Time Prototype
```

## ADVANCED / OPTIONAL

```text
Action Quality Assessment
Few-shot Workflow Adaptation
Cross-site Generalization
Multi-camera Fusion
Weak/Self-supervised Learning
Vision + VLM
Vision + Sensor Fusion
Advanced Foundation Models
```

---

# 24. FINAL SYSTEM ARCHITECTURE

Kiến trúc đích của project:

```text
                    ┌────────────────────┐
                    │   CAMERA / VIDEO   │
                    └─────────┬──────────┘
                              ↓
                 ┌────────────────────────┐
                 │ Scene Understanding    │
                 │ Person / Object / Tool │
                 │ Hand / Pose / Zone     │
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Tracking & Relations   │
                 │ Human-Object-Tool-Zone │
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Action Understanding  │
                 │ Gesture / Atomic / Task│
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Temporal Understanding │
                 │ Start/End/Duration     │
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Action Event Stream    │
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Workflow / State Engine│
                 └──────────┬─────────────┘
                            ↓
                 ┌────────────────────────┐
                 │ Compliance / Anomaly   │
                 └──────────┬─────────────┘
                            ↓
                ┌───────────┴────────────┐
                ↓                        ↓
         Evidence / Log             UI / API
```

**Nguyên tắc kiến trúc cốt lõi:**

**Perception ≠ Process Logic**

AI quan sát thế giới thực.
Workflow Engine đánh giá thế giới đó có đúng quy trình hay không.

---

# 25. MỤC TIÊU CUỐI CÙNG

Human Action không được xem đơn thuần là một bài toán:

**“Nhận diện người đang làm gì.”**

Mục tiêu cuối là:

> **Xây dựng một nền tảng Vision AI có khả năng hiểu hành động và quá trình thực hiện công việc của con người trong môi trường công nghiệp, từ đó đánh giá mức độ tuân thủ quy trình và phát hiện các bất thường có ý nghĩa vận hành.**

Nền tảng phải đủ modular để cùng một kiến trúc có thể áp dụng cho:

```text
Assembly
Inspection
Maintenance
Repair
Packing
Material Handling
Operator Procedure
Work Instruction Compliance
Process Monitoring
Execution Anomaly
```

mà không cần xây dựng lại toàn bộ hệ thống cho từng bài toán.
