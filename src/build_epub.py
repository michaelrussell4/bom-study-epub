"""EPUB3 compiler for the Book of Mormon Study Edition.

Combines 1830 First Edition vs. Latest Edition diffs, Book of Mormon Onomasticon
pop-up footnotes on every mention, and 19th-century historical scripture discourse citations.
"""

from __future__ import annotations
import os
import re
import sys
import json
import uuid
import html
import argparse
from typing import Dict, List, Optional, Set
import ebooklib
from ebooklib import epub

from .differ import diff_verse
from .onomasticon import OnomaMatcher, load_onomasticon, slugify_lemma
from .citations import (
    load_citations,
    get_citation_verse_key,
    render_citation_aside,
    SLUG_TO_CIT_PREFIX,
)
from .chiasmus import (
    get_chiasms_for_verse,
    get_legal_case_for_verse,
    get_study_note_for_verse,
)
from .appendices import (
    render_appendix_chiasmus_xhtml,
    render_appendix_geography_xhtml,
    render_appendix_legal_cases_xhtml,
    render_appendix_charts_xhtml,
)

# Canonical Book of Mormon order and chapter counts
BOOKS_METADATA = [
    {"name": "1 Nephi", "slug": "1-nephi", "chapters": 22},
    {"name": "2 Nephi", "slug": "2-nephi", "chapters": 33},
    {"name": "Jacob", "slug": "jacob", "chapters": 7},
    {"name": "Enos", "slug": "enos", "chapters": 1},
    {"name": "Jarom", "slug": "jarom", "chapters": 1},
    {"name": "Omni", "slug": "omni", "chapters": 1},
    {"name": "Words of Mormon", "slug": "words-of-mormon", "chapters": 1},
    {"name": "Mosiah", "slug": "mosiah", "chapters": 29},
    {"name": "Alma", "slug": "alma", "chapters": 63},
    {"name": "Helaman", "slug": "helaman", "chapters": 16},
    {"name": "3 Nephi", "slug": "3-nephi", "chapters": 30},
    {"name": "4 Nephi", "slug": "4-nephi", "chapters": 1},
    {"name": "Mormon", "slug": "mormon", "chapters": 9},
    {"name": "Ether", "slug": "ether", "chapters": 15},
    {"name": "Moroni", "slug": "moroni", "chapters": 10},
]


def load_stylesheet(path: Optional[str] = None) -> str:
    """Load CSS stylesheet from src/styles.css or custom path."""
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    default_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(default_path):
        with open(default_path, "r", encoding="utf-8") as f:
            return f.read()
    return "/* Missing styles.css */"


def render_title_page_xhtml() -> str:
    """Render elegant title page XHTML."""
    return """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
  <title>Title Page</title>
  <link rel="stylesheet" type="text/css" href="../styles/style.css" />
</head>
<body>
  <section epub:type="titlepage" class="titlepage-section">
    <div style="text-align: center; margin-top: 2.5em; margin-bottom: 2em;">
      <h1 class="title-main">The Book of Mormon</h1>
      <h2 class="title-sub">Scholarly Study Edition</h2>
      <p style="font-size: 0.92em; color: #8c6d3b; font-weight: 600; margin-top: 0.6em; letter-spacing: 0.04em;">
        1830 Revisions &#8226; Onomasticon &#8226; Historical Sources &#8226; Chiasmus &amp; Maps
      </p>

      <div class="ornament">&#10087; &#8226; &#10086; &#8226; &#10087;</div>

      <p style="font-size: 1.1em; color: #444; margin-top: 1.5em; font-style: italic;">
        An Account Written by the Hand of Mormon<br />
        upon Plates Taken from the Plates of Nephi
      </p>

      <p style="font-size: 0.95em; color: #666; margin-top: 2.5em;">
        Translated by Joseph Smith, Jun.
      </p>

      <div style="margin-top: 3.5em; padding-top: 1.5em; border-top: 1px solid #dcd3c5; font-size: 0.88em; color: #777;">
        <p>Featuring inline 1830 First Edition revisions (strikethrough / italics),<br />
        in-place lexical etymologies from the <em>Book of Mormon Onomasticon</em> on proper names,<br />
        verbatim 19th-century historical discourse excerpts (1830&#8211;1930),<br />
        and comprehensive study appendices with 16 visual aid charts and maps on Hebrew chiasmus, internal geography, legal cases, and chronology.</p>
        <p style="margin-top: 1.2em; font-weight: bold; color: #555;">Beautiful Feet Press &#8226; Scholarly Study Series</p>
      </div>
    </div>
  </section>
</body>
</html>"""


