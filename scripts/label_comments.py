import csv
from pathlib import Path

INPUT_PATH = Path("data/unlabeled_nba_comments.csv")
OUTPUT_PATH = Path("data/takemeter_dataset.csv")

LABEL_SHORTCUTS = {
    "a": "analysis",
    "h": "hot_take",
    "r": "reaction",
    "q": "question",
}

VALID_COMMANDS = set(LABEL_SHORTCUTS) | {"s", "x"}


def load_existing_texts():
    if not OUTPUT_PATH.exists():
        return set()

    with OUTPUT_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return {row["text"].strip() for row in reader if row.get("text")}


def ensure_output_file():
    if OUTPUT_PATH.exists():
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writeheader()


def append_labeled_row(text, label, notes):
    with OUTPUT_PATH.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writerow({
            "text": text,
            "label": label,
            "notes": notes,
        })


def main():
    if not INPUT_PATH.exists():
        print(f"ERROR: Could not find {INPUT_PATH}")
        print("Run scripts/import_raw_comments.py first.")
        return

    ensure_output_file()
    already_labeled = load_existing_texts()

    with INPUT_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = list(csv.DictReader(file))

    print("TakeMeter labeling helper")
    print("------------------------")
    print("a = analysis")
    print("h = hot_take")
    print("r = reaction")
    print("q = question")
    print("s = skip")
    print("x = exit")
    print()

    labeled_this_session = 0

    for index, row in enumerate(reader, start=1):
        text = (row.get("text") or "").strip()
        source_note = (row.get("notes") or "").strip()

        if not text or text in already_labeled:
            continue

        print("=" * 80)
        print(f"Comment {index} of {len(reader)}")
        print()
        print(text)
        print()
        print(source_note)
        print()

        command = ""
        while command not in VALID_COMMANDS:
            command = input("Label [a/h/r/q], skip [s], or exit [x]: ").strip().lower()

        if command == "x":
            break

        if command == "s":
            print("Skipped.")
            continue

        label = LABEL_SHORTCUTS[command]
        note = input("Optional note, or press Enter: ").strip()

        if not note:
            note = source_note

        append_labeled_row(text, label, note)
        already_labeled.add(text)
        labeled_this_session += 1

        print(f"Saved as {label}.")
        print()

    print()
    print(f"Labeled {labeled_this_session} new examples this session.")
    print(f"Saved labeled examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
