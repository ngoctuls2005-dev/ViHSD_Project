"""Thong ke mo ta va ve bieu do EDA cho binh luan."""

from collections import Counter
from pathlib import Path
import re
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


_WORD_PATTERN = re.compile(r"(?u)\b[^\W_]+\b")
_REPEATED_CHARACTER_PATTERN = re.compile(r"(.)\1{2,}", re.DOTALL)
_EMOJI_PATTERN = re.compile(
    "[\\U0001F300-\\U0001FAFF\\U00002600-\\U000027BF]"
)


def count_labels(frame: pd.DataFrame, label_column: str) -> pd.DataFrame:
    """Dem so mau moi nhan, tinh ca gia tri nhan bi thieu."""
    if label_column not in frame.columns:
        raise ValueError(f"Khong co cot nhan: {label_column}")
    counts = frame[label_column].value_counts(dropna=False, sort=False)
    result = counts.rename_axis("label").reset_index(name="count")
    result["label"] = result["label"].map(
        lambda value: "<missing>" if pd.isna(value) else value
    )
    denominator = max(len(frame), 1)
    result["percent"] = result["count"] * 100.0 / denominator
    return result


def comment_lengths(
    frame: pd.DataFrame,
    text_column: str,
    label_column: str,
) -> pd.DataFrame:
    """Tinh do dai ky tu va so don vi tach boi khoang trang moi binh luan."""
    if text_column not in frame.columns or label_column not in frame.columns:
        raise ValueError("Hay kiem tra lai cot van ban va cot nhan da chi dinh")
    text = frame[text_column].fillna("").astype(str)
    return pd.DataFrame(
        {
            "label": frame[label_column].reset_index(drop=True),
            "character_count": text.str.len().to_numpy(),
            "whitespace_token_count": text.map(
                lambda value: len(value.split())
            ).to_numpy(),
        }
    )


def length_summary(lengths: pd.DataFrame) -> pd.DataFrame:
    """Tong hop do dai theo nhan ma khong giu noi dung binh luan."""
    required = {"label", "character_count", "whitespace_token_count"}
    if not required.issubset(lengths.columns):
        raise ValueError(f"Thieu cot trong bang do dai: {sorted(required - set(lengths.columns))}")
    return (
        lengths.groupby("label", dropna=False)
        .agg(
            sample_count=("character_count", "size"),
            character_mean=("character_count", "mean"),
            character_median=("character_count", "median"),
            character_min=("character_count", "min"),
            character_max=("character_count", "max"),
            whitespace_token_mean=("whitespace_token_count", "mean"),
        )
        .reset_index()
    )


def top_surface_ngrams(
    frame: pd.DataFrame,
    text_column: str,
    label_column: str,
    n: int = 1,
    top_k: int = 20,
) -> pd.DataFrame:
    """Dem cum ky tu lien tiep tach theo khoang trang, khong tu nhan la tu tieng Viet."""
    if n < 1 or top_k < 1:
        raise ValueError("n va top_k phai la so nguyen duong")
    if text_column not in frame.columns or label_column not in frame.columns:
        raise ValueError("Hay kiem tra lai cot van ban va cot nhan da chi dinh")
    records: list[dict[str, Any]] = []
    for label, text in zip(frame[label_column], frame[text_column]):
        if pd.isna(label) or pd.isna(text):
            continue
        tokens = _WORD_PATTERN.findall(str(text).casefold())
        ngrams = (" ".join(tokens[index : index + n]) for index in range(len(tokens) - n + 1))
        records.extend({"label": label, "ngram": term} for term in ngrams)
    if not records:
        return pd.DataFrame(columns=["label", "ngram", "count"])
    counts = Counter((row["label"], row["ngram"]) for row in records)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], str(item[0][0]), item[0][1]))
    selected: list[dict[str, Any]] = []
    per_label: Counter[Any] = Counter()
    for (label, ngram), count in ordered:
        if per_label[label] >= top_k:
            continue
        selected.append({"label": label, "ngram": ngram, "count": count})
        per_label[label] += 1
    return pd.DataFrame(selected)


def writing_signal_summary(frame: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Dem mot so dau hieu viet khong chuan ma khong xuat binh luan."""
    if text_column not in frame.columns:
        raise ValueError(f"Khong co cot van ban: {text_column}")
    text = frame[text_column].fillna("").astype(str)
    letter_count = text.map(lambda value: sum(character.isalpha() for character in value))
    uppercase_count = text.map(lambda value: sum(character.isupper() for character in value))
    signals = pd.DataFrame(
        {
            "signal": [
                "repeated_character_run_3_plus",
                "uppercase_ratio_over_half",
                "contains_digit",
                "contains_emoji",
            ],
            "count": [
                int(text.map(lambda value: bool(_REPEATED_CHARACTER_PATTERN.search(value))).sum()),
                int(((letter_count > 0) & (uppercase_count / letter_count.clip(lower=1) > 0.5)).sum()),
                int(text.map(lambda value: any(character.isdigit() for character in value)).sum()),
                int(text.map(lambda value: bool(_EMOJI_PATTERN.search(value))).sum()),
            ],
        }
    )
    signals["percent"] = signals["count"] * 100.0 / max(len(frame), 1)
    return signals


def plot_label_distribution(counts: pd.DataFrame, output_path: str | Path) -> Path:
    """Ve bieu do so mau theo nhan tu bang thong ke da tinh."""
    required = {"label", "count"}
    if not required.issubset(counts.columns):
        raise ValueError("Bang dem can co cot label va count")
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.bar(counts["label"].astype(str), counts["count"], color="#4472C4")
    axis.set_title("Số lượng bình luận theo nhãn")
    axis.set_xlabel("Nhãn")
    axis.set_ylabel("Số bình luận")
    axis.tick_params(axis="x", rotation=15)
    figure.tight_layout()
    figure.savefig(destination, dpi=160)
    plt.close(figure)
    return destination


def plot_comment_lengths(lengths: pd.DataFrame, output_path: str | Path) -> Path:
    """Ve phan bo do dai ky tu theo nhan."""
    required = {"label", "character_count"}
    if not required.issubset(lengths.columns):
        raise ValueError("Bang do dai can co cot label va character_count")
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    groups = [group["character_count"].to_numpy() for _, group in lengths.groupby("label", dropna=False)]
    labels = [str(label) for label, _ in lengths.groupby("label", dropna=False)]
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.boxplot(groups, tick_labels=labels, showfliers=False)
    axis.set_title("Độ dài bình luận theo nhãn")
    axis.set_xlabel("Nhãn")
    axis.set_ylabel("Số ký tự")
    axis.tick_params(axis="x", rotation=15)
    figure.tight_layout()
    figure.savefig(destination, dpi=160)
    plt.close(figure)
    return destination