def render_intro_xhtml() -> str:
    """Render Introduction and Reader's Guide XHTML."""
    return """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
  <title>Reader's Guide</title>
  <link rel="stylesheet" type="text/css" href="../styles/style.css" />
</head>
<body>
  <section epub:type="frontmatter" class="intro-section">
    <h1 class="book-title">Reader&#8217;s Guide</h1>
    <div class="ornament">&#10087; &#8226; &#10086; &#8226; &#10087;</div>

    <div class="intro-box">
      <h3>About this Scholarly Study Edition</h3>
      <p>This digital study edition of the Book of Mormon integrates textual history, lexical etymology, early historical commentary, and foundational scholarly research directly into the reading flow:</p>
      <ol>
        <li>
          <strong>Inline 1830 First Edition Revisions:</strong> Where the modern reading differs from the 1830 Palmyra first edition, 1830 wording is rendered inline in strikethrough markup (<s>example</s>), immediately followed by modern wording in italic markup (<em>example</em>). Additions present only in the latest edition appear italicized (<em>added text</em>). This provides an immediate visual record of textual development from the first printing to the present day.
        </li>
        <li>
          <strong>Book of Mormon Onomasticon Pop-up Footnotes:</strong> Proper names of persons and places are tagged with interactive links on each occurrence. Tapping or clicking any name opens an EPUB3 modal pop-up note containing the canonical lemma, IPA pronunciation, classification, definition, and synthesized Semitic / Egyptian etymological roots.
        </li>
        <li>
          <strong>Early Historical Scripture Citations &amp; Excerpts (1830&#8211;1930):</strong> Verses expounded by early Church leaders are marked with crimson numbered citations (<span style="color:#990000; font-weight:bold;">[1]</span>). Each footnote features the <em>verbatim discourse excerpt</em> from the <em>Journal of Discourses</em> (1854&#8211;1886) or <em>Teachings of the Prophet Joseph Smith</em> (TPJS). When a discourse addresses a multi-verse passage, the note attaches to the concluding verse with the full span identified, highlighting the quoted scripture reference.
        </li>
        <li>
          <strong>Supplemental Study Appendices &amp; Verse Cross-Linking:</strong> Four comprehensive back-matter appendices provide in-depth scholarly references complete with 16 high-resolution visual charts, diagrams, and maps:
          <ul style="margin-top: 0.5em; padding-left: 1.2em;">
            <li><strong>Appendix A — Hebrew Poetic Parallelisms &amp; Prominent Chiasmus:</strong> Symmetrical poetic layouts and diagrams for the 10 best-attested chiasms (e.g., Alma 36, Mosiah 5:10&#8211;12, Mosiah 3:18&#8211;19, Helaman 6:7&#8211;13). Marked at relevant verses with <span class="fn-badge fn-badge-chiasmus">&#9781; Chiasmus</span>.</li>
            <li><strong>Appendix B — Internal Geography &amp; Mormon's Map:</strong> Dr. John L. Sorenson's internal relational topography, Welch's 10 essential criteria, a structured breakdown of the 12 journeys between Nephi and Zarahemla, and high-resolution route maps. Marked at Alma 22:27 with <span class="fn-badge fn-badge-geo">&#128506; Mormon's Map</span>.</li>
            <li><strong>Appendix C — Legal Cases &amp; Ancient Judicial Procedures:</strong> In-depth jurisprudence analysis and trial flowcharts for Abinadi, Sherem, Nehor, Korihor, Ammonihah, Paanchi, and Seantum based on John W. Welch's legal studies. Marked at relevant trial verses with <span class="fn-badge fn-badge-legal">&#9878; Law</span>.</li>
            <li><strong>Appendix D — Chronology, Plates, &amp; Structural Charts:</strong> Nephite plate lineages, Lehi lineage lifespans, King Mosiah's monetary weight system (<span class="fn-badge fn-badge-chart">&#128202; Monetary System</span> at Alma 11:1), and Zenos's Allegory of the Olive Tree (<span class="fn-badge fn-badge-chart">&#127795; Olive Tree</span> at Jacob 5:1).</li>
          </ul>
        </li>
      </ol>
    </div>

    <h3 class="footnotes-title">Kindle &amp; E-Reader Pop-up Navigation</h3>
    <p>On Kindle devices (Paperwhite, Oasis, Scribe, Colorsoft) and modern reading apps (Apple Books, Kobo, Thorium), tapping any tagged name, citation badge, or study badge displays the note in an instant pop-up panel without leaving your reading position. Tapping the link inside any study note takes you directly to the full appendix analysis, and the appendix entry provides a one-tap return link (&#8617;) directly back to the exact verse.</p>
  </section>
</body>
</html>"""


