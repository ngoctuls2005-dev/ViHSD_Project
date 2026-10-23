"""Phat hien van de chat luong ma khong xuat mau binh luan that."""

from itertools import combinations
import re
import unicodedata
from typing import Any, Mapping, Sequence

import pandas as pd

from vihsd.data import validate_schema


_REPEATED_CHARACTER_PATTERN = re.compile(r"(.)\1{2,}", re.DOTALL)
_CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_DEFAULT_TEENCODE_TERMS = ("ko", "khong", "khum", "k0", "dc", "đc", "mik", "mn", "vs")


def normalize_for_duplicate_check(value: Any) -> str | None:
    """Chuan hoa NFC, khoang trang va chu hoa chi de doi chieu trung lap."""
    if pd.isna(value):
        return None
    normalized = unicodedata.normalize("NFC", str(value))
    return re.sub(r"\s+", " ", normalized).strip().casefold()


def quality_issue_table(
    frame: pd.DataFrame,
    text_column: str,
    label_column: str,
    valid_labels: Sequence[Any],
) -> pd.DataFrame:
    """Thong ke loi du lieu va chi dung vi du an toan dang nhan."""
    validate_schema(frame, text_column, label_column)
    text = frame[text_column]
    labels = frame[label_column]
    text_strings = text.fillna("").astype(str)
    normalized = text.map(normalize_for_duplicate_check)
    usable_text = normalized.notna() & normalized.ne("")
    duplicate_mask = normalized[usable_text].duplicated(keep="first")
    duplicate_excess = int(duplicate_mask.sum())

    duplicate_rows = pd.DataFrame(
        {"normalized_text": normalized, "label": labels}
    ).loc[usable_text]
    conflicting_groups = duplicate_rows.groupby("normalized_text", sort=False).filter(
        lambda group: group["label"].dropna().nunique() > 1
    )

    label_values = set(valid_labels)
    invalid_mask = labels.notna() & ~labels.isin(label_values)
    nonblank_lengths = text_strings.loc[text.notna() & text_strings.str.strip().ne("")].str.len()
    if len(nonblank_lengths) >= 4:
        first_quartile = nonblank_lengths.quantile(0.25)
        third_quartile = nonblank_lengths.quantile(0.75)
        spread = third_quartile - first_quartile
        outlier_count = int(
            ((nonblank_lengths < first_quartile - 1.5 * spread)
             | (nonblank_lengths > third_quartile + 1.5 * spread)).sum()
        )
    else:
        outlier_count = 0

    teencode_pattern = re.compile(
        r"(?u)(?<!\w)(?:" + "|".join(re.escape(term) for term in _DEFAULT_TEENCODE_TERMS) + r")(?!\w)",
        re.IGNORECASE,
    )
    records = [
        ("missing_text", int(text.isna().sum()), "<gia tri thieu>"),
        (
            "blank_text",
            int((text.notna() & text_strings.str.strip().eq("")).sum()),
            "<chuoi rong hoac chi co khoang trang>",
        ),
        ("missing_label", int(labels.isna().sum()), "<gia tri nhan thieu>"),
        (
            "non_string_text",
            int(text.dropna().map(lambda value: not isinstance(value, str)).sum()),
            "<kieu du lieu khong phai chuoi>",
        ),
        ("duplicate_text_excess_rows", duplicate_excess, "[noi dung binh luan da luoc bo]"),
        (
            "conflicting_duplicate_rows",
            int(len(conflicting_groups)),
            "[noi dung da luoc bo; nhan khac nhau]",
        ),
        ("invalid_label", int(invalid_mask.sum()), "<nhan ngoai danh sach cho phep>"),
        (
            "control_character_text",
            int(text_strings.map(lambda value: bool(_CONTROL_CHARACTER_PATTERN.search(value))).sum()),
            "[chuoi co ky tu dieu khien; noi dung da luoc bo]",
        ),
        (
            "repeated_character_run_3_plus",
            int(text_strings.map(lambda value: bool(_REPEATED_CHARACTER_PATTERN.search(value))).sum()),
            "[chuoi co ky tu lap; noi dung da luoc bo]",
        ),
        (
            "teencode_term_rows",
            int(text_strings.map(lambda value: bool(teencode_pattern.search(value))).sum()),
            "[chuoi co tu viet tat; noi dung da luoc bo]",
        ),
        ("length_outlier_tukey", outlier_count, "[do dai ngoai le; noi dung da luoc bo]"),
    ]
    denominator = max(len(frame), 1)
    return pd.DataFrame(
        [
            {
                "issue": issue,
                "count": count,
                "percent_of_rows": count * 100.0 / denominator,
                "safe_example": example,
            }
            for issue, count, example in records
        ]
    )


def class_balance_summary(
    frame: pd.DataFrame,
    label_column: str,
    valid_labels: Sequence[Any],
) -> tuple[pd.DataFrame, float | None]:
    """Tra ve so luong theo lop va ti so lop dong/it mau nhat."""
    if label_column not in frame.columns:
        raise ValueError(f"Khong co cot nhan: {label_column}")
    labels = list(valid_labels)
    observed = frame[label_column].value_counts(dropna=True)
    total = int(observed.reindex(labels, fill_value=0).sum())
    rows = []
    for label in labels:
        count = int(observed.get(label, 0))
        rows.append(
            {
                "label": label,
                "sample_count": count,
                "percent_of_valid_labels": count * 100.0 / max(total, 1),
            }
        )
    counts = [row["sample_count"] for row in rows]
    ratio = None if not counts or min(counts) == 0 else max(counts) / min(counts)
    return pd.DataFrame(rows), ratio


def cross_split_duplicate_summary(
    splits: Mapping[str, pd.DataFrame],
    text_column: str,
) -> pd.DataFrame:
    """Dem binh luan trung giua tung cap split, khong tra lai noi dung."""
    if len(splits) < 2:
        return pd.DataFrame(columns=["split_a", "split_b", "shared_unique_texts"])
    normalized_by_split: dict[str, set[str]] = {}
    for split_name, frame in splits.items():
        if text_column not in frame.columns:
            raise ValueError(f"Split {split_name} khong co cot van ban: {text_column}")
        normalized_by_split[split_name] = {
            value
            for value in frame[text_column].map(normalize_for_duplicate_check)
            if value
        }
    rows = []
    for split_a, split_b in combinations(normalized_by_split, 2):
        shared = normalized_by_split[split_a] & normalized_by_split[split_b]
        rows.append(
            {
                "split_a": split_a,
                "split_b": split_b,
                "shared_unique_texts": len(shared),
            }
        )
    return pd.DataFrame(rows)
