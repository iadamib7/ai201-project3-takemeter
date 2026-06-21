import csv
import time
import requests
from pathlib import Path

SUBREDDITS = [
    "nba",
    "nbadiscussion",
    "lakers",
    "warriors",
    "bostonceltics",
    "denvernuggets",
    "NYKnicks",
]

OUTPUT_PATH = Path("data/unlabeled_nba_comments.csv")
TARGET_COMMENTS = 250

HEADERS = {
    "User-Agent": "TakeMeterStudentProject/1.0 by student"
}


def clean_text(text):
    return " ".join(text.replace("\n", " ").replace("\r", " ").split())


def fetch_recent_comments(subreddit, limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/comments.json?limit={limit}&raw_json=1"

    response = requests.get(url, headers=HEADERS, timeout=20)

    if response.status_code != 200:
        print(f"HTTP {response.status_code} from r/{subreddit}")
        print(response.text[:300])
        return []

    data = response.json()
    items = data.get("data", {}).get("children", [])

    comments = []

    for item in items:
        if item.get("kind") != "t1":
            continue

        comment_data = item.get("data", {})
        body = clean_text(comment_data.get("body", ""))
        permalink = comment_data.get("permalink", "")
        score = comment_data.get("score", "")

        if not body:
            continue

        if body in {"[deleted]", "[removed]"}:
            continue

        if len(body.split()) < 5:
            continue

        comments.append({
            "text": body,
            "label": "",
            "notes": f"Source: r/{subreddit}; score: {score}; link: https://www.reddit.com{permalink}"
        })

    return comments


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    collected = []
    seen = set()

    for subreddit in SUBREDDITS:
        if len(collected) >= TARGET_COMMENTS:
            break

        print(f"Collecting from r/{subreddit}...")

        try:
            comments = fetch_recent_comments(subreddit, limit=100)
        except Exception as error:
            print(f"Could not collect from r/{subreddit}: {error}")
            continue

        print(f"Found {len(comments)} usable comments from r/{subreddit}.")

        for comment in comments:
            if len(collected) >= TARGET_COMMENTS:
                break

            text = comment["text"]

            if text in seen:
                continue

            seen.add(text)
            collected.append(comment)

        time.sleep(2)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label", "notes"])
        writer.writeheader()
        writer.writerows(collected)

    print()
    print(f"Collected {len(collected)} comments.")
    print(f"Saved to {OUTPUT_PATH}")

    if len(collected) == 0:
        print()
        print("No comments were collected. Reddit may be blocking the request on this network.")
    else:
        print()
        print("Next step: label these comments using:")
        print("python scripts/label_comments.py")


if __name__ == "__main__":
    main()
