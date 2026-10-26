"""1830 First Edition vs. Latest Edition verse-by-verse diff engine."""

from __future__ import annotations
import re
import html
from difflib import SequenceMatcher
from typing import List


def tokenize(text: str) -> List[str]:
    """Tokenize text into words, punctuation, and whitespace tokens."""
    token_pattern = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*|[^\w\s]|\s+")
    return token_pattern.findall(text)


def _clean_whitespace_and_wrap(tag: str, text: str) -> str:
    """Wrap non-whitespace core in HTML tag, placing leading/trailing whitespace outside."""
    if not text:
        return ""
    m_lead = re.match(r"^\s+", text)
    lead = m_lead.group(0) if m_lead else ""
    m_trail = re.search(r"\s+$", text)
    trail = m_trail.group(0) if m_trail else ""
    core = text[len(lead):len(text) - len(trail) if trail else len(text)]
    if not core:
        return lead
    return f"{lead}<{tag}>{html.escape(core, quote=False)}</{tag}>{trail}"


def diff_verses_full(t_1830: str, t_latest: str) -> str:
    """Full word/punctuation comparison between 1830 and latest edition using SequenceMatcher."""
    if t_1830 == t_latest:
        return html.escape(t_latest, quote=False)
    if not t_1830:
        return _clean_whitespace_and_wrap("em", t_latest)
    if not t_latest:
        return _clean_whitespace_and_wrap("s", t_1830)

    tokens1 = tokenize(t_1830)
    tokens2 = tokenize(t_latest)

    sm = SequenceMatcher(None, tokens1, tokens2)
    out: List[str] = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            chunk = "".join(tokens2[j1:j2])
            out.append(html.escape(chunk, quote=False))
        elif tag == "delete":
            del_text = "".join(tokens1[i1:i2])
            out.append(_clean_whitespace_and_wrap("s", del_text))
        elif tag == "insert":
            ins_text = "".join(tokens2[j1:j2])
            out.append(_clean_whitespace_and_wrap("em", ins_text))
        elif tag == "replace":
            del_text = "".join(tokens1[i1:i2])
            ins_text = "".join(tokens2[j1:j2])

            lead1 = re.match(r"^\s*", del_text).group(0)
            lead2 = re.match(r"^\s*", ins_text).group(0)
            common_lead = lead1 if len(lead1) <= len(lead2) else lead2

            trail1 = re.search(r"\s*$", del_text).group(0)
            trail2 = re.search(r"\s*$", ins_text).group(0)
            common_trail = trail2 if len(trail2) <= len(trail1) else trail1

            core_del = del_text.strip()
            core_ins = ins_text.strip()

            part = ""
            if common_lead:
                part += common_lead
            if core_del:
                part += f"<s>{html.escape(core_del, quote=False)}</s>"
            if core_ins:
                part += f"<em>{html.escape(core_ins, quote=False)}</em>"
            if common_trail:
                part += common_trail
            out.append(part)

    res = "".join(out)
    return res


def diff_verses_substantive(t_1830: str, t_latest: str) -> str:
    """Substantive word diff that ignores pure punctuation and capitalization adjustments."""
    if not t_1830:
        return _clean_whitespace_and_wrap("em", t_latest)
    if not t_latest:
        return _clean_whitespace_and_wrap("s", t_1830)

    word_pattern = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
    matches_1830 = list(word_pattern.finditer(t_1830))
    matches_mod = list(word_pattern.finditer(t_latest))

    norm_1830 = [m.group(0).lower() for m in matches_1830]
    norm_mod = [m.group(0).lower() for m in matches_mod]

    # If all words match case-insensitively, no substantive changes exist
    if norm_1830 == norm_mod:
        return html.escape(t_latest, quote=False)

    sm = SequenceMatcher(None, norm_1830, norm_mod)
    opcodes = sm.get_opcodes()

    out: List[str] = []
    mod_cursor = 0

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            if j1 < j2:
                end_pos = matches_mod[j2 - 1].end()
                out.append(html.escape(t_latest[mod_cursor:end_pos], quote=False))
                mod_cursor = end_pos

        elif tag == "replace":
            start_pos = matches_mod[j1].start()
            if mod_cursor < start_pos:
                out.append(html.escape(t_latest[mod_cursor:start_pos], quote=False))
                mod_cursor = start_pos

            del_words = html.escape(
                " ".join(matches_1830[k].group(0) for k in range(i1, i2)), quote=False
            )
            end_pos = matches_mod[j2 - 1].end()
            rep_mod_text = html.escape(t_latest[start_pos:end_pos], quote=False)

            out.append(f"<s>{del_words}</s><em>{rep_mod_text}</em>")
            mod_cursor = end_pos

        elif tag == "delete":
            del_words = html.escape(
                " ".join(matches_1830[k].group(0) for k in range(i1, i2)), quote=False
            )
            out.append(f"<s>{del_words}</s> ")

        elif tag == "insert":
            start_pos = matches_mod[j1].start()
            if mod_cursor < start_pos:
                out.append(html.escape(t_latest[mod_cursor:start_pos], quote=False))
                mod_cursor = start_pos
            end_pos = matches_mod[j2 - 1].end()
            ins_mod_text = html.escape(t_latest[start_pos:end_pos], quote=False)
            out.append(f"<em>{ins_mod_text}</em>")
            mod_cursor = end_pos

    if mod_cursor < len(t_latest):
        out.append(html.escape(t_latest[mod_cursor:], quote=False))

    res = "".join(out)
    res = re.sub(r" +", " ", res)
    res = re.sub(r"\s+([,;:.\?!])", r"\1", res)
    return res


def diff_verse(t_1830: str, t_latest: str, substantive_only: bool = False) -> str:
    """Compare 1830 edition verse against latest edition verse.

    Args:
        t_1830: Raw verse text from 1830 edition.
        t_latest: Raw verse text from latest (2013) edition.
        substantive_only: If True, ignore pure punctuation and capitalization differences.

    Returns:
        XML-safe HTML string with <s> for deletions and <em> for additions.
    """
    if substantive_only:
        return diff_verses_substantive(t_1830, t_latest)
    return diff_verses_full(t_1830, t_latest)
    if substantive_only:
        return diff_verses_substantive(t_1830, t_latest)
    return diff_verses_full(t_1830, t_latest)
