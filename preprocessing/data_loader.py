from pathlib import Path

import numpy as np
import pandas as pd

TIME_STEPS = 250
CHANNELS = 90
NUM_CLASSES = 7

CLASS_NAMES = ["lie down", "fall", "pick up", "run", "sit down", "stand up", "walk"]

SPLITS = ("train", "val", "test")


def _read_array(path: Path) -> np.ndarray:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Place UT-HAR under data/UT_HAR/.")

    try:
        with open(path, "rb") as f:
            return np.load(f, allow_pickle=False)
    except ValueError:
        return pd.read_csv(path, header=None, dtype=np.float32).to_numpy()


def dataset_root_from_file(data_file) -> Path:
    return Path(data_file).resolve().parent.parent


def split_from_file(data_file) -> str:
    split = Path(data_file).stem.split("_", 1)[-1]
    if split not in SPLITS:
        raise ValueError(f"Can't tell which split {data_file} is (expected X_train/X_val/X_test).")
    return split


def load_split(root, split: str):
    if split not in SPLITS:
        raise ValueError(f"split must be one of {SPLITS}, got {split!r}")

    root = Path(root)
    X = _read_array(root / "data" / f"X_{split}.csv")
    y = _read_array(root / "label" / f"y_{split}.csv")

    X = X.reshape(-1, TIME_STEPS, CHANNELS).astype(np.float32)
    y = y.reshape(-1).astype(np.int64)

    if len(X) != len(y):
        raise ValueError(f"{split}: {len(X)} samples but {len(y)} labels.")

    return X, y


def load_ut_har(root="data/UT_HAR"):
    return {split: load_split(root, split) for split in SPLITS}


def load_from_test_file(data_file):
    root = dataset_root_from_file(data_file)
    split = split_from_file(data_file)
    train = load_split(root, "train")
    val = load_split(root, "val")
    evaluation = load_split(root, split)
    return train, val, evaluation


if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "data/UT_HAR"
    for name, (X, y) in load_ut_har(root).items():
        counts = np.bincount(y, minlength=NUM_CLASSES)
        print(f"{name:<5} X={X.shape} y={y.shape} samples per class={counts.tolist()}")
