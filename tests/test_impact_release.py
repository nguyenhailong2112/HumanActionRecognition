import json
import io
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from human_action.impact_release import annotation_member, load_release_sequence, parse_tas_s_annotation, validate_official_split_integrity  # noqa: E402
from tools.validate_workflow import validate_workflow  # noqa: E402


class ImpactReleaseTests(unittest.TestCase):
    def annotation(self, segments, frame_count=6):
        return json.dumps({
            "video_id": "W1_Disassembly_A_001_front",
            "view": "front",
            "meta_data": {"fps": 30.0, "resolution": {"width": 1280, "height": 720}, "num_frames": frame_count},
            "view_start": 0,
            "view_end": frame_count - 1,
            "segments": segments,
        }).encode()

    def test_segment_annotations_expand_to_dense_frame_labels(self):
        labels, metadata = parse_tas_s_annotation(self.annotation([
            {"label": "start", "f_start": 0, "f_end": 1},
            {"label": "place", "f_start": 2, "f_end": 4},
            {"label": "null", "f_start": 5, "f_end": 5},
        ]), "W1_Disassembly_A_001_front", ["NULL", "START", "PLACE"])
        np.testing.assert_array_equal(labels, [1, 1, 2, 2, 2, 0])
        self.assertEqual(metadata["segment_count"], 3)
        self.assertEqual(metadata["fps"], 30.0)

    def test_annotation_gap_overlap_and_unknown_class_are_rejected(self):
        class_order = ["NULL", "START", "PLACE"]
        cases = [
            [{"label": "start", "f_start": 0, "f_end": 1}, {"label": "place", "f_start": 3, "f_end": 5}],
            [{"label": "start", "f_start": 0, "f_end": 2}, {"label": "place", "f_start": 2, "f_end": 5}],
            [{"label": "unknown", "f_start": 0, "f_end": 5}],
            [{"label": "start", "f_start": 0, "f_end": 6}],
        ]
        for segments in cases:
            with self.subTest(segments=segments), self.assertRaises(ValueError):
                parse_tas_s_annotation(self.annotation(segments), "W1_Disassembly_A_001_front", class_order)

    def test_official_s2_is_execution_and_test_worker_disjoint_for_disassembly_a(self):
        split_dir = PROJECT_ROOT / "ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/splits_TAS-S"
        if not split_dir.is_dir():
            split_dir = PROJECT_ROOT / "ResearchDocuments/ResearchDocuments/01_IMPACT/code/IMPACT/dataset/TAS/splits_TAS-S"
        result = validate_official_split_integrity(split_dir, 2, "Disassembly_A", "front", cross_worker_test=True)
        self.assertEqual(result["counts"], {"train": 39, "val": 5, "test": 4})
        self.assertFalse(any(result["execution_overlap"].values()))
        self.assertEqual(result["worker_overlap"]["train_test"], [])

    def test_process_owner_workflow_checks_reject_unapproved_and_unknown_steps(self):
        vocabulary = {"START", "REMOVE", "STORE"}
        approved = {"workflow": {
            "id": "procedure", "version": "research-1", "status": "HUMAN_VALIDATED", "approved_by": "owner", "approved_on": "2026-09-26",
            "action_vocabulary": sorted(vocabulary), "valid_paths": [{"id": "main", "steps": ["START", "REMOVE", "STORE"]}],
            "action_disposition": {label: {"status": "required"} for label in vocabulary},
            "completion": {"condition": "process-owner-defined completion confirmation"},
            "valid_transitions": [["START", "REMOVE"], ["REMOVE", "STORE"]],
        }}
        self.assertEqual(validate_workflow(approved, vocabulary), [])
        approved["workflow"]["valid_paths"][0]["steps"].append("GUESS")
        self.assertTrue(any("unknown actions" in error for error in validate_workflow(approved, vocabulary)))

    def test_workflow_validation_rejects_unreachable_transition_and_incomplete_metadata(self):
        vocabulary = {"A", "B"}
        config = {"workflow": {
            "id": "procedure", "version": "research-1", "approved_by": "owner", "approved_on": "2026-09-26",
            "action_vocabulary": ["A", "B"], "action_disposition": {"A": {"status": "required"}, "B": {"status": "required"}},
            "valid_paths": [{"id": "main", "steps": ["A", "B"]}],
            "valid_transitions": [["A", "B"], ["B", "A"]],
        }}
        errors = validate_workflow(config, vocabulary)
        self.assertTrue(any("completion.condition" in error for error in errors))
        self.assertTrue(any("unreachable" in error for error in errors))

    def test_official_json_and_zipped_features_load_with_aligned_5fps_samples(self):
        video_id = "W1_Disassembly_A_001_front"
        payload = self.annotation([
            {"label": "start", "f_start": 0, "f_end": 5},
            {"label": "place", "f_start": 6, "f_end": 11},
        ], frame_count=12)
        feature_values = np.arange(12 * 4, dtype=np.float32).reshape(12, 4)
        feature_bytes = io.BytesIO()
        np.save(feature_bytes, feature_values, allow_pickle=False)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "configs").mkdir()
            ann_zip = root / "annotations.zip"
            feature_zip = root / "features.zip"
            with ZipFile(ann_zip, "w") as archive:
                archive.writestr(f"IMPACT-v1.1/annotations/TAS-S/front/{video_id}.json", payload)
            with ZipFile(feature_zip, "w") as archive:
                archive.writestr(f"IMPACT-v1.1/features/I3D/{video_id}.npy", feature_bytes.getvalue())
            config_path = root / "configs" / "cp01_1.yaml"
            config_path.write_text("", encoding="utf-8")
            config = {
                "dataset": {"source": "impact_official_release", "view": "front", "annotation_archive": "annotations.zip", "feature_archive": "features.zip", "feature_name": "I3D", "sample_fps": 5.0},
                "actions": {"class_order": ["NULL", "START", "PLACE"]},
            }
            sequence = load_release_sequence(config, video_id, "train", config_path)
            np.testing.assert_array_equal(sequence.frame_indices, [0, 6])
            np.testing.assert_array_equal(sequence.labels, [1, 2])
            np.testing.assert_array_equal(sequence.features, feature_values[[0, 6]])
            self.assertEqual(sequence.worker_id, "W1")

    def test_official_extractor_directory_features_load_without_zip(self):
        video_id = "W1_Disassembly_A_001_front"
        payload = self.annotation([{"label": "start", "f_start": 0, "f_end": 29}], frame_count=30)
        expected = np.arange(30 * 4, dtype=np.float32).reshape(30, 4)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "configs").mkdir()
            output_dir = root / "features" / "I3D"
            output_dir.mkdir(parents=True)
            np.save(output_dir / f"{video_id}.npy", expected)
            with ZipFile(root / "annotations.zip", "w") as archive:
                archive.writestr(annotation_member(video_id, "front"), payload)
            config_path = root / "configs" / "cp02.yaml"
            config_path.write_text("", encoding="utf-8")
            config = {
                "dataset": {
                    "source": "impact_official_release", "view": "front",
                    "annotation_archive": "annotations.zip", "feature_archive": "missing.zip",
                    "feature_roots": ["features"], "feature_name": "I3D", "sample_fps": 5.0,
                },
                "actions": {"class_order": ["NULL", "START"]},
            }
            sequence = load_release_sequence(config, video_id, "train", config_path)
            np.testing.assert_array_equal(sequence.features, expected[[0, 6, 12, 18, 24]])
            self.assertEqual(sequence.features.shape, (5, 4))


if __name__ == "__main__":
    unittest.main()
