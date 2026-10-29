"""Kiem tra notebook va chay cac cell tu dau bang fixture minh hoa."""

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest


class PracticeNotebookTests(unittest.TestCase):
    def test_notebook_cells_run_from_start_without_saved_outputs(self):
        project_root = Path(__file__).resolve().parents[1]
        notebook_path = project_root / "notebooks" / "exam1_practice.ipynb"
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertGreaterEqual(len(code_cells), 5)
        for cell in code_cells:
            self.assertEqual(cell["outputs"], [])
            self.assertIsNone(cell["execution_count"])

        prior_output_dir = os.environ.get("VIHSD_NOTEBOOK_OUTPUT_DIR")
        prior_suppress_display = os.environ.get("VIHSD_NOTEBOOK_SUPPRESS_DISPLAY")
        prior_fixture_mode = os.environ.get("VIHSD_NOTEBOOK_USE_FIXTURE")
        import matplotlib

        matplotlib.use("Agg", force=True)
        with tempfile.TemporaryDirectory() as temporary_directory:
            os.environ["VIHSD_NOTEBOOK_OUTPUT_DIR"] = temporary_directory
            os.environ["VIHSD_NOTEBOOK_SUPPRESS_DISPLAY"] = "1"
            os.environ["VIHSD_NOTEBOOK_USE_FIXTURE"] = "1"
            namespace = {"__name__": "__main__"}
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    for index, cell in enumerate(code_cells):
                        source = cell["source"]
                        if isinstance(source, list):
                            source = "".join(source)
                        compile(source, f"exam1_practice_cell_{index}", "exec")
                        exec(source, namespace)
                self.assertEqual(len(namespace["all_frame"]), 6)
                self.assertEqual(int(namespace["label_counts"]["count"].sum()), 6)
                self.assertTrue((Path(temporary_directory) / "label_distribution.png").is_file())
                self.assertTrue((Path(temporary_directory) / "comment_lengths.png").is_file())
                self.assertEqual(namespace["SOURCE_MODE"], "FIXTURE MINH HOA — KHONG PHAI ViHSD")
            finally:
                if prior_output_dir is None:
                    os.environ.pop("VIHSD_NOTEBOOK_OUTPUT_DIR", None)
                else:
                    os.environ["VIHSD_NOTEBOOK_OUTPUT_DIR"] = prior_output_dir
                if prior_suppress_display is None:
                    os.environ.pop("VIHSD_NOTEBOOK_SUPPRESS_DISPLAY", None)
                else:
                    os.environ["VIHSD_NOTEBOOK_SUPPRESS_DISPLAY"] = prior_suppress_display
                if prior_fixture_mode is None:
                    os.environ.pop("VIHSD_NOTEBOOK_USE_FIXTURE", None)
                else:
                    os.environ["VIHSD_NOTEBOOK_USE_FIXTURE"] = prior_fixture_mode


if __name__ == "__main__":
    unittest.main()
