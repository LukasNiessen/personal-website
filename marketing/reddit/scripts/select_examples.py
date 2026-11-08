#!/usr/bin/env python3
"""Read a bounded, curated set of frozen Reddit voice examples. No network calls."""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("gift-promotion", "project-showcase", "educational-story")


def select(category, count=6, exclude=()):
    if category not in CATEGORIES or not 1 <= count <= 6:
        raise ValueError("Choose an existing category and a count between 1 and 6")
    manifest = json.loads((ROOT / "corpus.json").read_text())
    index = {post["id"]: post for post in manifest["posts"]}
    selected, seen_bodies = [], set()
    for post_id in manifest["curated_examples"][category]:
        if post_id in exclude:
            continue
        post = index[post_id]
        if post["category"] != category or not post["eligible_for_voice"]:
            raise ValueError(f"Invalid curated example: {post_id}")
        path = (ROOT / post["path"]).resolve()
        if not path.is_relative_to(ROOT / "posts" / category):
            raise ValueError(f"Example path escapes category: {post_id}")
        text = path.read_text()
        body = text.split("\n\n## Original body\n\n", 1)[1]
        if hashlib.sha256(body.encode()).hexdigest() != post["body_sha256"]:
            raise ValueError(f"Frozen original has changed: {post_id}")
        normalized = " ".join(body.split()).casefold()
        if normalized in seen_bodies:
            continue
        seen_bodies.add(normalized)
        selected.append((post, text))
        if len(selected) == count:
            break
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", choices=CATEGORIES)
    parser.add_argument("--count", type=int, choices=range(1, 7), default=6)
    parser.add_argument("--list", action="store_true", help="Print metadata only")
    parser.add_argument("--exclude", action="append", default=[], metavar="ID",
                        help="Skip an example already read this session; repeat as needed")
    args = parser.parse_args()
    selected = select(args.category, args.count, set(args.exclude))
    print("Historical voice references only. Source removal labels are not acceptance evidence.")
    for post, text in selected:
        print(f"\n--- {post['id']} | r/{post['subreddit']} | removed_by_category={post['removed_by_category']} ---")
        print(post["path"])
        print(post["title"])
        if not args.list:
            print()
            print(text.split("\n\n## Original body\n\n", 1)[1])
    if not selected:
        print("No unread curated examples remain. Reuse the examples already read.")


if __name__ == "__main__":
    main()
