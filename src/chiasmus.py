"""Chiasmus, Hebrew poetic structures, and study appendix cross-references for the Book of Mormon Study EPUB.

Provides data definitions, poetic formatting, and verse-level footnote linking
for prominent chiasms, legal cases, and geographical overviews.
"""

from typing import Dict, List, Optional, Tuple, Any


PROMINENT_CHIASMS: List[Dict[str, Any]] = [
    {
        "id": "chiasmus-alma-36",
        "book_slug": "alma",
        "chapter": 36,
        "start_verse": 1,
        "end_verse": 30,
        "key_verses": [1, 18],
        "title": "Alma 36:1–30 — The Masterpiece of Hebrew Chiasmus",
        "subtitle": "Alma's Conversion: Remembering Jesus Christ, the Son of God",
        "summary": (
            "Discovered by John W. Welch in 1967, Alma 36 is widely acclaimed as one of the most "
            "magnificent and mathematically precise examples of multi-tiered chiasmus in ancient world literature. "
            "Across 30 verses, Alma's personal testament forms an elaborate 34-element inverse parallelism whose "
            "exact psychological, spiritual, and structural pivot point (verses 18–19) is Alma remembering and "
            "calling upon Jesus Christ."
        ),
        "center_focus": "Verses 18–19: Remembering and Crying unto Jesus Christ, Son of God",
        "chart_image": "chart_132_alma_36.png",
        "chart_caption": "Welch & Welch, Chart 132: Chiastic Structure of Alma 36.",
        "pairs": [
            ("A", "My son, give ear to my words (v. 1)", 0),
            ("B", "Keep the commandments of God and ye shall prosper in the land (v. 1)", 1),
            ("C", "Captivity of our fathers: bondage in the land of Egypt and in the wilderness (v. 2)", 2),
            ("D", "Trust in God: he did deliver them out of bonds and afflictions (v. 2–3)", 3),
            ("E", "Trust in God to be supported under trials, troubles, and afflictions (v. 3)", 4),
            ("F", "I know this not of myself, but of God (v. 4)", 5),
            ("G", "Born of God: born of the Spirit and changed (v. 5)", 6),
            ("H", "Seeking to destroy the church of God (v. 6)", 7),
            ("I", "Fell to the earth; voice of the angel like thunder (v. 7–8)", 8),
            ("J", "Limbs struck with paralysis; fell to the earth for three days and three nights (v. 10)", 9),
            ("K", "The Agony of Sin: Racked with eternal torment; memory of all my iniquities (v. 12)", 10),
            ("L", "Tormented with the pains of hell; soul harrowed up to the greatest degree (v. 13–14)", 11),
            ("M", "Inexpressible horror; wished to become extinct, both soul and body (v. 14–15)", 12),
            ("N", "Pains of a damned soul (v. 16)", 13),
            ("CENTER", "CENTER (vv. 18–19): 'And it came to pass that as I was thus racked with torment, while I was harrowed up by the memory of my many sins, behold, I remembered also to have heard my father prophesy unto the people concerning the coming of one Jesus Christ, a Son of God, to atone for the sins of the world. Now, as my mind caught hold upon this thought, I cried within my heart: O Jesus, thou Son of God, have mercy on me!'", 14),
            ("N'", "No more pain; soul no longer harrowed up (v. 19)", 13),
            ("M'", "Oh, what joy, and what marvelous light; nothing so exquisite and sweet (v. 20–22)", 12),
            ("L'", "Soul filled with joy as exceeding as was my pain; praising God (v. 20–22)", 11),
            ("K'", "The Joy of Redemption: Longed to be in the presence of God; praising his holy name (v. 22)", 10),
            ("J'", "Use of limbs returns; stood upon my feet and manifested unto the people (v. 23)", 9),
            ("I'", "Labored without ceasing to bring souls unto repentance (v. 24)", 8),
            ("H'", "Many have been born of God, tasting as I have tasted (v. 26)", 7),
            ("G'", "Born of God: Tasting the marvelous light of Christ (v. 26)", 6),
            ("F'", "My knowledge is of God; he hath made these things known unto me (v. 26)", 5),
            ("E'", "Supported under trials and troubles of every kind, and in all manner of afflictions (v. 27)", 4),
            ("D'", "Trust in him: He will still deliver me and raise me up at the last day (v. 27–28)", 3),
            ("C'", "Captivity and Deliverance: Delivered our fathers out of Egypt and out of bondage (v. 28–29)", 2),
            ("B'", "Keep the commandments of God and ye shall prosper in the land (v. 30)", 1),
            ("A'", "This according to his word; give heed unto my words (v. 30)", 0),
        ]
    },
    {
        "id": "chiasmus-mosiah-5",
        "book_slug": "mosiah",
        "chapter": 5,
        "start_verse": 10,
        "end_verse": 12,
        "key_verses": [10],
        "title": "Mosiah 5:10–12 — The Covenant Name of Christ",
        "subtitle": "King Benjamin's Coronation and Covenant Discourse",
        "summary": (
            "The historic chiasm discovered by John W. Welch on June 5, 1967 in Regensburg, Germany, which sparked "
            "modern Book of Mormon chiasmus scholarship. King Benjamin's words form a crisp, tightly constructed "
            "7-tier inverted parallelism revolving around the command to 'take heed that ye do not transgress'."
        ),
        "center_focus": "Verse 11: Take heed that ye do not transgress, that the name be not blotted out",
        "chart_image": "chart_131_mosiah_5.png",
        "chart_caption": "Welch & Welch, Chart 131: Chiasmus in Mosiah 5:10–12.",
        "pairs": [
            ("A", "Whosoever shall not take upon them the name of Christ (v. 10)", 0),
            ("B", "Must be called by some other name (v. 10)", 1),
            ("C", "Therefore, he findeth himself on the left hand of God (v. 10)", 2),
            ("D", "And I would that ye should remember also, that this is the name (v. 11)", 3),
            ("E", "That never should be blotted out, except it be through transgression (v. 11)", 4),
            ("CENTER", "CENTER (v. 11): 'Therefore, take heed that ye do not transgress, that the name be not blotted out of your hearts.'", 5),
            ("E'", "I say unto you, I would that ye should remember to retain the name written always in your hearts (v. 12)", 4),
            ("D'", "That it may not be blotted out (v. 12)", 3),
            ("C'", "That ye are not found on the left hand of God (v. 12)", 2),
            ("B'", "But that ye hear and know the voice by which ye shall be called (v. 12)", 1),
            ("A'", "And also the name by which he shall call you (v. 12)", 0),
        ]
    },
    {
        "id": "chiasmus-mosiah-3",
        "book_slug": "mosiah",
        "chapter": 3,
        "start_verse": 18,
        "end_verse": 19,
        "key_verses": [18],
        "title": "Mosiah 3:18–19 — The Natural Man and the Atoning Blood of Christ",
        "subtitle": "The Angel's Revelation to King Benjamin",
        "summary": (
            "King Benjamin's angelic discourse climaxes in this extraordinary 6-tier chiasmus. Statistically one of "
            "the strongest structures in the Book of Mormon, it introduces the unique term 'natural man' at its "
            "outer core and places the duration of the Fall ('from the fall of Adam / and will be, forever and ever') "
            "at its absolute center, framed by the redemptive blood of Christ."
        ),
        "center_focus": "Verse 19: The Fall of Adam and its eternal consequences answered by the Holy Spirit",
        "chart_image": "chart_130_mosiah_3.png",
        "chart_caption": "Welch & Welch, Chart 130: Chiasmus in Mosiah 3:18–19.",
        "pairs": [
            ("A", "Men drink damnation to their own souls except they humble themselves (v. 18)", 0),
            ("B", "And become as little children (v. 18)", 1),
            ("C", "And believe that salvation was, and is, and is to come, in and through the atoning blood of Christ, the Lord Omnipotent (v. 18)", 2),
            ("D", "For the natural man (v. 19)", 3),
            ("E", "Is an enemy to God (v. 19)", 4),
            ("CENTER", "CENTER (v. 19): 'And has been from the fall of Adam, and will be, forever and ever, unless he yields to the enticings of the Holy Spirit'", 5),
            ("E'", "And putteth off the natural man (v. 19)", 4),
            ("D'", "And becometh a saint through the atonement of Christ the Lord (v. 19)", 3),
            ("C'", "And becometh as a child (v. 19)", 2),
            ("B'", "Submissive, meek, humble, patient, full of love (v. 19)", 1),
            ("A'", "Willing to submit to all things which the Lord seeth fit to inflict upon him, even as a child doth submit to his father (v. 19)", 0),
        ]
    },
    {
        "id": "chiasmus-1ne-1",
        "book_slug": "1-nephi",
        "chapter": 1,
        "start_verse": 1,
        "end_verse": 20,
        "key_verses": [1],
        "title": "1 Nephi 1:1–2:1 — The Prophetic Commission of Lehi",
        "subtitle": "Nephi's Prologue and the Vision of the Throne of God",
        "summary": (
            "Nephi constructs the opening of his First Book around an overarching chiasmus framing Lehi's visionary "
            "call and departure from Jerusalem. The opening description of Nephi's parentage and learning parallels "
            "his final testimony of the tender mercies of the Lord over all whom he hath chosen."
        ),
        "center_focus": "Verses 8–12: Vision of God on His throne and the Pillar of Fire / Book delivered to Lehi",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "Nephi having been born of goodly parents; taught in the learning of my father and the Jews (1:1–2)", 0),
            ("B", "Making a record of my proceedings; a record that is true (1:3)", 1),
            ("C", "Lehi prays in behalf of his people at Jerusalem (1:5)", 2),
            ("D", "Pillar of fire upon a rock; Lehi trembles and quakes exceedingly (1:6)", 3),
            ("CENTER", "CENTER (1:8–12): 'He saw the heavens open, and he thought he saw God sitting upon his throne, surrounded with numberless concourses of angels... and one descending out of the midst of heaven... and he gave unto him a book, and bade him that he should read.'", 4),
            ("D'", "Lehi reads of the doom of Jerusalem; soul rejoices and whole heart is filled (1:13–15)", 3),
            ("C'", "Lehi testifies unto the Jews of their abominations and wickedness (1:19)", 2),
            ("B'", "Nephi abridges the record of his father; full account upon the other plates (1:16–17)", 1),
            ("A'", "The tender mercies of the Lord are over all those whom he hath chosen, because of their faith (1:20)", 0),
        ]
    },
    {
        "id": "chiasmus-1ne-15",
        "book_slug": "1-nephi",
        "chapter": 15,
        "start_verse": 9,
        "end_verse": 11,
        "key_verses": [9],
        "title": "1 Nephi 15:9–11 — Asking in Faith vs. Hardness of Heart",
        "subtitle": "Nephi's Rebuttal to Laman and Lemuel",
        "summary": (
            "A concise, punchy rhetorical chiasmus used by Nephi to expose the spiritual indolence of his brothers. "
            "The center is the pivotal question: 'Do ye not remember the things which the Lord hath said?'"
        ),
        "center_focus": "Verse 11: Do ye not remember the things which the Lord hath said?",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "The Lord maketh no such thing known unto us (v. 9)", 0),
            ("B", "How is it that ye do not keep the commandments of the Lord? (v. 10)", 1),
            ("C", "How is it that ye will perish, because of the hardness of your hearts? (v. 10)", 2),
            ("CENTER", "CENTER (v. 11): 'Do ye not remember the things which the Lord hath said?'", 3),
            ("C'", "If ye will not harden your hearts (v. 11)", 2),
            ("B'", "And ask me in faith, believing that ye shall receive, with diligence in keeping my commandments (v. 11)", 1),
            ("A'", "Surely these things shall be made known unto you (v. 11)", 0),
        ]
    },
    {
        "id": "chiasmus-2ne-27",
        "book_slug": "2-nephi",
        "chapter": 27,
        "start_verse": 1,
        "end_verse": 5,
        "key_verses": [1],
        "title": "2 Nephi 27:1–5 — The Vision of the Last Days",
        "subtitle": "Nephi's Prophecy of the Nations Fighting Against Zion",
        "summary": (
            "Interpreting Isaiah 29, Nephi weaves an intricate Hebrew parallelism contrasting the drunken slumber "
            "of the wicked with the hungry man's dream at its chiastic turning point."
        ),
        "center_focus": "Verse 3: The hungry and thirsty man's illusory dream versus reality",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "In the last days, or in the days of the Gentiles—yea, all nations of the Gentiles and also the Jews (v. 1)", 0),
            ("B", "Both they who shall come upon this land and they who shall be upon other lands; they will be drunken with iniquity (v. 1)", 1),
            ("C", "And all the nations that fight against Zion, and that distress her, shall be as a dream of a night vision (v. 2–3)", 2),
            ("CENTER", "CENTER (v. 3): 'Yea, it shall be unto them, even as unto a hungry man which dreameth, and behold he eateth but he awaketh and his soul is empty; or like unto a thirsty man which dreameth, and behold he drinketh but he awaketh and behold he is faint... even so shall the multitude of all the nations be that fight against Mount Zion.'", 3),
            ("C'", "All ye that do iniquity, stay yourselves and wonder... ye shall be drunken, but not with wine (v. 4)", 2),
            ("B'", "The Lord hath poured out upon you the spirit of deep sleep; for behold, ye have closed your eyes (v. 5)", 1),
            ("A'", "The prophets, and your rulers, the seers hath he covered because of your iniquity (v. 5)", 0),
        ]
    },
    {
        "id": "chiasmus-2ne-29",
        "book_slug": "2-nephi",
        "chapter": 29,
        "start_verse": 13,
        "end_verse": 13,
        "key_verses": [13],
        "title": "2 Nephi 29:13 — The Three Witnesses of Scripture",
        "subtitle": "The Words of Jews, Nephites, and the Lost Tribes",
        "summary": (
            "A brilliantly compact, interlocking four-part concentric chiasmus declaring the three scriptural records "
            "that will merge together in the latter days."
        ),
        "center_focus": "The mutual testimony of Nephites, Jews, and the Lost Tribes of Israel",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "And the Jews shall have the words of the Nephites (v. 13)", 0),
            ("B", "And the Nephites shall have the words of the Jews (v. 13)", 1),
            ("C", "And the Nephites and the Jews shall have the words of the lost tribes of Israel (v. 13)", 2),
            ("C'", "And the lost tribes of Israel shall have the words of the Nephites and the Jews (v. 13)", 2),
            ("B'", "And they shall be gathered home unto the lands of their possessions (v. 14)", 1),
            ("A'", "And my word also shall be gathered in one (v. 14)", 0),
        ]
    },
    {
        "id": "chiasmus-alma-29",
        "book_slug": "alma",
        "chapter": 29,
        "start_verse": 1,
        "end_verse": 7,
        "key_verses": [1],
        "title": "Alma 29:1–7 — O That I Were an Angel",
        "subtitle": "Alma's Soulful Meditation on Preaching Repentance",
        "summary": (
            "A rare A-B-C-C-C-B-A chiastic structure containing a threefold inner triplet. Scholars have noted striking "
            "structural parallels between this pattern and ancient Mesoamerican royal inscriptions (such as Quiriguá Stela C)."
        ),
        "center_focus": "Verses 4–5: God granteth unto men according to their desire, whether it be good or evil",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "O that I were an angel, and could have the wish of mine heart, that I might go forth and speak with the trump of God... (v. 1–2)", 0),
            ("B", "But behold, I am a man, and do sin in my wish; for I ought to be content with the things which the Lord hath allotted unto me (v. 3)", 1),
            ("C1", "I ought not to harrow up in my desires the firm decree of a just God, for I know that he granteth unto men according to their desire (v. 4)", 2),
            ("C2", "Yea, I know that he allotteth unto men, yea, decreeth unto them decrees which are unalterable, according to their wills (v. 4)", 2),
            ("C3", "Yea, and I know that good and evil have come before all men... to him it is given according to his desires, whether he desireth good or evil (v. 5)", 2),
            ("B'", "Now, seeing that I know these things, why should I desire more than to perform the work to which I have been called? (v. 6)", 1),
            ("A'", "Why should I desire that I were an angel, that I could speak unto all the ends of the earth? (v. 7)", 0),
        ]
    },
    {
        "id": "chiasmus-alma-41",
        "book_slug": "alma",
        "chapter": 41,
        "start_verse": 13,
        "end_verse": 15,
        "key_verses": [13],
        "title": "Alma 41:13–15 — The Law of Restoration",
        "subtitle": "Good for Good, Righteous for Righteous, Just for Just, Merciful for Merciful",
        "summary": (
            "Alma's famous discourse to his son Corianton contains what John W. Welch characterized as 'a list of pairs "
            "and then a pair of lists.' The four virtues—good, righteous, just, merciful—are stated, inverted, and "
            "then promised as divine retribution."
        ),
        "center_focus": "Verse 14: Deal justly, judge righteously, and do good continually",
        "chart_image": None,
        "chart_caption": None,
        "pairs": [
            ("A", "The meaning of the word restoration is to bring back again (v. 13)", 0),
            ("B", "Evil for evil, or carnal for carnal, or devilish for devilish— (v. 13)", 1),
            ("C", "Good for that which is good; righteous for that which is righteous; just for that which is just; merciful for that which is merciful (v. 13)", 2),
            ("CENTER", "CENTER (v. 14): 'Therefore, my son, see that you are merciful unto your brethren; deal justly, judge righteously, and do good continually; and if ye do all these things then shall ye receive your reward.'", 3),
            ("C'", "Yea, ye shall have mercy restored unto you again; ye shall have justice restored unto you again; ye shall have a righteous judgment restored unto you again; and ye shall have good rewarded unto you again (v. 14)", 2),
            ("B'", "For that which ye do send out shall return unto you again, and be restored (v. 15)", 1),
            ("A'", "Therefore, the word restoration more fully condemneth the sinner, and justifieth him not at all (v. 15)", 0),
        ]
    },
    {
        "id": "chiasmus-hel-6",
        "book_slug": "helaman",
        "chapter": 6,
        "start_verse": 7,
        "end_verse": 13,
        "key_verses": [7],
        "title": "Helaman 6:7–13 — Universal Peace and Prosperity",
        "subtitle": "The 64th Year of the Judges: The Center of the Lord and Zedekiah",
        "summary": (
            "An extraordinary archival chiasmus summarizing the sixty-fourth year of the judges. At the center "
            "stands a Hebrew wordplay: Mulek, son of Zedekiah (Zedeki-yah), paired with Yahweh / the Lord."
        ),
        "center_focus": "Verse 10: The son of Zedekiah / for the Lord did bring Mulek into the land north",
        "chart_image": "chart_133_helaman_6.png",
        "chart_caption": "Welch & Welch, Chart 133: Chiasmus in Helaman 6:7–13.",
        "pairs": [
            ("A", "And behold, there was peace in all the land (v. 7)", 0),
            ("B", "Nephites and Lamanites did go into whatsoever part of the land they would; free intercourse (v. 7–8)", 1),
            ("C", "Became exceedingly rich, both the Lamanites and the Nephites (v. 9)", 2),
            ("D", "Plenty of gold, and of silver, and of all manner of precious metals, both in the land south and in the land north (v. 9)", 3),
            ("E", "Land south was called Lehi, and the land north was called Mulek (v. 10)", 4),
            ("CENTER", "CENTER (v. 10): 'Which was after the son of Zedekiah; for the Lord did bring Mulek into the land north, and Lehi into the land south.'", 5),
            ("D'", "Behold, there was all manner of gold in both these lands, and of silver, and of precious ore of every kind (v. 11)", 3),
            ("C'", "Curious workmen did refine it, and thus they did become rich (v. 11)", 2),
            ("B'", "Did raise grain in abundance both north and south; did flourish exceedingly (v. 12)", 1),
            ("A'", "And thus the sixty and fourth year did pass away in peace (v. 13)", 0),
        ]
    },
]

