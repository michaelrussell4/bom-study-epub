"""Re-extract and enrich early historical scripture citations (1830-1930).

Produces complete, non-truncated excerpts with full paragraph context and
explicit footnote cross-references for Teachings of the Prophet Joseph Smith
and Journal of Discourses.
"""

from __future__ import annotations
import os
import re
import json
import time
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

TERMINAL_PUNCT = set(".?!\"'”’])")


def clean_text_unicode(text: str) -> str:
    """Clean unprintable or corrupted characters (\ufffd, non-breaking spaces, curly quotes)."""
    if not text:
        return ""
    text = text.replace("\xa0", " ")
    # Replace \ufffd between letters with apostrophe
    text = re.sub(r'([a-zA-Z])\ufffd([a-zA-Z])', r"\1'\2", text)
    # Replace \ufffd before words with left quote
    text = re.sub(r'(?:^|\s)\ufffd([a-zA-Z])', r" “\1", text)
    # Replace \ufffd after punctuation/words with right quote
    text = re.sub(r'([a-zA-Z.,!?])\ufffd(?:\s|$)', r"\1” ", text)
    # Replace \ufffd between spaces with em-dash
    text = re.sub(r'\s*\ufffd\s*', ' — ', text)
    text = text.replace('\ufffd', "'")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_paragraph_text(el) -> str:
    """Extract clean text from an element, removing pagination artifacts."""
    if not el:
        return ""
    c = BeautifulSoup(str(el), "html.parser")
    # Remove page break elements
    for tag in c.find_all(class_=re.compile(r"pagebreak|break")):
        tag.decompose()
    txt = c.get_text(" ", strip=True)
    # Remove page brackets like [ p. 48b] or [p. 70a]
    txt = re.sub(r"\[\s*p\.\s*[\d\w]+\s*\]", "", txt)
    return clean_text_unicode(txt)


def ensure_terminal_punct(text: str) -> str:
    """Ensure a paragraph ends with valid sentence-terminal punctuation."""
    text = text.strip()
    if text and text[-1] not in TERMINAL_PUNCT:
        return text + "."
    return text


