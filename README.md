# Vis4AI – Multilingual Intent Classification

**Group: The Gradient Gang**

| Student ID | Name | Pair |
|---|---|---|
| K11920581 | _add your name_ | |
| K52210093 | _add your name_ | |
| K12522555 | _add your name_ | |
| K12117401 | Frederik Bauer | |

Does a model make the same decision regardless of language?
We classify MASSIVE utterances (v1.1: 52 locales, identical labels) with **Laya Multilingual** (mmBERT-based, pretrained, no fine-tuning).

- **Phase I** – accuracy, confidence & calibration per language; which translations flip the prediction.
- **Phase II** – project embeddings (PCA/UMAP): do utterances cluster by intent or by language?

## Setup
```bash
pip install -r requirements.txt
python src/download_data.py   # MASSIVE -> data/raw/ (~650 MB, gitignored)
python src/model.py           # downloads Laya (~640 MB) + smoke test
```
```python
from src.data import load_massive      # DataFrame: id, locale, scenario, intent, utt
from src.model import load_model       # laya agent: agent.predict(state, questions)
```
⚠️ Model card: keep `choice` questions under ~20 options, but MASSIVE has 59 test intents → decide how we pose the intent question (per scenario / subset).

## Structure
| Folder | Purpose |
|---|---|
| `data/` | MASSIVE (`raw/`, gitignored) and cached model outputs (`processed/`) |
| `src/` | shared code used by both pairs: data loading, model inference |
| `phase1/` | common direction, one folder per pair, pair comparison, midpoint video |
| `phase2/` | same layout as Phase I, with the pair roles switched |
| `final/` | slide deck + final presentation |

Each pair keeps its own notebooks, scripts and figures inside its own folder.
The `ai_interaction_record.md` file sits in the folder of whichever pair is AI-aided in that phase.

## Links
- Dataset: https://huggingface.co/datasets/AmazonScience/massive
- Paper: https://arxiv.org/abs/2204.08582
- Model: https://huggingface.co/convaiinnovations/laya-multilingual
