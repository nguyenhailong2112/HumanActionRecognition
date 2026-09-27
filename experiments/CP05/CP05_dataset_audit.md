# CP05 Dataset Storage Audit

Audit date: 2026-09-27. Scanned `D:\HaiLongRnD\Datasets\HumanActionRecognition\IMPACT\v1.1` recursively; the repository remains separate from the large data.

| Area | Extracted files | Extracted bytes | Found content | Missing / caveat |
|---|---:|---:|---|---|
| annotations | 7,216 | 458,673,739 | IMPACT v1.1 TAS-S, TAS-B, PPR, ATR and related annotation/metadata trees; TAS-S front files cover all target IDs | No original annotations ZIP retained in this storage tree |
| I3D features | 560 `.npy` + 4 release metadata files | 16,887,125,878 | 112 executions × five views (ego/front/left/right/top); target front subset 48/48 passes CP05 preflight | Original ZIP absent, so no direct local SHA-256 or ZIP CRC audit |
| RGB videos | 224 `.mp4` | 45,978,494,085 | 112 front (31,487,210,926 bytes) + 112 top (14,491,275,243 bytes) | left/right/ego RGB not downloaded; no need for this frozen front-only experiment |
| Depth | 232 files | 24,549,277,309 | Extracted depth content present | No CP05 dependency; source bundle ZIP absent |
| Eye tracking | 116 files | 2,808,934,861 | Extracted egocentric eye-tracking content present | No CP05 dependency; source bundle ZIP absent |
| Sample | 391 files | 2,997,021,646 | IMPACT quick-start sample extraction | Not used for training or evaluation |
| Release metadata | 6 small files | 7,094 | README, changelog, data license, `MANIFEST.tsv`, `SHA256SUMS`, `VERIFICATION.tsv` | Manifest records source archives; verification status values are `published`, not proof of this machine's archive hash computation |

## Archive and extracted tree integrity

- Recursive search found no `.zip` archives in the dataset storage. In particular `IMPACT-v1.1-features-I3D.zip` is absent.
- The release manifest records the official I3D archive at 16,887,238,161 bytes and `SHA256SUMS` expects `97f9d81443d1a3978e77b5db119b69089ecd470af77d6bb60bd20f792446a111`. `VERIFICATION.tsv` reports `archive_structure=ok`, `embedded_metadata=ok`, `sha256=published`; that last value does not mean a locally observed hash passed.
- ZIP CRC cannot be run without an archive. Extracted I3D structure and values were checked directly for every target execution: correct file identifier/path, 2-D float32, exact annotation frame length, 1024 columns and all finite values (48/48). The release documentation specifies frame-aligned 1024-D I3D descriptors; loader samples 30 FPS arrays at the same 5 FPS indices as TAS-S labels.
- Therefore the working extracted features are structurally and numerically valid for this subset, while byte-level authenticity of the missing original archive remains unverified. No checksum mismatch was observed because no archive was available to hash.

## Cameras and experiment scope

The local RGB tree contains full `front` and `top` view bundles (112 videos each). It contains no RGB `left`, `right`, or `ego` bundle. Extracted I3D includes vectors for all five view names, but CP05 uses only `front`. No additional camera download is required to run or reproduce this CP05 protocol. Acquire the other RGB views only for a future multi-view/video-input experiment that explicitly needs them.


