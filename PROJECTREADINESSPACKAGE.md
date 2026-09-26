# HUMAN ACTION

## PRE-PROJECT READINESS PACKAGE

### Bộ chuẩn bị trước khi chính thức triển khai R&D

---

# 1. MỤC ĐÍCH

Bộ Pre-Project Readiness được xây dựng để bảo đảm trước khi bắt đầu implementation, dự án đã thống nhất được:

* Bài toán cần giải quyết.
* Phạm vi thực tế.
* Kiến trúc tổng thể.
* Dữ liệu và annotation.
* Phương pháp đánh giá.
* Môi trường nghiên cứu.
* Cách tổ chức code/repository.
* Cách thực hiện experiment.
* Rủi ro chính.
* Điều kiện để xác nhận một giải pháp là đạt.

Mục tiêu không phải tạo thêm thủ tục, mà là:

> **Giảm tối đa việc nghiên cứu sai bài toán, chọn sai dữ liệu, benchmark sai KPI hoặc xây kiến trúc quá sớm.**

---

# 2. PROJECT CHARTER

Roadmap và SOW đã có, nhưng dự án vẫn cần một trang “Project Charter” cực ngắn.

## 2.1. Project Mission

**Human Action & Procedure Understanding for Industrial Vision**

Xây dựng giải pháp Vision AI có khả năng quan sát hành vi thao tác của con người trong môi trường công nghiệp, chuyển video thành action/event có cấu trúc và đánh giá việc thực hiện theo workflow/procedure.

## 2.2. Core Outcome

```text
Video
→ Observation
→ Action
→ Temporal Event
→ Process State
→ Workflow
→ Compliance / Anomaly
→ Evidence
```

## 2.3. Hai miền chính

```text
A. Fine-Grained / Small-FOV
B. Large-Scale / Large-FOV
```

## 2.4. Nguyên tắc

```text
Correct
→ Sufficient
→ Simple
→ Effective
```

Không sử dụng phương pháp phức tạp nếu một phương pháp đơn giản hơn đã giải quyết đủ yêu cầu.

---

# 3. SYSTEM REQUIREMENT SPECIFICATION

Đây là tài liệu mình cho rằng **rất nên có**.

SOW nói về phạm vi công việc.

SRS nói về:

> **Hệ thống cuối cùng phải làm được gì.**

## Functional Requirements

Ví dụ:

```text
FR01:
Detect worker

FR02:
Track worker

FR03:
Recognize action

FR04:
Determine action start/end

FR05:
Map action to process step

FR06:
Track workflow state

FR07:
Detect wrong sequence

FR08:
Detect skipped step

FR09:
Detect repeated step

FR10:
Detect abnormal duration

FR11:
Provide evidence
```

## Non-Functional Requirements

Ví dụ:

```text
NFR01:
Real-time / near real-time

NFR02:
Stable tracking

NFR03:
Configurable workflow

NFR04:
Model/version traceability

NFR05:
Recover from camera interruption

NFR06:
Low false alarm
```

---

# 4. USE-CASE & SCENARIO CATALOG

Đừng bắt đầu bằng dataset.

Hãy bắt đầu bằng các **scenario mà hệ thống phải giải quyết**.

Ví dụ:

### Scenario A — Correct Procedure

```text
PICK
→ PLACE
→ SCAN
→ ASSEMBLE
→ INSPECT
```

Expected:

```text
PASS
```

### Scenario B — Wrong Sequence

```text
PICK
→ PLACE
→ ASSEMBLE
→ SCAN
```

Expected:

```text
WRONG_SEQUENCE
```

### Scenario C — Skip

```text
PICK
→ PLACE
→ ASSEMBLE
```

Expected:

```text
SKIPPED_SCAN
```

### Scenario D — Timeout

```text
ASSEMBLE = 40 sec
Expected = 5–20 sec
```

Expected:

```text
TIMEOUT
```

### Scenario E — Valid Alternative Route

```text
A → B → C → D

A → C → B → D
```

Nếu cả hai được procedure cho phép:

```text
PASS
```

Đây là scenario cực kỳ quan trọng.

---

# 5. GOLDEN SCENARIO SET

Từ Scenario Catalog, chúng ta chọn khoảng:

**10–20 scenario chuẩn**

để làm bộ kiểm thử xuyên suốt dự án.

Ví dụ:

```text
GS01 Correct
GS02 Wrong Order
GS03 Skip
GS04 Repeat
GS05 Too Fast
GS06 Too Slow
GS07 Idle
GS08 Timeout
GS09 Unexpected Action
GS10 Wrong Object
GS11 Wrong Zone
GS12 Incomplete
GS13 Valid Branch
GS14 Occlusion
GS15 Multiple Workers
```

