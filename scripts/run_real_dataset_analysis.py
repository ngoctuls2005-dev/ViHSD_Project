"""Tai va phan tich tong hop ViHSD that ma khong xuat binh luan."""

import json
import math
from pathlib import Path
import re
import sys
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from datasets import DatasetDict, load_dataset, load_from_disk
from huggingface_hub import HfApi

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from vihsd.eda import comment_lengths, length_summary
from vihsd.preparation import fit_tfidf_on_train
from vihsd.preprocessing import normalize_series, normalize_text, preprocessing_summary
from vihsd.quality import (
    cross_split_duplicate_audit,
    cross_split_duplicate_summary,
    quality_issue_table,
)


DATASET_ID = "uitnlp/vihsd"
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd"
PROVENANCE_PATH = PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd_provenance.json"
ARTIFACTS_PATH = PROJECT_ROOT / "artifacts" / "real_vihsd"
FIGURES_PATH = PROJECT_ROOT / "reports" / "figures"
TEXT_COLUMN = "free_text"
LABEL_COLUMN = "label_id"
LABEL_NAMES = {0: "CLEAN", 1: "OFFENSIVE", 2: "HATE"}
EXPECTED_ROWS = {"train": 24048, "validation": 2672, "test": 6680}
NEGATION_PATTERN = re.compile(r"(?iu)(?<!\w)(?:không|ko|khong|khum|k0)(?!\w)")
REPEATED_CHARACTER_PATTERN = re.compile(r"(.)\1{2,}", re.DOTALL)
EMOJI_PATTERN = re.compile("[\\U0001F300-\\U0001FAFF\\U00002600-\\U000027BF]")
URL_PATTERN = re.compile(r"(?i)\b(?:https?://|www\.)\S+")


def load_official_splits() -> tuple[DatasetDict, str, str]:
    """Nap split da luu; neu chua co thi tai dung revision hien hanh."""
    if RAW_DATA_PATH.exists():
        dataset = load_from_disk(str(RAW_DATA_PATH))
        if not isinstance(dataset, DatasetDict):
            raise TypeError("Du lieu cuc bo khong phai DatasetDict")
        if PROVENANCE_PATH.exists():
            provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        else:
            info = HfApi().dataset_info(DATASET_ID)
            provenance = {
                "dataset": DATASET_ID,
                "revision": info.sha,
                "last_modified": str(info.lastModified),
                "download_method": "load_dataset",
            }
            write_json(PROVENANCE_PATH, provenance)
        if provenance.get("dataset") != DATASET_ID:
            raise ValueError("Metadata cua ban du lieu cuc bo khong khop")
        return dataset, provenance["revision"], provenance["last_modified"]

    info = HfApi().dataset_info(DATASET_ID)
    revision = info.sha
    # Giu dung repository do nhiem vu yeu cau va ghim revision de tai lap.
    dataset = load_dataset(DATASET_ID, revision=revision)
    if not isinstance(dataset, DatasetDict):
        raise TypeError("Nguon ViHSD can cung cap DatasetDict co ba split")
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset.save_to_disk(str(RAW_DATA_PATH))
    write_json(
        PROVENANCE_PATH,
        {
            "dataset": DATASET_ID,
            "revision": revision,
            "last_modified": str(info.lastModified),
            "download_method": "load_dataset",
        },
    )
    return dataset, revision, str(info.lastModified)


