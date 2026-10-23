"""Chay EDA cho mot tep CSV duoc chi dinh ro cot van ban va nhan."""

import argparse
import json
from pathlib import Path

from vihsd.data import read_csv, validate_schema
from vihsd.eda import (
    comment_lengths,
    count_labels,
    length_summary,
    plot_comment_lengths,
    plot_label_distribution,
    top_surface_ngrams,
    writing_signal_summary,
)


def parse_args() -> argparse.Namespace:
    """Doc tham so dong lenh."""
    parser = argparse.ArgumentParser(
        description="Thong ke EDA ma khong xuat noi dung binh luan vao bao cao."
    )
    parser.add_argument("--input", required=True, help="Duong dan tep CSV du lieu cuc bo")
    parser.add_argument("--text-column", required=True, help="Ten cot van ban da xac minh")
    parser.add_argument("--label-column", required=True, help="Ten cot nhan da xac minh")
    parser.add_argument(
        "--output-dir",
        default="artifacts/eda",
        help="Thu muc dau ra cuc bo; mac dinh la artifacts/eda",
    )
    return parser.parse_args()


def main() -> None:
    """Doc tep, kiem tra schema va ghi bang/bieu do tong hop."""
    arguments = parse_args()
    frame = read_csv(arguments.input)
    schema = validate_schema(frame, arguments.text_column, arguments.label_column)
    output_dir = Path(arguments.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "schema.json").write_text(
        json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    counts = count_labels(frame, arguments.label_column)
    lengths = comment_lengths(frame, arguments.text_column, arguments.label_column)
    counts.to_csv(output_dir / "label_counts.csv", index=False, encoding="utf-8-sig")
    lengths.to_csv(output_dir / "comment_lengths.csv", index=False, encoding="utf-8-sig")
    length_summary(lengths).to_csv(
        output_dir / "length_summary.csv", index=False, encoding="utf-8-sig"
    )
    top_surface_ngrams(frame, arguments.text_column, arguments.label_column).to_csv(
        output_dir / "surface_ngrams.csv", index=False, encoding="utf-8-sig"
    )
    writing_signal_summary(frame, arguments.text_column).to_csv(
        output_dir / "writing_signals.csv", index=False, encoding="utf-8-sig"
    )
    plot_label_distribution(counts, output_dir / "label_distribution.png")
    plot_comment_lengths(lengths, output_dir / "comment_lengths.png")
    print(f"Da luu bang tong hop va bieu do tai: {output_dir}")


if __name__ == "__main__":
    main()
