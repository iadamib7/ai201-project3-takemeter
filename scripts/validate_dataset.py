import csv
from collections import Counter
from pathlib import Path

DATASET_PATH = Path("data/takemeter_dataset.csv")
VALID_LABELS = {"analysis", "hot_take", "reaction", "question"}


def normalize_text(text):
    return " ".join(text.lower().split())


def validate_dataset():
    if not DATASET_PATH.exists():
        print(f"ERROR: Could not find {DATASET_PATH}")
        return

    rows = []
    normalized_texts = []

    with DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"text", "label", "notes"}
        found_columns = set(reader.fieldnames or [])

        missing_columns = required_columns - found_columns
        if missing_columns:
            print(f"ERROR: Missing required columns: {sorted(missing_columns)}")
            return

        for line_number, row in enumerate(reader, start=2):
            text = (row.get("text") or "").strip()
            label = (row.get("label") or "").strip()
            notes = (row.get("notes") or "").strip()

            if not text:
                print(f"ERROR: Empty text at CSV line {line_number}")

            if label not in VALID_LABELS:
                print(
                    f"ERROR: Invalid label at CSV line {line_number}: '{label}'. "
                    f"Expected one of {sorted(VALID_LABELS)}"
                )

            rows.append({"text": text, "label": label, "notes": notes})

            if text:
                normalized_texts.append(normalize_text(text))

    label_counts = Counter(row["label"] for row in rows)
    duplicate_counts = Counter(normalized_texts)
    duplicates = [text for text, count in duplicate_counts.items() if count > 1]

    print("\nDataset validation summary")
    print("--------------------------")
    print(f"Total examples: {len(rows)}")

    for label in sorted(VALID_LABELS):
        print(f"{label}: {label_counts[label]}")

    print()

    if len(rows) < 200:
        print("WARNING: Dataset has fewer than 200 examples.")
    else:
        print("OK: Dataset has at least 200 examples.")

    if rows:
        largest_label, largest_count = label_counts.most_common(1)[0]
        largest_percentage = largest_count / len(rows)

        if largest_percentage > 0.70:
            print(
                f"WARNING: Label imbalance detected. '{largest_label}' is "
                f"{largest_percentage:.1%} of the dataset."
            )
        else:
            print("OK: No label is above 70% of the dataset.")

    if duplicates:
        print(f"WARNING: Found {len(duplicates)} duplicate text example(s).")
        print("Run this to remove duplicates:")
        print("python scripts/dedupe_dataset.py")
    else:
        print("OK: No duplicate text examples found.")

    print("\nValidation complete.")


if __name__ == "__main__":
    validate_dataset()
