# CP01.1 Dataset Audit — IMPACT v1.1

Source of truth: verified official annotation archive `data/raw/impact/v1.1/annotations/IMPACT-v1.1-annotations.zip`; official TAS-S split bundles in the IMPACT repository.

- Front-view TAS-S JSON annotations: 112
- Selected same-procedure executions: 48 (Disassembly_A, front)
- Official S2 split: train 39, val 5, test 4 — execution-disjoint.
- Workers: train 12, val 4, test 1; train/test worker overlap 0.
- Local source videos in target split: 2 / 48.
- Annotation QA: {'PASS': 112}; dispositions: {'KEEP': 48, 'EXCLUDE': 64}.
- PPR per-hand phase annotations: QA {'PASS_train_L': 39, 'PASS_train_R': 39, 'PASS_val_L': 5, 'PASS_val_R': 5, 'PASS_test_L': 4, 'PASS_test_R': 4}; state counts by split/hand recorded in JSON. PPR phase labels are distinct from workflow violation labels and are not used to score compliance.
- Annotation unit: official per-frame TAS-S labels represented as ordered inclusive frame intervals; QA checks unknown class, empty segments, invalid/out-of-range bounds, ordering, overlap, gaps, and coverage.
- Annotation/video quality (blur, occlusion, view adequacy) is not assessed automatically and remains NOT VERIFIED.
- Classification labels are data annotations, not approved workflow requirements or mistake/compliance labels.

