"""Onomasticon entity matching and EPUB3 pop-up footnote generator."""

from __future__ import annotations
import os
import re
import json
import html
from typing import Dict, List, Set, Tuple, Optional


def slugify_lemma(lemma: str) -> str:
    """Create a URL-safe lowercase slug for footnote and anchor IDs."""
    slug = lemma.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug


def load_onomasticon(path: str = "data/onomasticon.json") -> Dict[str, dict]:
    """Load the Book of Mormon Onomasticon dictionary from JSON."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Onomasticon data file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class OnomaMatcher:
    """Collision-free entity matcher for Book of Mormon proper names and places."""

    def __init__(self, onoma_dict: Dict[str, dict]):
        self.onoma_dict = onoma_dict
        self._build_patterns()

    def _build_patterns(self) -> None:
        self.pattern_to_lemma: Dict[str, str] = {}
        patterns: List[str] = []

        for upper_lemma, entry in self.onoma_dict.items():
            base_clean = entry.get("lemma", "").strip()
            if not base_clean or len(base_clean) < 2:
                continue

            variations: Set[str] = set()

            # Capitalized base form
            variations.add(base_clean.capitalize())

            # Forms with (S) e.g. NEPHITE(S) -> Nephite, Nephites
            if "(S)" in base_clean.upper():
                root = re.sub(r"\(S\)", "", base_clean, flags=re.I).strip().capitalize()
                variations.add(root)
                variations.add(root + "s")
            elif base_clean.endswith("ITES") or base_clean.endswith("ites"):
                root = base_clean[:-1].capitalize()
                variations.add(root)
                variations.add(base_clean.capitalize())

            # Hyphenated names e.g. Lehi-Nephi
            if "-" in base_clean:
                parts = [p.capitalize() for p in base_clean.split("-")]
                variations.add("-".join(parts))

            for v in variations:
                self.pattern_to_lemma[v] = upper_lemma
                patterns.append(re.escape(v))

        # Sort longer patterns first so compound names match before components
        patterns.sort(key=len, reverse=True)
        joined = "|".join(patterns)
        self.regex = re.compile(rf"\b({joined})(?:['’]s)?\b")

    def tag_verse_html(
        self,
        verse_html: str,
        tagged_set: Set[str],
        chapter_entries: Dict[str, dict],
        verse_num: int,
        onoma_verse_map: Dict[str, int],
        mention_counts: Optional[Dict[str, int]] = None,
        density: str = "all",  # "all", "chapter", "book"
    ) -> str:
        """Inject Onomasticon noteref anchors into verse HTML.

        Rule: Apply matching ONLY to unchanged tokens and <em> (modern) tokens,
        never inside <s> (deleted 1830) tokens, and never across HTML tags.

        When density == "all", every occurrence of each name is tagged.
        When density == "chapter", only the first mention in each chapter is tagged.
        When density == "book", only the first mention in each book is tagged.
        """
        parts = re.split(r"(<[^>]+>)", verse_html)
        in_s = False
        new_parts: List[str] = []

        for p in parts:
            if p.startswith("<"):
                if p.startswith("<s") or p.startswith("<del"):
                    in_s = True
                elif p.startswith("</s") or p.startswith("</del"):
                    in_s = False
                new_parts.append(p)
            else:
                if in_s or not p:
                    new_parts.append(p)
                else:
                    def replace_entity(m: re.Match) -> str:
                        matched_surface = m.group(1)
                        full_token = m.group(0)
                        upper_lemma = self.pattern_to_lemma.get(matched_surface)
                        if not upper_lemma:
                            return full_token

                        # Check density threshold
                        if density != "all" and upper_lemma in tagged_set:
                            return full_token

                        entry = self.onoma_dict.get(upper_lemma)
                        if not entry:
                            return full_token

                        tagged_set.add(upper_lemma)
                        slug = slugify_lemma(entry.get("lemma", upper_lemma))
                        chapter_entries[slug] = entry

                        if slug not in onoma_verse_map:
                            onoma_verse_map[slug] = verse_num

                        fn_id = f"fn-onoma-{slug}"
                        if mention_counts is not None:
                            mention_counts[slug] = mention_counts.get(slug, 0) + 1
                            count = mention_counts[slug]
                            ref_id = f"ref-onoma-{slug}" if count == 1 else f"ref-onoma-{slug}-{count}"
                        else:
                            ref_id = f"ref-onoma-{slug}"

                        return (
                            f'<a epub:type="noteref" class="noteref onoma-ref" '
                            f'href="#{fn_id}" id="{ref_id}">{full_token}</a>'
                        )

                    new_parts.append(self.regex.sub(replace_entity, p))

        return "".join(new_parts)

    def render_aside(
        self,
        slug: str,
        entry: dict,
        verse_num: Optional[int] = None,
    ) -> str:
        """Render a single Onomasticon footnote <aside> block for EPUB3 popups."""
        fn_id = f"fn-onoma-{slug}"
        ref_id = f"ref-onoma-{slug}"
        v_label = f"verse {verse_num}" if verse_num is not None else "verse"

        lemma_esc = html.escape(entry.get("lemma", slug.upper()))
        pron = entry.get("pronunciation", "")
        pron_html = (
            f'<span class="onoma-pron">/{html.escape(pron)}/</span>'
            if pron
            else ""
        )
        classification = entry.get("classification", "")
        class_html = (
            f'<span class="onoma-class">{html.escape(classification)}</span>'
            if classification
            else ""
        )
        definition = entry.get("definition", "")
        def_html = (
            f'        <p class="onoma-def">{html.escape(definition)}</p>\n'
            if definition
            else ""
        )

        lines: List[str] = [
            f'      <aside epub:type="footnote" id="{fn_id}" class="footnote-item onoma-footnote">',
            f'        <p class="onoma-title">Name Meaning of {lemma_esc}</p>',
            '        <div class="onoma-header">',
            f'          <span class="onoma-lemma">{lemma_esc}</span>{pron_html}{class_html}',
            '        </div>',
        ]
        if def_html:
            lines.append(def_html.rstrip())

        lines.append('        <div class="onoma-body">')
        etym_paras = entry.get("etymology_paragraphs", [])
        if etym_paras:
            for p in etym_paras:
                if p.strip():
                    lines.append(f'          <p class="onoma-p">{html.escape(p.strip())}</p>')
        elif entry.get("summary"):
            for p in entry["summary"].split("\n\n"):
                if p.strip():
                    lines.append(f'          <p class="onoma-p">{html.escape(p.strip())}</p>')
        else:
            lines.append('          <p class="onoma-p">No additional notes.</p>')
        lines.append('        </div>')

        lines.extend([
            f'        <p class="fn-nav-bottom"><a href="#{ref_id}" class="return-link" '
            f'title="Return to {v_label}">Return to {v_label} &#8617;</a></p>',
            '      </aside>',
        ])

        return "\n".join(lines)
