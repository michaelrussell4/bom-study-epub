# Book of Mormon Study EPUB3 Build Pipeline

A Python CLI build pipeline that compiles an enhanced, scholarly **Book of Mormon Study EPUB3** e-book.

This tool combines the structured 1830 and latest (2013) edition text data with:
- **Inline 1830 First Edition Revisions:** Verse-by-verse strikethrough (`<s>`) for 1830 Palmyra first edition wording, immediately followed by modern italic (`<em>`) markup for additions/replacements.
- **Book of Mormon Onomasticon Pop-up Footnotes:** EPUB3 `noteref` links on every mention of proper names (e.g., *Laman*, *Nephi*, *Zarahemla*) that trigger instant pop-up reading modals on Kindle devices (Paperwhite, Oasis, Scribe) and Apple Books.
- **Early Historical Scripture Citations (1830–1930):** Numbered discourse citations (`[1]`, `[2]`) at the end of cited verses linking to verbatim historical sermon excerpts from the *Journal of Discourses* and *Teachings of the Prophet Joseph Smith*.
- **Supplemental Study Resources & Appendices:** Four comprehensive back-matter appendices drawn from foundational scholarly works (John W. Welch, Donald W. Parry, Dr. John L. Sorenson):
  - **Appendix A — Hebrew Poetic Parallelisms & Prominent Chiasmus:** Inverted parallel poetic layouts for the 10 most prominent Book of Mormon chiasms (Alma 36, Mosiah 5:10–12, Mosiah 3:18–19, Helaman 6:7–13, etc.) highlighting symmetrical pairs, focal center climaxes, and embedded visual charts.
  - **Appendix B — Internal Geography & Mormon's Map:** Detailed spatial synthesis of Dr. John L. Sorenson's internal map, Welch's 10 essential geographic features, table of the 12 journeys between Nephi and Zarahemla, and high-resolution route maps.
  - **Appendix C — Legal Cases & Ancient Judicial Procedures:** In-depth legal analysis of ancient Near Eastern and Nephite jurisprudence across major trials (Abinadi, Sherem, Nehor, Korihor, Ammonihah, Paanchi, Seantum) with legal flowcharts.
  - **Appendix D — Chronology, Plates, & Structural Charts:** Plate lineages, Lehi lineage lifespans, King Mosiah's monetary weight system (Alma 11), and the Allegory of the Olive Tree (Jacob 5).
- **Interactive Verse Cross-Linking:** Verses with prominent poetic structures or historical context feature interactive study badges (`[☵ Chiasmus]`, `[⚖ Law: ...]`, `[🗺 Mormon's Map]`, `[📊 Monetary System]`, `[🌳 Olive Tree]`) with pop-up footnote modals that jump directly to the corresponding appendix analysis, complete with one-tap return links back to the scriptures.
- **E-Ink Compatible Typography:** Clean serif typography, justified layout, and full `@media (prefers-color-scheme: dark)` night mode support.

---

## Installation & Setup

