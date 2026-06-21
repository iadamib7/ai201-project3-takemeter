import csv
from collections import Counter
from pathlib import Path

DATASET_PATH = Path("data/takemeter_dataset.csv")
TARGET_PER_LABEL = 50
LABELS = ["analysis", "hot_take", "reaction", "question"]


def main():
    if not DATASET_PATH.exists():
        print(f"ERROR: Could not find {DATASET_PATH}")
        return

    with DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    counts = Counter(row["label"].strip() for row in rows if row.get("label"))

    print("\nTakeMeter Dataset Progress")
    print("--------------------------")
    print(f"Total examples: {len(rows)} / 200")
    print()

    for label in LABELS:
        current = counts[label]
        remaining = max(TARGET_PER_LABEL - current, 0)
        print(f"{label}: {current} / {TARGET_PER_LABEL}  |  remaining: {remaining}")

    print()

    if len(rows) >= 200 and all(counts[label] >= 40 for label in LABELS):
        print("Status: Dataset is likely ready for training.")
    else:
        print("Status: Keep collecting and labeling examples.")


if __name__ == "__main__":
    main()
