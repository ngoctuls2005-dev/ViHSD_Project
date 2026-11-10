"""Pipeline van ban va cac bo phan loai cho Bai kiem tra 2."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.special import logsumexp
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.svm import LinearSVC
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from vihsd.preparation import vietnamese_word_tokenize
from vihsd.preprocessing import normalize_text


LABEL_IDS = (0, 1, 2)
LABEL_NAMES = {0: "CLEAN", 1: "OFFENSIVE", 2: "HATE"}
RANDOM_STATE = 42


class NumpyMultinomialNB(ClassifierMixin, BaseEstimator):
    """Multinomial Naive Bayes tu tinh, ho tro ma tran sparse."""

    def __init__(self, alpha: float = 1.0, fit_prior: bool = True):
        self.alpha = alpha
        self.fit_prior = fit_prior

    def fit(self, X, y):
        """Uoc luong xac suat lop va dac trung, khong dense hoa X."""
        try:
            alpha = float(self.alpha)
        except (TypeError, ValueError) as error:
            raise ValueError("alpha phai la so huu han lon hon 0") from error
        if not np.isfinite(alpha) or alpha <= 0:
            raise ValueError("alpha phai la so huu han lon hon 0")
        X, y = check_X_y(X, y, accept_sparse="csr", dtype=np.float64)
        if sparse.issparse(X):
            if np.any(X.data < 0):
                raise ValueError("MultinomialNB yeu cau dac trung khong am")
        elif np.any(X < 0):
            raise ValueError("MultinomialNB yeu cau dac trung khong am")

        self.classes_, class_indices = np.unique(y, return_inverse=True)
        self.n_features_in_ = int(X.shape[1])
        self.class_count_ = np.bincount(class_indices, minlength=len(self.classes_)).astype(
            np.float64
        )
        self.feature_count_ = np.vstack(
            [
                np.asarray(X[class_indices == index].sum(axis=0)).reshape(-1)
                for index in range(len(self.classes_))
            ]
        )

        smoothed = self.feature_count_ + alpha
        self.feature_log_prob_ = np.log(smoothed) - np.log(smoothed.sum(axis=1))[:, None]
        if self.fit_prior:
            self.class_log_prior_ = np.log(self.class_count_ / self.class_count_.sum())
        else:
            self.class_log_prior_ = np.full(
                len(self.classes_), -np.log(len(self.classes_)), dtype=np.float64
            )
        return self

    def predict_log_proba(self, X):
        """Tinh log-xac-suat hau nghiem tren dau vao dense hoac sparse."""
        check_is_fitted(self, ("classes_", "feature_log_prob_", "class_log_prior_"))
        X = check_array(X, accept_sparse="csr", dtype=np.float64)
        if X.shape[1] != self.n_features_in_:
            raise ValueError("So chieu dac trung khong khop voi luc fit")
        if sparse.issparse(X):
            if np.any(X.data < 0):
                raise ValueError("MultinomialNB yeu cau dac trung khong am")
        elif np.any(X < 0):
            raise ValueError("MultinomialNB yeu cau dac trung khong am")

        joint_log_likelihood = X @ self.feature_log_prob_.T + self.class_log_prior_
        return joint_log_likelihood - logsumexp(joint_log_likelihood, axis=1)[:, None]

    def predict_proba(self, X):
        """Tra ve xac suat hau nghiem theo thu tu classes_."""
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        """Chon lop co log-xac-suat hau nghiem lon nhat."""
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]


def normalize_texts(texts: Iterable[object]) -> np.ndarray:
    """Chuan hoa tung van ban va giu gia tri thieu thanh chuoi rong."""
    normalized = []
    for value in texts:
        if pd.isna(value):
            normalized.append("")
        elif isinstance(value, str):
            normalized.append(str(normalize_text(value)))
        else:
            raise TypeError("Moi van ban phai la chuoi hoac gia tri thieu")
    return np.asarray(normalized, dtype=object)


def make_text_transformer(feature_mode: str = "word") -> Pipeline:
    """Tao pipeline chuan hoa va TF-IDF, de fit rieng trong tung fold."""
    if feature_mode not in {"word", "combined"}:
        raise ValueError("feature_mode phai la 'word' hoac 'combined'")

    word_vectorizer = TfidfVectorizer(
        tokenizer=vietnamese_word_tokenize,
        token_pattern=None,
        lowercase=False,
        ngram_range=(1, 2),
    )
    if feature_mode == "word":
        vectorizer = word_vectorizer
    else:
        vectorizer = FeatureUnion(
            [
                ("word", word_vectorizer),
                (
                    "char",
                    TfidfVectorizer(
                        analyzer="char",
                        lowercase=False,
                        ngram_range=(2, 5),
                    ),
                ),
            ]
        )
    return Pipeline(
        [
            ("normalize", FunctionTransformer(normalize_texts, validate=False)),
            ("tfidf", vectorizer),
        ]
    )


def build_text_pipeline(estimator, feature_mode: str = "word") -> Pipeline:
    """Noi buoc chuan hoa, TF-IDF va classifier thanh mot Pipeline."""
    transformer = make_text_transformer(feature_mode)
    return Pipeline(
        [
            ("normalize", transformer.named_steps["normalize"]),
            ("tfidf", transformer.named_steps["tfidf"]),
            ("classifier", estimator),
        ]
    )


def make_estimators(random_state: int = RANDOM_STATE) -> dict[str, BaseEstimator]:
    """Tao baseline va cac classifier co cau hinh ban dau co dinh."""
    return {
        "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
        "multinomial_nb_numpy": NumpyMultinomialNB(alpha=1.0),
        "multinomial_nb_sklearn": MultinomialNB(alpha=1.0),
        "logistic_regression_balanced": LogisticRegression(
            C=1.0,
            class_weight="balanced",
            max_iter=1000,
            random_state=random_state,
        ),
        "linear_svc_balanced": LinearSVC(
            C=1.0,
            class_weight="balanced",
            random_state=random_state,
        ),
    }