def to_frames(dataset: DatasetDict) -> dict[str, pd.DataFrame]:
    """Kiem tra schema va tao ban DataFrame chi dung trong bo nho."""
    if set(dataset.keys()) != set(EXPECTED_ROWS):
        raise ValueError(f"Split khong dung: {list(dataset.keys())}")
    frames: dict[str, pd.DataFrame] = {}
    for split_name, split in dataset.items():
        if split.column_names != [TEXT_COLUMN, LABEL_COLUMN]:
            raise ValueError(f"Schema bat ngo o {split_name}: {split.column_names}")
        if len(split) != EXPECTED_ROWS[split_name]:
            raise ValueError(
                f"So dong bat ngo o {split_name}: {len(split)} != {EXPECTED_ROWS[split_name]}"
            )
        if split.features[TEXT_COLUMN].dtype != "string":
            raise TypeError(f"Cot {TEXT_COLUMN} khong phai string o {split_name}")
        if split.features[LABEL_COLUMN].dtype != "int64":
            raise TypeError(f"Cot {LABEL_COLUMN} khong phai int64 o {split_name}")
        frame = split.to_pandas()
        values = set(frame[LABEL_COLUMN].dropna().unique().tolist())
        if values != set(LABEL_NAMES):
            raise ValueError(f"Ma nhan bat ngo o {split_name}: {sorted(values)}")
        frames[split_name] = frame
    return frames


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def build_label_counts(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for split_name, frame in frames.items():
        for label_id, label_name in LABEL_NAMES.items():
            count = int((frame[LABEL_COLUMN] == label_id).sum())
            rows.append(
                {
                    "split": split_name,
                    "label_id": label_id,
                    "label": label_name,
                    "count": count,
                    "percent_within_split": count * 100.0 / len(frame),
                }
            )
    return pd.DataFrame(rows)


def build_signal_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Dem dac trung theo lop; chi ghi gia tri tong hop, khong ghi van ban."""
    rows = []
    for split_name, frame in frames.items():
        text = frame[TEXT_COLUMN].fillna("").astype(str)
        upper = text.map(lambda value: sum(char.isupper() for char in value))
        alpha = text.map(lambda value: sum(char.isalpha() for char in value)).clip(lower=1)
        metrics = {
            "contains_negation_marker": text.map(lambda value: bool(NEGATION_PATTERN.search(value))),
            "contains_repeated_character_run_3_plus": text.map(
                lambda value: bool(REPEATED_CHARACTER_PATTERN.search(value))
            ),
            "uppercase_ratio_over_half": (upper / alpha) > 0.5,
            "contains_emoji": text.map(lambda value: bool(EMOJI_PATTERN.search(value))),
            "contains_digit": text.map(lambda value: any(char.isdigit() for char in value)),
            "contains_url": text.map(lambda value: bool(URL_PATTERN.search(value))),
            "contains_exclamation_or_question_run": text.str.contains(r"[!?]{2,}", regex=True),
        }
        lengths = comment_lengths(frame, TEXT_COLUMN, LABEL_COLUMN)
        for label_id, label_name in LABEL_NAMES.items():
            mask = frame[LABEL_COLUMN].eq(label_id).to_numpy()
            label_lengths = lengths.loc[mask]
            for metric_name, present in metrics.items():
                count = int(present.loc[mask].sum())
                rows.append(
                    {
                        "split": split_name,
                        "label_id": label_id,
                        "label": label_name,
                        "feature": metric_name,
                        "count": count,
                        "percent_of_label": count * 100.0 / max(int(mask.sum()), 1),
                        "label_rows": int(mask.sum()),
                    }
                )
            rows.append(
                {
                    "split": split_name,
                    "label_id": label_id,
                    "label": label_name,
                    "feature": "mean_whitespace_token_count",
                    "count": float(label_lengths["whitespace_token_count"].mean()),
                    "percent_of_label": math.nan,
                    "label_rows": int(mask.sum()),
                }
            )
    return pd.DataFrame(rows)


def build_lexical_coverage(features: Any, train_labels: pd.Series) -> pd.DataFrame:
    """Tom tat phu cua n-gram lien quan nhat den tung lop, khong xuat tu."""
    incidence = (features.word_train > 0).astype("int8").tocsr()
    vocabulary = features.word_vectorizer.get_feature_names_out()
    rows = []
    for label_id, label_name in LABEL_NAMES.items():
        target_mask = train_labels.eq(label_id).to_numpy()
        other_mask = ~target_mask
        target_rows = int(target_mask.sum())
        other_rows = int(other_mask.sum())
        if target_rows == 0 or other_rows == 0:
            continue
        target_present = incidence[target_mask]
        other_present = incidence[other_mask]
        target_hits = target_present.getnnz(axis=0)
        other_hits = other_present.getnnz(axis=0)
        minimum_support = min(20, target_rows)
        valid = target_hits >= minimum_support
        if not valid.any():
            continue
        target_odds = (target_hits[valid] + 0.5) / (target_rows - target_hits[valid] + 0.5)
        other_odds = (other_hits[valid] + 0.5) / (other_rows - other_hits[valid] + 0.5)
        enrichment = pd.Series(
            (target_odds / other_odds), index=vocabulary[valid]
        ).sort_values(ascending=False, kind="stable")
        selected_indices = features.word_vectorizer.vocabulary_
        top_terms = enrichment.head(20).index.tolist()
        term_indices = [selected_indices[term] for term in top_terms]
        target_coverage = float((target_present[:, term_indices].getnnz(axis=1) > 0).mean())
        other_coverage = float((other_present[:, term_indices].getnnz(axis=1) > 0).mean())
        rows.append(
            {
                "split_used_for_term_analysis": "train",
                "label_id": label_id,
                "label": label_name,
                "selected_word_unigrams_and_bigrams": len(term_indices),
                "minimum_document_support": minimum_support,
                "documents_in_target_label": target_rows,
                "documents_in_other_labels": other_rows,
                "target_label_coverage_percent": target_coverage * 100.0,
                "other_labels_coverage_percent": other_coverage * 100.0,
                "verbatim_terms_written": False,
            }
        )
    return pd.DataFrame(rows)


def plot_split_label_distribution(label_counts: pd.DataFrame, output_path: Path) -> None:
    pivot = label_counts.pivot(index="label", columns="split", values="percent_within_split")
    pivot = pivot.reindex([LABEL_NAMES[index] for index in LABEL_NAMES])
    pivot = pivot.reindex(columns=["train", "validation", "test"])
    axis = pivot.plot(kind="bar", figsize=(9, 5), color=["#4472C4", "#ED7D31", "#70AD47"])
    axis.set_title("Tỷ lệ nhãn theo tập ViHSD")
    axis.set_xlabel("Nhãn")
    axis.set_ylabel("Tỷ lệ trong tập (%)")
    axis.legend(title="Tập")
    axis.tick_params(axis="x", rotation=0)
    figure = axis.get_figure()
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def write_outputs(
    frames: dict[str, pd.DataFrame],
    revision: str,
    last_modified: str,
    source_version: str,
) -> None:
    ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    labels = build_label_counts(frames)
    lengths_parts = []
    quality_parts = []
    processed_frames: dict[str, pd.DataFrame] = {}
    prep_rows = []
    for split_name, frame in frames.items():
        named_frame = frame.copy()
        named_frame["label_id"] = named_frame[LABEL_COLUMN].map(LABEL_NAMES)
        lengths = comment_lengths(named_frame, TEXT_COLUMN, LABEL_COLUMN)
        lengths.insert(0, "split", split_name)
        lengths["label_id"] = lengths["label"].map(LABEL_NAMES)
        lengths_parts.append(lengths)
        quality = quality_issue_table(
            frame,
            TEXT_COLUMN,
            LABEL_COLUMN,
            list(LABEL_NAMES),
        )
        quality.insert(0, "split", split_name)
        quality_parts.append(quality)
        normalized = normalize_series(frame[TEXT_COLUMN])
        processed_frames[split_name] = pd.DataFrame(
            {TEXT_COLUMN: normalized.fillna("").astype(str), LABEL_COLUMN: frame[LABEL_COLUMN].copy()}
        )
        prep_rows.append(
            {
                "split": split_name,
                **preprocessing_summary(frame[TEXT_COLUMN], normalized),
                "original_missing_text_rows": int(frame[TEXT_COLUMN].isna().sum()),
                "original_blank_text_rows": int(
                    frame[TEXT_COLUMN].fillna("").astype(str).str.strip().eq("").sum()
                ),
            }
        )

    lengths = pd.concat(lengths_parts, ignore_index=True)
    summary = lengths.groupby(["split", "label"], dropna=False).agg(
        sample_count=("character_count", "size"),
        character_mean=("character_count", "mean"),
        character_median=("character_count", "median"),
        character_min=("character_count", "min"),
        character_max=("character_count", "max"),
        whitespace_token_mean=("whitespace_token_count", "mean"),
        whitespace_token_median=("whitespace_token_count", "median"),
    ).reset_index()
    all_lengths = lengths.copy()
    all_lengths["label"] = all_lengths["label"].astype(str)
    summary_all = length_summary(
        all_lengths.rename(columns={"label": "label"})[
            ["label", "character_count", "whitespace_token_count"]
        ]
    )
    quality = pd.concat(quality_parts, ignore_index=True)
    raw_overlaps = cross_split_duplicate_summary(frames, TEXT_COLUMN)
    raw_overlaps.insert(0, "stage", "before_preprocessing")
    processed_overlaps = cross_split_duplicate_summary(processed_frames, TEXT_COLUMN)
    processed_overlaps.insert(0, "stage", "after_preprocessing")
    overlaps = pd.concat([raw_overlaps, processed_overlaps], ignore_index=True)
    detailed_overlaps = pd.concat(
        [
            cross_split_duplicate_audit(
                frames["train"],
                frames["test"],
                TEXT_COLUMN,
                LABEL_COLUMN,
                LABEL_NAMES,
                "before_preprocessing",
            ),
            cross_split_duplicate_audit(
                frames["train"],
                frames["test"],
                TEXT_COLUMN,
                LABEL_COLUMN,
                LABEL_NAMES,
                "after_preprocessing",
                text_transform=normalize_text,
            ),
        ],
        ignore_index=True,
    )
    signals = build_signal_summary(frames)
    processed_quality_parts = []
    for split_name, frame in processed_frames.items():
        processed_quality = quality_issue_table(
            frame,
            TEXT_COLUMN,
            LABEL_COLUMN,
            list(LABEL_NAMES),
        )
        processed_quality.insert(0, "split", split_name)
        processed_quality_parts.append(processed_quality)
    processed_quality = pd.concat(processed_quality_parts, ignore_index=True)

    train = processed_frames["train"]
    validation = processed_frames["validation"]
    test = processed_frames["test"]
    feature_sets = fit_tfidf_on_train(
        train[TEXT_COLUMN].tolist(),
        validation[TEXT_COLUMN].tolist(),
        test[TEXT_COLUMN].tolist(),
        train[LABEL_COLUMN],
        validation[LABEL_COLUMN],
        test[LABEL_COLUMN],
    )
    feature_rows = []
    for split_name in ("train", "validation", "test"):
        word_matrix = getattr(feature_sets, f"word_{split_name}")
        char_matrix = getattr(feature_sets, f"char_{split_name}")
        combined_matrix = getattr(feature_sets, f"combined_{split_name}")
        feature_rows.append(
            {
                "split": split_name,
                "rows": int(combined_matrix.shape[0]),
                "word_features": int(word_matrix.shape[1]),
                "character_features": int(char_matrix.shape[1]),
                "combined_features": int(combined_matrix.shape[1]),
                "word_nonzero_values": int(word_matrix.nnz),
                "character_nonzero_values": int(char_matrix.nnz),
                "combined_nonzero_values": int(combined_matrix.nnz),
                "fit_split": "train",
                "transform_only": split_name != "train",
            }
        )
    lexical_coverage = build_lexical_coverage(feature_sets, feature_sets.y_train)

    schema = {
        "dataset": DATASET_ID,
        "dataset_revision": revision,
        "dataset_last_modified": last_modified,
        "load_source": source_version,
        "columns": [
            {"name": TEXT_COLUMN, "dtype": "string", "meaning": "Binh luan goc tieng Viet"},
            {"name": LABEL_COLUMN, "dtype": "int64", "meaning": "Ma nhan lop"},
        ],
        "label_mapping": {str(code): name for code, name in LABEL_NAMES.items()},
        "label_mapping_note": "Ma nhan int64; nguon khong khai bao ClassLabel metadata.",
        "splits": {name: len(frame) for name, frame in frames.items()},
        "total_rows": sum(len(frame) for frame in frames.values()),
        "raw_comments_written_to_outputs": False,
    }
    write_json(ARTIFACTS_PATH / "schema_and_manifest.json", schema)
    labels.to_csv(ARTIFACTS_PATH / "label_counts.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(ARTIFACTS_PATH / "length_summary_by_split_label.csv", index=False, encoding="utf-8-sig")
    summary_all.to_csv(ARTIFACTS_PATH / "length_summary_all_splits.csv", index=False, encoding="utf-8-sig")
    quality.to_csv(ARTIFACTS_PATH / "quality_issues_by_split.csv", index=False, encoding="utf-8-sig")
    overlaps.to_csv(ARTIFACTS_PATH / "cross_split_duplicates.csv", index=False, encoding="utf-8-sig")
    detailed_overlaps.to_csv(
        ARTIFACTS_PATH / "train_test_duplicate_audit.csv", index=False, encoding="utf-8-sig"
    )
    signals.to_csv(ARTIFACTS_PATH / "text_signals_by_label.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(prep_rows).to_csv(ARTIFACTS_PATH / "preprocessing_comparison.csv", index=False, encoding="utf-8-sig")
    processed_quality.to_csv(ARTIFACTS_PATH / "quality_after_preprocessing.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(feature_rows).to_csv(ARTIFACTS_PATH / "tfidf_dimensions.csv", index=False, encoding="utf-8-sig")
    lexical_coverage.to_csv(ARTIFACTS_PATH / "train_word_ngram_coverage.csv", index=False, encoding="utf-8-sig")

    label_distribution_path = FIGURES_PATH / "vihsd_label_distribution.png"
    length_distribution_path = FIGURES_PATH / "vihsd_comment_length_by_label.png"
    plot_split_label_distribution(labels, label_distribution_path)
    length_groups = [
        lengths.loc[lengths["label"] == label_name, "character_count"].to_numpy()
        for label_name in LABEL_NAMES.values()
    ]
    fig, axis = plt.subplots(figsize=(9, 5))
    axis.boxplot(length_groups, tick_labels=list(LABEL_NAMES.values()), showfliers=False)
    axis.set_title("Độ dài ký tự bình luận theo nhãn ViHSD")
    axis.set_xlabel("Nhãn")
    axis.set_ylabel("Số ký tự")
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(length_distribution_path, dpi=180)
    plt.close(fig)

    print(f"Verified dataset: {DATASET_ID}")
    print(f"Revision recorded: {revision}")
    print(f"Split rows: {schema['splits']} (total={schema['total_rows']})")
    print("Label counts:")
    print(labels.to_string(index=False, formatters={"percent_within_split": "{:.2f}%".format}))
    print("Length summary by label across splits:")
    print(summary_all.to_string(index=False))
    print("Cross-split duplicate counts:")
    print(overlaps.to_string(index=False))
    print("Train/Test affected rows and label conflicts:")
    print(detailed_overlaps.to_string(index=False))
    print("TF-IDF dimensions:")
    print(pd.DataFrame(feature_rows).to_string(index=False))
    print("Preprocessing summary:")
    print(pd.DataFrame(prep_rows).to_string(index=False))
    print("Artifacts contain aggregates only; no comment text was written.")
    print(f"Aggregate outputs: {ARTIFACTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Report figures: {label_distribution_path.relative_to(PROJECT_ROOT)}, {length_distribution_path.relative_to(PROJECT_ROOT)}")


def main() -> None:
    dataset, revision, last_modified = load_official_splits()
    frames = to_frames(dataset)
    write_outputs(frames, revision, last_modified, "local saved DatasetDict" if revision == "local-cache" else DATASET_ID)


if __name__ == "__main__":
    main()