class FullExcerptExtractor:
    def __init__(self, cache_dir: str = "data/talks_cache"):
        self.cache_dir = cache_dir
        self.soup_cache: Dict[str, Optional[BeautifulSoup]] = {}

    def get_soup(self, talk_id: str) -> Optional[BeautifulSoup]:
        if talk_id not in self.soup_cache:
            path = os.path.join(self.cache_dir, f"{talk_id}.html")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    self.soup_cache[talk_id] = BeautifulSoup(f.read(), "html.parser")
            else:
                self.soup_cache[talk_id] = None
        return self.soup_cache[talk_id]

    def extract_tpjs(self, talk_id: str, target_id: str) -> str:
        soup = self.get_soup(talk_id)
        if not soup:
            return ""
        target = soup.find(id=str(target_id))
        if not target:
            return ""

        # 1. Target footnote
        fn_div = target.find_parent(class_=re.compile(r"footnote"))
        fn_text = ""
        fn_num = ""
        if fn_div:
            fn_raw = clean_paragraph_text(fn_div)
            m = re.match(r"^(\d+)\.\s*(.*)", fn_raw)
            if m:
                fn_num = m.group(1)
                fn_content = m.group(2)
                fn_text = f"[Note {fn_num}: {fn_content}]"
            else:
                fn_text = f"[Note: {fn_raw}]"

        # 2. Find paragraphs on current page
        page_div = soup.find(id="talkwrapper") or soup.find(class_=re.compile(r"page|talkcontent")) or soup
        all_paras = page_div.find_all(["p", "div"], class_=re.compile(r"^(?:std|cont|paragraph)$"))

        target_idx = -1
        for idx, p in enumerate(all_paras):
            p_txt = p.get_text(" ", strip=True)
            if fn_num and re.search(rf"\b{fn_num}\b", p_txt):
                target_idx = idx
                break

        if target_idx == -1 and all_paras:
            for idx, p in enumerate(all_paras):
                if "std" in p.get("class", []):
                    target_idx = idx
                    break
            if target_idx == -1:
                target_idx = 0

        if target_idx == -1:
            return fn_text

        curr_p = all_paras[target_idx]
        curr_text = clean_paragraph_text(curr_p)

        # Stitch previous page if curr_p starts mid-sentence
        curr_classes = curr_p.get("class", [])
        if "cont" in curr_classes or (curr_text and curr_text[0].islower()):
            try:
                prev_tid = str(int(talk_id) - 1)
                prev_soup = self.get_soup(prev_tid)
                if prev_soup:
                    prev_page_div = prev_soup.find(id="talkwrapper") or prev_soup.find(class_=re.compile(r"page|talkcontent")) or prev_soup
                    prev_paras = prev_page_div.find_all(["p", "div"], class_=re.compile(r"^(?:std|cont|paragraph)$"))
                    if prev_paras:
                        last_prev = clean_paragraph_text(prev_paras[-1])
                        if last_prev and last_prev[-1] not in TERMINAL_PUNCT:
                            curr_text = last_prev + " " + curr_text
            except Exception:
                pass

        # Stitch next page if curr_p ends mid-sentence
        if curr_text and curr_text[-1] not in TERMINAL_PUNCT:
            try:
                next_tid = str(int(talk_id) + 1)
                next_soup = self.get_soup(next_tid)
                if next_soup:
                    next_page_div = next_soup.find(id="talkwrapper") or next_soup.find(class_=re.compile(r"page|talkcontent")) or next_soup
                    next_paras = next_page_div.find_all(["p", "div"], class_=re.compile(r"^(?:std|cont|paragraph)$"))
                    if next_paras:
                        first_next_p = next_paras[0]
                        if "cont" in first_next_p.get("class", []):
                            first_next_txt = clean_paragraph_text(first_next_p)
                            curr_text = curr_text + " " + first_next_txt
            except Exception:
                pass

        # In curr_text, format the footnote marker clearly as [N]
        if fn_num:
            curr_text = re.sub(rf"(?<=[,.;:\w])\s+{fn_num}\b", f" [{fn_num}]", curr_text)

        curr_text = ensure_terminal_punct(curr_text)

        result_paras = []
        # Preceding paragraph on the same page
        if target_idx > 0:
            prev_p = all_paras[target_idx - 1]
            if "std" in prev_p.get("class", []):
                prev_txt = ensure_terminal_punct(clean_paragraph_text(prev_p))
                if prev_txt and len(prev_txt) < 800:
                    result_paras.append(prev_txt)

        result_paras.append(curr_text)

        # Following paragraph on the same page
        if target_idx < len(all_paras) - 1:
            next_p = all_paras[target_idx + 1]
            if "std" in next_p.get("class", []):
                next_txt = ensure_terminal_punct(clean_paragraph_text(next_p))
                if next_txt and len(next_txt) < 800:
                    result_paras.append(next_txt)

        if fn_text:
            result_paras.append(fn_text)

        return "\n\n".join(result_paras)

    def extract_jd(self, talk_id: str, target_id: str) -> str:
        soup = self.get_soup(talk_id)
        if not soup:
            return ""
        target = soup.find(id=str(target_id))
        if not target:
            return ""

        all_paras = soup.find_all(class_=re.compile(r"paragraph|jod"))
        target_p = target.find_parent(class_=re.compile(r"paragraph|jod"))
        if not target_p or target_p not in all_paras:
            txt = clean_paragraph_text(target_p or target)
            return ensure_terminal_punct(txt)

        idx = all_paras.index(target_p)
        target_len = len(target_p.get_text())

        # Determine context window:
        # Default 3 paragraphs (1 before, target, 1 after).
        # If target paragraph is short (< 600 chars), expand to 5 paragraphs (2 before, 2 after).
        if target_len < 600:
            start_idx = max(0, idx - 2)
            end_idx = min(len(all_paras), idx + 3)
        else:
            start_idx = max(0, idx - 1)
            end_idx = min(len(all_paras), idx + 2)

        chosen = all_paras[start_idx:end_idx]
        cleaned = [ensure_terminal_punct(clean_paragraph_text(p)) for p in chosen if p]
        return "\n\n".join([p for p in cleaned if p])

    def extract(self, source: str, talk_id: str, target_id: str) -> str:
        if source == "Teachings of the Prophet Joseph Smith":
            return self.extract_tpjs(talk_id, target_id)
        elif source == "Journal of Discourses":
            return self.extract_jd(talk_id, target_id)
        return ""


def main():
    citations_file = "data/early_citations.json"
    print(f"Loading {citations_file}...")
    with open(citations_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    extractor = FullExcerptExtractor()
    total_cits = sum(len(cits) for cits in data.values())
    print(f"Re-extracting excerpts for {total_cits} citations...")

    t0 = time.time()
    updated_count = 0
    non_terminal = 0

    for vk, cits in data.items():
        for c in cits:
            src = c.get("source", "")
            tid = c.get("talk_id", "")
            tgt = c.get("target_id", "")
            if tid and tgt:
                exc = extractor.extract(src, tid, tgt)
                if exc:
                    c["excerpt"] = exc
                    updated_count += 1
                    if exc[-1] not in TERMINAL_PUNCT:
                        non_terminal += 1

    elapsed = time.time() - t0
    print(f"Updated {updated_count}/{total_cits} citations in {elapsed:.2f}s.")
    print(f"Non-terminal endings: {non_terminal}")

    # Save updated data/early_citations.json
    print(f"Saving updated {citations_file}...")
    with open(citations_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Done!")


if __name__ == "__main__":
    main()
