# HUMAN ACTION

## MASTER CODING & IMPLEMENTATION CHECKSHEET

### Coding / Research Implementation / Validation / Prototype

> **Current-status rule (2026-10-01):** Sections 1–38 are preserved checkpoint-time snapshots and may contain superseded acquisition/hardware states or earlier “SOP” wording. Use the latest dated checkpoint section, currently CP09, plus `ROADMAP.md` and the current CP09 handoff for present status. The current artifact is a **Research Workflow Specification / Benchmark Procedure Interpretation**, not an official factory SOP.

> **CP08 status (2026-10-01):** Frozen CP05 MS-TCN outputs were converted to 69 structured ActionEvents and linked 1:1 to existing source videos, snapshots and clips (programmatic file/link audit; no semantic visual review). Workflow finalization now distinguishes an observation ending from an explicitly ended incomplete procedure. The full current test suite reports 66 passing tests. `configs/workflows/disassembly_A.yaml` remains absent, the draft remains `HUMAN_REVIEW_REQUIRED`, and process compliance/anomaly metrics remain `NOT_EVALUATED`. Human workflow decisions and the 13-event evidence review are pending; see `experiments/CP08/` and the root CP08 handoffs. CP08 is **PARTIAL**, not end-to-end process completion.

> **CP09 status (2026-10-01):** CP08 finalization code is present and verified; pipeline EOF remains observation end. CP09 corrected confirmed event-history pollution so rejected events remain in observations but do not enter accepted workflow history or mutate current accepted state. Official TAS-S scope is recorded as 25 non-NULL + NULL; frozen project model scope remains 17 non-NULL + NULL. Full suite: 73 passed; compileall passed. Human workflow approval is still missing, so no executable workflow, real process trace, or process metric exists. CP09 is **PARTIAL**; see `experiments/EXP-CP09.md`.

> **CP10 status (2026-10-01):** Validator now separately enforces complete disposition coverage over project/model actions and a workflow vocabulary containing exactly non-`out_of_scope` actions. Synthetic valid mixed-disposition configuration passes; missing/extra/unknown/out-of-scope cases fail. Full suite: 74 passed; compileall passed. No human-approved YAML exists, so real workflow validation/trace and process metrics remain **NOT EVALUATED**. CP10 is **PARTIAL**; see `experiments/EXP-CP10.md`.

> **CP11 status (2026-10-01):** Closed for the project-level Research Workflow Specification / Benchmark Procedure Interpretation v1. The executable config has explicit `RESEARCH_APPROVED` / `PROJECT_RESEARCH` scope and `factory_sop_validated: false`; validator passes over all 17 model actions. UNSCREW precedes the four unordered component removals. Deterministic out-of-scope behavior and synthetic partial-order/completion tests pass. Full suite: 85 passed; compileall passed. The 69 frozen CP08 events all retain `evidence_status: unknown`; therefore the real held-out trace and all process-performance metrics remain **NOT EVALUATED** pending human visual evidence review and an explicit derived evidence policy. This is not factory-SOP validation. See `experiments/EXP-CP11.md`.

---

# 0. CÁCH SỬ DỤNG CHECKSHEET

## Status

Sử dụng thống nhất:

* `NS` — Not Started
* `IP` — In Progress
* `BL` — Blocked
* `RD` — R&D / Under Investigation
* `PASS` — Completed / Accepted
* `FAIL` — Completed nhưng chưa đạt
* `HOLD` — Tạm dừng
* `N/A` — Không áp dụng

## Progress

Mỗi task có thể ghi:

```text
0%   Chưa bắt đầu
25%  Đã chuẩn bị
50%  Đã implementation
75%  Đang validation / optimization
100% Đã nghiệm thu
```

## Evidence

Mỗi task hoàn thành nên có ít nhất một bằng chứng:

```text
Code commit
Config
Experiment ID
Dataset version
Model checkpoint
Result file
Screenshot
Video demo
Evaluation report
```

---

# 1. MASTER PROGRESS STRUCTURE

| WP   | Work Package                       | Trọng tâm                    |
| ---- | ---------------------------------- | ---------------------------- |
| WP01 | Environment & Project Setup        | Môi trường coding            |
| WP02 | Repository & Software Architecture | Kiến trúc code               |
| WP03 | Data Pipeline                      | Data ingestion/processing    |
| WP04 | Annotation & Dataset Pipeline      | Dataset/annotation           |
| WP05 | Scene Perception                   | Person/Object/Hand/Tool/Pose |
| WP06 | Tracking & Relationship            | Tracking + relations         |
| WP07 | Action Understanding               | Action recognition           |
| WP08 | Temporal Understanding             | Start/End/Duration/Event     |
| WP09 | Workflow & State Engine            | Process logic                |
| WP10 | Compliance & Anomaly               | Violation detection          |
| WP11 | Evidence & Output                  | Evidence/UI/API/log          |
| WP12 | Evaluation & Benchmark             | Đánh giá                     |
| WP13 | Optimization & Robustness          | Tối ưu                       |
| WP14 | End-to-End Prototype               | Tích hợp                     |
| WP15 | Deployment & Reliability           | Production foundation        |
| WP16 | Documentation & R&D Report         | Tổng hợp                     |
| WP17 | Regression & Final Acceptance      | Nghiệm thu                   |

---

# 2. WP01 — ENVIRONMENT & PROJECT SETUP

## 01.01 — Chuẩn hóa môi trường

[ ] Xác định OS
[ ] Xác định Python version
[ ] Xác định CUDA version
[ ] Xác định PyTorch version
[ ] Xác định GPU
[ ] Xác định OpenCV
[ ] Xác định CV/AI frameworks
[ ] Xác định tracking framework
[ ] Xác định annotation tools

### Phương thức

Khóa environment bằng:

```text
environment.yml
hoặc
requirements.txt
```

### Output

```text
Environment Specification
Reproducible Environment
```

### Acceptance

Một môi trường mới có thể cài đặt và chạy baseline thành công.

---

## 01.02 — GPU/Runtime validation

[ ] Kiểm tra GPU
[ ] CUDA
[ ] Driver
[ ] PyTorch CUDA
[ ] GPU memory
[ ] Inference test
[ ] Benchmark FPS

### Output

```text
GPU Benchmark
Runtime Baseline
```

---

## 01.03 — Project bootstrap

[ ] Tạo repository
[ ] Tạo README
[ ] Tạo `.gitignore`
[ ] Tạo environment
[ ] Tạo config structure
[ ] Tạo logging structure
[ ] Tạo `src/`

### Acceptance

Project chạy được:

```text
python main.py
```

hoặc entrypoint tương đương.

---

# 3. WP02 — REPOSITORY & SOFTWARE ARCHITECTURE

## 02.01 — Folder architecture

```text
human-action/
│
├── configs/
├── data/
├── models/
├── src/
│   ├── perception/
│   ├── tracking/
│   ├── action/
│   ├── temporal/
│   ├── workflow/
│   ├── anomaly/
│   ├── evidence/
│   └── runtime/
│
├── experiments/
├── evaluation/
├── demos/
├── tools/
└── docs/
```

[ ] Tạo structure
[ ] Quy ước naming
[ ] Module boundaries
[ ] Entry points
[ ] Config loading
[ ] Logging

---

## 02.02 — Data model / event schema

Định nghĩa thống nhất:

```python
Observation
Detection
Track
Action
ActionEvent
WorkflowState
Violation
Evidence
```

Ví dụ:

```text
ActionEvent
├── event_id
├── worker_id
├── action
├── object
├── tool
├── zone
├── start_time
├── end_time
└── confidence
```

### Acceptance

Các module truyền dữ liệu cho nhau bằng schema thống nhất.

---

## 02.03 — Configuration architecture

[ ] Camera config
[ ] Model config
[ ] Action config
[ ] Workflow config
[ ] Threshold config
[ ] Runtime config

### Acceptance

Thay đổi workflow/model/threshold không cần sửa source code chính.

---

# 4. WP03 — DATA PIPELINE

## 03.01 — Input

[ ] Video file
[ ] RTSP
[ ] Image sequence
[ ] FPS handling
[ ] Resolution handling
[ ] Timestamp

---

## 03.02 — Frame acquisition

[ ] Frame reader
[ ] Buffer
[ ] Drop-frame strategy
[ ] Reconnect logic
[ ] End-of-stream handling

---

## 03.03 — Preprocessing

[ ] Resize
[ ] Crop
[ ] Normalize
[ ] ROI
[ ] Frame sampling
[ ] Temporal window creation

### Acceptance

```text
Video
→ Clean Frame Stream
```

hoạt động ổn định.

---

# 5. WP04 — DATASET & ANNOTATION PIPELINE

## 04.01 — Dataset organization

[ ] Raw data
[ ] Processed data
[ ] Annotation
[ ] Train
[ ] Validation
[ ] Test

---

## 04.02 — Dataset metadata

