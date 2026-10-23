"""Kiem thu chat luong va tien xu ly bang du lieu nho cho ky thuat."""

import unittest
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

from vihsd.preprocessing import (
    compare_text_versions,
    normalize_series,
    normalize_text,
    preprocessing_summary,
)
from vihsd.quality import (
    class_balance_summary,
    cross_split_duplicate_summary,
    quality_issue_table,
)


VALID_LABELS = ("CLEAN", "OFFENSIVE", "HATE")


class QualityAndPreprocessingTests(unittest.TestCase):
    def test_quality_counts_missing_blank_duplicates_conflicts_and_invalid_labels(self):
        frame = pd.DataFrame(
            {
                "body": ["Xin   chào", "xin chào", "   ", None, "kooooo!!!"],
                "target": ["CLEAN", "HATE", "OFFENSIVE", "UNKNOWN", "INVALID"],
            }
        )
        issues = quality_issue_table(frame, "body", "target", VALID_LABELS)
        counts = issues.set_index("issue")["count"]
        self.assertEqual(int(counts["missing_text"]), 1)
        self.assertEqual(int(counts["blank_text"]), 1)
        self.assertEqual(int(counts["duplicate_text_excess_rows"]), 1)
        self.assertEqual(int(counts["conflicting_duplicate_rows"]), 2)
        self.assertEqual(int(counts["invalid_label"]), 2)
        self.assertFalse(issues["safe_example"].str.contains("Xin", case=False).any())

    def test_class_balance_reports_all_requested_labels_and_ratio(self):
        frame = pd.DataFrame({"target": ["CLEAN", "CLEAN", "OFFENSIVE", "HATE"]})
        distribution, ratio = class_balance_summary(frame, "target", VALID_LABELS)
        self.assertEqual(distribution["sample_count"].tolist(), [2, 1, 1])
        self.assertEqual(ratio, 2.0)

    def test_cross_split_overlap_normalizes_case_and_whitespace_without_text_output(self):
        splits = {
            "train": pd.DataFrame({"body": ["Xin  chào", "không sao"]}),
            "test": pd.DataFrame({"body": ["xin chào", "khác"]}),
            "validation": pd.DataFrame({"body": ["Không sao"]}),
        }
        overlap = cross_split_duplicate_summary(splits, "body")
        self.assertEqual(int(overlap["shared_unique_texts"].sum()), 2)
        self.assertNotIn("body", overlap.columns)

    def test_unicode_whitespace_and_controlled_abbreviations(self):
        raw = "  Ko   muo\u0302\u0301n!!! 😀  "
        normalized = normalize_text(raw)
        self.assertEqual(normalized, "không muốn!!! 😀")

    def test_negation_punctuation_emoji_and_unlisted_words_are_preserved(self):
        self.assertEqual(normalize_text("không phải không!!! 😀"), "không phải không!!! 😀")
        self.assertEqual(normalize_text("book ko!"), "book không!")
        self.assertEqual(
            normalize_text("nhe nhe", {"nhe": "nhé"}),
            "nhé nhé",
        )

    def test_series_processing_does_not_mutate_original_and_summarizes_changes(self):
        original = pd.Series(["ko vui", "không sao", None])
        processed = normalize_series(original)
        comparison = compare_text_versions(original)
        summary = preprocessing_summary(original, processed)
        self.assertEqual(original.iloc[0], "ko vui")
        self.assertEqual(processed.iloc[0], "không vui")
        self.assertEqual(summary["changed_row_count"], 1)
        self.assertEqual(len(comparison), 3)

    def test_quality_command_writes_safe_tables_and_cross_split_counts(self):
        project_root = Path(__file__).resolve().parents[1]
        train = pd.DataFrame(
            {"body": ["Same text", "kooooo!!!"], "target": ["CLEAN", "HATE"]}
        )
        test = pd.DataFrame({"body": ["same   text"], "target": ["OFFENSIVE"]})
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            train_path = temporary_path / "train.csv"
            test_path = temporary_path / "test.csv"
            output_path = temporary_path / "audit"
            train.to_csv(train_path, index=False, encoding="utf-8-sig")
            test.to_csv(test_path, index=False, encoding="utf-8-sig")
            command = [
                sys.executable,
                str(project_root / "scripts" / "audit_quality.py"),
                "--split",
                f"train={train_path}",
                "--split",
                f"test={test_path}",
                "--text-column",
                "body",
                "--label-column",
                "target",
                "--allowed-label",
                "CLEAN",
                "--allowed-label",
                "OFFENSIVE",
                "--allowed-label",
                "HATE",
                "--output-dir",
                str(output_path),
            ]
            completed = subprocess.run(
                command,
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            overlap = pd.read_csv(output_path / "cross_split_overlap.csv")
            self.assertEqual(int(overlap.loc[0, "shared_unique_texts"]), 1)
            issues = pd.read_csv(output_path / "quality_issues.csv")
            self.assertNotIn("Same text", " ".join(issues["safe_example"].astype(str)))


if __name__ == "__main__":
    unittest.main()
