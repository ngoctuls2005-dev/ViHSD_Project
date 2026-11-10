"""Kiem thu model, pipeline va danh gia tren fixture nho."""

import contextlib
import io
import json
import os
from pathlib import Path
import unittest

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.naive_bayes import MultinomialNB

from vihsd.model_evaluation import (
    classification_metrics,
    confusion_matrix_rows,
    cross_validate_text_models,
    duplicate_group_ids,
    duplicate_group_summary,
    make_cv_schemes,
)
from vihsd.models import (
    NumpyMultinomialNB,
    build_text_pipeline,
    make_text_transformer,
)


class ModelAndEvaluationTests(unittest.TestCase):
    def test_numpy_naive_bayes_matches_sklearn_on_sparse_data(self):
        matrix = csr_matrix(
            np.asarray(
                [
                    [2.0, 0.0, 1.0, 0.0],
                    [1.0, 1.0, 0.0, 0.0],
                    [0.0, 2.0, 0.0, 1.0],
                    [0.0, 1.0, 0.0, 2.0],
                    [1.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0, 2.0],
                ]
            )
        )
        labels = np.asarray([0, 0, 1, 1, 0, 2])
        expected = MultinomialNB(alpha=1.0).fit(matrix, labels)
        actual = NumpyMultinomialNB(alpha=1.0).fit(matrix, labels)

        np.testing.assert_array_equal(actual.classes_, expected.classes_)
        np.testing.assert_allclose(
            actual.predict_log_proba(matrix), expected.predict_log_proba(matrix), atol=1e-12
        )
        np.testing.assert_array_equal(actual.predict(matrix), expected.predict(matrix))

    def test_numpy_naive_bayes_rejects_negative_values_and_bad_alpha(self):
        with self.assertRaisesRegex(ValueError, "khong am"):
            NumpyMultinomialNB().fit(csr_matrix([[1.0, -0.1], [0.0, 1.0]]), [0, 1])
        for alpha in (0, -1, np.nan, np.inf, -np.inf):
            with self.subTest(alpha=alpha):
                with self.assertRaisesRegex(ValueError, "alpha"):
                    NumpyMultinomialNB(alpha=alpha).fit(
                        csr_matrix([[1.0], [0.0]]), [0, 1]
                    )

    def test_numpy_naive_bayes_zero_vectors_use_class_priors(self):
        model = NumpyMultinomialNB(alpha=1.0).fit(
            csr_matrix((3, 4), dtype=np.float64), [0, 0, 1]
        )
        probabilities = model.predict_proba(csr_matrix((2, 4), dtype=np.float64))
        np.testing.assert_allclose(probabilities, [[2 / 3, 1 / 3]] * 2)
        np.testing.assert_array_equal(model.predict(csr_matrix((2, 4))), [0, 0])

    def test_text_pipeline_fits_vocabulary_from_train_only(self):
        pipeline = build_text_pipeline(MultinomialNB(), feature_mode="word")
        pipeline.fit(["sach sach dep", "phim rat hay"], [0, 1])
        vocabulary = pipeline.named_steps["tfidf"].vocabulary_
        self.assertNotIn("valonlytokenxyz", vocabulary)
        self.assertIn("sach", vocabulary)

    def test_missing_text_becomes_empty_without_mutating_input(self):
        values = pd.Series(["ko thich", None])
        transformer = make_text_transformer("word")
        matrix = transformer.fit_transform(values)
        self.assertEqual(matrix.shape[0], 2)
        self.assertTrue(pd.isna(values.iloc[1]))

    def test_duplicate_groups_capture_normalized_conflicts_without_text_output(self):
        texts = ["Xin   chào", "xin chào", "ko thích", None]
        labels = [0, 1, 1, 2]
        groups = duplicate_group_ids(texts)
        self.assertEqual(groups[0], groups[1])
        self.assertNotEqual(groups[2], groups[3])
        self.assertEqual(
            duplicate_group_summary(texts, labels),
            {
                "rows": 4,
                "unique_text_groups": 3,
                "duplicate_excess_rows": 1,
                "conflicting_label_groups": 1,
            },
        )

    def test_group_cross_validation_keeps_duplicate_text_in_one_fold(self):
        texts = []
        labels = []
        for label, word in enumerate(("sach", "xuc pham", "thu ghet")):
            for index in range(6):
                text = f"{word} nhom {index}"
                texts.extend([text, text])
                labels.extend([label, label])
        groups = duplicate_group_ids(texts)
        splitter = make_cv_schemes(n_splits=3)["stratified_group"]
        results = cross_validate_text_models(
            texts,
            labels,
            {"nb": MultinomialNB(alpha=1.0)},
            splitter,
            "stratified_group",
            feature_mode="word",
            groups=groups,
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results["duplicate_groups_crossing_fold"].sum(), 0)
        self.assertTrue((results["feature_count"] > 0).all())
        self.assertTrue(results["validation_macro_f1"].between(0, 1).all())

    def test_metrics_use_fixed_three_class_order_and_no_division_errors(self):
        metrics = classification_metrics([0, 0, 1], [0, 0, 0])
        self.assertEqual(metrics["support_hate"], 0)
        self.assertEqual(metrics["f1_hate"], 0.0)
        self.assertTrue(0.0 <= metrics["macro_f1"] <= 1.0)
        cells = confusion_matrix_rows([0, 1, 2], [0, 0, 2], "demo", "validation")
        self.assertEqual(len(cells), 9)
        self.assertEqual(sum(row["count"] for row in cells), 3)

    def test_exam2_notebook_runs_fixture_without_saved_outputs(self):
        project_root = Path(__file__).resolve().parents[1]
        notebook_path = project_root / "notebooks" / "exam2_practice.ipynb"
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertTrue(code_cells)
        all_code = "\n".join(
            "".join(cell["source"])
            if isinstance(cell["source"], list)
            else cell["source"]
            for cell in code_cells
        )
        self.assertNotIn("test_texts", all_code)
        self.assertNotIn("test_y", all_code)
        self.assertIn("splits=DEVELOPMENT_SPLITS", all_code)
        for cell in code_cells:
            self.assertEqual(cell["outputs"], [])
            self.assertIsNone(cell["execution_count"])

        variable_names = (
            "VIHSD_NOTEBOOK_USE_FIXTURE",
            "MPLBACKEND",
        )
        previous_values = {name: os.environ.get(name) for name in variable_names}
        prior_directory = Path.cwd()
        try:
            os.chdir(project_root)
            os.environ["VIHSD_NOTEBOOK_USE_FIXTURE"] = "1"
            os.environ["MPLBACKEND"] = "Agg"
            namespace = {"__name__": "__main__"}
            with contextlib.redirect_stdout(io.StringIO()):
                for index, cell in enumerate(code_cells):
                    source = cell["source"]
                    if isinstance(source, list):
                        source = "".join(source)
                    exec(compile(source, f"exam2_notebook_fixture_{index}", "exec"), namespace)
            self.assertIn(namespace["selected_model"], namespace["estimators"])
            self.assertEqual(len(namespace["cv_folds"]), 30)
            self.assertNotIn("test_texts", namespace)
            self.assertNotIn("test_y", namespace)
            self.assertNotIn("test_summary", namespace)
            if "frames" in namespace:
                self.assertEqual(set(namespace["frames"]), {"train", "validation"})
        finally:
            os.chdir(prior_directory)
            for name, value in previous_values.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