def render_chiasmus_aside(chia: dict, verse_num: int) -> str:
    """Render a pop-up footnote aside for a prominent chiasmus with link to Appendix A."""
    chia_id = chia["id"]
    fn_id = f"fn-chia-{chia_id}"
    ref_id = f"ref-chia-{chia_id}"
    target_url = f"appendix_chiasmus.xhtml#{chia_id}"
    return f"""      <aside id="{fn_id}" epub:type="footnote" class="footnote-item footnote-chiasmus">
        <div class="fn-header">
          <span class="fn-badge fn-badge-chiasmus">Hebrew Poetic Structure</span>
          <strong>{html.escape(chia['title'])}</strong>
        </div>
        <div class="fn-body">
          <p>{html.escape(chia['summary'])}</p>
          <p class="center-callout"><strong>Chiastic Center:</strong> {html.escape(chia['center_focus'])}</p>
          <p class="fn-appendix-link"><a href="{target_url}">Explore the complete poetic structure and chiastic diagram in Appendix A &#8594;</a></p>
        </div>
        <div class="fn-nav-bottom">
          <a class="return-link" href="#{ref_id}" title="Return to verse {verse_num}">&#8617; Back to verse {verse_num}</a>
        </div>
      </aside>"""


def render_legal_aside(legal: dict, verse_num: int) -> str:
    """Render a pop-up footnote aside for a legal case with link to Appendix C."""
    fn_id = f"fn-legal-{legal['id']}"
    ref_id = f"ref-legal-{legal['id']}"
    target_url = legal["target"]
    return f"""      <aside id="{fn_id}" epub:type="footnote" class="footnote-item footnote-legal">
        <div class="fn-header">
          <span class="fn-badge fn-badge-legal">Ancient Jurisprudence</span>
          <strong>{html.escape(legal['title'])}</strong>
        </div>
        <div class="fn-body">
          <p>{html.escape(legal['summary'])}</p>
          <p class="fn-appendix-link"><a href="{target_url}">Read the full legal case analysis in Appendix C &#8594;</a></p>
        </div>
        <div class="fn-nav-bottom">
          <a class="return-link" href="#{ref_id}" title="Return to verse {verse_num}">&#8617; Back to verse {verse_num}</a>
        </div>
      </aside>"""


def render_study_note_aside(note: dict, verse_num: int) -> str:
    """Render a pop-up footnote aside for a geography or chart resource."""
    fn_id = f"fn-study-{note['id']}"
    ref_id = f"ref-study-{note['id']}"
    target_url = note["target"]
    badge_class = "fn-badge-geo" if "geo" in note["id"] else ("fn-badge-chart" if "chart" in note["id"] or "monetary" in note["id"] else "fn-badge")
    return f"""      <aside id="{fn_id}" epub:type="footnote" class="footnote-item {'footnote-geo' if 'geo' in note['id'] else 'footnote-chart'}">
        <div class="fn-header">
          <span class="fn-badge {badge_class}">Study Resource</span>
          <strong>{html.escape(note['title'])}</strong>
        </div>
        <div class="fn-body">
          <p>{html.escape(note['summary'])}</p>
          <p class="fn-appendix-link"><a href="{target_url}">View maps, charts, and analysis in the Appendices &#8594;</a></p>
        </div>
        <div class="fn-nav-bottom">
          <a class="return-link" href="#{ref_id}" title="Return to verse {verse_num}">&#8617; Back to verse {verse_num}</a>
        </div>
      </aside>"""


