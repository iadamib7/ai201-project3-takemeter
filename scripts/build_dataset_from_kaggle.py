import csv
import re
from collections import Counter
from pathlib import Path

import pandas as pd

INPUT_PATH = Path("kaggle_data/kaggle_RC_2019-05.csv")
OUTPUT_PATH = Path("data/takemeter_dataset.csv")
TARGET_PER_LABEL = 50

LABELS = ["analysis", "hot_take", "reaction", "question"]

NBA_KEYWORDS = [
    "nba", "basketball", "lakers", "warriors", "celtics", "knicks",
    "nuggets", "mavericks", "mavs", "bucks", "suns", "heat", "sixers",
    "clippers", "raptors", "bulls", "cavs", "cavaliers", "spurs",
    "jokic", "lebron", "curry", "tatum", "luka", "doncic", "embiid",
    "giannis", "booker", "durant", "brunson", "shai", "wemby",
    "edwards", "playoffs", "finals", "mvp", "coach", "defense",
    "offense", "screen", "paint", "shooters", "dunk", "three pointer",
    "midrange", "rebound", "guard", "center", "forward"
]

QUESTION_STARTERS = (
    "why", "what", "how", "who", "which", "should", "can", "does",
    "do", "is", "are", "would", "could"
)

REACTION_WORDS = [
    "wow", "insane", "crazy", "ridiculous", "unbelievable", "painful",
    "sick", "lol", "lmao", "wtf", "damn", "bruh", "wild", "amazing",
    "hilarious", "terrible", "awful", "i can't believe", "i cannot believe",
    "jumped out", "hate this", "love this"
]

HOT_TAKE_WORDS = [
    "never", "always", "best", "worst", "overrated", "underrated",
    "not even close", "washed", "cooked", "fraud", "trash", "goat",
    "no chance", "easily", "by far", "garbage", "terrible player",
    "better than everyone", "no one can"
]

ANALYSIS_WORDS = [
    "because", "since", "due to", "forces", "spacing", "rotation",
    "rotations", "efficiency", "matchup", "defense", "offense",
    "screen", "screens", "switch", "help", "paint", "midrange",
    "weak side", "weak-side", "shooters", "transition", "possession",
    "lineup", "scheme", "coverage", "double", "pick and roll",
    "free throw", "usage", "minutes", "adjustment"
]


def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = text.replace("\n", " ").replace("\r", " ")
    text = " ".join(text.split())
    return text.strip()


def choose_text_column(columns):
    preferred = ["body", "comment", "text", "content"]
    lower_map = {col.lower(): col for col in columns}

    for name in preferred:
        if name in lower_map:
            return lower_map[name]

    return columns[0]


def is_nba_related(text):
    lower = text.lower()
    return any(keyword in lower for keyword in NBA_KEYWORDS)


def auto_label(text):
    lower = text.lower()
    words = lower.split()

    if "?" in text and words and words[0] in QUESTION_STARTERS:
        return "question", "Auto-prelabel from real Kaggle Reddit comment: genuine question structure; manually reviewed/needs review."

    if any(phrase in lower for phrase in ANALYSIS_WORDS) and len(words) >= 10:
        return "analysis", "Auto-prelabel from real Kaggle Reddit comment: contains reasoning or basketball explanation; manually reviewed/needs review."

    if any(phrase in lower for phrase in REACTION_WORDS):
        return "reaction", "Auto-prelabel from real Kaggle Reddit comment: emotional reaction language; manually reviewed/needs review."

    if any(phrase in lower for phrase in HOT_TAKE_WORDS):
        return "hot_take", "Auto-prelabel from real Kaggle Reddit comment: strong confident claim language; manually reviewed/needs review."

    return None, ""


def main():
    if not INPUT_PATH.exists():
        print(f"ERROR: Could not find {INPUT_PATH}")
        return

    print(f"Reading from {INPUT_PATH}")

    buckets = {label: [] for label in LABELS}
    seen = set()

    first_chunk = pd.read_csv(INPUT_PATH, nrows=5, low_memory=False)
    text_column = choose_text_column(list(first_chunk.columns))
    print(f"Using text column: {text_column}")

    chunk_number = 0

    for chunk in pd.read_csv(INPUT_PATH, chunksize=50000, low_memory=False):
        chunk_number += 1
        print(f"Processing chunk {chunk_number}...")

        if text_column not in chunk.columns:
            print(f"ERROR: Column {text_column} not found.")
            return

        for value in chunk[text_column].dropna():
            text = clean_text(value)

            if len(text.split()) < 6:
                continue

            if len(text) > 350:
                continue

            normalized = text.lower()

            if normalized in seen:
                continue

            if not is_nba_related(text):
                continue

            label, note = auto_label(text)

            if label is None:
                continue

            if len(buckets[label]) >= TARGET_PER_LABEL:
                continue

            seen.add(normalized)
            buckets[label].append({
                "text": text,
                "label": label,
                "notes": note
            })

            if all(len(buckets[label]) >= TARGET_PER_LABEL for label in LABELS):
                break

        counts = {label: len(buckets[label]) for label in LABELS}
        print(f"Current counts: {counts}")

        if all(len(buckets[label]) >= TARGET_PER_LABEL for label in LABELS):
            break

    rows = []
    for label in LABELS:
        rows.extend(buckets[label])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("Created dataset:")
    counts = Counter(row["label"] for row in rows)
    for label in LABELS:
        print(f"{label}: {counts[label]}")
    print(f"Total: {len(rows)}")
    print(f"Saved to {OUTPUT_PATH}")

    if len(rows) < 200:
        print()
        print("WARNING: Fewer than 200 examples were found.")
        print("We may need to broaden the filters or use another Kaggle source.")

    print()
    print("Important: These are real Kaggle Reddit comments, but labels are auto-prelabels.")
    print("For the README, disclose that auto-prelabeling was used and manually reviewed/corrected.")


if __name__ == "__main__":
    main()
