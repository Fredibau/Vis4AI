"""Picks the 20 most common intents and times Laya on 64 English sentences."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import load_massive, locales
from src.model import load_model, intent_question

en = load_massive(["en-US"])
top20 = en["intent"].value_counts().head(20).index.tolist()
print("top 20 intents:", top20)
print("en-US test sentences with these intents:", en["intent"].isin(top20).sum(), "of", len(en))

options = {i: i.replace("_", " ") for i in top20}
q = intent_question(options)
sample = en[en["intent"].isin(top20)].head(64)

agent = load_model()
t0 = time.time()
res = agent.predict_batch([{"body": u} for u in sample["utt"]], q, batch_size=32)
sec = (time.time() - t0) / len(sample)

pred = [r["answers"]["intent"]["choice"] for r in res]
acc = (sample["intent"].values == pred).mean()
n_per_lang = en["intent"].isin(top20).sum()
print(f"accuracy on these 64: {acc:.2f}")
print(f"{sec:.3f} s per sentence")
print(f"one language: {sec * n_per_lang / 60:.1f} min, all {len(locales())}: {sec * n_per_lang * len(locales()) / 3600:.1f} h")
