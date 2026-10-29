"""Tich hop voi dataset that, chi chay khi bat co xac nhan."""

import os
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from datasets import load_dataset


@unittest.skipUnless(
    os.environ.get("VIHSD_RUN_INTEGRATION") == "1",
    "Set VIHSD_RUN_INTEGRATION=1 khi tai khoan Hugging Face da duoc cap quyen",
)
class RealDatasetIntegrationTests(unittest.TestCase):
    def test_official_splits_schema_and_label_codes(self):
        dataset = load_dataset(
            "uitnlp/vihsd",
            revision="88e81b36ca376867640dad9df295e0f7d499ab80",
        )
        self.assertEqual(set(dataset.keys()), {"train", "validation", "test"})
        expected_rows = {"train": 24048, "validation": 2672, "test": 6680}
        for split_name, expected_count in expected_rows.items():
            split = dataset[split_name]
            self.assertEqual(len(split), expected_count)
            self.assertEqual(split.column_names, ["free_text", "label_id"])
            self.assertEqual(split.features["free_text"].dtype, "string")
            self.assertEqual(split.features["label_id"].dtype, "int64")
            self.assertEqual(set(split.unique("label_id")), {0, 1, 2})

    def test_real_practice_notebook_cells_execute_without_saved_outputs(self):
        project_root = Path(__file__).resolve().parents[1]
        notebook_path = project_root / "notebooks" / "exam1_practice.ipynb"
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        for cell in code_cells:
            self.assertEqual(cell["outputs"], [])
            self.assertIsNone(cell["execution_count"])

        prior_directory = Path.cwd()
        variable_names = (
            "VIHSD_NOTEBOOK_OUTPUT_DIR",
            "VIHSD_NOTEBOOK_SUPPRESS_DISPLAY",
            "VIHSD_NOTEBOOK_USE_FIXTURE",
        )
        previous_values = {name: os.environ.get(name) for name in variable_names}
        import matplotlib

        matplotlib.use("Agg", force=True)
        try:
            os.chdir(project_root)
            with tempfile.TemporaryDirectory() as temporary_directory:
                os.environ["VIHSD_NOTEBOOK_OUTPUT_DIR"] = temporary_directory
                os.environ["VIHSD_NOTEBOOK_SUPPRESS_DISPLAY"] = "1"
                os.environ.pop("VIHSD_NOTEBOOK_USE_FIXTURE", None)
                namespace = {"__name__": "__main__"}
                with contextlib.redirect_stdout(io.StringIO()):
                    for index, cell in enumerate(code_cells):
                        source = cell["source"]
                        if isinstance(source, list):
                            source = "".join(source)
                        exec(compile(source, f"exam1_real_notebook_cell_{index}", "exec"), namespace)
                self.assertEqual(
                    {name: len(frame) for name, frame in namespace["frames"].items()},
                    {"train": 24048, "validation": 2672, "test": 6680},
                )
                self.assertEqual(namespace["features"].combined_train.shape[1], 560253)
        finally:
            os.chdir(prior_directory)
            for name, value in previous_values.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
