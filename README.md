# Quizlet2CSV

A tiny drag-and-drop app (macOS and Windows) that turns a saved Quizlet
flashcard-set page into a CSV of term/definition pairs — no scraping the
live site, no ads, no server, nothing leaves your machine.

**This guide assumes you've never used the command line before.** It's
longer than a normal README on purpose — every step is spelled out.

## Why bother with this?

The point isn't just "get a CSV" — it's to get your flashcards into a
format an AI (like ChatGPT or Claude) can actually work with, so it can
help you study better than flipping through cards ever could. A clean
term/definition CSV is small enough to paste or upload directly, and once
it's there you can ask the AI to:

- **Check the cards for factual errors.** Quizlet sets are made by other
  students and are often wrong or outdated — an AI can flag definitions
  that don't hold up.
- **Turn the cards into practice exam questions.** Multiple choice, short
  answer, scenario-based — generated straight from your terms instead of
  studying the same flashcard format over and over.
- **Build you a study roadmap.** Group the terms into topics, figure out
  what depends on what, and sequence a study plan instead of grinding
  through the deck in whatever order it happens to be in.

---

## Step 1: Get the project files onto your computer

1. Go to this project's page on GitHub.
2. Click the green **Code** button, then click **Download ZIP**.
3. Find the downloaded ZIP file (usually in your Downloads folder) and
   double-click it to unzip it. You'll get a folder — that's the project.

You don't need to know or use `git` for any of this.

## Step 2: Install Python (if you don't already have it)