[ ] Video ID
[ ] Worker ID
[ ] Session ID
[ ] Camera ID
[ ] Location
[ ] Workflow
[ ] Date/time
[ ] Data version

---

## 04.03 — Annotation

### Spatial

[ ] Person
[ ] Object
[ ] Tool
[ ] Hand
[ ] Zone

### Temporal

[ ] Action start
[ ] Action end

### Semantic

[ ] Action class
[ ] Object
[ ] Tool
[ ] Interaction

### Process

[ ] Workflow
[ ] Step
[ ] Sequence
[ ] Valid branch

### Error

[ ] Wrong order
[ ] Skip
[ ] Repeat
[ ] Unexpected
[ ] Too slow
[ ] Too fast
[ ] Idle
[ ] Timeout
[ ] Incomplete

---

## 04.04 — Dataset QA

[ ] Missing annotation
[ ] Invalid label
[ ] Temporal overlap
[ ] Incorrect class
[ ] Duplicate samples
[ ] Corrupted video
[ ] Class imbalance

### Acceptance

Dataset có thể được load tự động và kiểm tra integrity.

---

# 6. WP05 — SCENE PERCEPTION

# 05.01 Person Detection

[ ] Detector selection
[ ] Baseline model
[ ] Inference
[ ] Confidence threshold
[ ] ROI filtering
[ ] Benchmark

---

# 05.02 Object Detection

[ ] Define object classes
[ ] Dataset preparation
[ ] Baseline training
[ ] Validation
[ ] False-positive analysis

---

# 05.03 Tool Detection

[ ] Tool taxonomy
[ ] Dataset
[ ] Detector
[ ] Validation

---

# 05.04 Hand Perception — Fine-Grained

[ ] Hand detection
[ ] Hand pose nếu cần
[ ] Left/right hand association
[ ] Small-object visibility

---

# 05.05 Pose — Large-Scale

[ ] Pose estimation
[ ] Keypoint quality
[ ] Occlusion handling
[ ] Stability

---

# 05.06 Zone

[ ] ROI definition
[ ] Workspace
[ ] Interaction zone
[ ] Machine zone
[ ] Restricted zone

### CHECKPOINT WP05

Video phải sinh được:

```text
Person
Object
Tool
Hand
Pose
Zone
```

ở mức đủ dùng cho downstream task.

---

# 7. WP06 — TRACKING & RELATIONSHIP

## 06.01 Person Tracking

[ ] Track ID
[ ] Track creation
[ ] Track termination
[ ] ID switch analysis
[ ] Occlusion recovery

---

## 06.02 Object Tracking

[ ] Object ID
[ ] Object trajectory
[ ] State change

---

## 06.03 Human-object relationship

Xử lý:

```text
Near
Contact
Holding
Moving-With
Inside-Zone
Released
```

---

## 06.04 Human-tool relationship

[ ] Worker ↔ Tool
[ ] Tool usage
[ ] Tool release

---

## 06.05 Relationship validation

Ví dụ:

```text
Hand near component
→ Contact
→ Component moves
→ Hand separates
```

→ candidate `PICK`.

### CHECKPOINT WP06

Có thể duy trì:

```text
Worker
+
Object
+
Tool
+
Spatial relation
+
Temporal relation
```

theo thời gian.

---

# 8. WP07 — ACTION UNDERSTANDING

## 07.01 Action taxonomy implementation

[ ] Action dictionary
[ ] Class IDs
[ ] Label mapping
[ ] Unknown class
[ ] Transition class
[ ] Idle class

---

## 07.02 Fine-Grained Actions

[ ] Pick
[ ] Place
[ ] Insert
[ ] Remove
[ ] Press
[ ] Scan
[ ] Tighten
[ ] Inspect
[ ] Other domain-specific actions

---

## 07.03 Large-Scale Actions

[ ] Walk
[ ] Approach
[ ] Enter zone
[ ] Operate
[ ] Open/close
[ ] Maintenance
[ ] Assembly
[ ] Inspect
[ ] Leave zone

---

## 07.04 Baseline models

[ ] Rule-based baseline
[ ] Simple temporal baseline
[ ] Temporal CNN
[ ] MS-TCN++
[ ] ASFormer
[ ] ActionFormer nếu phù hợp

Không bắt buộc triển khai tất cả.

---

## 07.05 Action confidence

[ ] Confidence threshold
[ ] Unknown threshold
[ ] Ambiguous state
[ ] Temporal persistence

---

## 07.06 Action event

Output:

```text
ActionEvent
{
    worker_id,
    action,
    start_time,
    end_time,
    confidence,
    object,
    tool,
    zone
}
```

### CHECKPOINT WP07

Hệ thống chuyển được:

```text
Video
→ Action Events
```

---

# 9. WP08 — TEMPORAL UNDERSTANDING

## 08.01 Action Start Detection

[ ] Start condition
[ ] Temporal confirmation
[ ] Minimum duration

---

## 08.02 Action End Detection

[ ] End condition
[ ] Stable transition
[ ] Overlap handling

---

## 08.03 Duration

[ ] Start timestamp
[ ] End timestamp
[ ] Duration calculation
[ ] Expected range

---

## 08.04 Temporal smoothing

[ ] Flicker reduction
[ ] Majority vote
[ ] Hysteresis
[ ] Debounce
[ ] Minimum action duration

---

## 08.05 Action transition

[ ] Previous action
[ ] Current action
[ ] Next action
[ ] Transition validation

---

## 08.06 Idle / Unknown

[ ] Idle state
[ ] Unknown state
[ ] Occlusion
[ ] Out-of-view

### CHECKPOINT WP08

Có được:

```text
Action Timeline
```

ví dụ:

```text
10:21:03–10:21:05  PICK
10:21:05–10:21:07  PLACE
10:21:08–10:21:10  SCAN
10:21:11–10:21:28  ASSEMBLE
```

---

# 10. WP09 — WORKFLOW & PROCESS STATE ENGINE

## 09.01 Workflow schema

[ ] Step ID
[ ] Action
[ ] Expected object
[ ] Expected tool
[ ] Expected zone
[ ] Duration
[ ] Previous step
[ ] Next step

---

## 09.02 State Machine

[ ] Initial state
[ ] Current state
[ ] Transition
[ ] Completion
[ ] Reset

---

## 09.03 Branch

[ ] Multiple valid paths
[ ] Optional step
[ ] Conditional step

---

## 09.04 Rework

[ ] Return to previous step
[ ] Rework path
[ ] Restart procedure

---

## 09.05 Timeout state

[ ] Step timeout
[ ] Workflow timeout
[ ] Idle timeout

---

## 09.06 Workflow configuration

[ ] Workflow loaded from config
[ ] Multiple workflows
[ ] Workflow selection
[ ] Versioning

### CHECKPOINT WP09

```text
Action Timeline
→ Process State
```

và engine biết:

```text
Expected Step
Current Step
Valid Next Step
```

---

# 11. WP10 — COMPLIANCE & ANOMALY ENGINE

## 10.01 Sequence validation

[ ] Correct sequence
[ ] Wrong sequence
[ ] Skip
[ ] Repeat
[ ] Backward transition
[ ] Unexpected action

---

## 10.02 Duration validation

[ ] Too fast
[ ] Too slow
[ ] Timeout
[ ] Excessive idle

---

## 10.03 Semantic validation

[ ] Wrong object
[ ] Wrong tool
[ ] Wrong zone
[ ] Wrong interaction

---

## 10.04 Completion validation

[ ] Incomplete procedure
[ ] Premature completion
[ ] Abnormal termination

---

## 10.05 Confidence handling

[ ] High-confidence violation
[ ] Low-confidence warning
[ ] Unknown
[ ] Human review flag

---

## 10.06 Multiple-valid-path handling

[ ] Valid branch
[ ] Valid alternative route
[ ] Non-error deviation

### CHECKPOINT WP10

Engine có thể trả:

```text
PASS
WARNING
VIOLATION
```

kèm:

```text
violation_type
expected
observed
reason
timestamp
```

---

# 12. WP11 — EVIDENCE & RESULT OUTPUT

## 11.01 Event logging

[ ] Action event
[ ] Workflow state
[ ] Violation
[ ] Confidence
[ ] Duration

---

## 11.02 Snapshot

[ ] Violation frame
[ ] Before frame
[ ] After frame

---

## 11.03 Video evidence

[ ] Pre-event buffer
[ ] Event clip
[ ] Post-event buffer
[ ] Clip export

---

## 11.04 Structured result

Ví dụ:

```json
{
  "worker_id": "W07",
  "workflow": "ASSEMBLY_A",
  "expected_step": "SCAN",
  "observed_step": "ASSEMBLE",
  "violation": "WRONG_SEQUENCE"
}
```

---

## 11.05 Explainability

[ ] Why
[ ] What happened
[ ] Expected vs observed
[ ] Evidence

