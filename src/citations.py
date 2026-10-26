"""Early historical scripture citations and discourse excerpts integration (1830-1930)."""

from __future__ import annotations
import os
import re
import json
import html
from collections import defaultdict
from typing import Dict, List, Set, Optional, Tuple

# Mapping from canonical book slug to citation prefix used in early_citations.json
SLUG_TO_CIT_PREFIX: Dict[str, str] = {
    "1-nephi": "1-ne",
    "2-nephi": "2-ne",
    "jacob": "jacob",
    "enos": "enos",
    "jarom": "jarom",
    "omni": "omni",
    "words-of-mormon": "w-of-m",
    "mosiah": "mosiah",
    "alma": "alma",
    "helaman": "hel",
    "3-nephi": "3-ne",
    "4-nephi": "4-ne",
    "mormon": "morm",
    "ether": "ether",
    "moroni": "moroni",
}

BOM_REF_PATTERNS: Dict[str, str] = {
    "1-ne": r"1\s*(?:Nephi|Ne)\b\.?",
    "2-ne": r"2\s*(?:Nephi|Ne)\b\.?",
    "3-ne": r"3\s*(?:Nephi|Ne)\b\.?",
    "4-ne": r"4\s*(?:Nephi|Ne)\b\.?",
    "jacob": r"Jacob\b\.?",
    "enos": r"Enos\b\.?",
    "jarom": r"Jarom\b\.?",
    "omni": r"Omni\b\.?",
    "w-of-m": r"(?:Words\s+of\s+Mormon|W\.?\s*of\s*M\.?|W\s*M)\b\.?",
    "mosiah": r"Mosiah\b\.?",
    "alma": r"Alma\b\.?",
    "hel": r"(?:Helaman|Hel)\b\.?",
    "morm": r"(?:Mormon|Morm)\b\.?",
    "ether": r"Ether\b\.?",
    "moroni": r"(?:Moroni|Moro?)\b\.?",
}


def get_citation_verse_key(book_slug: str, chapter: int, verse: int) -> str:
    """Return the verse key string used in early_citations.json, e.g. '1-ne-1-2'."""
    prefix = SLUG_TO_CIT_PREFIX.get(book_slug, book_slug)
    return f"{prefix}-{chapter}-{verse}"


def parse_verse_range_token(v_spec: str) -> Set[int]:
    """Parse verse specification like '4', '18-20', '1–2', '11, 12' into a set of integer verse numbers."""
    verses: Set[int] = set()
    for part in re.split(r"[,;]", v_spec):
        part = part.strip()
        m = re.match(r"^(\d+)(?:\s*[–—\-]\s*(\d+))?$", part)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else start
            verses.update(range(start, end + 1))
    return verses


def format_verse_numbers(v_nums: List[int]) -> str:
    """Format a list of sorted verse integers into standard ranges like '18–20'."""
    if not v_nums:
        return ""
    v_nums = sorted(set(v_nums))
    ranges = []
    start = v_nums[0]
    prev = v_nums[0]
    for n in v_nums[1:]:
        if n == prev + 1:
            prev = n
        else:
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}–{prev}")
            start = n
            prev = n
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}–{prev}")
    return ", ".join(ranges)


def deduplicate_citations_to_last_verse(
    citation_dict: Dict[str, List[dict]]
) -> Dict[str, List[dict]]:
    """Deduplicate multi-verse citations so each unique citation appears ONLY on the last verse of its range."""
    chap_cits: Dict[str, Dict[Tuple, List[Tuple[int, str, dict]]]] = defaultdict(lambda: defaultdict(list))

    for v_key, c_list in citation_dict.items():
        parts = v_key.rsplit("-", 1)
        if len(parts) != 2 or not parts[1].isdigit():
            continue
        ch_key = parts[0]
        v_num = int(parts[1])
        for c in c_list:
            sig = (
                (c.get("source"), c.get("talk_id"), c.get("target_id"))
                if (c.get("talk_id") and c.get("target_id"))
                else (c.get("source"), c.get("citation"), c.get("speaker"), c.get("talk_title"))
            )
            chap_cits[ch_key][sig].append((v_num, v_key, c))

    deduped: Dict[str, List[dict]] = defaultdict(list)

    for ch_key, sig_map in chap_cits.items():
        for sig, vlist in sig_map.items():
            vlist.sort(key=lambda x: x[0])
            last_vnum, last_vkey, cit = vlist[-1]
            v_nums = [x[0] for x in vlist]

            cit_copy = dict(cit)
            if len(v_nums) > 1:
                cit_copy["covered_range"] = format_verse_numbers(v_nums)
            elif not cit_copy.get("covered_range"):
                cit_copy["covered_range"] = str(last_vnum)

            deduped[last_vkey].append(cit_copy)

    sorted_result: Dict[str, List[dict]] = {}
    for vk in sorted(
        deduped.keys(),
        key=lambda k: (k.rsplit("-", 1)[0], int(k.rsplit("-", 1)[1])),
    ):
        sorted_result[vk] = deduped[vk]

    return sorted_result


