"""Tai du lieu va thuc nghiem ViHSD theo ranh gioi development/final-test."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any, Iterable, Mapping

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
DEVELOPMENT_SPLITS = ("train", "validation")
FINAL_TEST_SPLITS = ("train", "test")


def write_json(path: Path, payload: Any) -> None:
    """Ghi metadata tong hop, khong ghi van ban hoac token."""
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def load_official_frames(
    raw_data_path: str | Path,
    provenance_path: str | Path,
    splits: Iterable[str] = DEVELOPMENT_SPLITS,
) -> tuple[dict[str, pd.DataFrame], str]:
    """Tai rieng cac split duoc yeu cau; mac dinh khong truy cap Test."""
    requested_splits = tuple(splits)
    if not requested_splits or len(set(requested_splits)) != len(requested_splits):
        raise ValueError("Can yeu cau cac split khac nhau va khong rong")
    if not set(requested_splits).issubset(EXPECTED_ROWS):
        raise ValueError(f"Split khong duoc ho tro: {requested_splits}")

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
        available_splits = set(dataset.keys())
        missing_splits = set(requested_splits) - available_splits
        if missing_splits:
            raise ValueError(f"Thieu split duoc yeu cau: {sorted(missing_splits)}")
        split_objects = {name: dataset[name] for name in requested_splits}
    else:
        # Hugging Face chi tai split duoc yeu cau; development khong tai nhan Test.
        loaded_splits = load_dataset(
            DATASET_ID,
            revision=DATASET_REVISION,
            split=list(requested_splits),
        )
        if isinstance(loaded_splits, (list, tuple)):
            if len(loaded_splits) != len(requested_splits):
                raise ValueError("So split tai ve khong khop yeu cau")
            split_objects = dict(zip(requested_splits, loaded_splits))
        elif len(requested_splits) == 1:
            split_objects = {requested_splits[0]: loaded_splits}
        else:
            raise TypeError("Hugging Face khong tra ve danh sach split nhu yeu cau")
        revision = DATASET_REVISION

    frames: dict[str, pd.DataFrame] = {}
    for split_name in requested_splits:
        split = split_objects[split_name]
        expected_count = EXPECTED_ROWS[split_name]
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
    return frames, revision


def _fold_class_rows(y, indices, scheme: str, fold: int) -> list[dict[str, int | str]]:
    """Tao thong ke phan bo lop moi fold ma khong hien noi dung."""
    values = np.asarray(y)[indices]
    counts = {label_id: int(np.sum(values == label_id)) for label_id in LABEL_IDS}
    rows = []
    for label_id in LABEL_IDS:
        rows.append(
            {
                "scheme": scheme,
                "fold": fold,
                "label_id": int(label_id),
                "label": LABEL_NAMES[label_id],
                "count": counts[label_id],
                "rows": int(len(indices)),
                "percent": float(counts[label_id] / len(indices) * 100),
            }
        )
    return rows


def _group_cv_diagnostics(texts, labels, splitter, n_splits: int) -> pd.DataFrame:
    """Kiem tra group khong cat ngang fold va ghi phan bo lop tong hop."""
    groups = duplicate_group_ids(texts)
    y = np.asarray(labels)
    rows = []
    for fold_index, (train_index, valid_index) in enumerate(
        splitter.split(np.zeros(len(y)), y, groups=groups), start=1
    ):
        overlap = set(groups[train_index]) & set(groups[valid_index])
        if overlap:
            raise AssertionError("StratifiedGroupKFold de group trung cat ngang fold")
        rows.extend(
            _fold_class_rows(y, train_index, "stratified_group_train", fold_index)
        )
        rows.extend(
            _fold_class_rows(y, valid_index, "stratified_group_validation", fold_index)
        )
    if len(rows) != 6 * n_splits:
        raise AssertionError("Thong ke phan bo lop group CV khong day du")
    return pd.DataFrame(rows)


def _plot_results(validation: pd.DataFrame, cv_summary: pd.DataFrame, output_dir: Path) -> None:
    """Ve bieu do metrics tong hop, khong hien thi hoac luu van ban."""
    import matplotlib.pyplot as plt

    ordered = validation.sort_values("validation_macro_f1", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(ordered["model"], ordered["validation_macro_f1"], color="#3274a1")
    ax.set_title("Validation Macro F1 theo mo hinh")
    ax.set_ylabel("Macro F1")
    ax.set_xlabel("Mo hinh")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "validation_macro_f1.png", dpi=160)
    plt.close(fig)

    svc = cv_summary[cv_summary["model"] == "linear_svc_balanced"]
    fig, ax = plt.subplots(figsize=(7, 4))
    scheme_labels = {
        "stratified": "Stratified",
        "stratified_group": "StratifiedGroup",
    }
    available_schemes = [
        scheme for scheme in ("stratified", "stratified_group")
        if scheme in set(svc["scheme"])
    ]
    labels = [scheme_labels[scheme] for scheme in available_schemes]
    means = []
    errors = []
    for scheme in available_schemes:
        row = svc[svc["scheme"] == scheme]
        means.append(float(row["validation_macro_f1_mean"].iloc[0]))
        errors.append(float(row["validation_macro_f1_std"].iloc[0]))
    colors = ["#3274a1" if scheme == "stratified" else "#e1812c" for scheme in available_schemes]
    ax.bar(labels, means, yerr=errors, capsize=5, color=colors)
    ax.set_title("Linear SVC: CV Validation Macro F1")
    ax.set_ylabel("Macro F1 mean ± std")
    ax.set_xlabel("Cach chia fold")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "cv_macro_f1.png", dpi=160)
    plt.close(fig)


def _create_output_dir(output_dir: str | Path) -> Path:
    """Tao thu muc moi va dung neu duong dan da ton tai de tranh ghi de."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=False)
    return output