### CHECKPOINT WP11

Một người không biết model vẫn có thể hiểu:

> **AI phát hiện lỗi gì và dựa trên bằng chứng nào.**

---

# 13. WP12 — EVALUATION & BENCHMARK

## 12.01 Perception Evaluation

[ ] Detection Precision
[ ] Detection Recall
[ ] F1
[ ] Tracking stability

---

## 12.02 Action Evaluation

[ ] Action Accuracy
[ ] Precision
[ ] Recall
[ ] F1

---

## 12.03 Temporal Evaluation

[ ] Temporal IoU
[ ] Start error
[ ] End error
[ ] Duration error

---

## 12.04 Process Evaluation

[ ] Sequence accuracy
[ ] Skip detection
[ ] Wrong-order detection
[ ] Repeat detection
[ ] Timeout detection
[ ] False alarm
[ ] Miss rate

---

## 12.05 System Evaluation

[ ] FPS
[ ] End-to-end latency
[ ] GPU utilization
[ ] CPU utilization
[ ] RAM/VRAM
[ ] Frame drop
[ ] Stability

---

## 12.06 Scenario-based evaluation

Chạy Golden Scenario:

```text
GS01 Correct
GS02 Wrong Order
GS03 Skip
GS04 Repeat
GS05 Too Slow
GS06 Too Fast
GS07 Idle
GS08 Timeout
GS09 Unexpected
GS10 Wrong Object
GS11 Wrong Zone
GS12 Incomplete
GS13 Valid Branch
GS14 Occlusion
GS15 Multi-worker
```

### CHECKPOINT WP12

Có một:

**Evaluation Report v1**

và có thể trả lời:

> “Hệ thống đang tốt ở đâu và yếu ở đâu?”

---

# 14. WP13 — OPTIMIZATION & ROBUSTNESS

## 13.01 Performance

[ ] Reduce inference latency
[ ] Reduce preprocessing overhead
[ ] Optimize memory
[ ] Batch nếu phù hợp
[ ] Frame skipping nếu phù hợp

---

## 13.02 Accuracy

[ ] Threshold tuning
[ ] Temporal smoothing
[ ] Better features
[ ] Better dataset
[ ] Hard negative mining

---

## 13.03 Robustness

[ ] Lighting variation
[ ] Motion blur
[ ] Occlusion
[ ] Worker variation
[ ] Clothing variation
[ ] Object variation
[ ] Camera variation
[ ] Background variation

---

## 13.04 Generalization

[ ] Cross-worker
[ ] Cross-session
[ ] Cross-location
[ ] Cross-camera

### Không làm mặc định

Không nhảy ngay sang:

```text
Foundation Model
VLM
Large Transformer
Complex multimodal system
```

trừ khi error analysis chứng minh baseline không đủ.

---

# 15. WP14 — END-TO-END PROTOTYPE

## 14.01 Input

[ ] Video file
[ ] RTSP

## 14.02 Pipeline

```text
Capture
→ Perception
→ Tracking
→ Relationship
→ Action
→ Temporal
→ Workflow
→ Anomaly
→ Evidence
```

## 14.03 Runtime

[ ] Stable loop
[ ] Error handling
[ ] Logging
[ ] Config loading
[ ] Camera reconnect

---

## 14.04 UI

Tối thiểu hiển thị:

[ ] Video
[ ] Worker ID
[ ] Current action
[ ] Current step
[ ] Workflow status
[ ] Violation
[ ] Duration
[ ] Confidence

---

## 14.05 API nếu cần

[ ] Current state
[ ] Event
[ ] Violation
[ ] Health status

### CHECKPOINT WP14

Một video thực tế chạy xuyên suốt:

```text
Camera
→ AI
→ Action
→ Workflow
→ Anomaly
→ Evidence
→ UI
```

không cần thao tác thủ công ở giữa.

---

# 16. WP15 — DEPLOYMENT & RELIABILITY

## 15.01 Runtime

[ ] Startup
[ ] Shutdown
[ ] Graceful recovery
[ ] Exception handling
[ ] Watchdog

---

## 15.02 Camera reliability

[ ] Connection loss
[ ] Reconnect
[ ] Empty frame
[ ] FPS degradation

---

## 15.03 Model reliability

[ ] Model load failure
[ ] GPU failure handling
[ ] Inference timeout

---

## 15.04 Data reliability

[ ] Log rotation
[ ] Evidence storage
[ ] Disk full warning
[ ] File corruption handling

---

## 15.05 Configuration

[ ] Model version
[ ] Workflow version
[ ] Config version

### CHECKPOINT WP15

Prototype có thể chạy liên tục trong thời gian kiểm thử định trước mà không cần restart thủ công.

---

# 17. WP16 — DOCUMENTATION & R&D REPORT

## 16.01 Technical Documentation

[ ] Architecture
[ ] Data flow
[ ] Module description
[ ] Config
[ ] Deployment

---

## 16.02 Experiment Documentation

Mỗi experiment ghi:

```text
Experiment ID
Objective
Dataset
Model
Configuration
Hardware
Metric
Result
Failure
Conclusion
```

---

## 16.03 Research findings

[ ] What works
[ ] What does not work
[ ] Why
[ ] Recommended approach

---

## 16.04 Limitations

[ ] Camera limitations
[ ] Dataset limitations
[ ] Model limitations
[ ] Environment limitations
[ ] Workflow limitations

---

## 16.05 Future Work

Chia:

```text
NEXT
OPTIONAL
ADVANCED
```

Không để Future Work phá vỡ Core Scope.

---

# 18. WP17 — REGRESSION TEST & FINAL ACCEPTANCE

## 17.01 Regression

Sau mỗi thay đổi lớn:

[ ] Golden Scenario
[ ] Action benchmark
[ ] Workflow benchmark
[ ] Anomaly benchmark

---

## 17.02 Performance regression

[ ] FPS
[ ] Latency
[ ] GPU
[ ] CPU
[ ] Memory

---

## 17.03 Functional regression

[ ] Detection
[ ] Tracking
[ ] Action
[ ] Temporal
[ ] Workflow
[ ] Anomaly
[ ] Evidence

---

# 19. FINAL ACCEPTANCE CHECKLIST

## CORE FUNCTION

[ ] Person detection
[ ] Tracking
[ ] Object/tool recognition
[ ] Hand/pose khi cần
[ ] Action recognition
[ ] Temporal segmentation/event
[ ] Workflow state
[ ] Sequence validation
[ ] Duration validation
[ ] Anomaly detection
[ ] Evidence

## ANOMALY

[ ] Wrong sequence
[ ] Skip
[ ] Repeat
[ ] Unexpected
[ ] Too slow
[ ] Too fast
[ ] Idle
[ ] Timeout
[ ] Incomplete

## SYSTEM

[ ] Real-time / near-real-time
[ ] Stable
[ ] Recoverable
[ ] Configurable
[ ] Observable
[ ] Reproducible

## DOCUMENT

[ ] Architecture
[ ] Dataset
[ ] Annotation
[ ] Experiment
[ ] Evaluation
[ ] Limitations
[ ] Deployment

---

# 20. MASTER PROGRESS REPORT TABLE

Đây là bảng bạn có thể dùng trực tiếp để cập nhật tiến độ.

| ID      | Work Package | Task              | Method / Approach  | Output         | Status | Progress | Evidence   | Result / Issue   | Next Action   |
| ------- | ------------ | ----------------- | ------------------ | -------------- | ------ | -------: | ---------- | ---------------- | ------------- |
| WP01.01 | Environment  | Python/CUDA setup | Miniconda          | Environment    | PASS   |     100% | Commit/Env | Stable           | —             |
| WP02.01 | Architecture | Module structure  | Modular            | Repo structure | IP     |      70% | Commit     | Workflow pending | Complete      |
| WP03.01 | Data         | RTSP reader       | OpenCV             | Frame stream   | NS     |       0% | —          | —                | Implement     |
| WP05.01 | Perception   | Person detection  | YOLO               | Detector       | RD     |      50% | EXP-001    | FPS issue        | Optimize      |
| WP06.01 | Tracking     | Person tracking   | Tracker X          | Track          | NS     |       0% | —          | —                | Implement     |
| WP07.01 | Action       | Pick/Place        | Temporal baseline  | Action model   | NS     |       0% | —          | —                | Prepare data  |
| WP08.01 | Temporal     | Start/end         | Temporal smoothing | Event          | NS     |       0% | —          | —                | Implement     |
| WP09.01 | Workflow     | Assembly A        | FSM                | State engine   | NS     |       0% | —          | —                | Define schema |
| WP10.01 | Anomaly      | Wrong order       | State transition   | Violation      | NS     |       0% | —          | —                | Implement     |
| WP11.01 | Evidence     | Snapshot          | Buffer             | Evidence       | NS     |       0% | —          | —                | Implement     |
| WP12.01 | Evaluation   | Baseline          | Golden set         | Report         | NS     |       0% | —          | —                | Prepare       |
| WP14.01 | Prototype    | Full pipeline     | End-to-end         | Demo           | NS     |       0% | —          | —                | —             |
| WP15.01 | Deployment   | Recovery          | Watchdog           | Stable runtime | NS     |       0% | —          | —                | —             |
| WP17.01 | Acceptance   | Final test        | Golden scenarios   | Sign-off       | NS     |       0% | —          | —                | —             |