| Video | Worker | Procedure | Duration s | FPS / resolution | Segments | Annotation QA | Local video | Split | Disposition |
|---|---|---|---:|---|---:|---|---|---|---|
| AL07EJ17_Disassembly_A_001_front | AL07EJ17 | Disassembly_A | 133.267 | 30.0 / 1280x720 | 24 | PASS | AVAILABLE | train | KEEP |
| AL07EJ17_Disassembly_A_002_front | AL07EJ17 | Disassembly_A | 118.5 | 30.0 / 1280x720 | 19 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| AL07EJ17_Disassembly_A_003_front | AL07EJ17 | Disassembly_A | 117.8 | 30.0 / 1280x720 | 26 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| AL07EJ17_Disassembly_A_004_front | AL07EJ17 | Disassembly_A | 126.4 | 30.0 / 1280x720 | 24 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| AL07EJ17_Disassembly_B_005_front | AL07EJ17 | Disassembly_B | 220.967 | 30.0 / 1280x720 | 38 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| AL07EJ17_Reassembly_A_002_front | AL07EJ17 | Reassembly_A | 173.8 | 30.0 / 1280x720 | 35 | PASS | AVAILABLE | NOT_IN_S2 | EXCLUDE |
| AL07EJ17_Reassembly_A_003_front | AL07EJ17 | Reassembly_A | 170.867 | 30.0 / 1280x720 | 26 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| AL07EJ17_Reassembly_A_004_front | AL07EJ17 | Reassembly_A | 187.433 | 30.0 / 1280x720 | 24 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| AL07EJ17_Reassembly_B_005_front | AL07EJ17 | Reassembly_B | 174.767 | 30.0 / 1280x720 | 22 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER07AD15_Disassembly_A_001_front | ER07AD15 | Disassembly_A | 115.933 | 30.0 / 1280x720 | 40 | PASS | AVAILABLE | train | KEEP |
| ER07AD15_Disassembly_A_002_front | ER07AD15 | Disassembly_A | 119.967 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| ER07AD15_Disassembly_A_003_front | ER07AD15 | Disassembly_A | 105.3 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| ER07AD15_Disassembly_A_004_front | ER07AD15 | Disassembly_A | 109.7 | 30.0 / 1280x720 | 36 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| ER07AD15_Reassembly_A_001_front | ER07AD15 | Reassembly_A | 168.2 | 30.0 / 1280x720 | 40 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER07AD15_Reassembly_A_002_front | ER07AD15 | Reassembly_A | 165.8 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER07AD15_Reassembly_A_003_front | ER07AD15 | Reassembly_A | 166.133 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER07AD15_Reassembly_A_004_front | ER07AD15 | Reassembly_A | 132.233 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Disassembly_A_001_front | ER10WE06 | Disassembly_A | 419.367 | 30.0 / 1280x720 | 49 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| ER10WE06_Disassembly_A_002_front | ER10WE06 | Disassembly_A | 144.067 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| ER10WE06_Disassembly_A_003_front | ER10WE06 | Disassembly_A | 148.733 | 30.0 / 1280x720 | 27 | PASS | MISSING_LOCAL_VIDEO | val | KEEP |
| ER10WE06_Disassembly_A_004_front | ER10WE06 | Disassembly_A | 124.067 | 30.0 / 1280x720 | 27 | PASS | MISSING_LOCAL_VIDEO | val | KEEP |
| ER10WE06_Disassembly_B_005_front | ER10WE06 | Disassembly_B | 139.5 | 30.0 / 1280x720 | 28 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Reassembly_A_001_front | ER10WE06 | Reassembly_A | 236.667 | 30.0 / 1280x720 | 46 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Reassembly_A_002_front | ER10WE06 | Reassembly_A | 171.1 | 30.0 / 1280x720 | 31 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Reassembly_A_003_front | ER10WE06 | Reassembly_A | 172.067 | 30.0 / 1280x720 | 25 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Reassembly_A_004_front | ER10WE06 | Reassembly_A | 175.8 | 30.0 / 1280x720 | 23 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| ER10WE06_Reassembly_B_005_front | ER10WE06 | Reassembly_B | 164.533 | 30.0 / 1280x720 | 27 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KE03ER16_Disassembly_A_001_front | KE03ER16 | Disassembly_A | 140.933 | 30.0 / 1280x720 | 37 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KE03ER16_Disassembly_A_002_front | KE03ER16 | Disassembly_A | 116.867 | 30.0 / 1280x720 | 26 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KE03ER16_Disassembly_A_003_front | KE03ER16 | Disassembly_A | 139.0 | 30.0 / 1280x720 | 28 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KE03ER16_Disassembly_A_004_front | KE03ER16 | Disassembly_A | 130.7 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KE03ER16_Reassembly_A_001_front | KE03ER16 | Reassembly_A | 173.867 | 30.0 / 1280x720 | 34 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KE03ER16_Reassembly_A_002_front | KE03ER16 | Reassembly_A | 192.633 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KE03ER16_Reassembly_A_003_front | KE03ER16 | Reassembly_A | 165.5 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KE03ER16_Reassembly_A_004_front | KE03ER16 | Reassembly_A | 168.033 | 30.0 / 1280x720 | 37 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI03AR28_Disassembly_A_001_front | KI03AR28 | Disassembly_A | 176.067 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI03AR28_Disassembly_A_002_front | KI03AR28 | Disassembly_A | 174.2 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI03AR28_Disassembly_A_003_front | KI03AR28 | Disassembly_A | 144.133 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI03AR28_Disassembly_A_004_front | KI03AR28 | Disassembly_A | 177.367 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI03AR28_Disassembly_B_005_front | KI03AR28 | Disassembly_B | 233.0 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI03AR28_Reassembly_A_001_front | KI03AR28 | Reassembly_A | 223.767 | 30.0 / 1280x720 | 33 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI03AR28_Reassembly_A_003_front | KI03AR28 | Reassembly_A | 222.1 | 30.0 / 1280x720 | 28 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI03AR28_Reassembly_A_004_front | KI03AR28 | Reassembly_A | 228.633 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI03AR28_Reassembly_B_005_front | KI03AR28 | Reassembly_B | 658.0 | 30.0 / 1280x720 | 54 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI05KO01_Disassembly_A_001_front | KI05KO01 | Disassembly_A | 365.433 | 30.0 / 1280x720 | 61 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI05KO01_Disassembly_A_002_front | KI05KO01 | Disassembly_A | 215.5 | 30.0 / 1280x720 | 40 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI05KO01_Disassembly_A_003_front | KI05KO01 | Disassembly_A | 241.267 | 30.0 / 1280x720 | 43 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI05KO01_Disassembly_A_004_front | KI05KO01 | Disassembly_A | 164.333 | 30.0 / 1280x720 | 34 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KI05KO01_Disassembly_B_005_front | KI05KO01 | Disassembly_B | 248.633 | 30.0 / 1280x720 | 33 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI05KO01_Reassembly_A_001_front | KI05KO01 | Reassembly_A | 473.7 | 30.0 / 1280x720 | 54 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI05KO01_Reassembly_A_003_front | KI05KO01 | Reassembly_A | 345.5 | 30.0 / 1280x720 | 37 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI05KO01_Reassembly_A_004_front | KI05KO01 | Reassembly_A | 293.733 | 30.0 / 1280x720 | 40 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KI05KO01_Reassembly_B_005_front | KI05KO01 | Reassembly_B | 298.433 | 30.0 / 1280x720 | 45 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KJ03JM25_Disassembly_A_003_front | KJ03JM25 | Disassembly_A | 201.833 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KJ03JM25_Disassembly_A_004_front | KJ03JM25 | Disassembly_A | 198.9 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| KJ03JM25_Reassembly_A_002_front | KJ03JM25 | Reassembly_A | 332.633 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KJ03JM25_Reassembly_A_003_front | KJ03JM25 | Reassembly_A | 238.833 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| KJ03JM25_Reassembly_A_004_front | KJ03JM25 | Reassembly_A | 323.367 | 30.0 / 1280x720 | 46 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Disassembly_A_001_front | LE06AS03 | Disassembly_A | 907.133 | 30.0 / 1280x720 | 78 | PASS | MISSING_LOCAL_VIDEO | val | KEEP |
| LE06AS03_Disassembly_A_002_front | LE06AS03 | Disassembly_A | 234.667 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE06AS03_Disassembly_A_003_front | LE06AS03 | Disassembly_A | 173.233 | 30.0 / 1280x720 | 26 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE06AS03_Disassembly_A_004_front | LE06AS03 | Disassembly_A | 169.767 | 30.0 / 1280x720 | 29 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE06AS03_Disassembly_B_005_front | LE06AS03 | Disassembly_B | 168.033 | 30.0 / 1280x720 | 36 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Reassembly_A_001_front | LE06AS03 | Reassembly_A | 1025.0 | 30.0 / 1280x720 | 118 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Reassembly_A_002_front | LE06AS03 | Reassembly_A | 628.5 | 30.0 / 1280x720 | 60 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Reassembly_A_003_front | LE06AS03 | Reassembly_A | 340.067 | 30.0 / 1280x720 | 48 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Reassembly_A_004_front | LE06AS03 | Reassembly_A | 281.933 | 30.0 / 1280x720 | 44 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE06AS03_Reassembly_B_005_front | LE06AS03 | Reassembly_B | 472.5 | 30.0 / 1280x720 | 97 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Disassembly_A_001_front | LE07UF17 | Disassembly_A | 323.8 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE07UF17_Disassembly_A_002_front | LE07UF17 | Disassembly_A | 369.1 | 30.0 / 1280x720 | 59 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE07UF17_Disassembly_A_003_front | LE07UF17 | Disassembly_A | 235.233 | 30.0 / 1280x720 | 38 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE07UF17_Disassembly_A_004_front | LE07UF17 | Disassembly_A | 214.667 | 30.0 / 1280x720 | 36 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| LE07UF17_Disassembly_B_005_front | LE07UF17 | Disassembly_B | 224.2 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Reassembly_A_001_front | LE07UF17 | Reassembly_A | 943.667 | 30.0 / 1280x720 | 69 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Reassembly_A_002_front | LE07UF17 | Reassembly_A | 320.267 | 30.0 / 1280x720 | 44 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Reassembly_A_003_front | LE07UF17 | Reassembly_A | 283.767 | 30.0 / 1280x720 | 31 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Reassembly_A_004_front | LE07UF17 | Reassembly_A | 223.733 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| LE07UF17_Reassembly_B_005_front | LE07UF17 | Reassembly_B | 313.067 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| MA07LF04_Disassembly_A_001_front | MA07LF04 | Disassembly_A | 525.767 | 30.0 / 1280x720 | 74 | PASS | MISSING_LOCAL_VIDEO | val | KEEP |
| MA07LF04_Disassembly_A_003_front | MA07LF04 | Disassembly_A | 187.033 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| MA07LF04_Disassembly_A_004_front | MA07LF04 | Disassembly_A | 178.1 | 30.0 / 1280x720 | 32 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| MA07LF04_Disassembly_B_005_front | MA07LF04 | Disassembly_B | 325.867 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| MA07LF04_Reassembly_A_001_front | MA07LF04 | Reassembly_A | 617.833 | 30.0 / 1280x720 | 83 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| MA07LF04_Reassembly_A_002_front | MA07LF04 | Reassembly_A | 341.667 | 30.0 / 1280x720 | 43 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| MA07LF04_Reassembly_A_003_front | MA07LF04 | Reassembly_A | 303.767 | 30.0 / 1280x720 | 22 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| MA07LF04_Reassembly_B_005_front | MA07LF04 | Reassembly_B | 824.0 | 30.0 / 1280x720 | 76 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| NA07GE21_Disassembly_A_001_front | NA07GE21 | Disassembly_A | 386.467 | 30.0 / 1280x720 | 55 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| NA07GE21_Disassembly_A_002_front | NA07GE21 | Disassembly_A | 233.033 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| NA07GE21_Disassembly_A_003_front | NA07GE21 | Disassembly_A | 199.733 | 30.0 / 1280x720 | 37 | PASS | MISSING_LOCAL_VIDEO | val | KEEP |
| NA07GE21_Disassembly_A_004_front | NA07GE21 | Disassembly_A | 191.133 | 30.0 / 1280x720 | 30 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| NA07GE21_Reassembly_A_001_front | NA07GE21 | Reassembly_A | 366.033 | 30.0 / 1280x720 | 58 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| NA07GE21_Reassembly_A_002_front | NA07GE21 | Reassembly_A | 238.2 | 30.0 / 1280x720 | 37 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| NA07GE21_Reassembly_A_003_front | NA07GE21 | Reassembly_A | 184.167 | 30.0 / 1280x720 | 47 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| NA07GE21_Reassembly_A_004_front | NA07GE21 | Reassembly_A | 198.667 | 30.0 / 1280x720 | 43 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| NA07GE21_Reassembly_B_005_front | NA07GE21 | Reassembly_B | 153.367 | 30.0 / 1280x720 | 22 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| SS07EL13_Disassembly_A_001_front | SS07EL13 | Disassembly_A | 225.2 | 30.0 / 1280x720 | 38 | PASS | MISSING_LOCAL_VIDEO | test | KEEP |
| SS07EL13_Disassembly_A_002_front | SS07EL13 | Disassembly_A | 131.3 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | test | KEEP |
| SS07EL13_Disassembly_A_003_front | SS07EL13 | Disassembly_A | 134.667 | 30.0 / 1280x720 | 35 | PASS | MISSING_LOCAL_VIDEO | test | KEEP |
| SS07EL13_Disassembly_A_004_front | SS07EL13 | Disassembly_A | 118.1 | 30.0 / 1280x720 | 34 | PASS | MISSING_LOCAL_VIDEO | test | KEEP |
| SS07EL13_Disassembly_B_005_front | SS07EL13 | Disassembly_B | 177.233 | 30.0 / 1280x720 | 38 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| SS07EL13_Reassembly_A_001_front | SS07EL13 | Reassembly_A | 339.1 | 30.0 / 1280x720 | 54 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| SS07EL13_Reassembly_A_002_front | SS07EL13 | Reassembly_A | 205.767 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| SS07EL13_Reassembly_A_004_front | SS07EL13 | Reassembly_A | 223.0 | 30.0 / 1280x720 | 41 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| SS07EL13_Reassembly_B_005_front | SS07EL13 | Reassembly_B | 229.5 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| TO08CO25_Disassembly_A_002_front | TO08CO25 | Disassembly_A | 229.9 | 30.0 / 1280x720 | 47 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| TO08CO25_Disassembly_A_003_front | TO08CO25 | Disassembly_A | 190.133 | 30.0 / 1280x720 | 39 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| TO08CO25_Disassembly_A_004_front | TO08CO25 | Disassembly_A | 175.133 | 30.0 / 1280x720 | 46 | PASS | MISSING_LOCAL_VIDEO | train | KEEP |
| TO08CO25_Disassembly_B_005_front | TO08CO25 | Disassembly_B | 200.367 | 30.0 / 1280x720 | 45 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| TO08CO25_Reassembly_A_002_front | TO08CO25 | Reassembly_A | 276.567 | 30.0 / 1280x720 | 44 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| TO08CO25_Reassembly_A_003_front | TO08CO25 | Reassembly_A | 214.2 | 30.0 / 1280x720 | 42 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| TO08CO25_Reassembly_A_004_front | TO08CO25 | Reassembly_A | 201.467 | 30.0 / 1280x720 | 40 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
| TO08CO25_Reassembly_B_005_front | TO08CO25 | Reassembly_B | 211.067 | 30.0 / 1280x720 | 38 | PASS | MISSING_LOCAL_VIDEO | NOT_IN_S2 | EXCLUDE |