def run_development_experiments(
    frames: Mapping[str, pd.DataFrame],
    revision: str,
    output_dir: str | Path,
    feature_mode: str = "word",
    n_splits: int = 3,
    include_group_cv: bool = True,
    random_state: int = 42,
) -> dict[str, Any]:
    """Chay Train/CV/Validation; ham nay khong nhan hoac doc split Test."""
    if set(frames) != set(DEVELOPMENT_SPLITS):
        raise ValueError("Development chi nhan hai split Train va Validation")
    output = _create_output_dir(output_dir)
    train = frames["train"]
    validation = frames["validation"]
    estimators = make_estimators(random_state)
    x_train = train[TEXT_COLUMN].tolist()
    y_train = train[LABEL_COLUMN].to_numpy()
    x_validation = validation[TEXT_COLUMN].tolist()
    y_validation = validation[LABEL_COLUMN].to_numpy()

    group_summary = duplicate_group_summary(x_train, y_train)
    groups = duplicate_group_ids(x_train)
    scheme_objects = make_cv_schemes(n_splits=n_splits, random_state=random_state)
    selected_schemes = ["stratified"] + (
        ["stratified_group"] if include_group_cv else []
    )
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
            output / "cv_group_class_distribution.csv",
            index=False,
            encoding="utf-8-sig",
        )

    # Fit TF-IDF chi tren Train, sau do chi transform Validation.
    transformer = make_text_transformer(feature_mode)
    transform_start = perf_counter()
    train_matrix = transformer.fit_transform(x_train)
    validation_matrix = transformer.transform(x_validation)
    transform_seconds = perf_counter() - transform_start
    validation_rows = []
    confusion_rows = []
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
        row.update(
            {
                f"train_{key}": value
                for key, value in classification_metrics(y_train, train_pred).items()
            }
        )
        row.update(
            {
                f"validation_{key}": value
                for key, value in classification_metrics(
                    y_validation, validation_pred
                ).items()
            }
        )
        validation_rows.append(row)
        confusion_rows.extend(
            confusion_matrix_rows(y_validation, validation_pred, model_name, "validation")
        )

    validation_results = pd.DataFrame(validation_rows)
    validation_results.to_csv(
        output / "validation_model_metrics.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(confusion_rows).to_csv(
        output / "validation_confusion_matrix.csv",
        index=False,
        encoding="utf-8-sig",
    )

    best_index = int(validation_results["validation_macro_f1"].to_numpy().argmax())
    selection = {
        "experiment_mode": "development",
        "model": str(validation_results.iloc[best_index]["model"]),
        "model_parameters": {
            str(name): value
            for name, value in estimators[
                str(validation_results.iloc[best_index]["model"])
            ].get_params(deep=False).items()
        },
        "selection_metric": "validation_macro_f1",
        "selection_value": float(
            validation_results.iloc[best_index]["validation_macro_f1"]
        ),
        "feature_mode": feature_mode,
        "dataset_revision": revision,
        "random_state": random_state,
        "selected_before_test_evaluation": True,
    }
    write_json(output / "selection.json", selection)
    _plot_results(validation_results, cv_summary, output)

    manifest = {
        "mode": "development",
        "dataset": DATASET_ID,
        "revision": revision,
        "splits_loaded": {
            "train": int(len(train)),
            "validation": int(len(validation)),
        },
        "feature_mode": feature_mode,
        "cv_schemes": selected_schemes,
        "cv_folds": n_splits,
        "random_state": random_state,
        "cv_train_duplicate_groups": group_summary,
        "feature_count": int(train_matrix.shape[1]),
        "selection": selection,
        "test_data_loaded": False,
        "test_evaluated": False,
        "raw_text_or_per_row_predictions_written": False,
    }
    write_json(output / "run_manifest.json", manifest)
    return {
        "selection": selection,
        "validation_results": validation_results,
        "cv_summary": cv_summary,
        "group_summary": group_summary,
        "manifest": manifest,
        "output_dir": output,
    }


