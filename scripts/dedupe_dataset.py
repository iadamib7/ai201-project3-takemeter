import csv
from pathlib import Path

DATASET_PATH = Path("data/takemeter_dataset.csv")


def main():
    if not DATASET_PATH.exists():
        print(f"ERROR: Could not find {DATASET_PATH}")
        return

    with DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    seen = set()
    deduped = []

    for row in rows:
        text = (row.get("text") or "").strip()
        label = (row.get("label") or "").strip()
        notes = (row.get("notes") or "").strip()

        if not text:
            continue

        normalized_text = " ".join(text.lower().split())

        if normalized_text in seen:
            continue

        seen.add(normalized_text)
        deduped.append({
            "text": text,
            "label": label,
            "notes": notes,
        })

    with DATASET_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writeheader()
        writer.writerows(deduped)

    print(f"Original rows: {len(rows)}")
    print(f"Duplicate rows removed: {len(rows) - len(deduped)}")
    print(f"Unique rows remaining: {len(deduped)}")


if __name__ == "__main__":
    main()