---

# 21. PROGRESS WEIGHTING

Để báo cáo tổng thể không bị “ảo” do hoàn thành nhiều task nhỏ, dùng trọng số theo Work Package.

| WP                      | Weight |
| ----------------------- | -----: |
| WP01 Environment        |     5% |
| WP02 Architecture       |     5% |
| WP03 Data Pipeline      |     7% |
| WP04 Dataset/Annotation |    10% |
| WP05 Perception         |    10% |
| WP06 Tracking/Relations |     8% |
| WP07 Action             |    12% |
| WP08 Temporal           |    10% |
| WP09 Workflow           |    10% |
| WP10 Anomaly            |     8% |
| WP11 Evidence           |     4% |
| WP12 Evaluation         |     5% |
| WP13 Optimization       |     2% |
| WP14 Prototype          |     2% |
| WP15 Deployment         |     1% |
| WP16 Documentation      |     1% |
| WP17 Acceptance         |    0%* |

`*` Acceptance là Gate cuối; không tính vào progress kỹ thuật để tránh hệ thống đạt 100% trước khi nghiệm thu.

### Công thức

```text
Overall Progress
=
Σ (WP Progress × WP Weight)
```

Ví dụ:

```text
WP05 = 80%
Weight = 10%

Contribution = 80 × 10% = 8%
```

---

# 22. WEEKLY R&D PROGRESS REPORT

Mỗi tuần chỉ cần cập nhật 6 phần:

## 22.1 Completed

```text
- Những task đã PASS
- Experiment đã hoàn thành
```

## 22.2 In Progress

```text
- Task đang thực hiện
- Progress
```

## 22.3 Research Findings

```text
- Phát hiện quan trọng
- Model/approach hoạt động tốt/xấu
```

## 22.4 Problems / Risks

```text
- Issue
- Root cause
- Impact
```

## 22.5 Next Actions

```text
- 3–5 công việc ưu tiên tiếp theo
```

## 22.6 Overall Status

```text
Overall Progress: XX%

Schedule:
GREEN / YELLOW / RED

Technical:
GREEN / YELLOW / RED

Data:
GREEN / YELLOW / RED

Integration:
GREEN / YELLOW / RED
```

---

# 23. R&D DECISION LOG

Mỗi quyết định kỹ thuật quan trọng ghi:

| Decision ID | Decision                 | Alternatives     | Evidence | Reason                 | Status   |
| ----------- | ------------------------ | ---------------- | -------- | ---------------------- | -------- |
| DEC-001     | Use FSM                  | Learned workflow | EXP-003  | Workflow predefined    | Accepted |
| DEC-002     | Use hand-object relation | Pose-only        | EXP-005  | Better Pick/Place      | Accepted |
| DEC-003     | Use ASFormer             | MS-TCN++         | EXP-008  | Better temporal result | Pending  |

---

# 24. EXPERIMENT TRACKING

Mỗi experiment:

```text
EXP-ID
│
├── Question
├── Hypothesis
├── Dataset Version
├── Code Version
├── Model
├── Configuration
├── Hardware
├── Metrics
├── Result
├── Failure Cases
└── Conclusion
```

### Kết luận bắt buộc:

```text
KEEP
CHANGE
DROP
```

---

# 25. BUG / ISSUE TRACKING

| ID      | Issue         | Component | Severity | Root Cause               | Action          | Status |
| ------- | ------------- | --------- | -------- | ------------------------ | --------------- | ------ |
| BUG-001 | ID switch     | Tracking  | High     | Occlusion                | Improve tracker | IP     |
| BUG-002 | Pick flicker  | Action    | Medium   | Short temporal window    | Smoothing       | PASS   |
| BUG-003 | False timeout | Workflow  | High     | Wrong duration threshold | Recalibrate     | IP     |

Severity:

```text
Critical
High
Medium
Low
```

---

# 26. CHECKPOINT GATES

## G1 — Foundation

```text
Environment
+
Repo
+
Config
+
Data schema
```

## G2 — Perception

```text
Person
+
Object
+
Tracking
```

## G3 — Action

```text
Action
+
Start/End
+
Timeline
```

## G4 — Process

```text
Workflow
+
State
+
Transition
```

## G5 — Compliance

```text
Anomaly
+
Evidence
```

## G6 — Prototype

```text
End-to-End
```

## G7 — Validation

```text
Golden Scenario
+
Metrics
```

## G8 — Deployment

```text
Stable
+
Recoverable
+
Documented
```

---

# 27. FINAL PROJECT STATUS

Cuối mỗi tuần/tháng, dashboard tiến độ chỉ cần:

```text
HUMAN ACTION R&D

Overall Progress: XX%

Foundation             ██████████ 100%
Data                   ██████░░░░  60%
Perception             ███████░░░  70%
Action                 ████░░░░░░  40%
Temporal               ██░░░░░░░░  20%
Workflow               ██░░░░░░░░  20%
Anomaly                ░░░░░░░░░░   0%
Evidence               ░░░░░░░░░░   0%
Evaluation             ░░░░░░░░░░   0%
Prototype              ░░░░░░░░░░   0%
Deployment             ░░░░░░░░░░   0%

Current Gate:
G1 — Foundation

Current Focus:
Data + Perception

Main Risk:
Action boundary ambiguity

Next Milestone:
Generate first stable Action Event stream
```

---

# 28. DEFINITION OF COMPLETE PROJECT

Dự án Core được hoàn thành khi:

```text
VIDEO
  ↓
FRAME
  ↓
PERSON / OBJECT / HAND / TOOL
  ↓
TRACKING
  ↓
ACTION
  ↓
TEMPORAL EVENT
  ↓
WORKFLOW STATE
  ↓
COMPLIANCE
  ↓
ANOMALY
  ↓
EVIDENCE
```

hoạt động end-to-end và vượt qua:

```text
Golden Scenario Set
+
AI Evaluation
+
Process Evaluation
+
Runtime Evaluation
```

trên ít nhất:

```text
1 Fine-Grained / Small-FOV use case
+
1 Large-Scale / Large-FOV use case
```

---

# 29. NGUYÊN TẮC QUẢN LÝ TIẾN ĐỘ

1. Không đánh dấu `PASS` khi chỉ code xong; phải có evidence.

2. Không đánh dấu `100%` khi chưa validation.

3. Không tăng scope chỉ vì phát hiện một paper/model mới.

4. Một research idea mới phải đi qua:

```text
Question
→ Experiment
→ Evidence
→ Decision
```

5. Một module chỉ được nâng complexity khi baseline hiện tại không đáp ứng KPI.

6. Mọi thay đổi kiến trúc phải được ghi trong Decision Log.

7. Mọi model phải gắn với Dataset Version + Experiment ID.

8. Mọi anomaly quan trọng phải có Evidence.

9. Mọi release prototype phải chạy Regression Test.

10. **Process KPI là tiêu chí cuối cùng; model KPI chỉ là phương tiện.**

---

# 30. PROJECT EXECUTION LOOP

Toàn bộ coding/R&D của dự án được vận hành theo vòng lặp:

```text
                    RESEARCH QUESTION
                           ↓
                      REQUIREMENT
                           ↓
                         DATA
                           ↓
                        BASELINE
                           ↓
                       EXPERIMENT
                           ↓
                       EVALUATION
                           ↓
                    ERROR ANALYSIS
                           ↓
                ┌──────────┴──────────┐
                ↓                     ↓
             SUCCESS                FAILURE
                ↓                     ↓
             KEEP                  MODIFY
                ↓                     ↓
          INTEGRATE              EXPERIMENT AGAIN
                │                     │
                └──────────┬──────────┘
                           ↓
                      VALIDATION
                           ↓
                      PROTOTYPE
                           ↓
                     REGRESSION
                           ↓
                       RELEASE
```

Đây là vòng lặp chính xuyên suốt toàn bộ Human Action R&D.

---

# 31. RESEARCH CORPUS IMMERSION — DEEP RESEARCH PASS

## Quy ước trạng thái của corpus

- `NS` — Chưa bắt đầu kiểm chứng sâu; chỉ có inventory/source locator thì chưa tính là đã đọc.
- `IP` — Đang đọc/đối chiếu nguồn và implementation.
- `PARTIAL` — Có phân tích nhưng còn thiếu một hoặc nhiều evidence bắt buộc.
- `VERIFIED` — Đã đọc paper, kiểm tra implementation liên quan, dataset/annotation, method/temporal/evaluation, limitations, reuse và evidence; **không đồng nghĩa đã reproduce kết quả**.
- `BLOCKED` — Nguồn trọng yếu không truy cập được sau khi thử các nguồn chính thức có thể có.