def render_chapter_xhtml(
    book_name: str,
    book_slug: str,
    chapter_num: int,
    total_chapters: int,
    verses: List[dict],
    chapter_onoma: Dict[str, dict],
    onoma_verse_map: Dict[str, int],
    chapter_citations: Dict[str, List[dict]],
    matcher: Optional[OnomaMatcher],
    chapter_chiasms: Optional[List[dict]] = None,
    chapter_legals: Optional[List[Tuple[dict, int]]] = None,
    chapter_study_notes: Optional[List[Tuple[dict, int]]] = None,
) -> str:
    """Render a chapter into valid EPUB3 XHTML."""
    title_text = f"{book_name}" if total_chapters == 1 else f"{book_name} {chapter_num}"
    lines: List[str] = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">',
        "<head>",
        f"  <title>{html.escape(title_text)}</title>",
        '  <link rel="stylesheet" type="text/css" href="../styles/style.css" />',
        "</head>",
        "<body>",
        '  <section epub:type="chapter" class="chapter-content">',
        f'    <h2 class="chapter-title">{html.escape(title_text)}</h2>',
    ]

    # Verse lines
    for v in verses:
        v_num = v["verse"]
        v_body = v["html"]
        lines.append(
            f'    <p class="verse" id="v{v_num}">'
            f'<span class="verse-num">{v_num}</span> '
            f"{v_body}</p>"
        )

    # Footnotes container (if Onomasticon, Citations, Chiasmus, Law, or Study Notes exist)
    has_footnotes = bool(chapter_onoma or chapter_citations or chapter_chiasms or chapter_legals or chapter_study_notes)
    if has_footnotes:
        lines.extend([
            '    <section epub:type="footnotes" class="footnotes-section">',
            '      <h3 class="footnotes-title">Study Notes &amp; Historical Expositions</h3>',
        ])
        rendered_count = 0

        # 1. Onomasticon Entries
        if chapter_onoma and matcher:
            lines.append("      <!-- Onomasticon Etymology Notes -->")
            for slug, entry in sorted(chapter_onoma.items()):
                if rendered_count > 0:
                    lines.append('      <hr class="fn-divider" />')
                rendered_count += 1
                v_num = onoma_verse_map.get(slug)
                aside_html = matcher.render_aside(slug, entry, verse_num=v_num)
                lines.append(aside_html)

        # 2. Historical Citation Entries
        if chapter_citations:
            lines.append("      <!-- Early Historical Citations & Discourse Excerpts -->")
            cit_prefix = SLUG_TO_CIT_PREFIX.get(book_slug, book_slug)
            for v_key, cits in sorted(
                chapter_citations.items(),
                key=lambda item: int(item[0].split("-")[-1]) if item[0].split("-")[-1].isdigit() else 0,
            ):
                if rendered_count > 0:
                    lines.append('      <hr class="fn-divider" />')
                rendered_count += 1
                v_num_int = int(v_key.split("-")[-1]) if v_key.split("-")[-1].isdigit() else 1
                cit_aside = render_citation_aside(
                    v_key=v_key,
                    cits=cits,
                    verse_num=v_num_int,
                    cit_prefix=cit_prefix,
                    chapter_num=chapter_num,
                )
                lines.append(cit_aside)

        # 3. Prominent Chiasmus Entries
        if chapter_chiasms:
            lines.append("      <!-- Hebrew Poetic & Chiastic Structure Notes -->")
            for chia in chapter_chiasms:
                if rendered_count > 0:
                    lines.append('      <hr class="fn-divider" />')
                rendered_count += 1
                k_verse = chia["key_verses"][0]
                lines.append(render_chiasmus_aside(chia, verse_num=k_verse))

        # 4. Legal Cases Entries
        if chapter_legals:
            lines.append("      <!-- Ancient Jurisprudence & Legal Proceedings -->")
            for legal, v_num in chapter_legals:
                if rendered_count > 0:
                    lines.append('      <hr class="fn-divider" />')
                rendered_count += 1
                lines.append(render_legal_aside(legal, verse_num=v_num))

        # 5. Special Study Notes (Geography, Monetary, Olive tree)
        if chapter_study_notes:
            lines.append("      <!-- Internal Geography & Topical Study Visuals -->")
            for note, v_num in chapter_study_notes:
                if rendered_count > 0:
                    lines.append('      <hr class="fn-divider" />')
                rendered_count += 1
                lines.append(render_study_note_aside(note, verse_num=v_num))

        lines.append("    </section>")

    lines.extend([
        "  </section>",
        "</body>",
        "</html>",
    ])

    return "\n".join([line for line in lines if line])


