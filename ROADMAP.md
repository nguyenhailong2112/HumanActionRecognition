# ROADMAP HUMAN ACTION RECOGNITION SYSTEM

1. Đích đến của toàn bộ Roadmap

Một hệ thống có khả năng:

VIDEO / CCTV
     │
     ▼
Scene Understanding
     │
     ├── Person
     ├── Tracking
     ├── Object
     ├── Tool
     ├── Hand / Pose
     └── Zone
     │
     ▼
Action Understanding
     │
     ├── Gesture
     ├── Atomic Action
     ├── Task
     └── Activity
     │
     ▼
Temporal Understanding
     │
     ├── Start
     ├── End
     ├── Duration
     └── Transition
     │
     ▼
Action Event Stream
     │
     ▼
Workflow / Procedure State
     │
     ▼
Compliance & Anomaly
     │
     ├── Wrong Sequence
     ├── Skipped Step
     ├── Repeated Step
     ├── Unexpected Action
     ├── Too Slow
     ├── Too Fast
     ├── Idle / Timeout
     └── Incomplete Procedure
     │
     ▼
Evidence + Decision

Và toàn bộ nghiên cứu phải hỗ trợ 2 miền chính:

                    HUMAN ACTION
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 Fine-Grained / Small FOV      Large-Scale / Large FOV
 Hand/Object/Tool               Person/Pose/Zone
 Manipulation                   Activity/Task
 

2. Roadmap cụ thể

Đề xuất triển khai 12 Phase, chia thành 4 lớp lớn:

| Lớp                   | Phase  | Mục tiêu                       |
| --------------------- | ------ | ------------------------------ |
| **A — Understand**    | 0 → 3  | Hiểu đúng bài toán             |
| **B — Build**         | 4 → 7  | Xây các thành phần AI + logic  |
| **C — Prove**         | 8 → 10 | Chứng minh hệ thống hoạt động  |
| **D — Industrialize** | 11     | Đưa thành kiến trúc production |

Có một nguyên tắc rất quan trọng: "Chúng ta không đi sang phase tiếp theo chỉ vì “đã làm xong code”. Chỉ đi tiếp khi checkpoint của phase trước đã được chứng minh."


# PHASE 0 — Research Charter & Problem Definition

Mục tiêu: Đây chính là checkpoint khởi công - công đoạn chuẩn bị trước khi chính thức bắt tay vào triển khai dự án.

Trước khi đọc sâu paper hoặc chọn model, chúng ta phải đóng một bản: 'Human Action Research Specification'

Nó trả lời được: "Chúng ta giải quyết cái gì?"

Ví dụ:

Understand human actions/tasks over time + Monitor predefined workflows + Detect procedural/execution deviations

Không giải quyết cái gì?

Ví dụ:

Không cố suy đoán trạng thái vật lý/logic mà camera không quan sát được.
Không ép mọi bài toán vào một model duy nhất.
Không dùng foundation model chỉ vì “mới”.

Xác định taxonomy:

Gesture
↓
Atomic Action
↓
Task
↓
Activity
↓
Procedure

Xác định anomaly taxonomy:

Wrong Order
Skip
Repeat
Unexpected
Too Slow
Too Fast
Idle
Timeout
Incomplete
Wrong Object
Wrong Zone

Xác định hai profile:

Profile A:
Fine-Grained / Small FOV

Profile B:
Large-Scale / Large FOV

Output

Deliverable D0: 'Human_Action_Research_Spec.md' 

gồm:

Problem Definition
Scope
Non-scope
Taxonomy
System Goal
Profile A
Profile B
Terminology
Success Criteria
Initial Architecture

### CHECKPOINT 0

Chúng ta phải có thể nói chính xác một câu:

“Hệ thống Human Action của chúng ta nhận đầu vào gì, hiểu cái gì, và cuối cùng phát hiện cái gì?”

Nếu câu này chưa rõ → không được bước sang model.


# PHASE 1 — Literature & State-of-the-Art Mapping