def load_locked_config(path: str | Path, revision: str = DATASET_REVISION) -> dict[str, Any]:
    """Nap cau hinh da khoa va khong chon lai model trong final-test."""
    config = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return load_locked_config_from_mapping(config, revision)


def run_final_test(
    train: pd.DataFrame,
    test: pd.DataFrame,
    revision: str,
    locked_config: Mapping[str, Any],
    output_dir: str | Path,
) -> dict[str, Any]:
    """Danh gia duy nhat cau hinh khoa; khong nhan Validation de chon model."""
    config = dict(locked_config)
    validated_config = load_locked_config_from_mapping(config, revision)
    output = _create_output_dir(output_dir)
    model_name = str(validated_config["model"])
    feature_mode = str(validated_config["feature_mode"])
    estimators = make_estimators()

    x_train = train[TEXT_COLUMN].tolist()
    y_train = train[LABEL_COLUMN].to_numpy()
    x_test = test[TEXT_COLUMN].tolist()
    y_test = test[LABEL_COLUMN].to_numpy()
    estimator = clone(estimators[model_name])
    estimator.set_params(**validated_config["model_parameters"])
    pipeline = build_text_pipeline(estimator, feature_mode)
    fit_start = perf_counter()
    pipeline.fit(x_train, y_train)
    fit_seconds = perf_counter() - fit_start
    predict_start = perf_counter()
    test_predictions = pipeline.predict(x_test)
    predict_seconds = perf_counter() - predict_start

    # Mask chi dua tren khoa van ban; nhan Test chi tinh metrics sau khi mask co dinh.
    combined_groups = duplicate_group_ids(x_train + x_test)
    train_group_set = set(combined_groups[: len(x_train)])
    test_group_ids = combined_groups[len(x_train) :]
    no_train_overlap_mask = np.asarray(
        [group_id not in train_group_set for group_id in test_group_ids], dtype=bool
    )
    sensitivity_y = y_test[no_train_overlap_mask]
    sensitivity_predictions = test_predictions[no_train_overlap_mask]

    result_rows = [
        {
            "evaluation": "official_test",
            "model": model_name,
            "rows": int(len(y_test)),
            "rows_removed_for_train_overlap": 0,
            **classification_metrics(y_test, test_predictions),
            "fit_seconds": float(fit_seconds),
            "predict_seconds": float(predict_seconds),
        },
        {
            "evaluation": "sensitivity_no_train_text_overlap",
            "model": model_name,
            "rows": int(len(sensitivity_y)),
            "rows_removed_for_train_overlap": int(len(y_test) - len(sensitivity_y)),
            **classification_metrics(sensitivity_y, sensitivity_predictions),
            "fit_seconds": float(fit_seconds),
            "predict_seconds": float(predict_seconds),
        },
    ]
    confusion_rows = confusion_matrix_rows(
        y_test, test_predictions, model_name, "official_test"
    )
    confusion_rows.extend(
        confusion_matrix_rows(
            sensitivity_y,
            sensitivity_predictions,
            model_name,
            "sensitivity_no_train_text_overlap",
        )
    )
    pd.DataFrame(result_rows).to_csv(
        output / "test_metrics.csv", index=False, encoding="utf-8-sig"
    )
    pd.DataFrame(confusion_rows).to_csv(
        output / "test_confusion_matrix.csv", index=False, encoding="utf-8-sig"
    )
    write_json(output / "locked_config.json", validated_config)
    manifest = {
        "mode": "final-test",
        "dataset": DATASET_ID,
        "revision": revision,
        "splits_loaded": {"train": int(len(train)), "test": int(len(test))},
        "model": model_name,
        "feature_mode": feature_mode,
        "selection_metric": validated_config["selection_metric"],
        "selection_value": validated_config["selection_value"],
        "selection_recomputed": False,
        "test_scored_once_in_this_final_run": True,
        "test_sensitivity_rows": int(len(sensitivity_y)),
        "test_sensitivity_removed_rows": int(len(y_test) - len(sensitivity_y)),
        "raw_text_or_per_row_predictions_written": False,
    }
    write_json(output / "run_manifest.json", manifest)
    return {
        "test_results": pd.DataFrame(result_rows),
        "manifest": manifest,
        "output_dir": output,
    }


