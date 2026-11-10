"""Kiem thu ranh gioi Development va bao ve cac dau ra Test da co."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from vihsd.experiment import (
    load_official_frames,
    load_locked_config_from_mapping,
    run_development_experiments,
    run_final_test,
)
from vihsd.models import make_estimators


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_cli_module():
    path = PROJECT_ROOT / "scripts" / "run_exam2_experiments.py"
    spec = importlib.util.spec_from_file_location("exam2_cli_for_tests", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _frame(prefix: str, repeats: int) -> pd.DataFrame:
    rows = []
    for label, word in enumerate(("sach", "xuc pham", "thu ghet")):
        for index in range(repeats):
            rows.append({"free_text": f"{prefix} {word} mau {index}", "label_id": label})
    return pd.DataFrame(rows)


class _FakeSplit:
    column_names = ["free_text", "label_id"]
    features = {
        "free_text": type("Feature", (), {"dtype": "string"})(),
        "label_id": type("Feature", (), {"dtype": "int64"})(),
    }

    def __init__(self, prefix: str):
        self.frame = pd.DataFrame(
            {
                "free_text": [f"{prefix} clean", f"{prefix} offensive", f"{prefix} hate"],
                "label_id": np.asarray([0, 1, 2], dtype=np.int64),
            }
        )

    def __len__(self):
        return len(self.frame)

    def to_pandas(self):
        return self.frame.copy()


class ExperimentModeTests(unittest.TestCase):
    def test_cli_defaults_to_development(self):
        cli = _load_cli_module()
        args = cli._parse_args([])
        self.assertEqual(args.mode, "development")
        self.assertIsNone(args.locked_config)

    def test_development_loader_requests_train_and_validation_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch("vihsd.experiment.EXPECTED_ROWS", {"train": 3, "validation": 3, "test": 3}),
                patch(
                    "vihsd.experiment.load_dataset",
                    return_value=[_FakeSplit("train"), _FakeSplit("validation")],
                ) as loader,
            ):
                frames, revision = load_official_frames(
                    Path(temp_dir) / "missing_raw",
                    Path(temp_dir) / "missing_provenance.json",
                )
        loader.assert_called_once_with(
            "uitnlp/vihsd",
            revision="88e81b36ca376867640dad9df295e0f7d499ab80",
            split=["train", "validation"],
        )
        self.assertEqual(set(frames), {"train", "validation"})
        self.assertNotIn("test", frames)
        self.assertTrue(revision)

    def test_development_runner_never_requests_test_or_writes_test_outputs(self):
        class GuardedFrames(dict):
            test_reads = 0

            def __getitem__(self, key):
                if key == "test":
                    self.test_reads += 1
                    raise AssertionError("Development attempted to read Test")
                return super().__getitem__(key)

        frames = GuardedFrames(
            train=_frame("train", 6),
            validation=_frame("validation", 3),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "development" / "word" / "fixture-run"
            result = run_development_experiments(
                frames,
                "fixture-revision",
                output,
                n_splits=2,
                include_group_cv=False,
            )
            self.assertEqual(frames.test_reads, 0)
            self.assertFalse(result["manifest"]["test_data_loaded"])
            self.assertFalse(result["manifest"]["test_evaluated"])
            self.assertFalse((output / "test_metrics.csv").exists())
            self.assertFalse((output / "test_confusion_matrix.csv").exists())
            self.assertFalse(any("test" in path.name.lower() for path in output.iterdir()))
            saved_manifest = json.loads((output / "run_manifest.json").read_text("utf-8"))
            self.assertIs(saved_manifest["test_data_loaded"], False)

    def test_development_rejects_test_split_before_indexing_any_split(self):
        class TestLabelTrap:
            def __iter__(self):
                raise AssertionError("Test mapping must not be read")

        frames = {"train": _frame("train", 6), "validation": _frame("val", 3), "test": TestLabelTrap()}
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(ValueError, "Train va Validation"):
                run_development_experiments(
                    frames,
                    "fixture-revision",
                    Path(temp_dir) / "not-created",
                )
            self.assertFalse((Path(temp_dir) / "not-created").exists())

    def test_output_paths_separate_modes_features_and_reject_baseline_root(self):
        cli = _load_cli_module()
        word = cli.build_output_path("development", "word", "unit-word")
        combined = cli.build_output_path("development", "combined", "unit-combined")
        final = cli.build_output_path(
            "final-test", "word", "unit-final", model="linear_svc_balanced"
        )
        self.assertNotEqual(word, combined)
        self.assertNotEqual(word, final)
        self.assertIn("development", word.parts)
        self.assertIn("final-test", final.parts)
        with self.assertRaisesRegex(ValueError, "mode/feature/model"):
            cli.build_output_path(
                "development",
                "word",
                "unsafe",
                output_dir=PROJECT_ROOT / "reports" / "exam2_results",
            )

    def test_final_test_fixture_uses_locked_model_without_reselection(self):
        locked = {
            "model": "dummy_most_frequent",
            "model_parameters": make_estimators()["dummy_most_frequent"].get_params(
                deep=False
            ),
            "feature_mode": "word",
            "selection_metric": "validation_macro_f1",
            "selection_value": 0.5,
            "dataset_revision": "fixture-revision",
            "selected_before_test_evaluation": True,
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "final-test-fixture"
            result = run_final_test(
                _frame("train", 3),
                _frame("fixture-only-test", 1),
                "fixture-revision",
                locked,
                output,
            )
            self.assertEqual(result["manifest"]["model"], "dummy_most_frequent")
            self.assertIs(result["manifest"]["selection_recomputed"], False)
            self.assertFalse((output / "selection.json").exists())
            self.assertTrue((output / "locked_config.json").is_file())

    def test_locked_config_requires_complete_frozen_model_parameters(self):
        config = {
            "model": "dummy_most_frequent",
            "feature_mode": "word",
            "selection_metric": "validation_macro_f1",
            "selection_value": 0.5,
            "selected_before_test_evaluation": True,
        }
        with self.assertRaisesRegex(ValueError, "model_parameters"):
            load_locked_config_from_mapping(config, "fixture-revision")


if __name__ == "__main__":
    unittest.main()
