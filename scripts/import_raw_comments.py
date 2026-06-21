import csv
from pathlib import Path

RAW_PATH = Path("raw_data/nba_comments_raw.txt")
OUTPUT_PATH = Path("data/unlabeled_nba_comments.csv")


def clean_text(text):
    return " ".join(text.replace("\n", " ").replace("\r", " ").split())


def main():
    if not RAW_PATH.exists():
        print(f"ERROR: Could not find {RAW_PATH}")
        return

    raw_text = RAW_PATH.read_text(encoding="utf-8")

    blocks = [clean_text(block) for block in raw_text.split("\n\n")]
    comments = []

    seen = set()

    for block in blocks:
        if not block:
            continue

        if block in seen:
            continue

        if len(block.split()) < 5:
            continue

        seen.add(block)
        comments.append({
            "text": block,
            "label": "",
            "notes": "Source: manually collected from public NBA discussion comments"
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writeheader()
        writer.writerows(comments)

    print(f"Imported {len(comments)} comments.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
