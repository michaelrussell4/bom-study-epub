"""Appendices generator for the Book of Mormon Study EPUB.

Generates rich, scholarly XHTML documents for:
- Appendix A: Hebrew Poetic Parallelisms & Prominent Chiasmus (Donald W. Parry, John W. Welch, Scripture Central)
- Appendix B: Internal Book of Mormon Geography & Mormon's Map (John L. Sorenson, Welch & Welch)
- Appendix C: Legal Cases & Judicial Procedures (John W. Welch)
- Appendix D: Chronology, Plates, & Structural Charts (Welch & Welch)
"""

import html
import os
from typing import List, Dict, Any
from .chiasmus import PROMINENT_CHIASMS


def _xhtml_doc(title: str, content: str) -> str:
    """Wrap content in a valid EPUB3 XHTML document."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="../styles/style.css" />
</head>
<body class="appendix-body">
{content}
</body>
</html>"""


def render_appendix_chiasmus_xhtml() -> str:
    """Render Appendix A: Hebrew Poetic Parallelisms and Prominent Chiasmus."""
    sections = [
        '  <section epub:type="appendix" class="appendix-section" id="appendix-a">',
        '    <header class="appendix-header">',
        '      <p class="appendix-subtitle">Supplemental Study Resources • Appendix A</p>',
        '      <h1 class="appendix-title">Hebrew Poetic Parallelisms &amp; Prominent Chiasmus</h1>',
        '      <p class="appendix-byline">Based on research by Donald W. Parry, John W. Welch, and Scripture Central</p>',
        '    </header>',
        '    <div class="appendix-intro">',
        '      <p>A primary internal evidence of the ancient Near Eastern heritage of the Book of Mormon is its pervasive use of ancient Hebrew poetic structures, most notably <em>parallelismus membrorum</em> ("parallelism of members") and <em>chiasmus</em> (inverted parallelism). Bishop Robert Lowth first systematically identified Hebrew poetic parallelism in 1753, but the existence of multi-tiered chiasmus was virtually unknown in the English-speaking world when Joseph Smith translated the Book of Mormon in 1829.</p>',
        '      <p>As documented by Donald W. Parry in <em>Poetic Parallelisms in the Book of Mormon</em>, Nephite record keepers utilized a vast repertoire of ancient poetic devices, including:</p>',
        '      <ul class="appendix-list">',
        '        <li><strong>Inverted Parallelism (Chiasmus):</strong> A symmetric structure where concepts, terms, or phrases appear in a specific sequence ($A, B, C \dots$) and are subsequently repeated in exact inverse order ($\dots C\', B\', A\'$), focusing attention upon a central pivotal message.</li>',
        '        <li><strong>Simple &amp; Extended Synonymous Parallelism:</strong> Where subsequent lines reinforce and echo the identical meaning of earlier lines with harmonious synonymy (e.g. 3 Nephi 8:13).</li>',
        '        <li><strong>Simple Alternate Parallelism:</strong> An $A-B / A\'-B\'$ arrangement balancing parallel thoughts across alternating lines.</li>',
        '        <li><strong>Climactic (Staircase) Parallelism:</strong> Step-by-step repetition where the concluding phrase of each line serves as the springboard for the following line.</li>',
        '        <li><strong>Antithetical Parallelism:</strong> Contrasting righteousness and wickedness, light and darkness, blessing and cursing.</li>',
        '      </ul>',
        '    </div>',
        '    <hr class="section-divider" />',
        '    <h2 class="appendix-h2">Ten Prominent Chiasms in the Book of Mormon</h2>',
        '    <p class="section-note">Tap any return link to navigate directly back to the scripture text.</p>',
    ]

    for chia in PROMINENT_CHIASMS:
        chia_id = chia["id"]
        book_slug = chia["book_slug"]
        ch_num = chia["chapter"]
        k_verse = chia["key_verses"][0]
        verse_filename = f"{book_slug}_{ch_num:02d}.xhtml"
        verse_anchor = f"v{k_verse}"

        sections.append(f'    <article class="chiasmus-entry" id="{chia_id}">')
        sections.append(f'      <div class="chiasmus-header">')
        sections.append(f'        <a class="back-to-verse-link" href="{verse_filename}#{verse_anchor}">&#8592; Return to Scripture ({chia["title"].split("—")[0].strip()})</a>')
        sections.append(f'        <h3 class="chiasmus-title">{html.escape(chia["title"])}</h3>')
        sections.append(f'        <p class="chiasmus-subtitle">{html.escape(chia["subtitle"])}</p>')
        sections.append(f'      </div>')

        sections.append(f'      <div class="chiasmus-summary">')
        sections.append(f'        <p>{html.escape(chia["summary"])}</p>')
        sections.append(f'        <p class="center-callout"><strong>Chiastic Center:</strong> {html.escape(chia["center_focus"])}</p>')
        sections.append(f'      </div>')

        # Visual Chart if available
        if chia.get("chart_image"):
            img_name = chia["chart_image"]
            caption = chia.get("chart_caption", "")
            sections.append('      <figure class="appendix-figure">')
            sections.append(f'        <img class="appendix-img" src="../images/appendix/{img_name}" alt="{html.escape(caption)}" />')
            sections.append(f'        <figcaption class="appendix-caption">{html.escape(caption)}</figcaption>')
            sections.append('      </figure>')

        # Poetic lines
        sections.append('      <div class="chiasmus-poetic-block">')
        for label, text, indent in chia["pairs"]:
            indent_class = f"chia-indent-{min(indent, 8)}"
            if label == "CENTER":
                sections.append(f'        <div class="chia-center-block {indent_class}">')
                sections.append(f'          <span class="chia-center-label">&#9733; FOCAL CENTER:</span>')
                sections.append(f'          <span class="chia-center-text">{html.escape(text)}</span>')
                sections.append('        </div>')
            else:
                is_prime = "'" in label
                prime_class = "chia-prime" if is_prime else "chia-base"
                sections.append(f'        <p class="chia-line {indent_class} {prime_class}">')
                sections.append(f'          <span class="chia-label">{html.escape(label)}</span>')
                sections.append(f'          <span class="chia-text">{html.escape(text)}</span>')
                sections.append('        </p>')
        sections.append('      </div>')
        sections.append('    </article>')
        sections.append('    <hr class="item-divider" />')

    sections.extend([
        '  </section>',
    ])

    return _xhtml_doc("Appendix A: Hebrew Poetic Parallelisms & Chiasmus", "\n".join(sections))