# Quick lookup mappings
CHIASMUS_BY_ID = {c["id"]: c for c in PROMINENT_CHIASMS}

# Key verses lookup: (book_slug, chapter, verse) -> List of chiasmus dicts
CHIASMUS_VERSE_MAP: Dict[Tuple[str, int, int], List[Dict[str, Any]]] = {}
for chia in PROMINENT_CHIASMS:
    for kv in chia["key_verses"]:
        key = (chia["book_slug"], chia["chapter"], kv)
        CHIASMUS_VERSE_MAP.setdefault(key, []).append(chia)


# Legal Cases mapping: (book_slug, chapter, verse) -> dict
LEGAL_CASES_MAP: Dict[Tuple[str, int, int], Dict[str, str]] = {
    ("jacob", 7, 1): {
        "id": "case-sherem",
        "badge": "⚖ Law: Case of Sherem",
        "title": "The Case of Sherem (Jacob 7)",
        "summary": "Sherem is accused of leading away the people, blaspheming against the coming of Christ, and demanding a divine sign under ancient Law of Moses procedures.",
        "target": "appendix_legal_cases.xhtml#case-sherem",
    },
    ("mosiah", 11, 20): {
        "id": "case-abinadi",
        "badge": "⚖ Law: Trial of Abinadi",
        "title": "The Trial of Abinadi (Mosiah 11–17)",
        "summary": "Abinadi is arraigned before King Noah and his royal priestly council on charges of reviling the king, false prophecy, and blasphemy.",
        "target": "appendix_legal_cases.xhtml#case-abinadi",
    },
    ("alma", 1, 1): {
        "id": "case-nehor",
        "badge": "⚖ Law: Trial of Nehor",
        "title": "The Trial of Nehor (Alma 1)",
        "summary": "The first capital trial under the reign of the judges: Nehor is convicted of introducing priestcraft, enforcing heresy with the sword, and murdering Gideon.",
        "target": "appendix_legal_cases.xhtml#case-nehor",
    },
    ("alma", 14, 1): {
        "id": "case-ammonihah",
        "badge": "⚖ Law: Trial at Ammonihah",
        "title": "The Trial of Alma and Amulek (Alma 14)",
        "summary": "Judicial corruption in the apostate city of Ammonihah, unlawful confinement of prophets, the martyrdom of women and children, and divine destruction of the prison.",
        "target": "appendix_legal_cases.xhtml#case-ammonihah",
    },
    ("alma", 30, 6): {
        "id": "case-korihor",
        "badge": "⚖ Law: Trial of Korihor",
        "title": "The Trial of Korihor (Alma 30)",
        "summary": "The anti-Christ Korihor's hearings before Giddonah in Jershon, the Chief Judge in Gideon, and Alma in Zarahemla; freedom of belief vs. blasphemy and the sign of muteness.",
        "target": "appendix_legal_cases.xhtml#case-korihor",
    },
    ("helaman", 1, 7): {
        "id": "case-paanchi",
        "badge": "⚖ Law: Trial of Paanchi",
        "title": "The Case of Paanchi (Helaman 1)",
        "summary": "Paanchi's trial and execution for treason and rebellion after refusing to accept the voice of the people in the election of the chief judge.",
        "target": "appendix_legal_cases.xhtml#case-paanchi",
    },
    ("helaman", 9, 1): {
        "id": "case-seantum",
        "badge": "⚖ Law: Trial of Seantum",
        "title": "The Trial of Seantum (Helaman 9)",
        "summary": "The murder of Chief Judge Seezoram, prophetic detection by Nephi son of Helaman, and ancient Near Eastern confession rules.",
        "target": "appendix_legal_cases.xhtml#case-seantum",
    },
}

