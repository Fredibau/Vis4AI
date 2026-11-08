"""Runs Laya on all MASSIVE test sentences (20 intents, all languages).
Saves one CSV per language to data/processed/preds/, so it can be stopped and resumed."""
import sys, time
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import load_massive, locales
from src.model import load_model, intent_question

OUT = ROOT / "data" / "processed" / "preds"
OUT.mkdir(parents=True, exist_ok=True)

# same 20 intents for everyone: the most common in en-US, without the catch-all general_quirky
counts = load_massive(["en-US"])["intent"].value_counts()
intents = [i for i in counts.index if i != "general_quirky"][:20]
(ROOT / "data" / "processed" / "intents.txt").write_text("\n".join(intents))
print("intents:", intents)

q = intent_question({i: i.replace("_", " ") for i in intents})
agent = load_model()

for n, loc in enumerate(locales(), 1):
    path = OUT / f"{loc}.csv"
    if path.exists():
        print(f"[{n}] {loc} already done, skipping")
        continue
    t0 = time.time()
    df = load_massive([loc])
    df = df[df["intent"].isin(intents)].reset_index(drop=True)
    res = agent.predict_batch([{"body": u} for u in df["utt"]], q, batch_size=32)
    ans = [r["answers"]["intent"] for r in res]
    df["pred"] = [a["choice"] for a in ans]
    df["confidence"] = [a["probabilities"][a["choice"]] for a in ans]
    df["p_true"] = [a["probabilities"].get(t, 0.0) for a, t in zip(ans, df["intent"])]
    df["correct"] = df["pred"] == df["intent"]
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"[{n}] {loc}: accuracy {df['correct'].mean():.3f}, {(time.time() - t0) / 60:.1f} min")

all_df = pd.concat(pd.read_csv(p) for p in sorted(OUT.glob("*.csv")))
all_df.to_csv(ROOT / "data" / "processed" / "predictions.csv", index=False, encoding="utf-8")
print("done:", len(all_df), "rows -> data/processed/predictions.csv")
