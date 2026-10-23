"""Kiem thu doc schema va thong ke tren fixture nho, khong phai du lieu ViHSD."""

import tempfile
import unittest
from pathlib import Path
import subprocess
import sys

import pandas as pd

from vihsd.data import invalid_label_values, read_csv, validate_schema
from vihsd.eda import (
    comment_lengths,
    count_labels,
    length_summary,
    plot_comment_lengths,
    plot_label_distribution,
    top_surface_ngrams,
    writing_signal_summary,
)


class DataAndEdaTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame(
            {
                "comment": ["chào bạn", "TỐT!!! 123 😀", "câu phủ định không"],
                "class_name": ["CLEAN", "OFFENSIVE", "HATE"],
                "extra": [1, 2, 3],
            }
        )

    def test_read_csv_preserves_vietnamese_text(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "fixture.csv"
            self.frame.to_csv(csv_path, index=False, encoding="utf-8-sig")
            loaded = read_csv(csv_path)
        self.assertEqual(loaded.loc[0, "comment"], "chào bạn")

    def test_read_csv_reports_missing_path(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("missing-fixture.csv")

    def test_schema_requires_explicit_existing_columns(self):
        profile = validate_schema(self.frame, "comment", "class_name")
        self.assertEqual(profile["row_count"], 3)
        self.assertEqual(profile["column_count"], 3)
        with self.assertRaises(ValueError):
            validate_schema(self.frame, "text", "class_name")

    def test_invalid_labels_use_caller_supplied_vocabulary(self):
        invalid = invalid_label_values(
            pd.Series(["CLEAN", "ALIEN", None]), {"CLEAN", "OFFENSIVE", "HATE"}
        )
        self.assertEqual(invalid, ["ALIEN"])

    def test_label_counts_and_comment_lengths_are_measured(self):
        counts = count_labels(self.frame, "class_name")
        lengths = comment_lengths(self.frame, "comment", "class_name")
        summary = length_summary(lengths)
        self.assertEqual(int(counts["count"].sum()), 3)
        self.assertEqual(int(lengths.loc[0, "character_count"]), 8)
        self.assertEqual(int(summary["sample_count"].sum()), 3)

    def test_ngrams_and_writing_signals_do_not_return_comment_examples(self):
        ngrams = top_surface_ngrams(self.frame, "comment", "class_name", n=1, top_k=5)
        signals = writing_signal_summary(self.frame, "comment")
        self.assertIn("ngram", ngrams.columns)
        self.assertNotIn("comment", ngrams.columns)
        self.assertEqual(int(signals.loc[signals["signal"] == "contains_digit", "count"].iloc[0]), 1)
        self.assertEqual(int(signals.loc[signals["signal"] == "contains_emoji", "count"].iloc[0]), 1)

    def test_plots_are_saved_to_requested_paths(self):
        counts = count_labels(self.frame, "class_name")
        lengths = comment_lengths(self.frame, "comment", "class_name")
        with tempfile.TemporaryDirectory() as temporary_directory:
            label_path = plot_label_distribution(counts, Path(temporary_directory) / "nested" / "labels.png")
            length_path = plot_comment_lengths(lengths, Path(temporary_directory) / "lengths.png")
            self.assertTrue(label_path.is_file())
            self.assertTrue(length_path.is_file())

    def test_eda_command_writes_summary_files_from_local_csv(self):
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            input_path = temporary_path / "input.csv"
            output_path = temporary_path / "output"
            self.frame.to_csv(input_path, index=False, encoding="utf-8-sig")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(project_root / "scripts" / "run_eda.py"),
                    "--input",
                    str(input_path),
                    "--text-column",
                    "comment",
                    "--label-column",
                    "class_name",
                    "--output-dir",
                    str(output_path),
                ],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for filename in (
                "schema.json",
                "label_counts.csv",
                "comment_lengths.csv",
                "length_summary.csv",
                "surface_ngrams.csv",
                "writing_signals.csv",
                "label_distribution.png",
                "comment_lengths.png",
            ):
                self.assertTrue((output_path / filename).is_file(), filename)


if __name__ == "__main__":
    unittest.main()
