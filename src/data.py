"""Load MASSIVE as a pandas DataFrame. One row = one utterance in one language.

Same `id` across locales = same utterance (translation), with the same `intent`.
"""
import json
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "1.1" / "data"


def locales() -> list[str]:
    return sorted(p.stem for p in DATA_DIR.glob("*.jsonl"))


def load_massive(langs: list[str] | None = None, partition: str = "test") -> pd.DataFrame:
    """langs: locale codes like ["en-US", "de-DE"] (None = all 51). partition: train | dev | test."""
    rows = []
    for loc in langs or locales():
        with open(DATA_DIR / f"{loc}.jsonl", encoding="utf8") as f:
            rows += [r for r in map(json.loads, f) if r["partition"] == partition]
    df = pd.DataFrame(rows)[["id", "locale", "scenario", "intent", "utt"]]
    df["id"] = df["id"].astype(int)
    return df