Đây là phase nghiên cứu học thuật chính.

Mục tiêu không phải đọc thật nhiều paper.

Mục tiêu là: Biết cộng đồng đã giải quyết được gì, chưa giải quyết tốt gì, và phần nào chúng ta nên kế thừa.

## 1.1. Chia literature thành các nhánh

A. Human Action Recognition
B. Temporal Action Segmentation
C. Temporal Action Localization
D. Human-Object Interaction
E. Hand / Pose Understanding
F. Procedural Activity Understanding
G. Procedure Step Recognition
H. Mistake Detection
I. Action Quality Assessment
J. Industrial Assembly / Manufacturing
K. Multi-view / Multi-camera
L. Real-time Industrial Deployment

## 1.2. Core papers

Ưu tiên:

IMPACT
IndustReal
Assembly101
Every Mistake Counts
HA4M
MS-TCN++
ASFormer
ActionFormer
IKEA ASM
HoloAssist
EPIC-KITCHENS
COIN
CrossTask
2026 Mistake Analysis Review

Mỗi paper không đọc kiểu “tóm tắt abstract”.

Chúng ta phải extract:

Problem
Input
Camera
Dataset
Annotation
Action granularity
Temporal representation
Architecture
Training
Evaluation
Failure cases
Limitations
Industrial relevance
What we can reuse

## 1.3. Output quan trọng nhất

Một Research Matrix:

Paper
Problem
Input
View
Action Level
Temporal
Error
Dataset
Code
Kế thừa

### CHECKPOINT 1

Sau phase này, chúng ta phải trả lời được:

“Human Action Recognition của chúng ta khác gì so với Action Recognition, TAS, Procedure Recognition, Mistake Detection?”

và:

“Đâu là những thành phần đã có lời giải tương đối tốt, đâu là phần còn khó?”

Đây sẽ là literature checkpoint đầu tiên.


# PHASE 2 — Industrial Use-Case & Action Taxonomy

Đây là phase chuyển từ học thuật sang factory reality.

Mục tiêu: Không lấy dataset academic làm chuẩn tuyệt đối.

Chúng ta xây: Industrial Human Action Taxonomy

Ví dụ:

### Level 1 — Motion

Walk
Reach
Bend
Turn
Move

### Level 2 — Interaction

Touch
Grab
Release
Interact
Operate

### Level 3 — Atomic Action

Pick
Place
Insert
Remove
Press
Scan
Tighten
Inspect

### Level 4 — Task

Assembly
Inspection
Packing
Maintenance
Loading
Repair

### Level 5 — Procedure

Assembly Procedure A
Maintenance Procedure B
Inspection Procedure C

### Đồng thời định nghĩa action contract

Ví dụ:

</> YAML

action: PICK_COMPONENT

start_condition:
  hand_near_object: true

end_condition:
  object_displaced: true

required_object:
  - component_A

expected_duration:
  min: 0.5
  max: 3.0

### CHECKPOINT 2

Chúng ta phải có:

Action Dictionary + Procedure Dictionary

Đây là nền móng cho dataset, annotation và workflow engine sau này.


# PHASE 3 — Observation & Camera/System Design

Đây là phase rất thực tế và mình muốn làm trước khi train AI nghiêm túc.

Bởi: Camera geometry sai thì model tốt đến đâu cũng khó cứu.

Chúng ta nghiên cứu: 

- Small FOV:

Camera
↓
Hands
↓
Objects
↓
Tools
↓
Workbench

- Large FOV:

Camera
↓
Whole worker
↓
Machine
↓
Workspace
↓
Zone

- Xác định:

Resolution
FPS
FOV
Distance
Height
Angle
Lighting
Occlusion
Background
Privacy
Camera count

- Output: Camera/View Design Matrix

Use case
FOV
View
Required detail
Camera type
Main challenge

### CHECKPOINT 3

Với mỗi loại Human Action, chúng ta phải biết:

Camera cần nhìn thấy cái gì để action đó có thể được suy ra đáng tin cậy?

Đây là checkpoint cực quan trọng.

### Note

Tạm thời tại Phase này, để triển khai core chương trình/hệ thống, mình đề xuất sử dụng datasets các image/video trong các datasets gốc của các bài nghiên cứu để triển khai, thử nghiệm. Hiện tại mình chưa có hệ thống camera, chưa có dữ liệu thực tế, nên bước này tạm thời sử dụng datasets local sẵn có đã thu thập được.
Chúng ta dùng datasets nào, sử dụng như thế nào, ... hãy trình bày và hướng dẫn mình rõ ràng chi tiết nhất nhé.


# PHASE 4 — Dataset & Annotation Strategy

Mục tiêu: Xác định Public dataset + Internal dataset + Synthetic / augmentation nếu cần

Public datasets chúng ta có thể dùng:

Assembly101
IndustReal
IMPACT
HA4M
IKEA ASM
HoloAssist
EPIC-KITCHENS
COIN
CrossTask

nhưng không được mặc định rằng dataset nào cũng phù hợp factory CCTV.

### Annotation hierarchy

Mình đề xuất annotation nhiều tầng:

Frame
 ├── Person
 ├── Object
 ├── Hand
 ├── Tool
 └── Zone

Temporal
 ├── Action Start
 └── Action End

Semantic
 ├── Action
 ├── Object
 └── Interaction

Procedure
 ├── Step
 ├── Sequence
 └── State

Anomaly
 ├── Type
 ├── Time
 └── Evidence

Điều rất quan trọng: Không annotation tất cả mọi thứ ngay từ đầu.

Ta chia: MVP annotation - Validate - Expanded annotation

### CHECKPOINT 4

Chúng ta phải có: 'Annotation Specification v1'

### Note

Bước "Data Annotation" này là vô cùng quan trọng, vậy nên gán những nhãn gì, label object nào, cách thức gán nhãn như thế nào, quá trình ra sao, ... bạn hãy trình bày và hướng dẫn mình thật chi tiết rõ ràng nhé.


# PHASE 5 — Perception Baseline

Đây là lúc bắt đầu code/model.

Nhưng không bắt đầu bằng Action Transformer.

Bắt đầu từ nền perception:

Person Detection
Person Tracking
Object Detection
Pose
Hand
Tool
Zone

### Profile A

Person + Hand + Object + Tool + Pose

### Profile B

Person + Tracking + Pose + Object + Zone + Trajectory

#### Output

Một representation thống nhất:

</> Python

Observation
{
    timestamp,
    worker_id,
    persons,
    hands,
    objects,
    tools,
    zones
}

### CHECKPOINT 5

Video → Perception phải chạy ổn định và có tracking.

Chưa cần hiểu workflow.


# PHASE 6 — Action Understanding

Đây mới là Human Action core.

Nghiên cứu hai hướng

### Hướng A — Feature-based / modular

Pose + Hand + Object + Trajectory
        ↓
Temporal model
        ↓
Action

### Hướng B — Video-based

Video clip
   ↓
Temporal model
   ↓
Action

Sau đó benchmark.

#### Không cần 20 model.

Chỉ cần một baseline hierarchy:

Baseline 1: Simple temporal classifier

Baseline 2: MS-TCN++

Baseline 3: ASFormer

Baseline 4: ActionFormer

Rồi benchmark trên cùng dataset.

### CHECKPOINT 6

Hệ thống phải tạo được:

Action Event

PICK
start = 12.2
end = 13.8
confidence = 0.93

chứ không chỉ:

class = PICK


# PHASE 7 — Temporal & State Engine

Đây là lúc hệ thống bắt đầu hiểu dòng thời gian.

Từ:

PICK
PLACE
SCAN
ASSEMBLE

thành:

S1 PICK
S2 PLACE
S3 SCAN
S4 ASSEMBLE

### Engine cần xử lý