Sau này mọi version AI phải chạy lại Golden Scenario Set.

Đây chính là một dạng:

> **Regression Test cho Vision AI.**

Mình đánh giá nó cực kỳ hữu ích.

---

# 6. OBSERVABILITY / EVIDENCE SPECIFICATION

Ngay từ đầu phải thống nhất:

> “AI cần lưu lại những gì để chứng minh quyết định của nó?”

Một event tối thiểu:

```text
event_id
worker_id
workflow_id
step_id
action
object
tool
zone
start_time
end_time
duration
confidence
status
violation_type
```

Evidence:

```text
frame
snapshot
short clip
event log
```

Không đợi đến cuối mới nghĩ đến logging.

---

# 7. RESEARCH QUESTION & HYPOTHESIS REGISTER

Đây là phần phân biệt **R&D thực sự** với việc chỉ implementation.

Ví dụ:

```text
RQ01:
Pose-only có đủ cho action không?

RQ02:
Hand-object relationship có cải thiện Pick/Place không?

RQ03:
MS-TCN++ và ASFormer khác nhau thế nào trên factory data?

RQ04:
Workflow FSM có đủ cho compliance không?

RQ05:
Object state có giảm false positive không?

RQ06:
Camera angle ảnh hưởng action recognition bao nhiêu?

RQ07:
Small-FOV có cần hand pose không?

RQ08:
Large-FOV có cần video foundation model không?
```

Mỗi câu hỏi nên có:

```text
Hypothesis
Experiment
Metric
Result
Conclusion
```

Ví dụ:

```text
Hypothesis:
Hand-object relationship cải thiện Pick/Place.

Experiment:
Pose-only vs Pose+Object.

Metric:
F1 + boundary error.

Conclusion:
Accept / Reject.
```

---

# 8. EXPERIMENT PROTOCOL

Đây là thứ cực kỳ nên chuẩn hóa từ đầu.

Mỗi experiment phải ghi:

```text
Experiment ID
Objective
Dataset version
Train/val/test
Model version
Input resolution
FPS
Features
Hyperparameters
Hardware
Runtime
Metrics
Result
Failure cases
Conclusion
```

Ví dụ:

```text
EXP-007

Objective:
Compare MS-TCN++ vs ASFormer

Dataset:
HA4M-v1

Input:
Skeleton

Metric:
F1 / Edit / Segmental F1

GPU:
RTX XXXX
```

Như vậy vài tháng sau nhìn lại vẫn biết:

> “Tại sao chúng ta chọn model này?”

---

# 9. BASELINE LADDER

Mình muốn cố định chiến lược benchmark trước.

Không:

```text
Model A
→ Model B
→ Model C
→ Model D
→ Model E
```

mà:

```text
Level 0
Rule / heuristic

Level 1
Simple ML baseline

Level 2
Temporal baseline

Level 3
Strong temporal model

Level 4
Advanced method nếu cần
```

Ví dụ:

```text
FSM / threshold
        ↓
simple temporal classifier
        ↓
MS-TCN++
        ↓
ASFormer
        ↓
advanced model only if justified
```

Đây là lớp bảo vệ rất mạnh chống over-engineering.

---

# 10. DATA GOVERNANCE

Đây là một phần nên chuẩn hóa rất sớm.

## Dataset Versioning

```text
dataset_v0.1
dataset_v0.2
dataset_v1.0
```

## Data Split

Không được split ngẫu nhiên một cách vô thức.

Nên có:

```text
Random split
+
Cross-worker split
+
Cross-session split
+
Cross-location split
```

khi phù hợp.

Bởi nếu cùng một worker xuất hiện cả train và test, kết quả có thể đẹp nhưng không phản ánh generalization thực tế.

## Dataset Card

Mỗi dataset nên ghi:

```text
Source
Camera
Resolution
FPS
Participants
Environment
Action classes
Annotation
Known bias
Limitations
License
```

---

# 11. ENVIRONMENT & REPRODUCIBILITY

Trước khi implementation, khóa:

```text
OS
Python
CUDA
PyTorch
OpenCV
Ultralytics / other CV libs
Tracking library
Annotation tools
Experiment tools
```

và:

```text
requirements.txt
environment.yml
```

hoặc tương đương.

Mỗi experiment phải biết:

```text
Code version
+
Model version
+
Dataset version
+
Environment version
```

Không cần DevOps phức tạp.

Chỉ cần **reproduce được một experiment quan trọng** là đạt yêu cầu ban đầu.

---

# 12. REPOSITORY ARCHITECTURE

Không nên vừa nghiên cứu vừa để repository phát triển hỗn loạn.

Một cấu trúc đơn giản:

