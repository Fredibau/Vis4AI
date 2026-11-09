import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDICTIONS = HERE.parents[1] / "data" / "processed" / "predictions.csv"
OUTPUT = HERE / "results"
N_BINS = 10


def write_csv(name, header, rows):
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    by_locale = defaultdict(list)
    by_id = defaultdict(dict)
    with PREDICTIONS.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            locale = row["locale"]
            utterance_id = int(row["id"])
            row["id"] = utterance_id
            row["confidence"] = float(row["confidence"])
            row["correct"] = int(row["pred"] == row["intent"])

            if locale in by_id[utterance_id]:
                raise ValueError(f"Duplicate prediction for {utterance_id} in {locale}")
            if not 0 <= row["confidence"] <= 1:
                raise ValueError(f"Invalid confidence for {utterance_id} in {locale}")

            by_locale[locale].append(row)
            by_id[utterance_id][locale] = row

    if not by_id:
        raise ValueError("No predictions found")

    language_rows = []
    bin_rows = []
    for locale, rows in sorted(by_locale.items()):
        total = len(rows)
        accuracy = sum(row["correct"] for row in rows) / total
        confidence = sum(row["confidence"] for row in rows) / total

        bins = [[] for _ in range(N_BINS)]
        for row in rows:
            # Put confidence 1.0 in the last bin.
            index = min(int(row["confidence"] * N_BINS), N_BINS - 1)
            bins[index].append(row)

        ece = 0.0
        for index, group in enumerate(bins):
            lower = index / N_BINS
            upper = (index + 1) / N_BINS
            count = len(group)
            bin_confidence = bin_accuracy = None
            if count:
                bin_confidence = sum(row["confidence"] for row in group) / count
                bin_accuracy = sum(row["correct"] for row in group) / count
                ece += count / total * abs(bin_accuracy - bin_confidence)
            bin_rows.append((locale, lower, upper, count, bin_confidence, bin_accuracy))
        language_rows.append((locale, total, accuracy, confidence, ece))

    columns = ("id", "locale", "scenario", "intent", "utt", "pred", "confidence", "correct")
    translation_rows = []
    for utterance_id, translations in sorted(by_id.items()):
        if len({row["intent"] for row in translations.values()}) != 1:
            raise ValueError(f"Different true intents for ID {utterance_id}")

        distinct = len({row["pred"] for row in translations.values()})
        for _, row in sorted(translations.items()):
            translation_rows.append([row[column] for column in columns] + [distinct])

    OUTPUT.mkdir(exist_ok=True)
    write_csv("language_stats.csv", ("locale", "n", "accuracy", "mean_confidence", "ece"), language_rows)
    write_csv(
        "calibration_bins.csv",
        ("locale", "bin_lower", "bin_upper", "n", "mean_confidence", "accuracy"),
        bin_rows,
    )
    write_csv("translation_predictions.csv", columns + ("distinct_predictions",), translation_rows)
    print(f"Saved three CSVs in {OUTPUT}")


if __name__ == "__main__":
    main()
