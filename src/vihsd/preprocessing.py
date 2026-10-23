"""Tien xu ly van ban bao toan ban goc va thong tin co ich."""

import re
import unicodedata
from typing import Mapping, Sequence

import pandas as pd


DEFAULT_ABBREVIATIONS = {
    "ko": "không",
    "khong": "không",
    "khum": "không",
    "k0": "không",
    "dc": "được",
    "đc": "được",
    "mik": "mình",
    "mn": "mọi người",
    "vs": "với",
}
_TOKEN_PATTERN = re.compile(r"(?u)\b\w+\b")
_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(
    text: object,
    abbreviation_map: Mapping[str, str] | None = None,
) -> object:
    """Chuan Unicode, khoang trang va mo rong tu viet tat dung token."""
    if pd.isna(text):
        return text
    if not isinstance(text, str):
        raise TypeError("Gia tri van ban phai la chuoi hoac gia tri thieu")
    rules = DEFAULT_ABBREVIATIONS if abbreviation_map is None else abbreviation_map
    normalized_rules = {key.casefold(): value for key, value in rules.items()}
    normalized = unicodedata.normalize("NFC", text)
    normalized = _WHITESPACE_PATTERN.sub(" ", normalized).strip()

    def replace_token(match: re.Match[str]) -> str:
        return normalized_rules.get(match.group(0).casefold(), match.group(0))

    return _TOKEN_PATTERN.sub(replace_token, normalized)


def normalize_series(
    texts: pd.Series,
    abbreviation_map: Mapping[str, str] | None = None,
) -> pd.Series:
    """Tao Series moi da xu ly; khong sua Series dau vao."""
    return texts.map(lambda value: normalize_text(value, abbreviation_map))


def compare_text_versions(
    original_texts: Sequence[object] | pd.Series,
    abbreviation_map: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    """Tao bang doi chieu cuc bo; khong luu bang nay vao repository cong khai."""
    originals = list(original_texts)
    processed = [normalize_text(text, abbreviation_map) for text in originals]
    return pd.DataFrame({"original": originals, "processed": processed})


def preprocessing_summary(
    original_texts: Sequence[object] | pd.Series,
    processed_texts: Sequence[object] | pd.Series,
) -> dict[str, int | float]:
    """Thong ke thay doi tong hop ma khong dua noi dung van ban vao ket qua."""
    originals = list(original_texts)
    processed = list(processed_texts)
    if len(originals) != len(processed):
        raise ValueError("So dong truoc va sau xu ly phai bang nhau")
    valid_pairs = [
        (before, after)
        for before, after in zip(originals, processed)
        if isinstance(before, str) and isinstance(after, str)
    ]
    changed = sum(before != after for before, after in valid_pairs)
    original_characters = sum(len(before) for before, _ in valid_pairs)
    processed_characters = sum(len(after) for _, after in valid_pairs)
    return {
        "row_count": len(originals),
        "non_missing_row_count": len(valid_pairs),
        "changed_row_count": changed,
        "changed_row_percent": changed * 100.0 / max(len(valid_pairs), 1),
        "characters_before": original_characters,
        "characters_after": processed_characters,
    }