```text
human-action/
│
├── configs/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── annotations/
│
├── models/
│
├── src/
│   ├── perception/
│   ├── tracking/
│   ├── action/
│   ├── temporal/
│   ├── workflow/
│   ├── anomaly/
│   └── evidence/
│
├── experiments/
│
├── evaluation/
│
├── tools/
│
├── demos/
│
├── docs/
│
└── README.md
```

Không cần tạo framework quá lớn ngay từ đầu.

---

# 13. CONFIGURATION ARCHITECTURE

Một nguyên tắc mình đặc biệt muốn khóa:

> **Model, camera, workflow và threshold không được hard-code trong logic chính.**

Tách:

```text
camera.yaml
model.yaml
action.yaml
workflow.yaml
threshold.yaml
runtime.yaml
```

Ví dụ:

```yaml
workflow: assembly_A

steps:
  - PICK
  - PLACE
  - SCAN
  - ASSEMBLE
  - INSPECT
```

Điều này rất quan trọng khi cùng một engine phải phục vụ nhiều workstation.

---

# 14. RISK REGISTER

Chúng ta chưa cần một hệ thống quản trị rủi ro phức tạp.

Chỉ cần một bảng:

| Risk                   | Khả năng   | Ảnh hưởng  | Mitigation                         |
| ---------------------- | ---------- | ---------- | ---------------------------------- |
| Action quá giống nhau  | Cao        | Cao        | Temporal + object relation         |
| Occlusion              | Cao        | Cao        | Camera design + multi-view khi cần |
| Tracking switch        | Trung bình | Cao        | Stable ID + validation             |
| Camera view không đủ   | Cao        | Cao        | Observation study                  |
| Dataset không đại diện | Cao        | Cao        | Internal data                      |
| False alarm            | Cao        | Cao        | Unknown + temporal filtering       |
| Workflow đa nhánh      | Trung bình | Cao        | Configurable state graph           |
| Action quá ngắn        | Cao        | Trung bình | Higher FPS / temporal model        |
| Multi-person           | Trung bình | Cao        | Identity association               |
| Domain shift           | Cao        | Cao        | Cross-worker/site test             |

---

# 15. TRACEABILITY MATRIX

Đây là một tài liệu rất nhỏ nhưng rất giá trị.

Liên kết:

```text
Requirement
    ↓
Use Case
    ↓
Action
    ↓
Dataset
    ↓
Annotation
    ↓
Model
    ↓
Metric
    ↓
Test Scenario
```

Ví dụ:

```text
REQ-07 Wrong Sequence Detection

→ UC-03
→ Action: SCAN
→ Workflow: Assembly_A
→ Dataset: Internal-v1
→ Model: ASFormer
→ Metric: Sequence Accuracy
→ Golden Scenario: GS02
```

Khi có thay đổi, chúng ta biết chính xác cái gì bị ảnh hưởng.

---

# 16. SUCCESS CRITERIA

Một vấn đề rất dễ xảy ra:

> Model đạt accuracy tốt nhưng hệ thống vẫn không dùng được.

Do đó cần định nghĩa thành công ở 3 tầng.

## Level A — Perception

```text
Person
Object
Hand
Tracking
```

## Level B — Action

```text
Action F1
Temporal boundary
Event stability
```

## Level C — Process

```text
Correct sequence
Wrong sequence
Skip
Repeat
Duration anomaly
False alarm
Latency
```

Đặc biệt:

> **Process KPI là KPI cuối cùng.**

---

# 17. DEMO ACCEPTANCE CRITERIA

Trước khi gọi prototype là “đạt”, phải có một bộ demo cố định.

Ví dụ:

```text
Demo 01
Correct procedure

Demo 02
Wrong sequence

Demo 03
Skipped step

Demo 04
Repeated step

Demo 05
Too slow

Demo 06
Too fast

Demo 07
Unexpected action

Demo 08
Two workers

Demo 09
Occlusion

Demo 10
Alternative valid path
```

Không dùng một video đẹp duy nhất để đánh giá hệ thống.

---

# 18. DECISION LOG

Trong R&D sẽ có rất nhiều quyết định:

```text
Why YOLO?
Why not detector X?
Why Pose?
Why MS-TCN++?
Why FSM?
Why RGB?
Why RGB-D?
Why one camera?
Why two cameras?
```

Mỗi quyết định quan trọng chỉ cần ghi:

```text
Decision
Alternatives
Evidence
Reason
Date
```

Ví dụ:

```text
Decision:
Use FSM for workflow engine.

Alternatives:
Learned workflow model.

Reason:
Workflow predefined and configurable.
FSM is interpretable, deterministic and sufficient.
```

Điều này giúp chúng ta không quay lại tranh luận cùng một vấn đề nhiều lần.