## Corpus checklist

| # | Research | Paper | Official implementation | Dataset / annotation | Method / temporal / evaluation | Limitations / reuse | EXPERIENCE.md | Status | Evidence / next action |
|--:|---|---|---|---|---|---|---|---|---|
| 01 | IMPACT | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Paper §§3–6; cloned official `code/IMPACT`; task wrappers, configs, split assets, MS-TCN++ PSR graph path inspected. Benchmark not rerun; raw media not downloaded. |
| 02 | IndustReal | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | arXiv full text + local 6-page WACV supplement; cloned official code; AR/ASD/PSR loaders, configs, model training and metrics inspected. Data portal 403; archive/license not verified; benchmark not rerun. |
| 03 | Assembly101 | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | CVPR paper + full supplement read; official annotations, TSM/MS-G3D recognition, C2F-TCN segmentation and mistake-label repos cloned/inspected. Raw archive/features and benchmark not downloaded/run; current release completeness/license use terms remain unverified. |
| 04 | Every Mistake Counts in Assembly | [x] | [ ] | [x] | [x] | [x] | [x] | PARTIAL | 2023 arXiv paper + expanded 2025 CVIU journal paper read; official 328-sequence annotation repo inspected (in `03_Assembly101/code/assembly101-mistake-detection`). Journal adds 20-sequence symbolic HA4M-EGT test and TSM verb/GT-parts integration; no official model/source implementation found, so implementation/reproduction remain NOT VERIFIED. |
| 05 | HA4M | [x] | [x] | [x] | [x] | [x] | [x] | PARTIAL | Full Scientific Data paper read; official Azure Kinect acquisition GUI and HA4Mfeatures repo cloned/inspected. 2025 segmentation follow-up read; no model code in feature repo. 4.1 TB release/full annotation files not downloaded, dataset GitLab checkout invalid, license/release mapping NOT VERIFIED. |
| 06 | MS-TCN / MS-TCN++ | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | CVPR 2019 paper + full method/results inspected; 2020 TPAMI/arXiv ++ paper read; both author repos cloned, model/loader/train/predict/eval inspected. Paper/code schedule and parameter-sharing caveats recorded; benchmark not run. |
| 07 | ASFormer | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full BMVC 2021 paper and official repo inspected (model, loader, train, inference, evaluation). Paper/code discrepancies and README-documented attention-mask indexing issue recorded; no source change or benchmark run. `07_ASFormer/EXPERIENCE.md`. |
| 08 | ActionFormer | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full ECCV/arXiv v2 paper + appendices; cloned authors' upstream and listed fork. Inspected loaders/model/train/eval/NMS/config and ERROR adaptation; its `has_error` field is dropped from model targets. No dataset feature bundle downloaded and no reproduction run. `08_ActionFormer/EXPERIENCE.md`. |
| 09 | IKEA ASM | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full WACV/arXiv v2 paper incl. localization appendix; official project/repo and action, pose, tracking code inspected; segmentation train/eval source verified on GitHub. Captured sparse-GT/pseudo-GT limitations, modality fusion, benchmark metrics and license. Full data/checkpoints not downloaded or reproduced. `09_IKEA ASM/EXPERIENCE.md`. |
| 10 | HoloAssist | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full ICCV/arXiv paper + supplement; official annotation guide/project page and cloned benchmark inspected (loaders, TimeSformer/Seq2Seq, configs/train/test). Paper/code release discrepancy and explicitly unsupported mistake training path recorded. Data/checkpoints not downloaded or reproduced. `10_HoloAssist/EXPERIENCE.md`. |
| 11 | EPIC-KITCHENS | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full IJCV/arXiv paper + appendices, official annotation schema/splits and baseline repositories inspected. Cloned C1 TSN/TRN/TSM and C2 BMN+SlowFast detection/evaluator; test-of-time, missing timestamps, noisy auto spatial labels and limits recorded. Raw media/features not downloaded or reproduced. `11_EPIC-KITCHENS/EXPERIENCE.md`. |
| 12 | COIN | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Author arXiv full text + supplemental content read; official COIN annotation, TC/OD code and annotation tool cloned/inspected; SSN/R-C3D baseline code traced. Raw videos not downloaded; benchmark not rerun. `12_COIN/EXPERIENCE.md`. |
| 13 | CrossTask | [x] | [x] | [x] | [x] | [x] | [x] | VERIFIED | Full author-hosted CVPR paper read after CVF PDF 403; official repo cloned and model/data/train/DP/config/eval inspected. Raw features/videos not fetched; training not rerun. `13_CrossTask/EXPERIENCE.md`. |
| 14 | FineGym | [x] | [ ] | [x] | [x] | [x] | [x] | PARTIAL | Full arXiv paper + official 13-page supplement read; project annotation schema and author GitHub repo inspected/cloned. Official repo has feature/model-zoo assets but no train/infer/eval code; reproduction implementation NOT VERIFIED. `14_FineGym/EXPERIENCE.md`. |
| 15 | Mistake Analysis review | [x] | N/A | [x] | [x] | [x] | [x] | PARTIAL | Full arXiv v2 review read. Secondary-source taxonomy/method families/evaluation extracted; no implementation is proposed (N/A). Not all cited primary papers were re-audited; publication status beyond arXiv NOT VERIFIED. `15_Mistake Analysis/EXPERIENCE.md`. |
| 16 | FIELDS | [ ] | [x] | [ ] | [x] | [x] | [x] | PARTIAL | Official public repository and project supplement inspected: BLIP-2→MS-TCN inference, sequence matching, UI score/data flow. Publisher/author full paper inaccessible; dataset protocol, numeric results, training details NOT VERIFIED. `16_FIELDS/EXPERIENCE.md`. |

## Corpus completion snapshot

**Last updated:** 2026-09-25

- Deep-read and implementation-checked: **12 / 16** (FIELDS code inspected, but full paper unavailable; Mistake Analysis is a secondary review with no implementation)
- `VERIFIED`: **11**
- `PARTIAL`: **5**
- `BLOCKED`: **0**
- `NS`: **0**
- `EXPERIENCE.md`: **16 / 16**
- `ResearchMatrix.md`: **DONE**
- `ResearchSynthesis.md`: **DONE**
- Overall corpus state: **PASS WITH PARTIAL EVIDENCE — all 16 have reports, but five remain PARTIAL and the corpus is not fully verified/reproduced.**

## Confirmed source-access issue

- Initial clone using the bundled Git runtime failed because its HTTPS remote helper was unavailable. System Git then failed to connect to GitHub in the sandbox. After the required network escalation approval, the official IMPACT repository cloned successfully.
- Existing local corpus audit found the source-list document and two saved papers, an IndustReal supplementary/video package, and a bundle of HA4M-related PDFs. The other research folders did not contain source files at audit time. This is inventory only, not evidence that the corresponding work is unavailable online.
- The official 4TU IndustReal data portal returned 403 to the research browser. Paper, local supplementary and official repo were accessible, so the paper understanding is verified; direct release archive/license inspection remains open.
- For HA4M, the primary paper, official acquisition GUI and official feature/split repo were accessible and inspected. Full raw data (4.1 TB reported by the paper) was not downloaded. The official HA4M dataset GitLab clone did not produce a valid `HEAD`; exact raw-release license/version alignment is therefore **NOT VERIFIED**. This is a partial corpus item, not a blocker to reading other sources.
- For IKEA ASM, the official dataset repository contains deeply nested Detectron2 build paths that exceed Windows checkout path limits. A sparse checkout of action, pose, tracking and toolbox code succeeded; official instance-segmentation README/train/eval files were inspected on GitHub. The ~240 GB dataset and pretrained bundles were not downloaded.
- For Mistake Analysis, the full arXiv v2 review was read. It is a secondary source without a proposed implementation; underlying cited works not independently inspected remain outside its VERIFIED evidence. Peer-reviewed publication status beyond the arXiv record is NOT VERIFIED.
- For FIELDS, the official public repository and official project page were inspected, including model, worker, sequence alignment, score/UI, and system flow. The publisher full-text page and official author manuscript could not be retrieved (HTTP/access failures); detailed study protocol, numerical results, and training evidence remain NOT VERIFIED. Code was not run; academic-use restriction is recorded from the repository.

## Per-research acceptance checklist

Only check a paper row when the corresponding source was actually inspected. A paper is `VERIFIED` only after every required cell above is checked and `EXPERIENCE.md` records source references. A source that cannot be reached must be explicitly recorded as `NOT VERIFIED` / `PARTIALLY VERIFIED` in its experience report and the row remains `PARTIAL` or `BLOCKED`.