Action Start
Action End
Duration
Transition
Current State
Next Expected State
Unknown
Idle

Có thể bắt đầu rất đơn giản:

Finite State Machine

chứ chưa cần học bằng neural network.

Ví dụ:

S1
 ↓
S2
 ↓
S3
 ↓
S4

Nhưng phải hỗ trợ branch

S1
 ↓
S2
 ├── S3A
 └── S3B
      ↓
     S4

### CHECKPOINT 7

Video thực tế phải biến thành:

Action Timeline + Current Process State


# PHASE 8 — Procedure Compliance & Anomaly Detection

Đây là đích thực tế quan trọng nhất.

Chúng ta implement:

Wrong Sequence
Skipped Step
Repeated Step
Unexpected Action
Too Slow
Too Fast
Idle
Timeout
Incomplete
Wrong Object
Wrong Zone

### Đặc biệt phải phân biệt:

- Procedural error
Expected:
A → B → C

Observed:
A → C → B

- Execution error
C thực hiện sai

Ví dụ:

Wrong Object
Wrong Tool
Wrong Interaction
Too Short
Too Long

Và phải hỗ trợ multiple valid paths

Ví dụ:

A
 ↓
B ──→ C
      │
      D

hoặc:

A
 ↓
C
 ↓
B

có thể cả hai đều hợp lệ, tùy procedure.

Đây là một vấn đề quan trọng được nhấn mạnh trong literature về procedural mistake analysis.

### CHECKPOINT 8

Hệ thống phải trả lời được:

Observed sequence có compliant với workflow không? Nếu không, sai ở đâu và vì sao?


# PHASE 9 — Evidence & Explainability

Đây là phase biến AI từ “demo” thành hệ thống có khả năng được sử dụng.

Mỗi violation cần:

Worker
Procedure
Expected Step
Observed Step
Timestamp
Duration
Confidence
Frame
Video clip
Reason

Ví dụ:

Worker: W07

Expected:
SCAN

Observed:
ASSEMBLE

Time:
14:32:17

Violation:
WRONG_SEQUENCE

Evidence:
14:32:14–14:32:20

### CHECKPOINT 9

Một supervisor không biết AI model vẫn phải hiểu được:

“AI vừa phát hiện lỗi gì?”


# PHASE 10 — System Evaluation

Đây là phase rất hay bị bỏ qua.

Chúng ta đánh giá ở 3 tầng.

#### AI level

Precision
Recall
F1
mAP
Temporal IoU
Boundary Error

#### Process level
Sequence Accuracy
Skip Detection
Wrong-order Detection
Duration Error Detection
False Alarm
Miss Rate

#### System level
FPS
Latency
GPU
CPU
Memory
Dropped Frame
Camera Failure
Recovery

#### Đặc biệt phải xây Error Taxonomy

Ví dụ:

False Positive
    ↓
Occlusion
Low resolution
Bad lighting
Wrong tracking
Ambiguous action

và:

False Negative
    ↓
Short action
Small object
Fast gesture
Similar action

### CHECKPOINT 10

Không chỉ biết:

“Model đạt 92%.”

Mà phải biết:

“Model sai 8% ở đâu, tại sao sai, và có cách khắc phục nào?”


# PHASE 11 — Industrialization / Production Prototype

Đây là phase cuối.

Chúng ta đóng gói thành:

Video Input
 ↓
Inference
 ↓
Tracking
 ↓
Action Engine
 ↓
Workflow Engine
 ↓
Anomaly Engine
 ↓
Evidence
 ↓
Database
 ↓
Dashboard / API

#### Các vấn đề production

RTSP
Multi-camera
Frame buffering
GPU scheduling
Watchdog
Crash recovery
Logging
Config
Model version
Workflow version
Database
Health monitoring

Nhưng chỉ triển khai những thứ thực sự cần.

Không xây cả microservice/Kubernetes/distributed architecture nếu một industrial PC chạy tốt bằng một application architecture đơn giản.

### CHECKPOINT 11