---

# 19. RESOURCE / COMPUTE PLAN

Không cần mua phần cứng lớn ngay từ đầu.

Chia:

### Stage 1 — Research

```text
Existing workstation/GPU
```

### Stage 2 — Prototype

```text
Target industrial GPU
```

### Stage 3 — Deployment

```text
Production hardware
```

Tương tự storage:

```text
Raw data
Processed data
Model
Evidence
Experiment outputs
```

phải tính trước để tránh đến giữa project mới phát sinh bottleneck.

---

# 20. PROJECT WORKING METHOD

Không cần Scrum/Kanban/MLOps phức tạp.

Mình đề xuất một vòng lặp rất đơn giản:

```text
Question
   ↓
Hypothesis
   ↓
Experiment
   ↓
Result
   ↓
Failure Analysis
   ↓
Decision
   ↓
Implementation
```

Mỗi vòng phải kết thúc bằng:

```text
KEEP
CHANGE
DROP
```

Ví dụ:

```text
Pose-only
→ FAIL

Pose + Object
→ KEEP

Complex VLM
→ DROP
```

Điều này giúp R&D cực kỳ “sạch”.

---

# 21. DOCUMENTATION SET

Chỉ cần duy trì một bộ tài liệu nhỏ:

```text
01_Project_Charter
02_System_Requirements
03_Roadmap
04_SOW
05_Research_Matrix
06_Action_Taxonomy
07_Workflow_Spec
08_Dataset_Spec
09_Annotation_Guideline
10_Experiment_Log
11_Evaluation_Report
12_Decision_Log
13_Risk_Register
14_Final_Technical_Report
```

Không cần viết tài liệu dài.

Tài liệu phải phục vụ implementation.

---

# 22. PROJECT READINESS CHECKPOINT

Trước khi chính thức bắt đầu coding, chúng ta phải kiểm tra:

### Problem

```text
☑ Problem defined
☑ Scope defined
☑ Non-scope defined
```

### Research

```text
☑ Literature mapped
☑ Core references selected
☑ Research questions defined
```

### System

```text
☑ Architecture defined
☑ Fine-Grained profile defined
☑ Large-Scale profile defined
☑ Workflow model defined
```

### Data

```text
☑ Dataset strategy defined
☑ Annotation strategy defined
☑ Test scenarios defined
```

### Evaluation

```text
☑ AI metrics defined
☑ Process metrics defined
☑ System metrics defined
☑ Golden scenarios defined
```

### Engineering

```text
☑ Repository defined
☑ Environment defined
☑ Config structure defined
☑ Experiment logging defined
```

### Risk

```text
☑ Main risks identified
☑ Mitigation strategy defined
```

---

# 23. FINAL “GO / NO-GO” GATE

Chỉ khi toàn bộ câu hỏi sau đều có câu trả lời rõ ràng:

```text
1. What are we solving?
2. What are we not solving?
3. What is an Action?
4. What is a Step?
5. What is a Workflow?
6. What is a Violation?
7. What must the camera see?
8. What data do we need?
9. How will we annotate it?
10. How will we measure success?
11. What is our baseline?
12. What is our first experiment?
13. What is our fallback if it fails?
```

→ **GO**

Sau đó mới chính thức:

```text
Research
   ↓
Dataset
   ↓
Baseline
   ↓
Experiment
```

---

# 24. TOÀN BỘ BỘ KHUNG CỦA DỰ ÁN

Sau khi bổ sung Pre-Project Readiness, toàn bộ cấu trúc dự án của chúng ta sẽ là:

```text
                    HUMAN ACTION R&D
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
     ROADMAP              SOW          READINESS PACK
   Làm thế nào?       Làm những gì?    Đã sẵn sàng chưa?
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                    RESEARCH EXECUTION
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Literature            Data              System
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                       EXPERIMENT
                           │
                           ▼
                     VALIDATION
                           │
                           ▼
                       PROTOTYPE
                           │
                           ▼
                    INDUSTRIALIZE
```

---

# 25. HẠNG MỤC CUỐI CÙNG: “RESEARCH BACKLOG”

Mình muốn thêm đúng **một thứ nữa**, và đây sẽ là nơi chứa mọi ý tưởng chưa làm.

Ví dụ:

```text
BACKLOG

[CORE]
- Compare pose vs hand-object
- Build action event format
- Implement workflow FSM
- Test MS-TCN++

[NEXT]
- Multi-camera
- Action quality
- Cross-worker generalization

[ADVANCED]
- VLM
- Foundation model
- Few-shot workflow learning
```

Nguyên tắc:

> **Ý tưởng hay nhưng chưa cần thiết không được chen ngang Core Roadmap.**

Nó chỉ đi vào Backlog.