This tool runs on [Python](https://python.org), a programming language.
Follow the instructions for your operating system below — they cover
checking whether you already have it and installing it if not.

---

## macOS instructions

### 2a. Check for Python

1. Open **Terminal**. The easiest way: press `Cmd + Space`, type
   `Terminal`, and press `Enter`. A window with white or black background
   and a blinking cursor will open — that's Terminal.
2. Type exactly this and press `Enter`:
   ```
   python3 --version
   ```
3. **If you see something like** `Python 3.11.4`, you already have Python
   — skip to Step 3.
4. **If a popup appears** asking to install "Command Line Developer
   Tools," click **Install**, wait for it to finish (a few minutes), then
   run the command above again.
5. **If you see an error** like `command not found`, download and install
   Python from [python.org/downloads](https://www.python.org/downloads/),
   then try the command again.

### 2b. Build the app (one-time step)

1. In the same Terminal window, type `cd ` — that's the letters `c` and
   `d` followed by **one space**. Don't press Enter yet.
2. Open Finder, find the project folder from Step 1, and **drag that
   folder's icon into the Terminal window**. A file path will appear
   after `cd `.
3. Now press `Enter`. This moves Terminal "into" the project folder.
4. Type this and press `Enter`:
   ```
   ./build.sh
   ```
5. You'll see some text scroll by, ending with `Built Quizlet2CSV.app`.
   That means it worked. A new file called `Quizlet2CSV.app` now exists
   inside the project folder.

> **If Terminal says** `permission denied`, type `chmod +x build.sh` and
> press Enter, then try `./build.sh` again.

### 2c. Use the app

1. Open the project folder in Finder and find `Quizlet2CSV.app`.
   Optionally drag it into your **Applications** folder, or onto your
   **Dock**, so it's easy to get to.
2. On [quizlet.com](https://quizlet.com), open the flashcard set you want
   to convert.
3. Press `Cmd + S` to save the page. In the save dialog, make sure the
   format dropdown says **Webpage, Complete**, then save it (Desktop or
   Downloads is fine).
4. Drag the saved `.html` file onto `Quizlet2CSV.app`. (Or just
   double-click the app — it'll show instructions and let you pick the
   file instead.)
5. A `.csv` file appears right next to the saved HTML file, and a Finder
   window pops up showing it to you. That CSV is what you hand to an AI.

> **First time opening the app**, macOS may say it's "from an
> unidentified developer" and refuse to open it. Right-click (or
> `Control`-click) `Quizlet2CSV.app`, choose **Open**, then click **Open**
> again in the popup. You only need to do this once.

---

## Windows instructions

### 2a. Check for Python

1. Open **Command Prompt**. Click the Start menu, type `cmd`, and press
   `Enter`. A black window with a blinking cursor will open.
2. Type exactly this and press `Enter`:
   ```
   python --version
   ```
3. **If you see something like** `Python 3.12.1`, you already have Python
   — skip to Step 3.
4. **If you see an error**, or a Microsoft Store window pops up, go to
   [python.org/downloads](https://www.python.org/downloads/) and download
   the installer yourself instead. **Important:** on the first screen of
   the installer, check the box that says **"Add python.exe to PATH"**
   before clicking Install. This step is easy to miss and the tool won't
   work without it.
5. After installing, close Command Prompt, reopen it, and run the version
   check again to confirm it worked.

### 2b. Build the app (one-time step)

1. Open **File Explorer** and go into the project folder from Step 1.
2. Find the file `build_windows.bat` and **double-click it**. A black
   window will open and run for a bit — this is expected.
3. When it finishes, it will say `Built dist\Quizlet2CSV.exe` and
   `You can close this window now`. Press any key or close the window.
4. Inside the project folder, you'll now see a new subfolder called
   `dist` — open it, and you'll find `Quizlet2CSV.exe` inside.

> **If the window flashes an error about Python not being found**, go
> back to Step 2a and make sure you checked "Add python.exe to PATH"
> during install (you may need to reinstall Python to fix this).

### 2c. Use the app

1. In the `dist` folder, find `Quizlet2CSV.exe`. You can move it
   anywhere you like — your Desktop, or pin it to your Start menu/taskbar
   for easy access.
2. On [quizlet.com](https://quizlet.com), open the flashcard set you want
   to convert.
3. Press `Ctrl + S` to save the page. In the save dialog, make sure the
   format dropdown says **Webpage, Complete**, then save it (Desktop or
   Downloads is fine).
4. Drag the saved `.html` file onto `Quizlet2CSV.exe`. (Or just
   double-click the app — it'll show instructions and let you pick the
   file instead.)
5. A `.csv` file appears right next to the saved HTML file, and a File
   Explorer window pops up showing it to you. That CSV is what you hand
   to an AI.

> **First time opening the app**, Windows may show a blue "Windows
> protected your PC" SmartScreen warning, since it's not a commercially
> signed app. Click **More info**, then **Run anyway**. You only need to
> do this once.

---

## Troubleshooting

- **"I double-clicked `build.sh` on Mac and it opened in a text editor
  instead of running."** That's expected — `.sh` files don't run by
  double-clicking on macOS. You have to run it through Terminal using the
  steps in section 2b above.
- **"Nothing happens when I drag the HTML file onto the app."** Make sure
  you're dragging the `.html` file itself, not the matching `_files`
  folder that gets saved alongside it. Also confirm you saved the page as
  "Webpage, Complete" (not "Webpage, HTML Only" — that version is missing
  the data this tool needs).
- **"I can't find the CSV file it made."** It's saved in the exact same
  folder as the `.html` file you dragged in, with the same name but
  ending in `.csv` instead of `.html`. The app should also open a
  Finder/Explorer window pointing right at it.
- **"It says it couldn't find flashcard data in this file."** You may
  have saved the wrong page — this only works on the actual flashcard-set
  page (the one showing all the terms), not a "Learn," "Test," or "Match"
  mode page. Re-open the set itself and re-save it from there.
- **Still stuck?** Open an issue on this project's GitHub page and
  describe exactly what you see (screenshots help).

---

## How it works (optional reading)

When you save a Quizlet set page as "Webpage, Complete," the saved HTML
still contains the full flashcard data — Quizlet's app embeds it as JSON
in a hidden `<script>` tag so the page can render itself. This tool finds
that tag, unwraps a nested layer of encoded data inside it, and pulls out
the term/definition pairs for every card. `quizlet_html_to_csv.py`
contains that logic and is shared by both the Mac and Windows versions —
only the "drag a file onto an app icon" part differs between platforms.

## Custom icon

Drop a square `icon.png` (1024×1024 recommended) into the project folder
before building — it's the single source of truth for both platforms.
`build.sh` converts it to `.icns` for the Mac app; `build_windows.bat`
converts it to `.ico` for the Windows `.exe`. No `icon.png` present, and
each platform falls back to its own default icon. `icon.png` is tracked
in git, so if you commit one, everyone who downloads the project gets the
same branding on both platforms.

## Limitations

- Only works on a saved **set page** (the study-set view with all terms),
  not a saved "test" or "match" mode page.
- Quizlet's internal page structure has changed before. The script
  searches recursively for the flashcard data rather than hardcoding an
  exact path, so it should tolerate small changes, but a larger redesign
  on Quizlet's end could break it. If it stops working, open an issue with
  a (sanitized, no personal data) copy of the failing HTML.

## Files (for the curious)

- `quizlet_html_to_csv.py` — the extraction logic shared by both
  platforms; also runnable standalone:
  `python3 quizlet_html_to_csv.py file1.html file2.html ...`
- `Quizlet2CSV.applescript` — the macOS droplet source
- `build.sh` — compiles the `.applescript` + `.py` into `Quizlet2CSV.app`
  (macOS), baking in `icon.png` if present
- `quizlet_gui.py` — the Windows entry point (drag target / file picker
  UI, built via Tkinter)
- `make_ico.py` — converts `icon.png` to `icon.ico` for the Windows build
- `build_windows.bat` — compiles `quizlet_gui.py` into `Quizlet2CSV.exe`
  via PyInstaller, baking in `icon.png` if present
- `icon.png` (optional) — custom app icon, square, 1024×1024 recommended,
  shared by both platforms