```text
[ ] Official paper read
[ ] Relevant implementation inspected (entry, loader, model, train/inference, eval, config)
[ ] Dataset understood
[ ] Annotation understood
[ ] Method reconstructed
[ ] Temporal handling understood
[ ] Evaluation and reported results understood
[ ] Failure cases / limitations identified
[ ] Reusable and non-reusable ideas decided
[ ] Evidence references recorded
[ ] EXPERIENCE.md created
```

The research-immersion scope above describes the completed preparation phase. Implementation is now authorized under CP01; this historical note does not restrict the current implementation phase.

---

# 32. IMPLEMENTATION PHASE — CP01

**Checkpoint:** EXP-CP01 — first executable video/action/workflow/evidence slice  
**Status:** PARTIAL — integrated execution verified, recognition/workflow validity not accepted  
**Last updated:** 2026-09-25

| Work item | Status | Evidence / result |
|---|---|---|
| Repo foundation, requirements, config, ignore rules | PASS | `src/`, `configs/cp01.yaml`, `requirements.txt`, `.gitignore`, `README.md` |
| IMPACT sample data load, TAS-S annotation mapping, splits | PASS WITH LIMITATION | Official v1.1 sample archive SHA-256 verified; 3 videos; one execution per split |
| Frame feature extraction and cache | PASS | Deterministic 283-D RGB/HSV/motion features at 5 FPS; cached under ignored processed data |
| Framewise reference + MS-TCN training/checkpoints | PASS (execution only) | Both models trained 8 epochs on CPU; run record in `results/cp01/training_report.json` |
| Action evaluation / GT vs predicted visualization | FAIL (quality gate) | Test framewise accuracy 0.0310, macro-F1 0.0015, segment F1@10/25/50 = 0; MS-TCN action metrics = 0 |
| Temporal decoding and action events | PASS (logic/execution) | `src/human_action/temporal.py`; decoder tests and end-to-end JSON |
| Workflow transitions and anomaly logic | PASS (deterministic logic) / PARTIAL (dataset integration) | Tests cover valid path, skip, order, repeat, duration and incomplete process; configured route does not faithfully encode repeated component operations |
| Structured evidence frames/clips | PASS (execution) | Demo wrote snapshots/clips linked to violation results; no evidence platform or retention layer |
| Process anomaly precision/recall | NOT EVALUATED | Pilot annotations have no ground-truth procedure violation labels |
| End-to-end command | PASS (execution path only) | `run_pipeline.py` emitted result JSON, events, violations and timeline for held-out video; recognition output was poor |
| Tests | PASS | `python -m unittest discover -s tests -v` — 12 deterministic tests |
| Experiment record | PASS | `experiments/EXP-CP01.md` |

## CP01 acceptance summary

- Data, training, temporal decoding, workflow decision code, evidence export and evaluation artifacts execute.
- CP01 is **not accepted as an action-recognition or compliance baseline**: held-out action metrics fail, the workflow route is illustrative, and anomaly precision/recall cannot be measured without violation labels.
- Next: align splits to one procedure and multiple executions/workers, preserve fine-grained step labels, encode repeated workflow cycles, then rerun the same baseline and process-level tests on labeled deviations.

---

# 33. IMPLEMENTATION PHASE — CP01.1

**Checkpoint:** EXP-CP01.1 — same-procedure data readiness and baseline validation  
**Status:** PARTIAL — official same-procedure S2 split and annotation QA are verified; model retraining is blocked because the official I3D feature bundle could not be downloaded, and real workflow policy awaits process-owner review.  
**Last updated:** 2026-09-26

| Work item | Status | Evidence / result |
|---|---|---|
| CP01 code/data audit | PASS | Existing dataset parser, CP01 model heads, evaluation, workflow, evidence, tests and artifacts inspected. |
| Same-procedure split | PASS | IMPACT TAS-S S2 split 2, Disassembly_A/front; 39 train / 5 validation / 4 test; execution-disjoint and held-out test worker. |
| Dataset inventory and annotations | PASS (structural) | Official v1.1 archive; 112/112 JSON annotation records pass interval/class/coverage QA; 48 target executions retained. |
| Source footage quality | NOT VERIFIED | Only 2/48 target videos exist in sample bundle; blur/occlusion/view judged manually is pending. |
| PPR annotation inspection | PASS (separate target) | Per-hand NORMAL/ANOMALY/RECOVERY labels validate, but are not workflow violations and are not used as such. |
| Target action vocabulary | PASS | All observed Disassembly_A labels and NULL included, including the three RETRIEVE_LOCKING_LEVER_ASSEMBLY annotations. |
| Official I3D features | BLOCKED | Expected 16.9 GB archive absent after two official download attempts; no local feature archive to train against. Expected SHA-256 is recorded in EXP-CP01.1. |
| Framewise/MS-TCN retraining | NOT RUN | Correctly withheld because complete official train/validation/test features are unavailable. No CP01.1 checkpoint/results claimed. |
| Real Disassembly A workflow | HUMAN REVIEW REQUIRED | No approved SOP/policy in repository. Workflow disabled; exact human handoff at `HUMAN_HANDOFF.md`. |
| Process anomaly evaluation | NOT EVALUATED | No matching violation ground truth; TAS-S and PPR targets are not substituted. |
| Ground-truth timeline | PASS | Five SVG timelines generated for one validation and four held-out test executions. |
| Deterministic test suite | PASS | `python -m unittest discover -s tests -v` — 19 tests passed. |
| Experiment record | PASS | `experiments/EXP-CP01.1.md`; explicitly records what did not run and exact resume path. |

## CP01.1 acceptance summary

- The prior cross-procedure split defect is resolved with a real official same-procedure, same-vocabulary, cross-subject protocol.
- Annotation structure and split integrity are verified; footage quality and operational procedure semantics are not.
- CP01.1 is **not accepted as a retrained action or compliance baseline**. Feature download prevented model training/evaluation; workflow ground truth awaits the process owner.
- Resume with the archived I3D features, train both existing models on S2, inspect all four test timelines, and separately integrate only an approved SOP.

---

# 34. IMPLEMENTATION PHASE — CP02

**Checkpoint:** EXP-CP02 — validated action baseline and procedure grounding  
**Status:** PARTIAL — official same-procedure protocol, annotation QA and all locally available sample input are validated; complete feature acquisition and process-owner SOP remain unresolved. No CP02 model training/test metrics are claimed.  
**Last updated:** 2026-09-26

| Work item | Status | Evidence / result |
|---|---|---|
| CP01/CP01.1 audit | PASS | Config, loader, baselines, evaluation, workflow, evidence tests and experiment artifacts inspected. |
| Official S2 protocol | PASS | Disassembly_A/front; 39/5/4; execution-disjoint; test worker held out. |
| Annotation/action vocabulary | PASS (structural) | 48/48 target JSON records pass; 17 observed labels plus NULL frozen; uppercase internal mapping is identity. |
| Input availability | INCOMPLETE | `tools/cp02_preflight.py`: 48/48 annotations; 2/48 I3D feature arrays; 2/48 source videos. Both local videos fully decode and match annotation frame count at 30 FPS, 1280×720. |
| Official feature retrieval | HUMAN HANDOFF | Three HF I3D attempts across CP01.1/CP02 and one smaller official MViTv2 attempt produced no verifiable archive. Official I3D bundle size/checksum and mirror download/verification instructions in `HUMAN_HANDOFF_CP02.md`. |
| Official extraction fallback | ASSESSED, NOT EXECUTABLE HERE | Extractor exists; depends on external I3D code/pretrained weights and CUDA; this host has CPU-only PyTorch and insufficient volume for full raw front-video archive. |
| Framewise/MS-TCN training | NOT RUN | 46/48 input feature sequences missing; no checkpoints/metrics created. |
| Validation/test action evaluation | NOT EVALUATED | No CP02 model. Test evaluation is now separable/deferred to prevent test use during model selection. |
| Procedure SOP | HUMAN REVIEW REQUIRED | Current workflow disabled; process owner template and request in `HUMAN_HANDOFF_CP02.md`. |
| Process anomaly data | PARTIAL | Official PPR-L/R NORMAL/ANOMALY/RECOVERY labels exist, but do not represent workflow skip/order/repeat/timeout truth; compliance metrics remain NOT EVALUATED. |
| Evidence / inference integration | NOT RUN | Synthetic evidence unit test passes; no model-generated CP02 prediction or test-source evidence. |
| Runtime | NOT MEASURED | No CP02 model; evaluation path records future offline whole-sequence timing. CUDA unavailable; memory not instrumented. |
| Workflow logic tests | PASS | 24 synthetic deterministic tests pass, including branch, explicit rework, skip, repeat, wrong order, unexpected, duration, reset, incomplete and workflow metadata/transition validation. |
| CP02 records / handoffs | PASS | `experiments/EXP-CP02.md`, `experiments/CP02/data_readiness.json`, `HUMAN_HANDOFF_CP02.md`. |

