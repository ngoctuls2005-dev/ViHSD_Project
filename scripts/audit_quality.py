"""Thong ke van de chat luong va rui ro trung lap giua cac split."""

import argparse
import json
from pathlib import Path

import pandas as pd

from vihsd.data import read_csv, validate_schema
from vihsd.quality import (
    class_balance_summary,
    cross_split_duplicate_summary,
    quality_issue_table,
)


def parse_split(value: str) -> tuple[str, Path]:
    """Doc doi so TEN=DUONG_DAN_CSV."""
    if "=" not in value:
        raise argparse.ArgumentTypeError("Moi split can co dang TEN=DUONG_DAN_CSV")
    name, path = value.split("=", 1)
    if not name or not path:
        raise argparse.ArgumentTypeError("Ten split va duong dan khong duoc rong")
    return name, Path(path)


def parse_args() -> argparse.Namespace:
    """Doc cac tham so can thiet, khong tu doan ten cot/nhan."""
    parser = argparse.ArgumentParser(
        description="Dem van de du lieu ma khong xuat noi dung binh luan."
    )
    parser.add_argument(
        "--split",
        action="append",
        required=True,
        type=parse_split,
        metavar="TEN=CSV",
        help="Khai bao tung split; lap lai cho train, validation, test",
    )
    parser.add_argument("--text-column", required=True, help="Ten cot van ban da xac minh")
    parser.add_argument("--label-column", required=True, help="Ten cot nhan da xac minh")
    parser.add_argument(
        "--allowed-label",
        action="append",
        required=True,
        help="Gia tri nhan hop le; khai bao mot lan cho moi lop",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/quality",
        help="Thu muc dau ra cuc bo; mac dinh la artifacts/quality",
    )
    return parser.parse_args()


def main() -> None:
    """Ghi bang tong hop loi va trung lap ma khong ghi van ban mau."""
    arguments = parse_args()
    split_paths = dict(arguments.split)
    if len(split_paths) != len(arguments.split):
        raise SystemExit("Ten split bi lap; moi split can mot ten rieng")
    frames = {name: read_csv(path) for name, path in split_paths.items()}
    for frame in frames.values():
        validate_schema(frame, arguments.text_column, arguments.label_column)
    combined = pd.concat(frames.values(), ignore_index=True)
    issues = quality_issue_table(
        combined,
        arguments.text_column,
        arguments.label_column,
        arguments.allowed_label,
    )
    balance, ratio = class_balance_summary(
        combined, arguments.label_column, arguments.allowed_label
    )
    overlap = cross_split_duplicate_summary(frames, arguments.text_column)

    output_dir = Path(arguments.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    issues.to_csv(output_dir / "quality_issues.csv", index=False, encoding="utf-8-sig")
    balance.to_csv(output_dir / "class_balance.csv", index=False, encoding="utf-8-sig")
    overlap.to_csv(output_dir / "cross_split_overlap.csv", index=False, encoding="utf-8-sig")
    metadata = {
        "split_row_counts": {name: int(len(frame)) for name, frame in frames.items()},
        "allowed_labels": arguments.allowed_label,
        "majority_minority_ratio": ratio,
        "text_column": arguments.text_column,
        "label_column": arguments.label_column,
        "raw_comment_examples_written": False,
    }
    (output_dir / "audit_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Da luu bang kiem tra chat luong tai: {output_dir}")


if __name__ == "__main__":
    main()