def render_appendix_geography_xhtml() -> str:
    """Render Appendix B: Internal Book of Mormon Geography and Mormon's Map."""
    content = """  <section epub:type="appendix" class="appendix-section" id="appendix-b">
    <header class="appendix-header">
      <p class="appendix-subtitle">Supplemental Study Resources • Appendix B</p>
      <h1 class="appendix-title">Internal Book of Mormon Geography &amp; Mormon's Map</h1>
      <p class="appendix-byline">Based on <em>Mormon's Map</em> by Dr. John L. Sorenson and Welch &amp; Welch, <em>Charting the Book of Mormon</em></p>
    </header>

    <div class="appendix-intro" id="geography-overview">
      <p>One of the most remarkable literary and historical qualities of the Book of Mormon is its rigorous internal geographical consistency. Across more than 500 pages authored by multiple prophetic writers over a thousand-year span, hundreds of geographical statements detailing distances, travel times, elevations, river flows, mountain passes, and borders harmonize with extraordinary precision.</p>
      <p>As demonstrated in Dr. John L. Sorenson's foundational study <em>Mormon's Map</em>, the chief abridger and record keeper Mormon possessed a vivid, consistent mental map of his homeland. When the text is examined strictly on its own terms—without imposing external modern cartography—a clear, logical topological structure emerges.</p>
    </div>

    <hr class="section-divider" />

    <h2 class="appendix-h2">Ten Essential Features of Book of Mormon Geography</h2>
    <p>In <em>Charting the Book of Mormon</em> (Chart 149), Welch and Sorenson identify ten fundamental topological criteria that any internal reconstruction of Book of Mormon geography must satisfy:</p>

    <ol class="appendix-list">
      <li><strong>A Narrow Neck of Land:</strong> An isthmus separated the land southward from the land northward (Alma 22:32; 63:5; Mormon 2:29).</li>
      <li><strong>The Land Southward:</strong> Comprised the land of Nephi (in the south) and the land of Zarahemla (in the north), separated by a narrow strip of wilderness extending from the sea east to the sea west (Alma 22:27).</li>
      <li><strong>Elevation Gradients ("Up" and "Down"):</strong> Travelers consistently went <em>up</em> from Zarahemla to the land of Nephi, and <em>down</em> from Nephi to Zarahemla, indicating that Nephi was situated in higher mountainous highlands (Omni 1:13; Mosiah 7:1–4; 28:1).</li>
      <li><strong>The River Sidon:</strong> Flowed from the south wilderness northward through the heart of the land of Zarahemla past the city of Zarahemla, emptying into the sea (Alma 16:6–7; 22:27–29; 43:22).</li>
      <li><strong>East and West Seas:</strong> The land southward was bounded on the west by the Sea West and on the east by the Sea East (Alma 22:27).</li>
      <li><strong>A Day and a Half's Journey:</strong> The distance across the narrow neck of land from the Sea East to the Sea West was approximately "a day and a half's journey for a Nephite" (Alma 22:32), indicating an isthmus width of roughly 30 to 45 miles along defensive lines.</li>
      <li><strong>The Land Northward:</strong> Known as the land of Desolation, where the Jaredite civilization lived and was ultimately destroyed at the hill Ramah (Cumorah) (Omni 1:21–22; Alma 22:30; Ether 15:8–11).</li>
      <li><strong>Strategic Narrow Pass:</strong> A strategic mountain pass led into the land northward by the west sea, which Nephite military commanders fortified to prevent Lamanite encirclement (Alma 50:34; 52:9; Mormon 3:5).</li>
      <li><strong>Defensive Border Cities:</strong> Fortified frontier lines established by Captain Moroni along the east seashore (Moroni, Lehi, Morianton, Omner, Gid, Mulek) and west seashore (Antiparah, Judea, Cumeni, Zeezrom, Manti) (Alma 50:13–15; 53:8).</li>
      <li><strong>Travel Times between Major Capitals:</strong> Travel between the city of Lehi-Nephi and the city of Zarahemla required roughly 21 days for groups traveling with flocks and women and children (Mosiah 23:3; 24:20–25).</li>
    </ol>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_149_geography_features.png" alt="Chart 149: Ten Essential Features of Book of Mormon Geography" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 149: Ten Essential Features of Book of Mormon Geography.</figcaption>
    </figure>

    <hr class="section-divider" />

    <h2 class="appendix-h2">The Twelve Journeys between Nephi and Zarahemla</h2>
    <p>Between approximately 200 B.C. and 60 B.C., twelve major recorded expeditions traveled between the high mountain valley of the land of Nephi and the lower river basin of Zarahemla. These documented journeys provide critical benchmarks for rates of travel and geography:</p>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_153_twelve_journeys.png" alt="Chart 153: Twelve Journeys between Nephi and Zarahemla" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 153: Twelve Journeys between the Cities of Nephi and Zarahemla.</figcaption>
    </figure>

    <div class="geography-journeys-list">
      <div class="journey-item">
        <h4>1. Mosiah₁'s Exodus to Zarahemla (Omni 1:12–14)</h4>
        <p>Warned of the Lord to flee out of the land of Nephi, Mosiah₁ led the righteous through the wilderness down to the discovery of the people of Zarahemla.</p>
      </div>
      <div class="journey-item">
        <h4>2. First Ill-Fated Return Expedition (Omni 1:27–28)</h4>
        <p>A contentious party attempted to reclaim their ancestral inheritance in Nephi; contention broke out in the wilderness, and only fifty survivors returned to Zarahemla.</p>
      </div>
      <div class="journey-item">
        <h4>3. Zeniff's Colony to Nephi (Omni 1:29–30; Mosiah 9:1–7)</h4>
        <p>Zeniff led a zealous group back to the land of Lehi-Nephi, entering into a deceptive treaty with Lamanite King Laman to inhabit the lands of Lehi-Nephi and Shilom.</p>
      </div>
      <div class="journey-item">
        <h4>4. Ammon's Rescue Party from Zarahemla (Mosiah 7:1–16)</h4>
        <p>Mosiah₂ dispatched Ammon and fifteen strong men to ascertain the fate of Zeniff's colony; after wandering forty days in the wilderness, they located King Limhi.</p>
      </div>
      <div class="journey-item">
        <h4>5. Limhi's Explorers Searching for Zarahemla (Mosiah 8:7–11; 21:25–28)</h4>
        <p>A party of 43 men traveled north seeking Zarahemla but bypassed it, discovering instead the Jaredite battlefield covered with dry bones and 24 gold plates.</p>
      </div>
      <div class="journey-item">
        <h4>6. Limhi's People Escape to Zarahemla (Mosiah 22:11–13)</h4>
        <p>Guided by Ammon, the people of Limhi intoxicated their Lamanite guards and escaped through the back pass into the wilderness, reaching Zarahemla.</p>
      </div>
      <div class="journey-item">
        <h4>7. Alma₁ Flees to the Waters of Mormon (Mosiah 18:4–16)</h4>
        <p>Having repented upon hearing Abinadi, Alma fled Noah's court and gathered believers to the thicket of Mormon to establish the covenant of baptism.</p>
      </div>
      <div class="journey-item">
        <h4>8. Alma's Colony to Helam and Bondage (Mosiah 23:1–20)</h4>
        <p>Warned of an approaching army of King Noah, Alma's people traveled eight days into the wilderness and founded the peaceful city of Helam.</p>
      </div>
      <div class="journey-item">
        <h4>9. Alma's People Escape to Zarahemla (Mosiah 24:18–25)</h4>
        <p>Delivered by divine power from the taskmasters of Amulon, Alma's people traveled one day to the Valley of Alma, and after twelve more days arrived safely in Zarahemla (total 21 days from Helam).</p>
      </div>
      <div class="journey-item">
        <h4>10. Sons of Mosiah on their 14-Year Mission (Alma 17:6–9)</h4>
        <p>Ammon, Aaron, Omner, and Himni traveled up to the land of Nephi to preach repentance to the Lamanites, spending fourteen years among them.</p>
      </div>
      <div class="journey-item">
        <h4>11. Anti-Nephi-Lehies (People of Ammon) Relocate to Jershon (Alma 27:14–26)</h4>
        <p>The thousands of converted Lamanites who laid down their weapons of war were escorted down to Zarahemla and granted the land of Jershon on the east coast.</p>
      </div>
      <div class="journey-item">
        <h4>12. Nephi and Lehi Preach in Nephi and Zarahemla (Helaman 5:14–52)</h4>
        <p>Nephi and Lehi preached throughout the Nephite cities and then went up to the land of Nephi, where they were miraculously encircled with fire in prison.</p>
      </div>
    </div>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_155_almas_escape.png" alt="Chart 155: Alma's Escape from Nephi to Zarahemla" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 155: From Nephi to Zarahemla — Alma's Escape Route.</figcaption>
    </figure>

    <hr class="section-divider" />

    <h2 class="appendix-h2">Alma's Missionary Journeys in Zarahemla</h2>
    <p>Following his resignation as Chief Judge in the ninth year of the judges, Alma the Younger embarked on a systematic missionary circuit through the river basin and western borders of Zarahemla (Alma 5–16):</p>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_157_almas_journeys.png" alt="Chart 157: Alma's Journeys in the Land of Zarahemla" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 157: Alma's Missionary Circuit in the Land of Zarahemla.</figcaption>
    </figure>

    <hr class="section-divider" />

    <h2 class="appendix-h2">Plausible Geographic Correlations in Mesoamerica</h2>
    <p>While the Church of Jesus Christ of Latter-day Saints takes no official position on external Book of Mormon geography, scholarly consensus among LDS anthropologists (such as John L. Sorenson) notes that the Isthmus of Tehuantepec in southern Mexico matches the internal topological constraints, orientations, and distances of Mormon's map with remarkable fidelity:</p>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_160_mesoamerica_locations.png" alt="Chart 160: Plausible Geographic Correlations in Mesoamerica" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 160: Plausible Geographic Correlations in Mesoamerica.</figcaption>
    </figure>
  </section>"""
    return _xhtml_doc("Appendix B: Internal Book of Mormon Geography & Mormon's Map", content)