def load_locked_config_from_mapping(
    config: Mapping[str, Any], revision: str = DATASET_REVISION
) -> dict[str, Any]:
    """Xac nhan cau hinh da khoa tu object ma khong doc them du lieu."""
    if config.get("model") not in make_estimators():
        raise ValueError("Model trong locked config khong hop le")
    model_name = str(config["model"])
    estimator = make_estimators()[model_name]
    model_parameters = config.get("model_parameters")
    if not isinstance(model_parameters, Mapping):
        raise ValueError("Locked config phai co snapshot model_parameters")
    expected_parameter_names = set(estimator.get_params(deep=False))
    if set(model_parameters) != expected_parameter_names:
        raise ValueError("model_parameters khong day du tham so classifier")
    try:
        json.dumps(dict(model_parameters), allow_nan=False)
        estimator.set_params(**dict(model_parameters))
    except (TypeError, ValueError) as error:
        raise ValueError("model_parameters trong locked config khong hop le") from error
    if config.get("feature_mode") not in {"word", "combined"}:
        raise ValueError("feature_mode trong locked config khong hop le")
    if config.get("selection_metric") != "validation_macro_f1":
        raise ValueError("Locked config phai duoc chon bang validation_macro_f1")
    if config.get("selected_before_test_evaluation") is not True:
        raise ValueError("Locked config chua xac nhan chon truoc khi danh gia Test")
    if "dataset_revision" in config and config["dataset_revision"] != revision:
        raise ValueError("Revision trong locked config khong khop du lieu")
    try:
        selection_value = float(config["selection_value"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Locked config thieu validation score hop le") from error
    if not np.isfinite(selection_value) or not 0 <= selection_value <= 1:
        raise ValueError("Validation score trong locked config khong hop le")
    validated = dict(config)
    validated["model_parameters"] = dict(model_parameters)
    return validated