## CP02 acceptance summary

- Same-procedure split integrity and all target annotation structures are verified. The two available sample features/videos are also shape/alignment/decode checked.
- CP02 remains **not accepted as a validated action or procedure baseline**: full protocol features are not available, models were not trained, and no approved SOP is present.
- The dominant immediate blocker is data access; the separate compliance blocker is procedure policy. Resume with the exact source/checksum steps in `HUMAN_HANDOFF_CP02.md`, then train/evaluate before drawing a model decision.

---

# 35. IMPLEMENTATION PHASE — CP03

**Checkpoint:** EXP-CP03 — first validated action baseline and procedure grounding  
**Status:** PARTIAL — official split and annotation QA pass, but only 2/48 feature sequences and 2/48 videos are present; no process-owner-approved SOP is available. Training, final action evaluation, model-to-workflow integration, and real process evaluation were not run.  
**Last updated:** 2026-09-26

| Work item | Status | Evidence / result |
|---|---|---|
| Existing experiment/code audit | PASS | CP01, CP01.1, CP02 experiment records; config, loader, models, training/evaluation and workflow implementation inspected. |
| Official data protocol | PASS | S2 split 2; Disassembly_A/front; 39/5/4, execution-disjoint, held-out test worker as recorded in the official split. |
| Current data preflight | PASS / INCOMPLETE | `experiments/CP03_data_readiness.json`: split PASS, annotations PASS (48/48), features 2/48, videos 2/48. |
| Feature artifact | HUMAN HANDOFF | Official I3D archive absent; 46 sequences missing. Exact source, expected checksum, location, verification command and resume commands are in `HUMAN_HANDOFF_CP02.md`. |
| Full video QA | INCOMPLETE | Two train-side videos decode/alignment pass; 46 videos unavailable locally, including all held-out test executions. |
| Framewise/MS-TCN training | NOT RUN | No valid full-protocol training input; no checkpoints or model metrics claimed. |
| Action / temporal / per-class evaluation | NOT EVALUATED | No trained checkpoints and no final test run. |
| Procedure SOP | HUMAN REVIEW REQUIRED | `configs/workflows/disassembly_A.yaml` not supplied; workflow stays disabled. See `HUMAN_HANDOFF_CP02.md`. |
| Real process evaluation | NOT EVALUATED | PPR NORMAL/ANOMALY/RECOVERY is a different target; no reviewed workflow-deviation ground truth. |
| Actual model evidence / runtime | NOT RUN / NOT MEASURED | No genuine model inference on test video; no inference FPS/latency/memory result. |
| Deterministic tests | PASS | `.venv\\Scripts\\python.exe -m unittest discover -s tests -v` — 24 passed. Tests are logic/unit evidence, not process benchmark. |
| Experiment record | PASS | `experiments/EXP-CP03.md` separates verified execution, non-verified items, non-evaluated metrics, and human dependencies. |

## CP03 acceptance summary

- CP03 did not establish a validated action baseline: missing official feature sequences prevent both retained baselines from training on the protocol; no result supports a model-quality conclusion.
- Two independent human dependencies remain: official full feature acquisition and process-owner SOP approval. Real process metrics additionally require reviewed deviation labels.
- Evidence supports conclusion **F — system cannot yet be evaluated reliably**. Main immediate bottleneck is data/feature availability; the separate compliance bottleneck is workflow grounding. Do not escalate model complexity.
- Next direction: **Improve Data**. Resume with the exact verification steps in `HUMAN_HANDOFF_CP02.md`, then run training/evaluation only after 48/48 features pass preflight.

---

# 36. IMPLEMENTATION PHASE — CP04

**Checkpoint:** EXP-CP04 — official data recovery, benchmark alignment and first real baseline  
**Status:** PARTIAL — current audit reconfirmed 2/48 features, 2/48 videos, CPU-only runtime and no approved SOP. No CP04 training/evaluation or model-to-workflow run occurred.  
**Last updated:** 2026-09-26

| Work item | Status | Evidence / result |
|---|---|---|
| Project and prior checkpoint audit | PASS | Relevant project docs and EXP-CP01 through EXP-CP03 reviewed; existing model checkpoints identified as invalid CP01 smoke-test artifacts, not reused. |
| Official acquisition routes | PARTIAL / HUMAN HANDOFF | Official downloader, release docs and archive list inspected; HF retries are documented from prior checkpoint; Drive URL inaccessible to web reader. Exact artifact handoff in `HUMAN_HANDOFF_CP04.md`. |
| Feature readiness | INCOMPLETE | Fresh preflight: 2/48 features; 46 missing. Official I3D archive (15.7 GiB, published SHA-256 in EXP-CP04) absent. |
| Official TAS-S protocol alignment | PASS (documented boundary) | Official TAS-S methods/metrics recorded. Current 48-item Disassembly_A/front selection is a procedure-filtered subset of official S2, not full benchmark evaluation. |
| Official benchmark reproduction | NOT RUN | Official TAS-S lists LTContext, ASQuery, DiffAct, FACT. Our MS-TCN is explicitly “our temporal baseline on IMPACT”; no official reproduction claim. |
| GPU/extractor audit | PASS | CPU-only PyTorch 2.14.0, CUDA false, zero devices, `nvidia-smi` unavailable. Official I3D extractor calls CUDA; extraction not reproduced. |
| Framewise/our MS-TCN training | NOT RUN | Full valid feature set unavailable. CP01 smoke checkpoints excluded. |
| Action and temporal evaluation | NOT EVALUATED | No CP04 training/checkpoint; no test result or timeline generated. |
| SOP/workflow | HUMAN REVIEW REQUIRED | No approved SOP. `HUMAN_HANDOFF_CP04.md` supplies exact template and validation/resume expectations. |
| Real process metrics/evidence | NOT EVALUATED / NOT RUN | No validated workflow ground truth or genuine model inference evidence. |
| Deterministic tests | PASS | 24 `unittest` tests pass; CP04 made no code changes. |
| Experiment/handoff | PASS | `experiments/EXP-CP04.md`, `HUMAN_HANDOFF_CP04.md`, and `experiments/CP04_data_readiness.json`. |

## CP04 acceptance summary

- The official acquisition and benchmark boundary are now recorded, but the full input artifact and process-owner policy remain unavailable. The direct I3D archive is large relative to current free space; the official extraction path requires CUDA absent on this laptop.
- No training or evaluation result is claimed. The project cannot yet be evaluated reliably (decision F); there is no evidence that the model itself is the bottleneck.
- Resume from the CP04 feature handoff and require 48/48 feature QA before training. Keep workflow disabled until the SOP passes validation. If CPU training is not practical after data arrives, execute the retained baselines on the planned RTX 5060 machine.




# 37. IMPLEMENTATION PHASE — CP05

**Checkpoint:** EXP-CP05 — validated IMPACT front-view action baseline and procedure grounding  
**Status:** PARTIAL (historical CP05 status) — both action baselines trained/evaluated; workflow semantics were human-dependent. The ZIP was absent at CP05 time but verified in CP06.  
**Last updated:** 2026-09-27

| Work item | Status | Evidence / result |
|---|---|---|
| Context recovery | PASS | `experiments/CP05/CP05_context_recovery.md`; read repository direction, prior checkpoints, source/config/tools/models/tests and actual nested research corpus paths. |
| Dataset inventory | PASS with provenance caveat | `experiments/CP05/CP05_dataset_audit.md`; extracted annotations, 560 I3D arrays, 112 front + 112 top videos, depth, eye tracking and sample inventoried. Raw dataset remains external. |
| Archive integrity at CP05 | NOT VERIFIED THEN; RESOLVED IN CP06 | ZIP absent during CP05. CP06 later verified SHA-256 against release manifest and official ZIP structure/CRC; see `experiments/CP06/CP06_context_and_audit.md`. |
| S2 data readiness | PASS | `experiments/CP05_data_readiness.json`: 48/48 annotations, 48/48 finite frame-aligned 1024-D features, 48/48 front videos fully decoded; video metadata/frame counts align exactly with annotations. |
| Frozen protocol | PASS (research subset) | IMPACT v1.1 TAS-S S2 split2, Disassembly_A/front, 39/5/4, execution-disjoint, held-out worker SS07EL13. Not an official leaderboard reproduction. |
| Environment | PASS | Python 3.12.14; PyTorch 2.14.0+cu132; CUDA 13.2; RTX 5060 Ti / 16 GiB; driver 596.21; OpenCV 4.14.0. Rebuilt `.venv-cp05`; inherited `.venv` fails to launch. |
| FramewiseBaseline | PASS | 12 epochs; best epoch 11; validation CE 1.60675; 22.68 s; best/final checkpoints saved. |
| Our MS-TCN | PASS | 12 epochs; best epoch 11; validation CE 1.27032; 31.49 s; best/final checkpoints saved. |
| Test action metrics | PASS | Mean over 4 held-out videos: Framewise accuracy .445 / macro-F1 .319 / Edit 11.70 / F1@10 .149 / @25 .094 / @50 .032. MS-TCN: .569 / .390 / 50.39 / .445 / .445 / .207. Per-class and confusion outputs saved. |
| Timelines and evidence | PASS for action path | GT, Framewise and MS-TCN timelines saved. 69 actual non-background MS-TCN test events linked to timestamp/frame/snapshot/clip; event-to-frame timing and files verified. Workflow decision is NOT EVALUATED. |
| Workflow integration | HUMAN REVIEW REQUIRED | No reliable TAS-S process interpretation. Official PSR graph is mined from data and uses component-state nodes; it is not mapped onto action labels. Workflow remains disabled. Handoff: `HUMAN_HANDOFF_CP05.md`. |
| Process anomaly metrics | NOT EVALUATED | No held-out ground truth matching workflow violations; PPR is not substituted. |
| Runtime | PARTIAL | Offline precomputed-feature model inference on CUDA recorded. Does not include video decode/feature extraction or streaming. CPU utilization and peak memory not measured. |
| Existing tests | PASS | `python -m unittest discover -s tests -v`: 24 passed. |