def build_study_epub(
    output_path: str = "output/Book_of_Mormon_Study_Edition.epub",
    data_dir: str = "data",
    onomasticon_path: str = "data/onomasticon.json",
    citations_path: str = "data/early_citations.json",
    cover_path: str = "assets/images/cover.jpg",
    substantive_only: bool = False,
    density: str = "all",  # "all", "chapter", "book"
    book_filter: Optional[List[str]] = None,
    skip_diff: bool = False,
    skip_onoma: bool = False,
    skip_citations: bool = False,
    skip_appendices: bool = False,
) -> str:
    """Build the EPUB3 Book of Mormon Study Edition e-book."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Initialize Onomasticon matcher if enabled
    matcher: Optional[OnomaMatcher] = None
    if not skip_onoma and os.path.exists(onomasticon_path):
        onoma_dict = load_onomasticon(onomasticon_path)
        matcher = OnomaMatcher(onoma_dict)
        print(f"Loaded {len(onoma_dict)} Onomasticon lemmas from {onomasticon_path}")
    elif not skip_onoma:
        print(f"Warning: Onomasticon data file not found at {onomasticon_path}; proceeding without Onomasticon notes.")

    # 2. Initialize Early Historical Citations if enabled
    citations_dict: Dict[str, List[dict]] = {}
    if not skip_citations and os.path.exists(citations_path):
        citations_dict = load_citations(citations_path)
        total_cit_verses = len(citations_dict)
        total_cit_records = sum(len(cl) for cl in citations_dict.values())
        print(f"Loaded {total_cit_records} historical citations across {total_cit_verses} verses from {citations_path}")
    elif not skip_citations:
        print(f"Warning: Citations data file not found at {citations_path}; proceeding without historical citations.")

    # 3. Setup ebooklib EpubBook
    book = epub.EpubBook()
    book.set_identifier(f"urn:uuid:{uuid.uuid4()}")
    book.set_title("The Book of Mormon: Scholarly Study Edition")
    book.set_language("en")
    book.add_author("Translated by Joseph Smith, Jun.")
    book.add_metadata(
        "DC",
        "description",
        "Scholarly study edition of the Book of Mormon featuring inline 1830 First Edition revisions (strikethrough / italics), in-place lexical etymologies from the Book of Mormon Onomasticon, verbatim 19th-century historical discourse excerpts (1830–1930), and comprehensive study appendices with 16 visual aid charts and maps on Hebrew chiasmus, internal geography, legal cases, and chronology.",
    )
    book.add_metadata("DC", "publisher", "Beautiful Feet Press")

    # 4. Add Cover image & page if present
    cover_item = None
    if os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            cover_bytes = f.read()
        book.set_cover("images/cover.jpg", cover_bytes, create_page=True)
        for item in book.get_items():
            if item.get_name() == "cover.xhtml":
                cover_item = item
                cover_item.content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
  <title>Cover</title>
  <style type="text/css">
    @page {{ margin: 0; padding: 0; }}
    body {{ margin: 0; padding: 0; text-align: center; background-color: #0b172a; }}
    div.cover-wrapper {{ height: 100vh; margin: 0; padding: 0; text-align: center; display: flex; justify-content: center; align-items: center; }}
    img.cover-image {{ max-height: 100%; max-width: 100%; height: 100vh; object-fit: contain; margin: 0 auto; }}
  </style>
</head>
<body>
  <div class="cover-wrapper">
    <img class="cover-image" src="images/cover.jpg" alt="Cover: The Book of Mormon Study Edition" />
  </div>
</body>
</html>""".encode("utf-8")
                break
        print(f"Embedded cover image from {cover_path}")

    # 5. Add Stylesheet
    css_content = load_stylesheet()
    style_item = epub.EpubItem(
        uid="style_css",
        file_name="styles/style.css",
        media_type="text/css",
        content=css_content.encode("utf-8"),
    )
    book.add_item(style_item)

    # 6. Add Title Page & Reader's Guide
    title_html = render_title_page_xhtml()
    title_item = epub.EpubHtml(
        title="Title Page",
        file_name="text/titlepage.xhtml",
        lang="en",
        content=title_html.encode("utf-8"),
    )
    title_item.add_item(style_item)
    book.add_item(title_item)

    intro_html = render_intro_xhtml()
    intro_item = epub.EpubHtml(
        title="Reader's Guide",
        file_name="text/intro.xhtml",
        lang="en",
        content=intro_html.encode("utf-8"),
    )
    intro_item.add_item(style_item)
    book.add_item(intro_item)

    # 7. Process Books & Chapters
    spine_items = ["nav"]
    toc_structure = []

    if cover_item:
        spine_items.append(cover_item)
        toc_structure.append(cover_item)

    spine_items.extend([title_item, intro_item])
    toc_structure.extend([title_item, intro_item])

    dir_1830 = os.path.join(data_dir, "1830")
    dir_latest = os.path.join(data_dir, "latest")

    total_chapters_built = 0
    total_verses_built = 0
    total_onoma_mentions_tagged = 0
    total_diffs_injected = 0
    total_citations_injected = 0
    total_chiasms_injected = 0
    total_legals_injected = 0
    total_study_notes_injected = 0

    target_books = BOOKS_METADATA
    if book_filter:
        filter_set = set(b.lower().strip() for b in book_filter)
        target_books = [b for b in BOOKS_METADATA if b["slug"] in filter_set or b["name"].lower() in filter_set]

    print(f"Processing {len(target_books)} books (substantive_only={substantive_only}, density={density})...")

    for b_meta in target_books:
        book_slug = b_meta["slug"]
        book_name = b_meta["name"]
        chapter_count = b_meta["chapters"]

        book_tagged_lemmas: Set[str] = set()
        book_toc_subitems = []

        for ch_num in range(1, chapter_count + 1):
            file_1830 = os.path.join(dir_1830, book_slug, f"{ch_num}.json")
            file_latest = os.path.join(dir_latest, book_slug, f"{ch_num}.json")

            if not os.path.exists(file_latest):
                continue

            with open(file_latest, "r", encoding="utf-8") as f:
                data_latest = json.load(f)

            data_1830 = {"verses": []}
            if os.path.exists(file_1830):
                with open(file_1830, "r", encoding="utf-8") as f:
                    data_1830 = json.load(f)

            verses_1830_map = {v["verse"]: v["text"] for v in data_1830.get("verses", [])}
            verses_latest = data_latest.get("verses", [])

            # Density tracking
            if density == "chapter":
                tagged_lemmas_set = set()
            elif density == "book":
                tagged_lemmas_set = book_tagged_lemmas
            else:
                # "all" density
                tagged_lemmas_set = set()

            chapter_onoma: Dict[str, dict] = {}
            onoma_verse_map: Dict[str, int] = {}
            mention_counts: Dict[str, int] = {}
            chapter_citations: Dict[str, List[dict]] = {}
            chapter_chiasms: List[dict] = []
            chapter_legals: List[Tuple[dict, int]] = []
            chapter_study_notes: List[Tuple[dict, int]] = []
            citation_chapter_counter = 0

            processed_verses: List[dict] = []

            for v in verses_latest:
                v_num = v["verse"]
                t_latest = v["text"]
                t_1830 = verses_1830_map.get(v_num, "")

                # 1. Diff engine
                if skip_diff:
                    v_html = html.escape(t_latest, quote=False)
                else:
                    v_html = diff_verse(t_1830, t_latest, substantive_only=substantive_only)
                    if "<s" in v_html or "<em" in v_html:
                        total_diffs_injected += 1

                # 2. Onomasticon tagging (every mention by default)
                if matcher and not skip_onoma:
                    v_html = matcher.tag_verse_html(
                        verse_html=v_html,
                        tagged_set=tagged_lemmas_set,
                        chapter_entries=chapter_onoma,
                        verse_num=v_num,
                        onoma_verse_map=onoma_verse_map,
                        mention_counts=mention_counts,
                        density=density,
                    )

                # 3. Citation tagging
                if citations_dict and not skip_citations:
                    v_key = get_citation_verse_key(book_slug, ch_num, v_num)
                    cits = citations_dict.get(v_key, [])
                    if cits:
                        citation_chapter_counter += 1
                        total_citations_injected += len(cits)
                        chapter_citations[v_key] = cits
                        ref_id = f"ref-cit-{v_key}"
                        fn_id = f"fn-cit-{v_key}"
                        cit_link = (
                            f' <a epub:type="noteref" class="noteref cit-ref" '
                            f'href="#{fn_id}" id="{ref_id}"><sup>[{citation_chapter_counter}]</sup></a>'
                        )
                        v_html = v_html.rstrip() + cit_link

                # 4. Prominent Chiasmus tagging
                if not skip_appendices:
                    chias = get_chiasms_for_verse(book_slug, ch_num, v_num)
                    for chia in chias:
                        total_chiasms_injected += 1
                        chia_id = chia["id"]
                        ref_id = f"ref-chia-{chia_id}"
                        fn_id = f"fn-chia-{chia_id}"
                        chia_link = (
                            f' <a epub:type="noteref" class="noteref chiasmus-ref" '
                            f'href="#{fn_id}" id="{ref_id}" title="Hebrew Chiastic Structure"><sup>[☵ Chiasmus]</sup></a>'
                        )
                        v_html = v_html.rstrip() + chia_link
                        chapter_chiasms.append(chia)

                    # 5. Legal Cases tagging
                    legal = get_legal_case_for_verse(book_slug, ch_num, v_num)
                    if legal:
                        total_legals_injected += 1
                        ref_id = f"ref-legal-{legal['id']}"
                        fn_id = f"fn-legal-{legal['id']}"
                        badge_label = legal["badge"].split(":")[-1].strip()
                        legal_link = (
                            f' <a epub:type="noteref" class="noteref legal-ref" '
                            f'href="#{fn_id}" id="{ref_id}" title="{html.escape(legal["title"])}"><sup>[⚖ {badge_label}]</sup></a>'
                        )
                        v_html = v_html.rstrip() + legal_link
                        chapter_legals.append((legal, v_num))

                    # 6. Special Study Notes tagging (Geography, Monetary, Olive tree)
                    sn = get_study_note_for_verse(book_slug, ch_num, v_num)
                    if sn:
                        total_study_notes_injected += 1
                        ref_id = f"ref-study-{sn['id']}"
                        fn_id = f"fn-study-{sn['id']}"
                        sn_symbol = "🗺" if "geo" in sn["id"] else "📊"
                        sn_label = sn["title"].split(":")[0]
                        sn_link = (
                            f' <a epub:type="noteref" class="noteref chart-ref" '
                            f'href="#{fn_id}" id="{ref_id}" title="{html.escape(sn["title"])}"><sup>[{sn_symbol} {sn_label}]</sup></a>'
                        )
                        v_html = v_html.rstrip() + sn_link
                        chapter_study_notes.append((sn, v_num))

                processed_verses.append({"verse": v_num, "html": v_html})
                total_verses_built += 1

            total_onoma_mentions_tagged += sum(mention_counts.values()) if mention_counts else len(chapter_onoma)

            # Render XHTML
            ch_xhtml = render_chapter_xhtml(
                book_name=book_name,
                book_slug=book_slug,
                chapter_num=ch_num,
                total_chapters=chapter_count,
                verses=processed_verses,
                chapter_onoma=chapter_onoma,
                onoma_verse_map=onoma_verse_map,
                chapter_citations=chapter_citations,
                matcher=matcher,
                chapter_chiasms=chapter_chiasms,
                chapter_legals=chapter_legals,
                chapter_study_notes=chapter_study_notes,
            )

            file_name = f"text/{book_slug}_{ch_num:02d}.xhtml"
            ch_title = f"{book_name}" if chapter_count == 1 else f"{book_name} {ch_num}"

            ch_item = epub.EpubHtml(
                title=ch_title,
                file_name=file_name,
                lang="en",
                content=ch_xhtml.encode("utf-8"),
            )
            ch_item.add_item(style_item)
            book.add_item(ch_item)

            spine_items.append(ch_item)
            book_toc_subitems.append(ch_item)
            total_chapters_built += 1

        if len(book_toc_subitems) == 1:
            toc_structure.append(book_toc_subitems[0])
        elif book_toc_subitems:
            toc_structure.append((epub.Section(book_name), book_toc_subitems))

    # 8. Appendices (Supplemental Study Resources)
    if not skip_appendices:
        appendix_items = []
        appendix_toc_subitems = []

        # Appendix A: Chiasmus
        app_a_xhtml = render_appendix_chiasmus_xhtml()
        app_a_item = epub.EpubHtml(
            title="Appendix A: Hebrew Poetic Parallelisms & Chiasmus",
            file_name="text/appendix_chiasmus.xhtml",
            lang="en",
            content=app_a_xhtml.encode("utf-8"),
        )
        app_a_item.add_item(style_item)
        book.add_item(app_a_item)
        appendix_items.append(app_a_item)
        appendix_toc_subitems.append(app_a_item)

        # Appendix B: Geography
        app_b_xhtml = render_appendix_geography_xhtml()
        app_b_item = epub.EpubHtml(
            title="Appendix B: Internal Geography & Mormon's Map",
            file_name="text/appendix_geography.xhtml",
            lang="en",
            content=app_b_xhtml.encode("utf-8"),
        )
        app_b_item.add_item(style_item)
        book.add_item(app_b_item)
        appendix_items.append(app_b_item)
        appendix_toc_subitems.append(app_b_item)

        # Appendix C: Legal Cases
        app_c_xhtml = render_appendix_legal_cases_xhtml()
        app_c_item = epub.EpubHtml(
            title="Appendix C: Legal Cases & Judicial Procedures",
            file_name="text/appendix_legal_cases.xhtml",
            lang="en",
            content=app_c_xhtml.encode("utf-8"),
        )
        app_c_item.add_item(style_item)
        book.add_item(app_c_item)
        appendix_items.append(app_c_item)
        appendix_toc_subitems.append(app_c_item)

        # Appendix D: Charts & Chronology
        app_d_xhtml = render_appendix_charts_xhtml()
        app_d_item = epub.EpubHtml(
            title="Appendix D: Chronology, Plates, & Structural Charts",
            file_name="text/appendix_charts.xhtml",
            lang="en",
            content=app_d_xhtml.encode("utf-8"),
        )
        app_d_item.add_item(style_item)
        book.add_item(app_d_item)
        appendix_items.append(app_d_item)
        appendix_toc_subitems.append(app_d_item)

        # Bundle Appendix Images into EPUB manifest
        app_img_dir = "assets/images/appendix"
        if os.path.exists(app_img_dir):
            for img_file in sorted(os.listdir(app_img_dir)):
                if img_file.endswith(".png") or img_file.endswith(".jpg"):
                    img_path = os.path.join(app_img_dir, img_file)
                    with open(img_path, "rb") as f:
                        img_bytes = f.read()
                    img_item = epub.EpubItem(
                        uid=f"img_{img_file.replace('.', '_')}",
                        file_name=f"images/appendix/{img_file}",
                        media_type="image/png" if img_file.endswith(".png") else "image/jpeg",
                        content=img_bytes,
                    )
                    book.add_item(img_item)

        spine_items.extend(appendix_items)
        toc_structure.append((epub.Section("Supplemental Study Resources"), appendix_toc_subitems))

    # Configure TOC & Spine
    book.toc = toc_structure
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine_items

    # Write EPUB file
    print(f"Writing EPUB3 file to {output_path}...")
    epub.write_epub(output_path, book, {"epub3_landmark": True, "epub3_pages": False})
    size_mb = os.path.getsize(output_path) / (1024 * 1024)

    print("\n--- Build Complete ---")
    print(f"Output File:             {output_path} ({size_mb:.2f} MB)")
    print(f"Books Processed:         {len(target_books)}")
    print(f"Chapters Processed:      {total_chapters_built}")
    print(f"Verses Processed:        {total_verses_built}")
    print(f"Verses with Diffs:       {total_diffs_injected}")
    print(f"Onomasticon Links:       {total_onoma_mentions_tagged}")
    print(f"Historical Citations:    {total_citations_injected}")
    print(f"Chiasmus Verse Links:    {total_chiasms_injected}")
    print(f"Legal Case Links:        {total_legals_injected}")
    print(f"Special Study Links:     {total_study_notes_injected}")
    if not skip_appendices:
        print("Appendices:              4 (A: Chiasmus, B: Geography, C: Law, D: Charts)")
    print("----------------------\n")

    return output_path