def render_appendix_legal_cases_xhtml() -> str:
    """Render Appendix C: The Legal Cases and Judicial Procedures."""
    content = """  <section epub:type="appendix" class="appendix-section" id="appendix-c">
    <header class="appendix-header">
      <p class="appendix-subtitle">Supplemental Study Resources • Appendix C</p>
      <h1 class="appendix-title">The Legal Cases &amp; Judicial Procedures in the Book of Mormon</h1>
      <p class="appendix-byline">Based on <em>The Legal Cases in the Book of Mormon</em> by John W. Welch (BYU Press &amp; Maxwell Institute)</p>
    </header>

    <div class="appendix-intro">
      <p>The Book of Mormon contains detailed records of numerous formal legal controversies, judicial inquests, and trials. Far from being generic legal fiction, these accounts reflect the precise technical jurisprudence of ancient Israelite law (the Law of Moses) combined with the institutional legal reforms instituted by King Mosiah around 91 B.C.</p>
      <p>In his landmark 500-page treatise <em>The Legal Cases in the Book of Mormon</em>, legal scholar John W. Welch demonstrates that every legal proceeding in the Nephite text faithfully reflects ancient biblical rules of criminal procedure, including:</p>
      <ul class="appendix-list">
        <li><strong>The Two-Witness Rule:</strong> No person could be put to death or convicted of a capital crime without the concurrent testimony of two or three eyewitnesses (Deuteronomy 17:6; 19:15; Numbers 35:30).</li>
        <li><strong>Judicial Bribery &amp; Official Corruption:</strong> Mosiah's legal code strictly prohibited judges from accepting gifts, fees, or bribes, fixing judicial pay at one <em>senine</em> of silver per day on the bench (Alma 11:1–3).</li>
        <li><strong>Divine Inquest &amp; Signs:</strong> In trials where human testimony was insufficient, ancient Near Eastern courts resorted to divine trial or signs to establish divine verdict (as seen in the trials of Sherem and Korihor).</li>
        <li><strong>The Law of the Rebellious False Prophet:</strong> Deuteronomy 13 and 18 prescribed capital punishment for any prophet who enticed Israel to follow other gods or falsely prophesied in the name of the Lord.</li>
      </ul>
    </div>

    <figure class="appendix-figure">
      <img class="appendix-img" src="../images/appendix/chart_121_legal_cases.png" alt="Chart 121: Legal Cases and Procedures in the Book of Mormon" />
      <figcaption class="appendix-caption">Welch &amp; Welch, Chart 121: Legal Cases and Procedures in the Book of Mormon.</figcaption>
    </figure>

    <hr class="section-divider" />

    <h2 class="appendix-h2">Seven Landmark Book of Mormon Legal Cases</h2>

    <!-- 1. SHEREM -->
    <article class="legal-case-card" id="case-sherem">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="jacob_07.xhtml#v1">&#8592; Return to Scripture (Jacob 7:1)</a>
        <h3 class="legal-case-title">1. The Case of Sherem (Jacob 7:1–23)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> ~500 B.C. &bull; <strong>Court:</strong> Public Inquest before Jacob &bull; <strong>Accusation:</strong> Overthrowing the Law of Moses &amp; Preaching False Doctrine</p>
      </div>
      <div class="legal-case-body">
        <p>Sherem was an articulate, learned polemicist who challenged Jacob, arguing that Jacob had committed blasphemy by preaching that the Law of Moses pointed toward a future Messiah. Sherem argued that no man could know of things to come and that Jacob was perverting the divine law.</p>
        <p>When Jacob testified of Christ through the scriptures and the Holy Ghost, Sherem insolently demanded a sign: <em>"Show me a sign by this power of the Holy Ghost, in the which ye know so much."</em> Jacob refused to tempt God, leaving the verdict in the hands of the Lord. God struck Sherem to the earth. After lying paralyzed for many days, Sherem assembled the multitude, confessed his sins, retracted his false teachings, confessed the true Christ, and died.</p>
      </div>
    </article>

    <!-- 2. ABINADI -->
    <article class="legal-case-card" id="case-abinadi">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="mosiah_11.xhtml#v20">&#8592; Return to Scripture (Mosiah 11:20)</a>
        <h3 class="legal-case-title">2. The Trial of Abinadi (Mosiah 11–17)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> ~150–148 B.C. &bull; <strong>Court:</strong> Royal Council of King Noah and his Priests &bull; <strong>Accusation:</strong> False Prophecy, Reviling the King, and Blasphemy</p>
      </div>
      <div class="legal-case-body">
        <p>Abinadi was indicted under three specific charges in Noah's royal court: (1) false prophecy against the city, (2) reviling the king (Exodus 22:28), and (3) blasphemy for declaring that God Himself should come down among men. When Noah sought an excuse to execute him, Abinadi challenged the corrupt priests on their observance of the Ten Commandments and delivered his magnificent exposition of Isaiah 53.</p>
        <p>Although Noah hesitated and was almost persuaded to release him, his wicked priests incited him to condemn Abinadi. Abinadi was executed by fire (scourged with burning faggots), sealing his testimony with his blood, while Alma₁ fled Noah's wrath to preserve the prophetic record.</p>
      </div>
      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_123_charges_abinadi.png" alt="Chart 123: Legal Charges Brought against Abinadi" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 123: Legal Charges Brought against Abinadi.</figcaption>
      </figure>
    </article>

    <!-- 3. NEHOR -->
    <article class="legal-case-card" id="case-nehor">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="alma_01.xhtml#v1">&#8592; Return to Scripture (Alma 1:1)</a>
        <h3 class="legal-case-title">3. The Trial of Nehor (Alma 1:1–15)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> 91 B.C. (1st Year of Judges) &bull; <strong>Court:</strong> Alma the Younger, Chief Judge &bull; <strong>Accusation:</strong> Priestcraft and the Murder of Gideon</p>
      </div>
      <div class="legal-case-body">
        <p>Nehor was the first criminal brought before Alma the Younger under the newly established reign of the judges. Nehor had introduced priestcraft—teaching that priests ought to become popular and supported by the people—and universal salvation without repentance. When the venerable patriot Gideon confronted him with the words of God, Nehor drew his sword and slew Gideon.</p>
        <p>Alma judged Nehor according to the law: <em>"Thou art condemned to die, according to the law which has been given us by Mosiah, our last king; and it has been acknowledged by this people; therefore this people must abide by the law."</em> Nehor was executed on top of Hill Manti, ignominiously confessing between the heavens and the earth that his doctrine was false.</p>
      </div>
      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_122_opponents.png" alt="Chart 122: Three Diverse Opponents: Sherem, Nehor, Korihor" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 122: Comparison of Sherem, Nehor, and Korihor.</figcaption>
      </figure>
    </article>

    <!-- 4. AMMONIHAH -->
    <article class="legal-case-card" id="case-ammonihah">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="alma_14.xhtml#v1">&#8592; Return to Scripture (Alma 14:1)</a>
        <h3 class="legal-case-title">4. The Judicial Corruption &amp; Martyrdom at Ammonihah (Alma 14)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> 81 B.C. &bull; <strong>Court:</strong> Corrupt Judges &amp; Lawyers of the Order of Nehor &bull; <strong>Accusation:</strong> Reviling the Law, Judges, and People</p>
      </div>
      <div class="legal-case-body">
        <p>In Ammonihah, Alma and Amulek faced corrupt lawyers like Zeezrom who sought to snare them for financial gain. After Amulek exposed Zeezrom's attempted bribery, the enraged magistrates arrested the prophets, subjected them to unlawful cross-examination, and cast their converts (women and children) into a fiery furnace while forcing Alma and Amulek to witness the martyrdom.</p>
        <p>While imprisoned, naked and bound, the Chief Judge and other judges smote them repeatedly. In divine response, Alma cried unto God, their cords were miraculously burst, and a massive earthquake flattened the prison walls, killing all the corrupt judges while leaving Alma and Amulek unharmed.</p>
      </div>
    </article>

    <!-- 5. KORIHOR -->
    <article class="legal-case-card" id="case-korihor">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="alma_30.xhtml#v6">&#8592; Return to Scripture (Alma 30:6)</a>
        <h3 class="legal-case-title">5. The Trial of Korihor (Alma 30:6–60)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> 74 B.C. &bull; <strong>Court:</strong> High Priest Giddonah (Jershon), Chief Judge (Gideon), Alma &amp; Chief Judge (Zarahemla) &bull; <strong>Accusation:</strong> Blasphemy, Anti-Christ Defamation, Sign-Seeking</p>
      </div>
      <div class="legal-case-body">
        <p>Nephite constitutional law guaranteed absolute freedom of personal belief: <em>"There was no law against a man's belief... for if a man desired to serve God, it was his privilege; but if he did not believe in him there was no law to punish him"</em> (Alma 30:7–9). However, when Korihor traveled through the lands ridiculing ordinances, accusing the priesthood of tyranny, and demanding a miraculous sign, he crossed into actionable blasphemy.</p>
        <p>Before Alma in Zarahemla, Korihor persisted in demanding a sign from God. Alma warned him, and by the power of God, Korihor was struck dumb. Reduced to writing on paper, Korihor confessed: <em>"I always knew that there was a God. But behold, the devil hath deceived me."</em> Cast out, Korihor went begging from house to house until he was trodden down and killed by the Zoramites.</p>
      </div>
    </article>

    <!-- 6. PAANCHI -->
    <article class="legal-case-card" id="case-paanchi">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="helaman_01.xhtml#v7">&#8592; Return to Scripture (Helaman 1:7)</a>
        <h3 class="legal-case-title">6. The Trial of Paanchi (Helaman 1:7–8)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> 52 B.C. &bull; <strong>Court:</strong> Nephite Tribunal &bull; <strong>Accusation:</strong> Sedition, Treason, and Insurrection</p>
      </div>
      <div class="legal-case-body">
        <p>Following the death of Chief Judge Pahoran, his three sons Pahoran₂, Paanchi, and Pacumeni contested for the judgment seat. The voice of the people elected Pahoran₂. Paanchi, refusing to accept the constitutional democratic outcome, attempted to flatter a faction to rise up in armed rebellion.</p>
        <p>Paanchi was swiftly arrested, tried according to the voice of the people, convicted of high treason, and condemned to death. In retaliation, his secret band dispatched the assassin Kishkumen, who murdered Pahoran₂ upon the judgment seat.</p>
      </div>
    </article>

    <!-- 7. SEANTUM -->
    <article class="legal-case-card" id="case-seantum">
      <div class="legal-case-header">
        <a class="back-to-verse-link" href="helaman_09.xhtml#v1">&#8592; Return to Scripture (Helaman 9:1)</a>
        <h3 class="legal-case-title">7. The Trial of Seantum (Helaman 9:1–38)</h3>
      </div>
      <div class="legal-case-meta">
        <p><strong>Date:</strong> 23 B.C. &bull; <strong>Court:</strong> Judges of Zarahemla &bull; <strong>Accusation:</strong> Murder of Chief Judge Seezoram</p>
      </div>
      <div class="legal-case-body">
        <p>When the prophet Nephi warned the people of the secret murder of Chief Judge Seezoram, corrupt judges accused Nephi of conspiracy. Nephi answered with a divine forensic test: he instructed the judges to go to the house of Seantum, the brother of Seezoram, inspect the skirts of his cloak for blood, and interrogate him.</p>
        <p>Nephi prophesied the exact dialogue and Seantum's trembling guilt. When the magistrates followed Nephi's instructions, they found fresh blood upon Seantum's garments; Seantum turned pale, trembled, and confessed that he had murdered his brother. Seantum was condemned, and Nephi was exonerated.</p>
      </div>
    </article>
  </section>"""
    return _xhtml_doc("Appendix C: Legal Cases & Judicial Procedures", content)


