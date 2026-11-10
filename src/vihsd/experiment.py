"""Tai, xac minh va danh gia ViHSD cho Bai kiem tra 2."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import pandas as pd
from datasets import DatasetDict, load_dataset, load_from_disk
from sklearn.base import clone

from vihsd.data import validate_schema
from vihsd.model_evaluation import (
    classification_metrics,
    confusion_matrix_rows,
    cross_validate_text_models,
    duplicate_group_ids,
    duplicate_group_summary,
    make_cv_schemes,
    summarize_cross_validation,
)
from vihsd.models import (
    LABEL_IDS,
    LABEL_NAMES,
    build_text_pipeline,
    make_estimators,
    make_text_transformer,
)


DATASET_ID = "uitnlp/vihsd"
DATASET_REVISION = "88e81b36ca376867640dad9df295e0f7d499ab80"
TEXT_COLUMN = "free_text"
LABEL_COLUMN = "label_id"
EXPECTED_ROWS = {"train": 24048, "validation": 2672, "test": 6680}


def write_json(path: Path, payload: Any) -> None:
    """Ghi metadata tong hop, khong ghi van ban hoac token."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def load_official_frames(
    raw_data_path: str | Path,
    provenance_path: str | Path,
) -> tuple[dict[str, pd.DataFrame], str]:
    """Nap split da duoc phe duyet va kiem tra revision/schema/nhan."""
    raw_path = Path(raw_data_path)
    provenance_file = Path(provenance_path)
    if raw_path.exists():
        dataset = load_from_disk(str(raw_path))
        if not isinstance(dataset, DatasetDict):
            raise TypeError("Du lieu cuc bo khong phai DatasetDict")
        if not provenance_file.is_file():
            raise FileNotFoundError(
                "Thieu data/raw/uitnlp_vihsd_provenance.json de xac minh revision"
            )
        provenance = json.loads(provenance_file.read_text(encoding="utf-8"))
        if provenance.get("dataset") != DATASET_ID:
            raise ValueError("Nguon trong provenance khong khop dataset ViHSD")
        revision = provenance.get("revision")
        if revision != DATASET_REVISION:
            raise ValueError(
                f"Revision dataset khong khop: {revision!r} != {DATASET_REVISION}"
            )
    else:
        dataset = load_dataset(DATASET_ID, revision=DATASET_REVISION)
        if not isinstance(dataset, DatasetDict):
            raise TypeError("Nguon ViHSD can cung cap DatasetDict")
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        dataset.save_to_disk(str(raw_path))
        write_json(
            provenance_file,
            {"dataset": DATASET_ID, "revision": DATASET_REVISION, "download_method": "load_dataset"},
        )

    if set(dataset.keys()) != set(EXPECTED_ROWS):
        raise ValueError(f"Split khong dung: {sorted(dataset.keys())}")
    frames: dict[str, pd.DataFrame] = {}
    for split_name, expected_count in EXPECTED_ROWS.items():
        split = dataset[split_name]
        if len(split) != expected_count:
            raise ValueError(f"So dong bat ngo o {split_name}: {len(split)}")
        if split.column_names != [TEXT_COLUMN, LABEL_COLUMN]:
            raise ValueError(f"Schema bat ngo o {split_name}: {split.column_names}")
        if split.features[TEXT_COLUMN].dtype != "string":
            raise TypeError(f"{TEXT_COLUMN} khong co kieu string o {split_name}")
        if split.features[LABEL_COLUMN].dtype != "int64":
            raise TypeError(f"{LABEL_COLUMN} khong co kieu int64 o {split_name}")
        frame = split.to_pandas()
        validate_schema(frame, TEXT_COLUMN, LABEL_COLUMN)
        observed = set(frame[LABEL_COLUMN].dropna().unique().tolist())
        if observed != set(LABEL_IDS):
            raise ValueError(f"Ma nhan bat ngo o {split_name}: {sorted(observed)}")
        frames[split_name] = frame
    return frames, DATASET_REVISION


def _fold_class_rows(y, indices, scheme: str, fold: int) -> list[dict[str, int | str]]:
    """Tao thong ke phan bo lop moi fold ma khong hien noi dung."""
    values = np.asarray(y)[indices]
    rows = []
    for label_id in LABEL_IDS:
        count = int(np.count_nonzero(values == label_id))
        rows.append(
            {
                "scheme": scheme,
                "fold": fold,
                "label_id": label_id,
                "label": LABEL_NAMES[label_id],
                "count": count,
                "rows": int(len(values)),
                "percent": count * 100.0 / max(len(values), 1),
            }
        )
    return rows


