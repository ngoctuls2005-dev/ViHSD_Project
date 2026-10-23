"""Doc va kiem tra schema du lieu ViHSD."""

from pathlib import Path
from typing import Any

import pandas as pd


def read_csv(path: str | Path, **read_csv_options: Any) -> pd.DataFrame:
    """Doc CSV ma khong tu suy doan ten cot."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Khong tim thay tep du lieu: {csv_path}")
    return pd.read_csv(csv_path, encoding="utf-8-sig", **read_csv_options)


def validate_schema(
    frame: pd.DataFrame,
    text_column: str,
    label_column: str,
) -> dict[str, Any]:
    """Kiem tra cot duoc nguoi dung chi dinh va tra ve mo ta schema."""
    missing = [name for name in (text_column, label_column) if name not in frame.columns]
    if missing:
        available = ", ".join(str(name) for name in frame.columns)
        raise ValueError(
            f"Thieu cot bat buoc {missing}; cac cot hien co: [{available}]"
        )
    return {
        "row_count": int(len(frame)),
        "column_count": int(frame.shape[1]),
        "columns": [str(name) for name in frame.columns],
        "dtypes": {str(name): str(dtype) for name, dtype in frame.dtypes.items()},
        "text_column": text_column,
        "label_column": label_column,
    }


def invalid_label_values(
    labels: pd.Series,
    allowed_labels: set[Any] | tuple[Any, ...] | list[Any],
) -> list[Any]:
    """Tra ve cac gia tri nhan khong nam trong danh sach duoc chi dinh."""
    allowed = set(allowed_labels)
    observed = labels.dropna().unique().tolist()
    return [value for value in observed if value not in allowed]
