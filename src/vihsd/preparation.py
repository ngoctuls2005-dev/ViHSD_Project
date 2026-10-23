"""Chia hold-out va tao TF-IDF chi hoc tu Train."""

from dataclasses import dataclass
from typing import Callable, Mapping, Sequence

import pandas as pd
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from vihsd.data import validate_schema
from vihsd.quality import cross_split_duplicate_summary


@dataclass(frozen=True)
class DataSplits:
    """Ba bang du lieu dung cho hold-out."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


@dataclass(frozen=True)
class TfidfFeatureSets:
    """Ma tran TF-IDF va nhan tuong ung voi tung split."""

    word_train: csr_matrix
    word_validation: csr_matrix
    word_test: csr_matrix
    char_train: csr_matrix
    char_validation: csr_matrix
    char_test: csr_matrix
    combined_train: csr_matrix
    combined_validation: csr_matrix
    combined_test: csr_matrix
    y_train: pd.Series
    y_validation: pd.Series
    y_test: pd.Series
    word_vectorizer: TfidfVectorizer
    char_vectorizer: TfidfVectorizer


def use_official_splits(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    text_column: str,
    label_column: str,
) -> DataSplits:
    """Giu nguyen ba split chinh thuc, khong noi/chia lai du lieu."""
    for frame in (train, validation, test):
        validate_schema(frame, text_column, label_column)
    return DataSplits(train.copy(), validation.copy(), test.copy())


def stratified_holdout(
    frame: pd.DataFrame,
    label_column: str,
    test_size: float = 0.2,
    validation_size: float = 0.1,
    random_state: int = 42,
) -> DataSplits:
    """Chia Train/Validation/Test co phan tang neu khong co split chinh thuc."""
    if label_column not in frame.columns:
        raise ValueError(f"Khong co cot nhan: {label_column}")
    if frame[label_column].isna().any():
        raise ValueError("Can xu ly hoac loai rieng nhan thieu truoc khi chia")
    if test_size <= 0 or validation_size <= 0 or test_size + validation_size >= 1:
        raise ValueError("test_size va validation_size phai duong va co tong nho hon 1")

    temporary_size = test_size + validation_size
    try:
        train, temporary = train_test_split(
            frame,
            test_size=temporary_size,
            random_state=random_state,
            stratify=frame[label_column],
        )
        test_fraction_of_temporary = test_size / temporary_size
        validation, test = train_test_split(
            temporary,
            test_size=test_fraction_of_temporary,
            random_state=random_state,
            stratify=temporary[label_column],
        )
    except ValueError as error:
        raise ValueError(
            "Khong the chia phan tang voi kich thuoc/lop hien co; kiem tra so mau moi lop va ty le chia"
        ) from error
    return DataSplits(
        train=train.reset_index(drop=True),
        validation=validation.reset_index(drop=True),
        test=test.reset_index(drop=True),
    )


def assert_no_cross_split_duplicates(
    splits: Mapping[str, pd.DataFrame], text_column: str
) -> None:
    """Dung lai neu cung van ban xuat hien o nhieu split."""
    overlaps = cross_split_duplicate_summary(splits, text_column)
    leaked = overlaps.loc[overlaps["shared_unique_texts"] > 0]
    if not leaked.empty:
        details = ", ".join(
            f"{row.split_a}/{row.split_b}: {row.shared_unique_texts}"
            for row in leaked.itertuples(index=False)
        )
        raise ValueError(f"Phat hien van ban trung giua cac split: {details}")


def vietnamese_word_tokenize(
    text: str,
    segmenter: Callable[[str], Sequence[str] | str] | None = None,
) -> list[str]:
    """Tach tu tieng Viet bang PyVi hoac segmenter duoc tiem vao."""
    if not isinstance(text, str):
        raise TypeError("Van ban can tach tu phai la chuoi")
    if segmenter is None:
        try:
            from pyvi import ViTokenizer
        except ImportError as error:
            raise RuntimeError(
                "Can cai PyVi bang 'python -m pip install -r requirements.txt' de tach tu tieng Viet"
            ) from error
        segmented: Sequence[str] | str = ViTokenizer.tokenize(text)
    else:
        segmented = segmenter(text)
    if isinstance(segmented, str):
        return segmented.split()
    return list(segmented)


def fit_tfidf_on_train(
    train_texts: Sequence[str],
    validation_texts: Sequence[str],
    test_texts: Sequence[str],
    y_train: Sequence[object],
    y_validation: Sequence[object],
    y_test: Sequence[object],
    word_tokenizer: Callable[[str], Sequence[str]] | None = None,
    word_ngram_range: tuple[int, int] = (1, 2),
    char_ngram_range: tuple[int, int] = (2, 5),
) -> TfidfFeatureSets:
    """Fit hai vectorizer chi tren Train, transform Validation/Test."""
    texts = {
        "train": list(train_texts),
        "validation": list(validation_texts),
        "test": list(test_texts),
    }
    labels = {
        "train": pd.Series(y_train).reset_index(drop=True),
        "validation": pd.Series(y_validation).reset_index(drop=True),
        "test": pd.Series(y_test).reset_index(drop=True),
    }
    for split_name, values in texts.items():
        if len(values) != len(labels[split_name]):
            raise ValueError(f"So van ban va nhan khong khop o split {split_name}")
        if any(not isinstance(value, str) for value in values):
            raise TypeError(f"Van ban trong split {split_name} phai la chuoi")
    if not texts["train"]:
        raise ValueError("Train khong duoc rong")

    tokenizer = word_tokenizer or vietnamese_word_tokenize
    word_vectorizer = TfidfVectorizer(
        tokenizer=tokenizer,
        token_pattern=None,
        lowercase=False,
        ngram_range=word_ngram_range,
    )
    char_vectorizer = TfidfVectorizer(
        analyzer="char",
        lowercase=False,
        ngram_range=char_ngram_range,
    )

    word_train = word_vectorizer.fit_transform(texts["train"]).tocsr()
    word_validation = word_vectorizer.transform(texts["validation"]).tocsr()
    word_test = word_vectorizer.transform(texts["test"]).tocsr()
    char_train = char_vectorizer.fit_transform(texts["train"]).tocsr()
    char_validation = char_vectorizer.transform(texts["validation"]).tocsr()
    char_test = char_vectorizer.transform(texts["test"]).tocsr()

    return TfidfFeatureSets(
        word_train=word_train,
        word_validation=word_validation,
        word_test=word_test,
        char_train=char_train,
        char_validation=char_validation,
        char_test=char_test,
        combined_train=hstack([word_train, char_train], format="csr"),
        combined_validation=hstack([word_validation, char_validation], format="csr"),
        combined_test=hstack([word_test, char_test], format="csr"),
        y_train=labels["train"],
        y_validation=labels["validation"],
        y_test=labels["test"],
        word_vectorizer=word_vectorizer,
        char_vectorizer=char_vectorizer,
    )