def main():
    """CLI entrypoint for building the EPUB3 file."""
    parser = argparse.ArgumentParser(
        description="Compile the Book of Mormon Study EPUB3 e-book with 1830 diffs, Onomasticon notes on every mention, and historical citations."
    )
    parser.add_argument(
        "-o", "--output",
        default="output/Book_of_Mormon_Study_Edition.epub",
        help="Path for compiled .epub file (default: output/Book_of_Mormon_Study_Edition.epub)",
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Path to root data directory containing '1830' and 'latest' folders (default: data)",
    )
    parser.add_argument(
        "--onomasticon",
        default="data/onomasticon.json",
        help="Path to onomasticon.json dictionary (default: data/onomasticon.json)",
    )
    parser.add_argument(
        "--citations",
        default="data/early_citations.json",
        help="Path to early_citations.json historical scripture citations (default: data/early_citations.json)",
    )
    parser.add_argument(
        "--cover",
        default="assets/images/cover.jpg",
        help="Path to cover image (default: assets/images/cover.jpg)",
    )
    parser.add_argument(
        "--substantive-only",
        action="store_true",
        help="Ignore pure punctuation and capitalization adjustments, highlighting only substantive word differences.",
    )

    # Link density options
    density_group = parser.add_mutually_exclusive_group()
    density_group.add_argument(
        "--all-mentions",
        dest="density",
        action="store_const",
        const="all",
        help="Tag proper names on every occurrence (default).",
    )
    density_group.add_argument(
        "--first-mention-per-chapter",
        dest="density",
        action="store_const",
        const="chapter",
        help="Tag proper names only on their first appearance in each chapter.",
    )
    density_group.add_argument(
        "--first-mention-per-book",
        dest="density",
        action="store_const",
        const="book",
        help="Tag proper names only on their first appearance in each entire book.",
    )
    parser.set_defaults(density="all")

    parser.add_argument(
        "--books",
        nargs="+",
        help="Compile only specific books by slug or name (e.g. --books 1-nephi 2-nephi enos)",
    )
    parser.add_argument(
        "--skip-diff",
        action="store_true",
        help="Omit 1830 inline diff strikethrough/italic tags, rendering clean modern text.",
    )
    parser.add_argument(
        "--skip-onoma",
        action="store_true",
        help="Omit Onomasticon etymology noteref popups and footnote sections.",
    )
    parser.add_argument(
        "--skip-citations",
        action="store_true",
        help="Omit 19th-century historical scripture citations and discourse excerpts.",
    )
    parser.add_argument(
        "--skip-appendices",
        action="store_true",
        help="Omit supplemental study appendices (chiasmus, geography, law, charts).",
    )

    args = parser.parse_args()

    build_study_epub(
        output_path=args.output,
        data_dir=args.data_dir,
        onomasticon_path=args.onomasticon,
        citations_path=args.citations,
        cover_path=args.cover,
        substantive_only=args.substantive_only,
        density=args.density,
        book_filter=args.books,
        skip_diff=args.skip_diff,
        skip_onoma=args.skip_onoma,
        skip_citations=args.skip_citations,
        skip_appendices=args.skip_appendices,
    )


if __name__ == "__main__":
    main()

