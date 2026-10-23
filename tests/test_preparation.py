"""Kiem thu chia hold-out va TF-IDF tren fixture ky thuat."""

import unittest

import pandas as pd

from vihsd.preparation import (
    assert_no_cross_split_duplicates,
    fit_tfidf_on_train,
    stratified_holdout,
    use_official_splits,
    vietnamese_word_tokenize,
)


class PreparationTests(unittest.TestCase):
    def test_official_splits_are_copied_without_repartitioning(self):
        train = pd.DataFrame({"body": ["mau 1"], "target": ["CLEAN"]})
        validation = pd.DataFrame({"body": ["mau 2"], "target": ["HATE"]})
        test = pd.DataFrame({"body": ["mau 3"], "target": ["OFFENSIVE"]})
        splits = use_official_splits(train, validation, test, "body", "target")
        splits.train.loc[0, "body"] = "changed"
        self.assertEqual(train.loc[0, "body"], "mau 1")
        self.assertEqual(splits.validation.loc[0, "body"], "mau 2")

    def test_stratified_holdout_is_reproducible_and_keeps_all_rows(self):
        frame = pd.DataFrame(
            {
                "body": [f"comment {index}" for index in range(60)],
                "target": ["CLEAN"] * 20 + ["OFFENSIVE"] * 20 + ["HATE"] * 20,
            }
        )
        first = stratified_holdout(frame, "target", 0.2, 0.2, 19)
        second = stratified_holdout(frame, "target", 0.2, 0.2, 19)
        self.assertEqual(len(first.train) + len(first.validation) + len(first.test), 60)
        self.assertEqual(first.train["body"].tolist(), second.train["body"].tolist())
        self.assertEqual(first.validation["target"].value_counts().to_dict(), {"CLEAN": 4, "OFFENSIVE": 4, "HATE": 4})

    def test_split_overlap_checker_reports_duplicates_without_printing_text(self):
        clean_splits = {
            "train": pd.DataFrame({"body": ["mot a"]}),
            "test": pd.DataFrame({"body": ["mot b"]}),
        }
        assert_no_cross_split_duplicates(clean_splits, "body")
        leaked_splits = {
            "train": pd.DataFrame({"body": ["Same text"]}),
            "test": pd.DataFrame({"body": ["same   text"]}),
        }
        with self.assertRaisesRegex(ValueError, "train/test: 1"):
            assert_no_cross_split_duplicates(leaked_splits, "body")

    def test_vietnamese_tokenizer_adapter_accepts_injected_segmenter(self):
        tokens = vietnamese_word_tokenize(
            "Trường đại học", segmenter=lambda _text: "Trường_đại_học"
        )
        self.assertEqual(tokens, ["Trường_đại_học"])

    def test_tfidf_fits_only_on_train_and_preserves_label_alignment(self):
        result = fit_tfidf_on_train(
            train_texts=["toi tot", "ban tot", "toi chao"],
            validation_texts=["validationonly words"],
            test_texts=["ΩΩΩ"],
            y_train=["CLEAN", "OFFENSIVE", "HATE"],
            y_validation=["CLEAN"],
            y_test=["HATE"],
            word_tokenizer=lambda text: text.casefold().split(),
            word_ngram_range=(1, 2),
            char_ngram_range=(2, 3),
        )
        self.assertEqual(result.word_train.shape[0], len(result.y_train))
        self.assertEqual(result.word_validation.shape[0], len(result.y_validation))
        self.assertEqual(result.combined_test.shape[0], len(result.y_test))
        self.assertEqual(result.word_test.nnz, 0)
        self.assertEqual(result.char_test.nnz, 0)
        self.assertNotIn("validationonly", result.word_vectorizer.vocabulary_)

    def test_tfidf_rejects_misaligned_text_and_label_counts(self):
        with self.assertRaisesRegex(ValueError, "khong khop"):
            fit_tfidf_on_train(
                train_texts=["mot hai"],
                validation_texts=[],
                test_texts=[],
                y_train=[],
                y_validation=[],
                y_test=[],
                word_tokenizer=lambda text: text.split(),
            )


if __name__ == "__main__":
    unittest.main()