Một pipeline end-to-end phải chạy được:

RTSP
→ AI
→ Action
→ Workflow
→ Anomaly
→ Evidence
→ UI/API

ổn định trong thời gian thực.

3. Sau 12 phase, chúng ta sẽ có 4 sản phẩm R&D

## Product A — Human Action Engine

Video
→ Human / Object / Hand
→ Action

## Product B — Temporal Activity Engine

Action
→ Timeline
→ State
→ Duration

## Product C — Procedure Compliance Engine
Timeline
→ Workflow
→ Compliance
→ Anomaly

## Product D — Factory Human Action Platform
Camera
→ AI
→ Procedure Understanding
→ Monitoring
→ Evidence
→ Integration

Nếu một ngày nào đó chúng ta thay model AI, B/C/D vẫn giữ nguyên.

Đây chính là modularity mà mình muốn bảo vệ.

4. Hai track nghiên cứu nên chạy song song

Thay vì tuần tự 100%:

Fine-Grained
Large-Scale

mình muốn:

                    COMMON CORE
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
     TRACK A                       TRACK B
 Fine-Grained                   Large-Scale
 Small FOV                      Large FOV
 Hand/Object                    Person/Zone
 Assembly                       Maintenance
 Inspection                     Large task
          │                           │
          └─────────────┬─────────────┘
                        ▼
               COMMON EVENT FORMAT
                        ↓
               TEMPORAL ENGINE
                        ↓
               WORKFLOW ENGINE
                        ↓
               ANOMALY ENGINE

Điều này giúp chúng ta không nghiên cứu hai hệ thống độc lập, nhưng vẫn tôn trọng sự khác biệt về perception.

5. Một “Research Gate” mình đặc biệt muốn đặt

Đây là thứ giúp dự án không bị trôi.

| Gate | Câu hỏi bắt buộc                                 |
| ---- | ------------------------------------------------ |
| G0   | Ta đang giải quyết chính xác bài toán gì?        |
| G1   | Literature đã làm được gì?                       |
| G2   | Action của factory được định nghĩa thế nào?      |
| G3   | Camera cần thấy gì?                              |
| G4   | Dữ liệu phải annotate thế nào?                   |
| G5   | Perception có đáng tin chưa?                     |
| G6   | Action có temporal boundary chưa?                |
| G7   | Timeline có ổn định chưa?                        |
| G8   | Workflow có phát hiện violation không?           |
| G9   | Người vận hành có kiểm chứng được kết quả không? |
| G10  | KPI hệ thống đạt yêu cầu chưa?                   |
| G11  | Có thể chạy production prototype chưa?           |

6. Và đây là thứ tự công việc mình khuyên chúng ta thực sự làm

Không phải:

Paper
→ YOLO
→ Train
→ Demo

mà là:

                    HUMAN ACTION R&D
                          │
                          ▼
                [0] Problem Definition
                          │
                          ▼
                [1] Literature Mapping
                          │
                          ▼
                [2] Action Taxonomy
                          │
                          ▼
                [3] Camera / Observation
                          │
                          ▼
                [4] Dataset / Annotation
                          │
                          ▼
                [5] Perception Baseline
                          │
                          ▼
                [6] Action Recognition
                          │
                          ▼
                [7] Temporal State Engine
                          │
                          ▼
                [8] Workflow / Compliance
                          │
                          ▼
                [9] Evidence
                          │
                          ▼
                [10] Evaluation
                          │
                          ▼
                [11] Production Prototype

7. Nhưng mình muốn thêm một nhánh “R&D Question”

Mỗi phase không chỉ có implementation task.

Chúng ta nên duy trì một file:

Research Questions & Hypotheses

Ví dụ:

RQ01:
Pose-only có đủ cho industrial action không?

RQ02:
Hand-object relationship cải thiện PICK/PLACE bao nhiêu?

RQ03:
MS-TCN++ vs ASFormer trong factory?

RQ04:
FSM đơn giản có đủ cho workflow compliance không?

