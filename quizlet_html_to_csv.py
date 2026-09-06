#!/usr/bin/env python3
"""Extract term/definition pairs from a saved Quizlet flashcard-set page into a CSV.

Usage:
    quizlet_html_to_csv.py <saved-quizlet-page.html> [more files ...]

How it works:
    A saved Quizlet set page embeds its initial state in a
    <script id="__NEXT_DATA__"> tag. Buried inside that JSON is a field
    holding a *second*, JSON-encoded string (Quizlet's dehydrated Redux
    state). Somewhere inside that nested JSON is a "studiableItems" array
    with one entry per flashcard, each holding "cardSides" for the word
    and definition text. This script finds that array regardless of which
    field it's nested under, since Quizlet's exact structure has shifted
    before and may shift again.
"""

import sys
import re
import json
import csv
import os


def find_studiable_items(obj):
    """Recursively search a parsed JSON structure for the flashcard array."""
    if isinstance(obj, dict):
        items = obj.get("studiableItems")
        if isinstance(items, list) and items and isinstance(items[0], dict) and "cardSides" in items[0]:
            return items
        for value in obj.values():
            found = find_studiable_items(value)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_studiable_items(value)
            if found:
                return found
    return None


def find_nested_json_strings(obj):
    """Yield long string values that might themselves be JSON-encoded."""
    if isinstance(obj, dict):
        for value in obj.values():
            yield from find_nested_json_strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from find_nested_json_strings(value)
    elif isinstance(obj, str) and len(obj) > 1000:
        yield obj


def extract_pairs(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise ValueError("Could not find __NEXT_DATA__ script tag — is this a saved Quizlet set page?")

    next_data = json.loads(match.group(1))

    items = find_studiable_items(next_data)

    if items is None:
        for candidate in find_nested_json_strings(next_data):
            try:
                inner = json.loads(candidate)
            except (json.JSONDecodeError, TypeError):
                continue
            items = find_studiable_items(inner)
            if items:
                break

    if not items:
        raise ValueError(
            "Could not locate flashcard data in this file. "
            "Quizlet may have changed its page format, or this isn't a set page."
        )

    pairs = []
    for item in items:
        sides = {}
        for side in item.get("cardSides", []):
            media = side.get("media") or []
            text = next((m.get("plainText") for m in media if m.get("plainText")), None)
            if text:
                sides[side.get("label")] = text
        term = sides.get("word", "")
        definition = sides.get("definition", "")
        if term or definition:
            pairs.append((term, definition))

    return pairs


def main():
    if len(sys.argv) < 2:
        print("Usage: quizlet_html_to_csv.py <saved-quizlet-page.html> [more files ...]")
        sys.exit(1)

    for html_path in sys.argv[1:]:
        try:
            pairs = extract_pairs(html_path)
        except Exception as e:
            print(f"FAILED: {html_path}\n  {e}")
            continue

        out_path = os.path.splitext(html_path)[0] + ".csv"
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "definition"])
            writer.writerows(pairs)

        print(f"Wrote {len(pairs)} cards -> {out_path}")


if __name__ == "__main__":
    main()
