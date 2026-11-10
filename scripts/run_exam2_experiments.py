"""Chay thuc nghiem Bai kiem tra 2 voi che do an toan mac dinh Development."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from vihsd.experiment import (  # noqa: E402
    DEVELOPMENT_SPLITS,
    FINAL_TEST_SPLITS,
    load_locked_config,
    load_official_frames,
    run_development_experiments,
    run_final_test,
)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Development (mac dinh) chi doc Train/Validation. "
            "Final-test can locked config da chon bang Validation."
        )
    )
    parser.add_argument(
        "--mode",
        choices=("development", "final-test"),
        default="development",
        help="Mac dinh development; final-test chi chay khi duoc goi ro rang.",
    )
    parser.add_argument(
        "--raw-data",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd",
        help="Thu muc DatasetDict da tai.",
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw" / "uitnlp_vihsd_provenance.json",
        help="Tep provenance de xac minh revision dataset.",
    )
    parser.add_argument(
        "--features",
        choices=("word", "combined"),
        default=None,
        help="Development mac dinh word; final-test lay feature mode tu locked config.",
    )
    parser.add_argument("--cv-folds", type=int, default=3)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--skip-group-cv",
        action="store_true",
        help="Bo qua StratifiedGroupKFold trong development.",
    )
    parser.add_argument(
        "--locked-config",
        type=Path,
        help="selection.json da khoa bang Validation; bat buoc cho final-test.",
    )
    parser.add_argument(
        "--run-id",
        help="Ten thu muc ket qua moi; mac dinh la UTC timestamp.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Thu muc ket qua moi nam ben trong mode/feature; khong duoc ghi de.",
    )
    return parser.parse_args(argv)


def _safe_run_id(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", value):
        raise ValueError("run-id chi duoc gom chu, so, cham, gach ngang va gach duoi")
    if value in {".", ".."}:
        raise ValueError("run-id khong hop le")
    return value


def build_output_path(
    mode: str,
    feature_mode: str,
    run_id: str,
    model: str | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Tao duong dan moi trong khu vuc rieng cua mode va feature."""
    if mode not in {"development", "final-test"}:
        raise ValueError("mode khong hop le")
    if feature_mode not in {"word", "combined"}:
        raise ValueError("feature_mode khong hop le")
    base = PROJECT_ROOT / "reports" / "exam2_results" / mode / feature_mode
    if mode == "final-test":
        if not model or not re.fullmatch(r"[A-Za-z0-9_-]+", model):
            raise ValueError("final-test can ten model trong locked config")
        base = base / model

    candidate = (output_dir if output_dir is not None else base / run_id).resolve()
    base_resolved = base.resolve()
    if candidate == base_resolved or not candidate.is_relative_to(base_resolved):
        raise ValueError("output-dir phai nam trong thu muc rieng mode/feature/model")
    if candidate.exists():
        raise FileExistsError(f"Thu muc ket qua da ton tai, tu choi ghi de: {candidate}")
    return candidate


def _print_development_result(result: dict) -> None:
    print("\nValidation Macro F1:")
    columns = [
        "model",
        "train_macro_f1",
        "validation_macro_f1",
        "validation_f1_clean",
        "validation_f1_offensive",
        "validation_f1_hate",
    ]
    print(
        result["validation_results"][columns]
        .sort_values("validation_macro_f1", ascending=False)
        .to_string(index=False, float_format=lambda value: f"{value:.4f}")
    )
    print("\nCV Macro F1 mean/std:")
    cv_columns = ["scheme", "model", "validation_macro_f1_mean", "validation_macro_f1_std"]
    print(
        result["cv_summary"][cv_columns].to_string(
            index=False, float_format=lambda value: f"{value:.4f}"
        )
    )
    print("\nDa khoa theo Validation:", result["selection"]["model"])
    print("Khong tai hoac danh gia Test trong che do Development.")


def main(argv: list[str] | None = None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = _parse_args(argv)

    if args.mode == "development":
        if args.locked_config is not None:
            raise ValueError("Development khong nhan locked-config hoac tai split Test")
        feature_mode = args.features or "word"
        splits = DEVELOPMENT_SPLITS
        locked_config = None
        model_name = None
    else:
        if args.locked_config is None:
            raise ValueError("final-test bat buoc co --locked-config da khoa tu Validation")
        locked_config = load_locked_config(args.locked_config)
        feature_mode = str(locked_config["feature_mode"])
        if args.features is not None and args.features != feature_mode:
            raise ValueError("--features khong khop feature_mode trong locked config")
        splits = FINAL_TEST_SPLITS
        model_name = str(locked_config["model"])

    run_id = _safe_run_id(args.run_id)
    output_dir = build_output_path(
        args.mode,
        feature_mode,
        run_id,
        model=model_name,
        output_dir=args.output_dir,
    )
    frames, revision = load_official_frames(
        args.raw_data,
        args.provenance,
        splits=splits,
    )
    print(f"Dataset: uitnlp/vihsd | revision {revision}")
    print(
        "Split duoc tai: "
        + ", ".join(f"{name}={len(frame):,}" for name, frame in frames.items())
    )

    if args.mode == "development":
        result = run_development_experiments(
            frames,
            revision,
            output_dir,
            feature_mode=feature_mode,
            n_splits=args.cv_folds,
            include_group_cv=not args.skip_group_cv,
            random_state=args.random_state,
        )
        _print_development_result(result)
    else:
        result = run_final_test(
            frames["train"],
            frames["test"],
            revision,
            locked_config,
            output_dir,
        )
        print("Cau hinh da khoa, khong chon lai:", model_name)
        print(
            result["test_results"]
            [["evaluation", "model", "rows", "macro_f1", "accuracy"]]
            .to_string(index=False, float_format=lambda value: f"{value:.4f}")
        )
    print(f"Ket qua tong hop: {result['output_dir']}")
    print("Khong ghi binh luan goc hoac du doan theo tung dong.")


if __name__ == "__main__":
    main()