def _group_cv_diagnostics(texts, labels, splitter, n_splits: int) -> pd.DataFrame:
    """Thong ke group/fold va xac nhan khong co group cat ngang fold."""
    groups = duplicate_group_ids(texts)
    rows = []
    for fold, (train_index, valid_index) in enumerate(
        splitter.split(np.zeros(len(labels)), labels, groups=groups), start=1
    ):
        overlap = set(groups[train_index]) & set(groups[valid_index])
        if overlap:
            raise AssertionError("StratifiedGroupKFold de group trung cat ngang fold")
        rows.extend(_fold_class_rows(labels, train_index, "stratified_group_train", fold))
        rows.extend(_fold_class_rows(labels, valid_index, "stratified_group_validation", fold))
    return pd.DataFrame(rows)


def _plot_results(validation: pd.DataFrame, cv_summary: pd.DataFrame, output_dir: Path) -> None:
    """Ve bieu do chi tu diem tong hop, khong dua van ban vao hinh."""
    import matplotlib.pyplot as plt

    output_dir.mkdir(parents=True, exist_ok=True)
    ordered = validation.sort_values("validation_macro_f1", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(ordered["model"], ordered["validation_macro_f1"], color="#315f86")
    ax.set_ylabel("Macro F1")
    ax.set_xlabel("Mô hình")
    ax.set_title("So sánh mô hình trên Validation ViHSD")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "validation_macro_f1.png", dpi=160)
    plt.close(fig)

    if not cv_summary.empty:
        score_column = "validation_macro_f1_mean"
        if score_column in cv_summary:
            pivot = cv_summary.pivot(index="model", columns="scheme", values=score_column)
            ax = pivot.plot(kind="bar", figsize=(10, 5.5), color=["#4477aa", "#cc6677"])
            ax.set_ylabel("Macro F1 trung bình trên các fold")
            ax.set_xlabel("Mô hình")
            ax.set_title("Cross-validation trên Train")
            ax.grid(axis="y", alpha=0.25)
            ax.figure.tight_layout()
            ax.figure.savefig(output_dir / "cv_macro_f1.png", dpi=160)
            plt.close(ax.figure)