## CP05 acceptance summary

Action data, training/validation/test evaluation, per-class and temporal error analysis, timelines, actual action-event evidence, and offline runtime were available at CP05. CP05 remains **PARTIAL historically** because workflow policy/integration required human input. The ZIP limitation was resolved in CP06; CP07 documents current workflow and system status. CP05 action results are our procedure-scoped IMPACT baseline, not official leaderboard reproduction.

# 38. IMPLEMENTATION PHASE — CP06

**Checkpoint:** EXP-CP06 — workflow semantics infrastructure and action-baseline reliability  
**Status:** PARTIAL — archive provenance, frozen action metrics, seed repeats, deterministic workflow tests, and review package verified; human workflow semantics and visual review pending.  
**Last updated:** 2026-09-27

| Work item | Status | Evidence / result |
|---|---|---|
| CP05 context/artifact audit | PASS with historical ZIP note updated | `experiments/CP06/CP06_context_and_audit.md`; CP05 reports checked against config, code, checkpoints and results. |
| I3D archive | PASS | SHA-256 matches release manifest; official IMPACT verifier returns archive structure and CRC PASS. |
| Metric definition and held-out action report | PASS | `experiments/CP06/metric_definition_audit.md`, `action_metrics.json`; four per-execution reports, equal-execution mean/sample SD and pooled frames. |
| MS-TCN seed reliability | PASS | Three seeds (CP05 seed17 plus new seeds23/41), validation-only selection; `seed_reliability.md/.json`, training log/reports and checkpoints saved. Test results did not tune models. |
| Workflow draft and human spec | HUMAN REVIEW REQUIRED | `configs/workflows/disassembly_A.draft.yaml`; no executable routes fabricated. `HUMAN_HANDOFF_CP06.md` requests explicit source-backed semantics. |
| Deterministic workflow engine/validator | PASS for synthetic logic | Existing engine extended for event outcomes/uncertain evidence/policy-driven timeout. Validator checks graph/path structure and policies. |
| Golden workflow tests | PASS | 20 CP06 golden tests plus repository suite (44 total passed); see execution record in EXP-CP06. |
| Action error analysis | PASS, semantic cause pending | `experiments/CP06/action_error_analysis.md` and `action_error_events.json`; visual reason and bottleneck attribution remain undetermined. |
| Evidence review package | HUMAN REVIEW REQUIRED | `HUMAN_HANDOFF_CP06_EVIDENCE_REVIEW.md`; representative linked CP05 events only, not converted to labels. |
| Process compliance/anomaly/duration | NOT EVALUATED | No human-validated workflow or matching process-violation ground truth; no timing policy. |
| Workflow integration | NOT EVALUATED | No actual ActionEvent-to-compliance trace until the reviewed workflow YAML is supplied. |

# 39. IMPLEMENTATION PHASE — CP07

**Checkpoint:** EXP-CP07 — procedure grounding and ActionEvent integration  
**Status:** PASS — CP07 checkpoint deliverables complete; project process layer remains PARTIAL at human semantic and evidence-review gates.  
**Last updated:** 2026-09-27

| Work item | Status | Evidence / result |
|---|---|---|
| CP06 context/artifact audit | PASS | `experiments/CP07/CP07_context_and_audit.md`; checked reports, metrics, timelines, checkpoints, workflow artifacts and handoffs. |
| Current environment audit | PASS (snapshot) | `experiments/CP07/environment_audit.json`; RTX/CUDA verified. Dependency ranges are not a lockfile. |
| Metric aggregation boundary | PASS | `experiments/CP07/metric_aggregation_audit.md`; pooled temporal metrics retain execution boundaries; synthetic regression test. |
| ActionEvent contract | PASS | `experiments/CP07/action_event_contract.md`; event ID/view/evidence refs and serialization tested. |
| Error structure | PASS, causal explanation pending | `experiments/CP07/action_error_structure.md/.json`; descriptive n=4 execution and confusion measurements. |
| Workflow specification | HUMAN REVIEW REQUIRED | No `configs/workflows/disassembly_A.yaml`; draft remains non-executable. Exact owner YAML handoff in `HUMAN_HANDOFF_CP07.md`. |
| Workflow validator | PASS as gate | Validator correctly rejects draft as not HUMAN_VALIDATED and lacking owner routes/dispositions/completion. |
| Workflow trace adapter | PASS for synthetic interface | `src/human_action/workflow_trace.py`; state-before/after, result, evidence and uncertainty emitted; real traces require enabled + HUMAN_VALIDATED. Separate workflow-YAML loading and automatic event evidence linking remain CP08 wiring; no real held-out execution. |
| Workflow activation safety | PASS | Workflow defaults disabled; enabling requires `HUMAN_VALIDATED`; legacy CP01 illustrative routes/timing rules removed. Regression test included. |
| Evidence review | HUMAN REVIEW REQUIRED | 21 category selections deduplicate to 13 unique events in `experiments/CP07/evidence_review_manifest.json`; fixed handoff in `HUMAN_HANDOFF_CP07_EVIDENCE_REVIEW.md`. |
| Process compliance / anomaly / duration | NOT EVALUATED | No validated workflow and matching process ground truth or timing policy. |
| Test suite | PASS | 56 repository tests and Python compileall passed after CP07 safeguards. See `experiments/EXP-CP07.md`. |

# 40. ENGINEERING HARDENING — CP07.1

**Checkpoint:** CP07.1 — system hardening and workflow architecture alignment  
**Status:** PASS — generic workflow/metric correctness changes verified; project process semantics remain HUMAN_REVIEW_REQUIRED.  
**Last updated:** 2026-09-27

| Work item | Status | Evidence / result |
|---|---|---|
| Pre-change context and audit | PASS | `experiments/CP07.1/CP07.1_context_and_audit.md`; HEAD `2a89bc9355b2f8a8453e831ba6b1a7e1fb0fdedc`; baseline 56 tests. |
| Partial-order workflow capability | PASS, synthetic only | Existing `WorkflowEngine` accepts either `valid_paths` or `required_actions` + acyclic `prerequisites`; both A/B orders and prerequisite rejection tested. No Disassembly_A rules added. |
| Route skip handling | PASS | Regression with two candidate routes at different positions verifies route-local skipped steps and post-event position. |
| Observation and process acceptance separation | PASS | `observations` preserves uncertain/malformed events; only sufficient, valid events progress the workflow. Confidence remains separate. |
| Metric alignment/background | PASS | Unequal and non-1D inputs fail; background resolves by configured class label; tests include nonzero background ID. |
| Workflow semantic activation | PASS as safety gate | No executable workflow file was created or draft/worksheet semantically modified. Draft validator rejects unapproved/incomplete semantics as expected. |
| Temporal decoder | INSPECTED, unchanged | Existing deterministic heuristic and tests remain; no concrete defect reproduced and no held-out tuning performed. |
| Frozen CP05/CP06 provenance | PRESERVED | No files written to CP05/CP06 experiment outputs or `models/`; no training, result regeneration, or checkpoint replacement. |
| Repository hygiene | PASS, low-risk only | `.idea/` ignored; no tracked `.idea/` entries were present; stale help/package/workflow README wording corrected. |
| Complete verification | PASS | `.venv-cp05` unittest discovery: **63 passed**; `compileall -q src tools tests` passed; draft validator exited 1 for expected semantic approval errors. |
| Process metrics / real workflow trace | NOT EVALUATED | No owner-validated workflow or matching process ground truth. |

**CP08 entry:** generic workflow and strict scoring plumbing are available. Actual Disassembly_A trace interpretation remains gated on the human-owned worksheet and approved YAML; process compliance remains NOT EVALUATED.
