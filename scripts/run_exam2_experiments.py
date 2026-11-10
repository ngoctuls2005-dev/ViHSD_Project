"""Chay cac thu nghiem mo hinh an toan cho Bai kiem tra 2."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from vihsd.experiment import load_official_frames, run_experiments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fit baseline/classifier va danh gia ViHSD theo split chinh thuc."
    )
    parser.add_argument(
        "--raw-data",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd",
        help="Thu muc DatasetDict da tai; mac dinh data/raw/uitnlp_vihsd.",
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd_provenance.json",
        help="Tep provenance de xac minh revision dataset.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reports" / "exam2_results",
        help="Thu muc ket qua tong hop, khong chua van ban goc.",
    )
    parser.add_argument(
        "--features",
        choices=("word", "combined"),
        default="word",
        help="Word TF-IDF de chay baseline nhanh; combined gom word va char.",
    )
    parser.add_argument("--cv-folds", type=int, default=3)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--skip-group-cv",
        action="store_true",
        help="Bo qua CV theo nhom van ban trung; mac dinh chay ca hai cach chia.",
    )
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = parse_args()
    frames, revision = load_official_frames(args.raw_data, args.provenance)
    print(f"Dataset: uitnlp/vihsd | revision {revision}")
    print(
        "Split da xac minh: "
        + ", ".join(f"{name}={len(frame):,}" for name, frame in frames.items())
    )
    result = run_experiments(
        frames,
        revision,
        args.output_dir,
        feature_mode=args.features,
        n_splits=args.cv_folds,
        include_group_cv=not args.skip_group_cv,
        random_state=args.random_state,
    )
    print("\nKet qua Validation (Macro F1):")
    print(
        result["validation_results"]
        [["model", "train_macro_f1", "validation_macro_f1", "validation_f1_clean", "validation_f1_offensive", "validation_f1_hate"]]
        .sort_values("validation_macro_f1", ascending=False)
        .to_string(index=False, float_format=lambda value: f"{value:.4f}")
    )
    print("\nCV Macro F1 mean/std:")
    cv_columns = [
        "scheme",
        "model",
        "validation_macro_f1_mean",
        "validation_macro_f1_std",
    ]
    print(
        result["cv_summary"][cv_columns].to_string(
            index=False, float_format=lambda value: f"{value:.4f}"
        )
    )
    print("\nMo hinh da khoa truoc khi danh gia Test:", result["selection"]["model"])
    print("Ket qua Test va sensitivity:")
    print(
        result["test_results"]
        [["evaluation", "model", "rows", "rows_removed_for_train_overlap", "macro_f1", "accuracy"]]
        .to_string(index=False, float_format=lambda value: f"{value:.4f}")
    )
    print(f"\nChi ghi bang tong hop an toan vao: {args.output_dir}")
    print("Khong ghi binh luan, van ban mau, hay du doan theo tung dong.")


if __name__ == "__main__":
    main()