def run_experiments(
    frames: dict[str, pd.DataFrame],
    revision: str,
    output_dir: str | Path,
    feature_mode: str = "word",
    n_splits: int = 3,
    include_group_cv: bool = True,
    random_state: int = 42,
) -> dict[str, Any]:
    """Chay CV, chon tren Validation, roi cham Test dung mot lan."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    train = frames["train"]
    validation = frames["validation"]
    test = frames["test"]
    estimators = make_estimators(random_state)
    x_train = train[TEXT_COLUMN].tolist()
    y_train = train[LABEL_COLUMN].to_numpy()
    x_validation = validation[TEXT_COLUMN].tolist()
    y_validation = validation[LABEL_COLUMN].to_numpy()
    x_test = test[TEXT_COLUMN].tolist()
    y_test = test[LABEL_COLUMN].to_numpy()

    group_summary = duplicate_group_summary(x_train, y_train)
    groups = duplicate_group_ids(x_train)
    scheme_objects = make_cv_schemes(n_splits=n_splits, random_state=random_state)
    selected_schemes = ["stratified"] + (["stratified_group"] if include_group_cv else [])
    fold_tables = []
    group_diagnostics = pd.DataFrame()
    for scheme_name in selected_schemes:
        splitter = scheme_objects[scheme_name]
        fold_tables.append(
            cross_validate_text_models(
                x_train,
                y_train,
                estimators,
                splitter,
                scheme_name,
                feature_mode=feature_mode,
                groups=groups,
            )
        )
        if scheme_name == "stratified_group":
            group_diagnostics = _group_cv_diagnostics(
                x_train, y_train, splitter, n_splits
            )

    fold_results = pd.concat(fold_tables, ignore_index=True)
    cv_summary = summarize_cross_validation(fold_results)
    fold_results.to_csv(output / "cv_folds.csv", index=False, encoding="utf-8-sig")
    cv_summary.to_csv(output / "cv_summary.csv", index=False, encoding="utf-8-sig")
    if not group_diagnostics.empty:
        group_diagnostics.to_csv(
            output / "cv_group_class_distribution.csv", index=False, encoding="utf-8-sig"
        )

    # Dung cung mot ma tran train/validation da fit chi tren Train de so sanh model.
    transformer = make_text_transformer(feature_mode)
    transform_start = perf_counter()
    train_matrix = transformer.fit_transform(x_train)
    validation_matrix = transformer.transform(x_validation)
    transform_seconds = perf_counter() - transform_start
    validation_rows = []
    confusion_rows = []
    validation_models = {}
    for model_name, estimator in estimators.items():
        model = clone(estimator)
        fit_start = perf_counter()
        model.fit(train_matrix, y_train)
        fit_seconds = perf_counter() - fit_start
        train_pred = model.predict(train_matrix)
        validation_pred = model.predict(validation_matrix)
        row: dict[str, object] = {
            "model": model_name,
            "feature_mode": feature_mode,
            "feature_count": int(train_matrix.shape[1]),
            "train_rows": int(len(y_train)),
            "validation_rows": int(len(y_validation)),
            "transform_seconds": float(transform_seconds),
            "fit_seconds": float(fit_seconds),
        }
        row.update({f"train_{key}": value for key, value in classification_metrics(y_train, train_pred).items()})
        row.update({f"validation_{key}": value for key, value in classification_metrics(y_validation, validation_pred).items()})
        validation_rows.append(row)
        confusion_rows.extend(
            confusion_matrix_rows(y_validation, validation_pred, model_name, "validation")
        )
        validation_models[model_name] = model

    validation_results = pd.DataFrame(validation_rows)
    validation_results.to_csv(
        output / "validation_model_metrics.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(confusion_rows).to_csv(
        output / "validation_confusion_matrix.csv", index=False, encoding="utf-8-sig"
    )

    # Chot mo hinh theo Macro F1 Validation truoc khi doc nhan Test.
    best_index = int(validation_results["validation_macro_f1"].to_numpy().argmax())
    selected_model = str(validation_results.iloc[best_index]["model"])
    selection = {
        "model": selected_model,
        "selection_metric": "validation_macro_f1",
        "selection_value": float(validation_results.iloc[best_index]["validation_macro_f1"]),
        "feature_mode": feature_mode,
        "selected_before_test_evaluation": True,
    }
    write_json(output / "selection.json", selection)

    final_pipeline = build_text_pipeline(clone(estimators[selected_model]), feature_mode)
    final_fit_start = perf_counter()
    final_pipeline.fit(x_train, y_train)
    final_fit_seconds = perf_counter() - final_fit_start
    # Test duoc du doan mot lan sau khi da khoa model va feature_mode.
    test_predict_start = perf_counter()
    test_predictions = final_pipeline.predict(x_test)
    test_predict_seconds = perf_counter() - test_predict_start

    # Khoa nhan duoc xac dinh tu van ban Train/Test, khong doc nhan Test de loc dong.
    combined_groups = duplicate_group_ids(x_train + x_test)
    train_group_set = set(combined_groups[: len(x_train)])
    test_group_ids = combined_groups[len(x_train) :]
    no_train_overlap_mask = np.asarray(
        [group_id not in train_group_set for group_id in test_group_ids], dtype=bool
    )
    test_result_rows = []
    test_confusion_rows = []
    test_result_rows.append(
        {
            "evaluation": "official_test",
            "model": selected_model,
            "rows": int(len(y_test)),
            "rows_removed_for_train_overlap": 0,
            **classification_metrics(y_test, test_predictions),
            "fit_seconds": float(final_fit_seconds),
            "predict_seconds": float(test_predict_seconds),
        }
    )
    test_confusion_rows.extend(
        confusion_matrix_rows(y_test, test_predictions, selected_model, "official_test")
    )
    # Nhãn Test chi duoc dung de tinh chi so sau khi mask van ban da co dinh.
    sensitivity_y = y_test[no_train_overlap_mask]
    sensitivity_predictions = test_predictions[no_train_overlap_mask]
    test_result_rows.append(
        {
            "evaluation": "sensitivity_no_train_text_overlap",
            "model": selected_model,
            "rows": int(len(sensitivity_y)),
            "rows_removed_for_train_overlap": int(len(y_test) - len(sensitivity_y)),
            **classification_metrics(sensitivity_y, sensitivity_predictions),
            "fit_seconds": float(final_fit_seconds),
            "predict_seconds": float(test_predict_seconds),
        }
    )
    test_confusion_rows.extend(
        confusion_matrix_rows(
            sensitivity_y,
            sensitivity_predictions,
            selected_model,
            "sensitivity_no_train_text_overlap",
        )
    )
    pd.DataFrame(test_result_rows).to_csv(
        output / "test_metrics.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(test_confusion_rows).to_csv(
        output / "test_confusion_matrix.csv", index=False, encoding="utf-8-sig"
    )

    _plot_results(validation_results, cv_summary, output)
    manifest = {
        "dataset": DATASET_ID,
        "revision": revision,
        "splits": {name: int(len(frame)) for name, frame in frames.items()},
        "feature_mode": feature_mode,
        "cv_schemes": selected_schemes,
        "cv_folds": n_splits,
        "random_state": random_state,
        "cv_train_duplicate_groups": group_summary,
        "feature_count": int(train_matrix.shape[1]),
        "selection": selection,
        "test_scored_once_after_selection": True,
        "test_sensitivity_rows": int(len(sensitivity_y)),
        "test_sensitivity_removed_rows": int(len(y_test) - len(sensitivity_y)),
        "raw_text_or_per_row_predictions_written": False,
    }
    write_json(output / "run_manifest.json", manifest)
    return {
        "selection": selection,
        "validation_results": validation_results,
        "cv_summary": cv_summary,
        "test_results": pd.DataFrame(test_result_rows),
        "group_summary": group_summary,
        "manifest": manifest,
    }