This project uses [uv](https://docs.astral.sh/uv/) for fast, reproducible Python 3.11+ environment management.

```bash
# Clone the repository
git clone https://github.com/michaelrussell4/bom-study-epub.git
cd bom-study-epub

# Install dependencies and create virtual environment
uv sync
```

---

## Usage

### 1. Compile the Full Book of Mormon Study Edition
Builds the complete edition with inline 1830 revisions, Onomasticon popups on every mention, historical discourse citations, and the 4 study appendices:
```bash
uv run bom-study-epub -o output/Book_of_Mormon_Study_Edition.epub
```

### 2. Focus on Substantive Changes Only
Ignore pure punctuation and capitalization adjustments to highlight only substantive word differences:
```bash
uv run bom-study-epub --substantive-only -o output/Book_of_Mormon_Substantive_Edition.epub
```

### 3. Adjust Onomasticon Link Density
By default, every occurrence of a name is tagged (`--all-mentions`). If you prefer lighter footnote density:
```bash
# Tag proper names on first mention per chapter
uv run bom-study-epub --first-mention-per-chapter -o output/Book_of_Mormon_Chapter_Density.epub

# Tag proper names on first mention per book
uv run bom-study-epub --first-mention-per-book -o output/Book_of_Mormon_Book_Density.epub
```

### 4. Compile Specific Books for Fast Testing
```bash
uv run bom-study-epub --books 1-nephi 2-nephi enos -o output/Sample.epub
```

---

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o`, `--output` | Output filepath for the compiled `.epub` | `output/Book_of_Mormon_Study_Edition.epub` |
| `--substantive-only` | Ignore pure punctuation and capitalization differences | `False` (full word/punctuation diff) |
| `--all-mentions` | Tag proper names on every occurrence | **Enabled by default** |
| `--first-mention-per-chapter` | Tag proper names on first mention in each chapter | `False` |
| `--first-mention-per-book` | Tag proper names on first mention in each book | `False` |
| `--books` | List of specific books to compile by slug or name | All 15 books |
| `--data-dir` | Path to folder containing `1830/` and `latest/` editions | `data` |
| `--onomasticon` | Path to Onomasticon JSON dictionary | `data/onomasticon.json` |
| `--citations` | Path to early historical citations JSON file | `data/early_citations.json` |
| `--cover` | Path to cover image | `assets/images/cover.jpg` |
| `--skip-diff` | Omit 1830 diff tags and render clean modern text | `False` |
| `--skip-onoma` | Omit Onomasticon footnote popups and section | `False` |
| `--skip-citations` | Omit 19th-century historical discourse citations | `False` |
| `--skip-appendices` | Omit back-matter study appendices and verse cross-links | `False` |

---

## Project Structure

```text
bom-study-epub/
├── assets/
│   ├── bom_study_supplemental_resources/ # Scholarly source PDFs (Welch, Sorenson, Parry)
│   └── images/
│       ├── cover.jpg              # High-resolution EPUB cover
│       └── appendix/              # 16 High-resolution visual aid charts & maps (PNG)
├── data/
│   ├── 1830/                      # 1830 First Edition chapter JSONs
│   ├── latest/                    # Latest (2013) Edition chapter JSONs
│   ├── onomasticon.json           # 376 Book of Mormon proper name etymologies
│   └── early_citations.json       # 4,418 historical sermon citations (1830–1930)
├── data-source/                   # Reference source processing scripts
├── src/
│   ├── __init__.py                # Package exports
│   ├── appendices.py              # XHTML generator for Appendices A–D
│   ├── build_epub.py              # EPUB3 compilation pipeline and CLI
│   ├── chiasmus.py                # Data dictionary & verse mappings for chiasms & legal cases
│   ├── citations.py               # Historical citation loader & aside generator
│   ├── differ.py                  # Verse-by-verse 1830 vs. latest diff engine
│   ├── onomasticon.py             # Collision-free entity matcher & footnote generator
│   └── styles.css                 # EPUB3 styling (e-ink & dark mode optimized)
├── pyproject.toml                 # uv / Python project configuration
└── README.md
```

---

## Data Attribution & Scholarly Sources

- **Textual Editions:** BYU Open Scripture Project ([GitHub](https://github.com/BYU-ODH/OpenScripture)).
- **Onomasticon Etymologies:** [Book of Mormon Onomasticon](https://onoma.lib.byu.edu/) (Brigham Young University).
- **Early Scripture Citations (1830–1930):** Excerpted and aligned from the *Journal of Discourses* and *Teachings of the Prophet Joseph Smith*.
- **Poetic Parallelisms & Chiasmus:** Donald W. Parry, *Poetic Parallelisms in the Book of Mormon: The Complete Text Reformatted in Worth-while Poetic Lines* (FARMS / Neal A. Maxwell Institute, 2007); John W. Welch, "Chiasmus in the Book of Mormon" (*BYU Studies*, 1969); Scripture Central / KnoWhy, *What Can We Learn from 10 of the Best Chiasms in the Book of Mormon?*.
- **Internal Geography:** Dr. John L. Sorenson, *Mormon's Map* (FARMS, 1990); John W. Welch and J. Gregory Welch, *Charting the Book of Mormon: Visual Aids for Personal Study and Teaching* (FARMS, 1999).
- **Nephite Legal Cases & Ancient Law:** John W. Welch, *The Legal Cases in the Book of Mormon* (Brigham Young University Press / Neal A. Maxwell Institute, 2008).
