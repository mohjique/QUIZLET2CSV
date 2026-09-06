#!/usr/bin/env python3
"""Windows entry point for Quizlet2CSV.

This is compiled into a standalone Quizlet2CSV.exe via PyInstaller (see
build_windows.bat), giving Windows users the same drag-a-file-onto-the-icon
experience as the macOS app: drag a saved Quizlet HTML file onto the .exe,
or double-click it to get instructions and a file picker instead.

Reuses the extraction logic from quizlet_html_to_csv.py so the actual
parsing code has one implementation shared by both platforms.
"""

import sys
import os
import csv
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from quizlet_html_to_csv import extract_pairs

INTRO_TEXT = (
    "Quizlet2CSV converts a saved Quizlet flashcard-set page into a clean "
    "term/definition CSV — ready to hand to an AI for studying.\n\n"
    "How to use:\n"
    "1. On quizlet.com, open the flashcard set, then press Ctrl+S and save "
    "it as a Webpage, Complete (.html) file.\n"
    "2. Drag the saved .html file onto this app icon (or click OK to pick "
    "one now).\n\n"
    "The resulting .csv is saved right next to the original .html file, "
    "with the same name."
)


def convert_files(paths):
    successes = []
    failures = []
    for path in paths:
        try:
            pairs = extract_pairs(path)
        except Exception as e:
            failures.append(f"{os.path.basename(path)}: {e}")
            continue
        out_path = os.path.splitext(path)[0] + ".csv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "definition"])
            writer.writerows(pairs)
        successes.append(out_path)
    return successes, failures


def reveal_in_explorer(path):
    try:
        subprocess.run(["explorer", f"/select,{os.path.normpath(path)}"])
    except OSError:
        pass


def show_summary(successes, failures):
    lines = []
    if successes:
        lines.append(f"Converted {len(successes)} file(s):")
        lines.extend(f"  - {os.path.basename(p)}" for p in successes)
    if failures:
        if lines:
            lines.append("")
        lines.append("Problems:")
        lines.extend(f"  - {f}" for f in failures)
    message = "\n".join(lines) if lines else "No files were converted."
    if failures and not successes:
        messagebox.showerror("Quizlet2CSV", message)
    else:
        messagebox.showinfo("Quizlet2CSV", message)


def main():
    root = tk.Tk()
    root.withdraw()

    dropped = sys.argv[1:]

    if dropped:
        paths = dropped
    else:
        messagebox.showinfo("Quizlet2CSV", INTRO_TEXT)
        paths = filedialog.askopenfilenames(
            title="Select saved Quizlet flashcard-set HTML file(s)",
            filetypes=[("HTML files", "*.html *.htm")],
        )
        if not paths:
            return

    successes, failures = convert_files(paths)
    if successes:
        reveal_in_explorer(successes[0])
    show_summary(successes, failures)


if __name__ == "__main__":
    main()
