# Phase I – How does the model behave? (black box)
Deadline: 11.11.2026 · Pair A = AI-aided · Pair B = human-only

### Main question
Does Laya Multilingual make the same decision regardless of language? We compare accuracy, confidence and calibration across languages, and check which translations of the same utterance lead to a different prediction (flips).

### Data
- MASSIVE v1.1 test split, all 52 locales.
- The 20 most common intents in en-US, excluding the catch-all `general_quirky` (Laya's choice questions should stay under ~20 options). We use the same 20 intents for every language ([intents.txt](../data/processed/intents.txt)).
- That gives 1,905 utterances per locale, each present in all 52 locales (99,060 rows in total).
- The model is asked one choice question per utterance. The options are the bare intent names (e.g. "iot hue lightoff") with no descriptions, and the instructions are in English.
- Outputs: [predictions.csv](../data/processed/predictions.csv) (`id, locale, scenario, intent, utt, pred, confidence, p_true, correct`), produced once with [src/run_all.py](../src/run_all.py) and shared by both pairs.

### Initial visualization
A heatmap of language × intent showing accuracy: each cell is the share of correct predictions for one intent in one language. Both pairs start from this idea and develop their analyses separately.