def load_citations(path: str = "data/early_citations.json") -> Dict[str, List[dict]]:
    """Load and deduplicate early historical citations (1830-1930)."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw_cits = json.load(f)
    return deduplicate_citations_to_last_verse(raw_cits)


def highlight_verse_reference_in_excerpt(
    text: str,
    cit_prefix: str,
    chapter_num: int,
    target_verses: Set[int],
) -> str:
    """Escape text and bold embedded scripture references matching the target verse/range."""
    escaped = html.escape(text)
    b_pat = BOM_REF_PATTERNS.get(cit_prefix)
    if not b_pat or not target_verses:
        return escaped

    pattern = re.compile(
        rf"\b({b_pat}\s+{chapter_num}\s*:\s*([0-9]+(?:\s*[–—\-]\s*[0-9]+)?(?:\s*,\s*[0-9]+(?:\s*[–—\-]\s*[0-9]+)?)*))\b",
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        full_ref = m.group(1)
        v_spec = m.group(2)
        ref_verses = parse_verse_range_token(v_spec)
        if ref_verses & target_verses:
            return f'<strong class="cit-verse-highlight">{full_ref}</strong>'
        return full_ref

    return pattern.sub(repl, escaped)


def render_citation_aside(
    v_key: str,
    cits: List[dict],
    verse_num: int,
    cit_prefix: str,
    chapter_num: int,
) -> str:
    """Render a footnote <aside> block for historical citations expounding this verse."""
    fn_id = f"fn-cit-{v_key}"
    ref_id = f"ref-cit-{v_key}"
    v_num_str = str(verse_num)

    multi_ranges = [
        c.get("covered_range", "")
        for c in cits
        if c.get("covered_range") and c.get("covered_range") != v_num_str
    ]
    distinct_ranges = set(multi_ranges)
    all_have_same_range = len(distinct_ranges) == 1 and len(multi_ranges) == len(cits)

    if all_have_same_range:
        common_range = list(distinct_ranges)[0]
        header_label = f"Early Historical Discourses on Verses {html.escape(common_range)}:"
    else:
        header_label = f"Early Historical Discourses on Verse {v_num_str}:"

    lines: List[str] = [
        f'      <aside epub:type="footnote" id="{fn_id}" class="footnote-item cit-footnote">',
        f'        <p class="cit-header">{header_label}</p>',
        '        <div class="cit-discourse-list">',
    ]

    for c in cits:
        speaker = c.get("speaker", "")
        speaker_html = f'<span class="cit-speaker">{html.escape(speaker)}</span>' if speaker else ""
        source = c.get("source", "")
        source_html = f'<span class="cit-source-pill">{html.escape(source)}</span>' if source else ""
        citation_str = c.get("citation", "")
        cit_str_html = f'<span class="cit-ref-details">{html.escape(citation_str)}</span>' if citation_str else ""
        year = c.get("year")
        year_html = f'<span class="cit-year">({year})</span>' if year else ""
        covered_range = c.get("covered_range", "")
        range_badge = (
            f'<span class="cit-range-badge">Verses {html.escape(covered_range)}</span>'
            if covered_range and covered_range != v_num_str
            else ""
        )
        talk_title = c.get("talk_title", "")
        title_html = (
            f'<p class="cit-title-line">&ldquo;{html.escape(talk_title)}&rdquo;</p>'
            if talk_title
            else ""
        )

        meta_parts = [p for p in [speaker_html, source_html, cit_str_html, year_html, range_badge] if p]
        meta_line = " &#8226; ".join(meta_parts[:2])
        if len(meta_parts) > 2:
            meta_line += " " + " ".join(meta_parts[2:])

        lines.extend([
            '          <div class="cit-discourse-item">',
            f'            <div class="cit-meta">{meta_line}</div>',
            f'            {title_html}' if title_html else "",
        ])

        excerpt = c.get("excerpt", "")
        if excerpt:
            target_verses: Set[int] = set()
            if covered_range:
                target_verses.update(parse_verse_range_token(covered_range))
            target_verses.add(verse_num)

            paras = excerpt.split("\n\n")
            lines.append('            <blockquote class="cit-excerpt">')
            for p in paras:
                p_str = p.strip()
                if p_str:
                    highlighted_p = highlight_verse_reference_in_excerpt(
                        p_str,
                        cit_prefix,
                        chapter_num,
                        target_verses,
                    )
                    if p_str.startswith("[Note"):
                        lines.append(f'              <p class="cit-note-line">{highlighted_p}</p>')
                    else:
                        lines.append(f'              <p>{highlighted_p}</p>')
            lines.append('            </blockquote>')

        lines.append('          </div>')

    lines.extend([
        '        </div>',
        f'        <p class="fn-nav-bottom"><a href="#{ref_id}" class="return-link" '
        f'title="Return to verse {v_num_str}">Return to verse {v_num_str} &#8617;</a></p>',
        '      </aside>',
    ])

    return "\n".join([line for line in lines if line])