RQ05:
Object state có giúp giảm false positive không?

RQ06:
Small-FOV có cần hand pose hay chỉ hand-object tracking?

RQ07:
Large-FOV có cần full video model không?

RQ08:
Temporal smoothing ảnh hưởng latency thế nào?

RQ09:
Camera angle ảnh hưởng performance bao nhiêu?

RQ10:
Một workflow model có generalize được sang workflow khác không?

Đây mới thực sự là R&D.

Chứ nếu chỉ train model rồi xem accuracy thì mới là implementation/benchmark.

8. Roadmap “không over-engineering” của chúng ta

Mình muốn đặt 3 tầng ưu tiên.

#### CORE — nhất định phải làm

Action Definition
Person/Object/Hand/Tool
Tracking
Temporal Action
Workflow State
Sequence Check
Duration
Anomaly
Evidence
Evaluation

#### EXTENSION — chỉ làm khi CORE đã ổn

Multi-camera
Pose refinement
Action quality
Multiple valid workflow paths
Human-in-loop
Cross-workstation generalization

#### ADVANCED — để mở, không mặc định làm
VLM
Foundation Video Model
Multimodal LLM
Graph reasoning
Self-supervised representation
Zero-shot action
Few-shot workflow induction

Như vậy chúng ta không bị mắc vào “AI càng to càng tốt”.

9. Điểm khởi công thực sự của chúng ta

Mặc dù roadmap có 12 phase, checkpoint đầu tiên mình muốn chúng ta làm ngay bây giờ chỉ là PHASE 0 + một phần PHASE 1.

Cụ thể, sản phẩm đầu tiên phải là:

Human Action Research Blueprint

Nội dung:

01. Problem Statement
02. Scope / Non-Scope
03. Human Action Taxonomy
04. Procedure Taxonomy
05. Anomaly Taxonomy
06. Fine-Grained Profile
07. Large-Scale Profile
08. Common System Architecture
09. Research Questions
10. Evaluation Objectives
11. Literature Categories
12. Initial Research Matrix
13. Development Checkpoints
14. Definition of Done

---

# CURRENT EXECUTION STATUS — 2026-09-27

Roadmap phases above describe the intended system, not completed implementation. Current evidenced implementation is a procedure-scoped research slice:

| Checkpoint | Current status | Evidence boundary |
|---|---|---|
| CP01–CP04 | Historical / superseded where later evidence applies | Initial implementation, protocol work and acquisition states remain as dated history. CP05–CP06 supersede old missing-data/environment status. |
| CP05 | PARTIAL, action baseline established | IMPACT v1.1 TAS-S S2, `Disassembly_A/front`, 39/5/4; Framewise and our MS-TCN trained/evaluated; not official leaderboard reproduction. |
| CP06 | PARTIAL, action reliability and synthetic workflow logic | Three-seed study, per-execution/pooled metrics, error review package, deterministic engine/validator tests. No validated process semantics. |
| CP07 | Implementation/audit package CLOSED; system remains PARTIAL | Event contract, trace adapter, activation gate, review handoff, boundary audit and 56-test suite; no human-validated workflow or process metrics. See `experiments/EXP-CP07.md`. |
| CP07.1 | Engineering hardening CLOSED; semantic gate remains | One engine supports route and prerequisite-DAG inputs; route skip handling corrected; metrics enforce sequence alignment and configured background; observations persist independently from accepted workflow events. 63 tests pass. See `experiments/CP07.1/CP07.1_system_hardening.md`. |

Current next gate: process owner completes the human-owned `HumanSemanticWorksheet.md` and supplies the reviewed Research Workflow Specification. CP08 should validate that input, add narrow workflow-YAML and event-evidence-reference plumbing to the current API, and only then run frozen ActionEvents through actual workflow semantics. Do not mark the full architecture above as implemented: person/object/tool/pose/zone tracking, validated compliance evaluation, streaming runtime, and factory deployment remain future work.
