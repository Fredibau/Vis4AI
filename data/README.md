# Data
- `raw/` – MASSIVE v1.1, created by `python src/download_data.py` (gitignored).
  `raw/1.1/data/<locale>.jsonl`, 51 locales, fields: id, locale, partition, scenario, intent, utt, annot_utt.
  Same `id` across locales = translations of the same utterance.
- `processed/` – cached model outputs (predictions, probabilities, embeddings) so the model runs only once.

Source: https://huggingface.co/datasets/AmazonScience/massive · Paper: https://arxiv.org/abs/2204.08582
