"""Danh gia classifier va cross-validation tren van ban thuan."""

from __future__ import annotations

from collections import defaultdict
from time import perf_counter
from typing import Iterable, Mapping

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold

from vihsd.models import LABEL_IDS, LABEL_NAMES, make_text_transformer, normalize_texts
from vihsd.preprocessing import normalize_text
from vihsd.quality import normalize_for_duplicate_check


def classification_metrics(y_true, y_pred) -> dict[str, float | int]:
    """Tao chi so tong hop va theo lop, khong kem mau van ban."""
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=list(LABEL_IDS),
        zero_division=0,
    )
    result: dict[str, float | int] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_precision": float(precision_recall_fscore_support(
            y_true, y_pred, labels=list(LABEL_IDS), average="macro", zero_division=0
        )[0]),
        "macro_recall": float(precision_recall_fscore_support(
            y_true, y_pred, labels=list(LABEL_IDS), average="macro", zero_division=0
        )[1]),
        "macro_f1": float(f1_score(
            y_true, y_pred, labels=list(LABEL_IDS), average="macro", zero_division=0
        )),
    }
    for index, label_id in enumerate(LABEL_IDS):
        label = LABEL_NAMES[label_id].lower()
        result[f"precision_{label}"] = float(precision[index])
        result[f"recall_{label}"] = float(recall[index])
        result[f"f1_{label}"] = float(f1[index])
        result[f"support_{label}"] = int(support[index])
    return result


def confusion_matrix_rows(y_true, y_pred, model: str, split: str) -> list[dict[str, int | str]]:
    """Tao cac o ma tran nham lan theo thu tu nhan co dinh."""
    matrix = confusion_matrix(y_true, y_pred, labels=list(LABEL_IDS))
    return [
        {
            "split": split,
            "model": model,
            "true_label": LABEL_NAMES[true_id],
            "predicted_label": LABEL_NAMES[predicted_id],
            "count": int(matrix[row, column]),
        }
        for row, true_id in enumerate(LABEL_IDS)
        for column, predicted_id in enumerate(LABEL_IDS)
    ]


def duplicate_group_ids(texts: Iterable[object]) -> np.ndarray:
    """Gom van ban trung theo khoa da chuan hoa, khong tra noi dung ra ngoai."""
    keys = []
    for index, value in enumerate(texts):
        if pd.isna(value):
            keys.append(("missing", index))
            continue
        normalized = normalize_text(value)
        key = normalize_for_duplicate_check(normalized)
        keys.append(("text", key))
    lookup: dict[tuple[str, object], int] = {}
    group_ids = np.empty(len(keys), dtype=np.int64)
    for index, key in enumerate(keys):
        if key not in lookup:
            lookup[key] = len(lookup)
        group_ids[index] = lookup[key]
    return group_ids


def duplicate_group_summary(texts: Iterable[object], labels) -> dict[str, int]:
    """Dem nhom van ban duy nhat va nhom co nhieu nhan."""
    group_ids = duplicate_group_ids(texts)
    y = np.asarray(labels)
    if len(group_ids) != len(y):
        raise ValueError("So van ban va nhan khong khop")
    label_sets: dict[int, set[object]] = defaultdict(set)
    for group_id, label in zip(group_ids, y):
        label_sets[int(group_id)].add(label.item() if hasattr(label, "item") else label)
    return {
        "rows": int(len(group_ids)),
        "unique_text_groups": int(len(label_sets)),
        "duplicate_excess_rows": int(len(group_ids) - len(label_sets)),
        "conflicting_label_groups": int(sum(len(values) > 1 for values in label_sets.values())),
    }


def make_cv_schemes(n_splits: int = 3, random_state: int = 42):
    """Tao stratified split va grouped split co seed co dinh."""
    if n_splits < 2:
        raise ValueError("n_splits phai tu 2 tro len")
    return {
        "stratified": StratifiedKFold(
            n_splits=n_splits, shuffle=True, random_state=random_state
        ),
        "stratified_group": StratifiedGroupKFold(
            n_splits=n_splits, shuffle=True, random_state=random_state
        ),
    }


def cross_validate_text_models(
    texts,
    labels,
    estimators: Mapping[str, object],
    splitter,
    scheme_name: str,
    feature_mode: str = "word",
    groups=None,
) -> pd.DataFrame:
    """Fit lai TF-IDF ben trong moi fold roi danh gia cac classifier."""
    text_values = np.asarray(list(texts), dtype=object)
    y = np.asarray(labels)
    group_values = None if groups is None else np.asarray(groups)
    if len(text_values) != len(y):
        raise ValueError("So van ban va nhan khong khop")
    if group_values is not None and len(group_values) != len(y):
        raise ValueError("So group va nhan khong khop")

    rows = []
    split_groups = group_values if isinstance(splitter, StratifiedGroupKFold) else None
    for fold_index, (train_index, valid_index) in enumerate(
        splitter.split(text_values, y, groups=split_groups), start=1
    ):
        train_groups = set(group_values[train_index]) if group_values is not None else set()
        valid_groups = set(group_values[valid_index]) if group_values is not None else set()
        overlap_count = len(train_groups & valid_groups)

        # Vectorizer moi duoc fit trong phan train cua fold hien tai.
        transformer = make_text_transformer(feature_mode)
        transform_start = perf_counter()
        train_matrix = transformer.fit_transform(text_values[train_index])
        valid_matrix = transformer.transform(text_values[valid_index])
        transform_seconds = perf_counter() - transform_start
        feature_count = int(train_matrix.shape[1])

        for model_name, estimator in estimators.items():
            model = clone(estimator)
            fit_start = perf_counter()
            model.fit(train_matrix, y[train_index])
            fit_seconds = perf_counter() - fit_start

            predict_start = perf_counter()
            train_pred = model.predict(train_matrix)
            valid_pred = model.predict(valid_matrix)
            predict_seconds = perf_counter() - predict_start

            train_metrics = classification_metrics(y[train_index], train_pred)
            valid_metrics = classification_metrics(y[valid_index], valid_pred)
            row: dict[str, object] = {
                "scheme": scheme_name,
                "fold": fold_index,
                "model": model_name,
                "train_rows": int(len(train_index)),
                "validation_rows": int(len(valid_index)),
                "feature_count": feature_count,
                "duplicate_groups_crossing_fold": int(overlap_count),
                "transform_seconds": float(transform_seconds),
                "fit_seconds": float(fit_seconds),
                "predict_seconds": float(predict_seconds),
            }
            row.update({f"train_{key}": value for key, value in train_metrics.items()})
            row.update({f"validation_{key}": value for key, value in valid_metrics.items()})
            rows.append(row)
    return pd.DataFrame(rows)


def summarize_cross_validation(fold_results: pd.DataFrame) -> pd.DataFrame:
    """Tong hop trung binh va do lech chuan tren cac fold."""
    if fold_results.empty:
        return pd.DataFrame()
    numeric_columns = [
        column
        for column in fold_results.select_dtypes(include=[np.number]).columns
        if column != "fold"
    ]
    summary = (
        fold_results.groupby(["scheme", "model"], sort=False)[numeric_columns]
        .agg(["mean", "std"])
        .reset_index()
    )
    summary.columns = [
        "_".join(str(part) for part in column if part).rstrip("_")
        if isinstance(column, tuple)
        else str(column)
        for column in summary.columns
    ]
    return summary