# Geography and Charts mapping: (book_slug, chapter, verse) -> dict
SPECIAL_STUDY_NOTES: Dict[Tuple[str, int, int], Dict[str, str]] = {
    ("alma", 22, 27): {
        "id": "geo-overview",
        "badge": "🗺 Mormon's Map: Internal Geography",
        "title": "Mormon's Geography of the Book of Mormon Lands",
        "summary": "Alma 22:27–34 is Mormon's primary geopolitical baseline description of the Nephite and Lamanite territories, the Narrow Neck, and the seas East and West.",
        "target": "appendix_geography.xhtml#geography-overview",
    },
    ("alma", 11, 1): {
        "id": "chart-monetary",
        "badge": "📊 Study Chart: Monetary System",
        "title": "King Mosiah's System of Weights and Measures",
        "summary": "Alma 11 establishes standardized legal weights and measures of silver and gold tied directly to measures of barley and other grains.",
        "target": "appendix_charts.xhtml#chart-monetary-system",
    },
    ("jacob", 5, 1): {
        "id": "chart-olive-tree",
        "badge": "🌳 Study Chart: Allegory of the Olive Tree",
        "title": "Zenos's Allegory of the Tame and Wild Olive Trees",
        "summary": "Jacob 5 preserves Zenos's extensive prophetic allegory detailing the scattering, grafting, decay, and final gathering of the House of Israel.",
        "target": "appendix_charts.xhtml#chart-olive-tree",
    },
}


def get_chiasms_for_verse(book_slug: str, chapter: int, verse: int) -> List[Dict[str, Any]]:
    """Return prominent chiasms that have a key noteref on this verse."""
    return CHIASMUS_VERSE_MAP.get((book_slug, chapter, verse), [])


def get_legal_case_for_verse(book_slug: str, chapter: int, verse: int) -> Optional[Dict[str, str]]:
    """Return legal case cross-reference for this verse, if any."""
    return LEGAL_CASES_MAP.get((book_slug, chapter, verse))


def get_study_note_for_verse(book_slug: str, chapter: int, verse: int) -> Optional[Dict[str, str]]:
    """Return special study note cross-reference for this verse, if any."""
    return SPECIAL_STUDY_NOTES.get((book_slug, chapter, verse))