def render_appendix_charts_xhtml() -> str:
    """Render Appendix D: Chronology, Plates, and Structural Charts."""
    content = """  <section epub:type="appendix" class="appendix-section" id="appendix-d">
    <header class="appendix-header">
      <p class="appendix-subtitle">Supplemental Study Resources • Appendix D</p>
      <h1 class="appendix-title">Chronology, Plates, &amp; Structural Charts</h1>
      <p class="appendix-byline">Based on <em>Charting the Book of Mormon</em> by John W. Welch and J. Gregory Welch</p>
    </header>

    <div class="appendix-intro">
      <p>This appendix compiles foundational structural, chronological, and doctrinal visual aids from <em>Charting the Book of Mormon</em> (FARMS / BYU Press). These charts summarize the complex archival sources, lineages, monetary standards, and prophetic allegories embedded within the Nephite records.</p>
    </div>

    <hr class="section-divider" />

    <!-- 1. PLATES AND RECORDS -->
    <article class="chart-section" id="chart-plates">
      <h2 class="appendix-h2">1. The Plates and Records of the Book of Mormon</h2>
      <p>The Book of Mormon is an abridgment compiled primarily from four distinct sets of metal plate records:</p>
      <ul class="appendix-list">
        <li><strong>The Plates of Nephi:</strong> Divided into the <em>Small Plates</em> (focused on spiritual ministry, prophesying, and revelations, from 1 Nephi through Omni) and the <em>Large Plates</em> (containing the detailed secular, monarchic, political, and military history from Lehi down to Mormon).</li>
        <li><strong>The Plates of Mormon:</strong> An abridgment engraved on golden plates by the prophet-general Mormon, summarizing the Large Plates of Nephi from the Reign of Mosiah down to his own day, supplemented with the original Small Plates of Nephi intact.</li>
        <li><strong>The Plates of Ether:</strong> Twenty-four gold plates discovered by the expedition of King Limhi, containing the ancient history of the Jaredites from the Tower of Babel down to their extinction, abridged by Moroni as the Book of Ether.</li>
        <li><strong>The Plates of Brass:</strong> Brought from Jerusalem by Nephi and his brothers from Laban's treasury, containing the Five Books of Moses, historical records down to the reign of Zedekiah, prophecies of Isaiah, Jeremiah, Zenos, Zenock, and Neum, and the genealogy of Joseph.</li>
      </ul>

      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_13_plates.png" alt="Chart 13: Book of Mormon Plates and Records" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 13: Book of Mormon Plates and Records.</figcaption>
      </figure>
    </article>

    <hr class="section-divider" />

    <!-- 2. RECORD KEEPERS & LIFE SPANS -->
    <article class="chart-section" id="chart-lifespans">
      <h2 class="appendix-h2">2. Life Spans of Lehi's Lineage and Record Keepers</h2>
      <p>The primary lineage responsible for keeping the Small Plates of Nephi passed from father to son (and brother to brother) across nine generations: Lehi &rarr; Nephi &rarr; Jacob &rarr; Enos &rarr; Jarom &rarr; Omni &rarr; Amaron &rarr; Chemish &rarr; Abinadom &rarr; Amaleki, who delivered the plates into the custody of King Benjamin.</p>

      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_26_lifespans.png" alt="Chart 26: Life Spans of Lehi's Lineage" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 26: Life Spans of Lehi's Lineage.</figcaption>
      </figure>
    </article>

    <hr class="section-divider" />

    <!-- 3. MONETARY SYSTEM -->
    <article class="chart-section" id="chart-monetary-system">
      <div class="chiasmus-header">
        <a class="back-to-verse-link" href="alma_11.xhtml#v1">&#8592; Return to Scripture (Alma 11:1)</a>
        <h2 class="appendix-h2">3. King Mosiah's Monetary System (Alma 11)</h2>
      </div>
      <p>In Alma 11, the text records King Mosiah's standardization of weights and measures. This was not a coin system (coins are stamped tokens with state seals), but a precision weight standard of precious metals calibrated against agricultural grain measurement (one <em>senine</em> of silver or <em>senum</em> of gold equaled one measure of barley or other grain):</p>

      <div class="monetary-table-wrapper">
        <table class="appendix-table">
          <thead>
            <tr>
              <th>Metal</th>
              <th>Unit Name</th>
              <th>Relative Value</th>
              <th>Barley Equivalency</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Silver</td><td>Senine</td><td>1.0 unit</td><td>1 measure of barley (1 judge's daily wage)</td></tr>
            <tr><td>Silver</td><td>Seon</td><td>2.0 units</td><td>2 measures of barley</td></tr>
            <tr><td>Silver</td><td>Shum</td><td>4.0 units</td><td>4 measures of barley</td></tr>
            <tr><td>Silver</td><td>Onti</td><td>7.0 units</td><td>7 measures of barley</td></tr>
            <tr class="table-subhdr"><td colspan="4">Gold Standard Units</td></tr>
            <tr><td>Gold</td><td>Senum</td><td>1.0 unit</td><td>1 measure of barley</td></tr>
            <tr><td>Gold</td><td>Antion</td><td>1.5 units</td><td>1.5 measures of barley (3 shiblons)</td></tr>
            <tr><td>Gold</td><td>Seon</td><td>2.0 units</td><td>2 measures of barley</td></tr>
            <tr><td>Gold</td><td>Shum</td><td>4.0 units</td><td>4 measures of barley</td></tr>
            <tr><td>Gold</td><td>Limnah</td><td>7.0 units</td><td>7 measures of barley</td></tr>
            <tr class="table-subhdr"><td colspan="4">Fractional Silver Units</td></tr>
            <tr><td>Silver</td><td>Shiblon</td><td>0.5 unit (1/2 senine)</td><td>1/2 measure of barley</td></tr>
            <tr><td>Silver</td><td>Shiblum</td><td>0.25 unit (1/4 senine)</td><td>1/4 measure of barley</td></tr>
            <tr><td>Silver</td><td>Leah</td><td>0.125 unit (1/8 senine)</td><td>1/8 measure of barley</td></tr>
          </tbody>
        </table>
      </div>

      <p class="section-note">Notice the mathematical brilliance: 1 onti/limnah (7 units) equals the sum of a senine (1) + a seon (2) + a shum (4). This is a base-2 binary scale supplemented with 7 for weekly transactions!</p>

      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_110_monetary.png" alt="Chart 110: King Mosiah's Monetary System" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 110: King Mosiah's Monetary System (Alma 11:1–19).</figcaption>
      </figure>
    </article>

    <hr class="section-divider" />

    <!-- 4. ALLEGORY OF THE OLIVE TREE -->
    <article class="chart-section" id="chart-olive-tree">
      <div class="chiasmus-header">
        <a class="back-to-verse-link" href="jacob_05.xhtml#v1">&#8592; Return to Scripture (Jacob 5:1)</a>
        <h2 class="appendix-h2">4. Zenos's Allegory of the Olive Tree (Jacob 5)</h2>
      </div>
      <p>Jacob 5 preserves the ancient prophet Zenos's extensive prophetic allegory of the tame and wild olive trees. This magnificent masterwork traces the entire history of the House of Israel from antiquity through the scattering, the times of the Gentiles, the Great Apostasy, the latter-day restoration, the Millennium, and the final judgment.</p>

      <figure class="appendix-figure">
        <img class="appendix-img" src="../images/appendix/chart_81_olive_tree.png" alt="Chart 81: Allegory of the Olive Tree" />
        <figcaption class="appendix-caption">Welch &amp; Welch, Chart 81: The Allegory of the Olive Tree (Jacob 5).</figcaption>
      </figure>
    </article>
  </section>"""
    return _xhtml_doc("Appendix D: Chronology, Plates, & Structural Charts", content)
