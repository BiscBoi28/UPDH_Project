#!/usr/bin/env python3
"""
Builds every printable document for Section 2 ("What Can Be Taken?") of the
Museum of Theft into ../section-2/. Same method as build_section1.py: HTML at
real millimetre size, printed to PDF with headless Chrome.

Run:  python3 build_section2.py
"""
import html
from common import (S1, ROOT, QR, u, doc, paras, label, webprint, BUILT, ORN, use_section, copy_pdf,
                    image_pages, qr_panel, section_header, voting, tent_card, object_labels)

use_section(2)
HERE = S1.HERE
OUT = ROOT / "section-2"
A = HERE / "assets" / "section-2"
NEWS = A / "news"
CASE = {"h": OUT / "00_section-header", "r": OUT / "01_seventy-thousand-seeds", "v": OUT / "02_what-the-blood-was-for",
        "c": OUT / "03_a-search-engine-for-faces", "s": OUT / "shared-desk-items"}
for p in CASE.values():
    p.mkdir(parents=True, exist_ok=True)

# =====================================================================================
# TEXT (Phase 4 text, as on the Section 2 layout mock-up)
# =====================================================================================
INTRO = [
    "Most theft is easy to recognise. Something leaves its owner without permission, and the owner no longer has it. The three cases here are harder. In each, something small moved: seeds from a forest, blood from a village, photos from the internet. Yet it is hard to say what the owner lost. Brazil kept its rubber trees. The donors gave their blood willingly. The original photos stayed online.",
    "What changed was what each thing became: plantations on another continent, data for studies the donors say they never agreed to, a search engine for faces. Those who call these cases theft point to what the thing became, not only to what moved.",
    "The cases span 150 years, from the age of empire to the age of the internet. Each panel sets out what happened, who calls it theft and why, and how the other side answers.",
]
RUB = [
    "In 1876, Henry Wickham, an Englishman living in the Amazon, shipped about 70,000 rubber seeds to Kew Gardens in London, paid by Britain’s India Office. By his own later account, he told customs they were “exceedingly delicate botanical specimens”. Brazil was then the world’s main source of rubber. The seedlings went on to British Asia. For twenty years little changed; then plantation labour, investment and the demand for bicycle and car tyres turned them into an industry. By 1913 Asian plantations had overtaken the Amazon, and Brazil’s rubber boom ended. Kerala’s rubber trees descend largely from the same seeds.",
    "In Brazil, Wickham is remembered as “the father of bio-piracy”: someone who profited from Brazil’s plants without its consent. Wickham called it patriotism. No Brazilian law in 1876 banned taking the seeds, Brazil kept its trees, and the plantations took decades of work to succeed. Britain knighted him in 1920.",
]
HAV = [
    "The Havasupai are a Native American tribe of about 650 people, living deep in the Grand Canyon. From 1990, researchers from Arizona State University (ASU) collected blood from more than 200 members. Tribal leaders were told the study was about diabetes; the written consent form spoke more broadly, of “behavioral/medical disorders”.",
    "The samples were used in 23 papers and dissertations. Fifteen had nothing to do with diabetes; they covered schizophrenia, inbreeding and the tribe’s origins. One suggested its ancestors came from Asia, while the tribe’s own history says they began in the canyon. Tribal council member Carletta Tilousi said: “people got degrees and grants, and they never asked our permission.”",
    "The lead researcher defended the work as ethical: science often advances through studies not tied to one disease. In 2010, ASU’s governing board settled. It paid $700,000 to 41 tribe members, returned the samples and apologised. No court ever ruled on whether the research broke the law. The blood went home. The published papers did not.",
]
CLV = [
    "Clearview AI, an American company founded in 2017, copies publicly posted photos from social media, news sites and other websites, without telling the people in them. Its software turns each face into a faceprint, a list of numbers describing its geometry. One uploaded photo can then find other photos of the same face online. By its own count, it holds more than 100 billion images, and it sells searches mainly to police and government agencies.",
    "Regulators in Canada, Australia and several European countries found it broke their privacy laws. Canada’s privacy commissioner said: “What Clearview does is mass surveillance and it is illegal.” Illinois law draws its line at the faceprint: it protects scans of face geometry, but not photographs.",
    "Clearview’s co-founder, Hoan Ton-That, said: “All the data inside Clearview AI is publicly available, as it is with Google.” The company says police use it to identify suspects and abused children. It admits no wrongdoing, and has not paid several European fines.",
]

# Story palettes (from the layout mock-up)
VIC_BG = "linear-gradient(160deg,#f6efdf 0%,#f1e8d4 60%,#ebdfc6 100%)"
GRN, BRN, VINK = "#2f4a3a", "#8a5a2e", "#2b2a26"
SCOUT, KHAKI, SINK, SMUTE = "#fdf6e3", "#b6a883", "#33303d", "#8a7a4e"
FEED, TAN, RUST, FINK = "#fbf6f2", "#d5b7a3", "#9b5a3c", "#241a15"
UNNA, MONT, DMS = "Unna,Georgia,serif", "Montserrat,Arial,sans-serif", "'DM Sans',Arial,sans-serif"

hl = lambda l, t, w, h: f'<div style="position:absolute;left:{l}%;top:{t}%;width:{w}%;height:{h}%;background:rgba(253,224,71,.55);mix-blend-mode:multiply"></div>'
clip = lambda f, extra="", pad=1.5, border="#c9c2b0": f'<div style="background:#fff;border:.3mm solid {border};padding:{pad}mm;box-shadow:.4mm .6mm 1.4mm rgba(0,0,0,.18)"><img src="{u(A/f)}" style="width:100%;{extra}"></div>'


def build_header():
    section_header("BOARD_H_section-header_What-Can-Be-Taken_1180x90mm", CASE["h"], kicker="Section 2", title="What Can Be Taken?",
                   sub="Three cases, from 1876 to today", intro=INTRO, qr_file="07_What_Can_Be_Taken.png", qr_caption="Audio guide · Section 2")


# =====================================================================================
# STORY 1 · SEVENTY THOUSAND SEEDS (Victorian template)
# =====================================================================================
def build_rubber():
    F = CASE["r"]
    frame = f'<div style="position:absolute;inset:4.5mm;border:.5mm solid {GRN};pointer-events:none"></div>'
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:{VINK};font-family:{UNNA}">{frame}
      <div style="position:absolute;left:12mm;right:12mm;top:10mm">
        <div style="height:8mm;background:url('{u(ORN)}') repeat-x center/auto 100%;margin-bottom:4mm"></div>
        <div style="font-size:10pt;letter-spacing:3pt;text-transform:uppercase;color:{BRN}">Section 2 · Story 1</div>
        <div style="font-family:'Diplomata SC',Georgia,serif;color:{GRN};font-size:21pt;line-height:1.2;margin-top:2mm">Seventy Thousand Seeds</div>
        <div style="font-size:11pt;font-style:italic;color:{BRN};margin-top:1.5mm;padding-bottom:2.5mm;border-bottom:.4mm solid {GRN}">Henry Wickham · the Amazon to Kew Gardens, London · 1876</div></div>
      <div class="fit" style="position:absolute;left:12mm;right:12mm;top:62mm;bottom:40mm;font-size:32pt;line-height:1.42;overflow:hidden">{paras(RUB,'margin-bottom:.6em')}</div>
      <div style="position:absolute;left:12mm;right:12mm;bottom:11mm;border-top:.4mm solid {GRN};padding-top:3mm;font-size:15pt;line-height:1.3">Brazil kept its rubber trees.<br><b>What, if anything, did Britain take?</b></div></div>"""
    doc("BOARD_R1_wall-text_Seventy-Thousand-Seeds_210x297mm", F, 210, 297, body)

    # R2 · Timeline, drawn to scale (1876–1920)
    events = [(1876, "1876", "Wickham’s 70,000 seeds leave Brazil. No law forbids it."), (1884, "1884", "Amazonas puts high export duties on rubber seeds."),
              (1895, "1890s", "First commercial rubber plantings in Malaya."), (1912, "1912", "Brazil passes the Rubber Defence Law."),
              (1913, "1913", "Asian plantations overtake the Amazon."), (1918, "1918", "Brazil bans the export of rubber seeds."),
              (1920, "1920", "Wickham is knighted in Britain.")]
    top, bot = 38, 262
    ypos = lambda y: top + (y - 1876) / (1920 - 1876) * (bot - top)
    lab_y = [36, 66, 112, 176, 198, 220, 242]          # label positions (mm), kept apart
    items = ""
    for (y, t, d), ly in zip(events, lab_y):
        ty = ypos(y)
        items += f"""<div style="position:absolute;left:24mm;top:{ty-.25:.2f}mm;width:5mm;height:.5mm;background:{GRN}"></div>
          <svg style="position:absolute;left:29mm;top:0;width:8mm;height:297mm" viewBox="0 0 8 297"><line x1="0" y1="{ty:.2f}" x2="8" y2="{ly+3:.2f}" stroke="{BRN}" stroke-width=".25"/></svg>
          <div style="position:absolute;left:38mm;right:9mm;top:{ly}mm"><div style="font-family:'Diplomata SC',Georgia,serif;font-size:13pt;color:{GRN}">{t}</div>
          <div style="font-size:12.5pt;line-height:1.22">{d}</div></div>"""
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:{VINK};font-family:{UNNA}">
      <div style="position:absolute;inset:4.5mm;border:.5mm solid {GRN}"></div>
      <div style="position:absolute;left:11mm;right:9mm;top:11mm"><div style="font-family:'Diplomata SC',Georgia,serif;color:{GRN};font-size:16pt">It took decades</div>
        <div style="font-size:11pt;font-style:italic;color:{BRN}">1876–1920, drawn to scale</div></div>
      <div style="position:absolute;left:25.75mm;top:{top}mm;height:{bot-top}mm;width:1.2mm;background:{GRN}"></div>
      <div style="position:absolute;left:12mm;top:{ypos(1876)+8}mm;height:{ypos(1904)-ypos(1876)-16}mm;width:8mm;display:flex;align-items:center;justify-content:center">
        <div style="transform:rotate(-90deg);white-space:nowrap;font-size:9pt;font-style:italic;color:{BRN}">28 quiet years</div></div>
      {items}
      <div style="position:absolute;left:38mm;right:9mm;top:140mm;font-size:12pt;font-style:italic;color:{BRN};line-height:1.3">Twenty years after the seeds left, Brazil is still the world’s main source of rubber.</div>
      <div class="credit" style="position:absolute;left:11mm;bottom:8mm">Timeline · Made for this exhibition</div></div>"""
    doc("BOARD_R2_timeline_It-Took-Decades_155x297mm", F, 155, 297, body)

    # R3 · Britain's verdict: the real London Gazette, 4 June 1920 (published 5 June)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:{VINK};font-family:{UNNA};padding:5mm 6mm;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:.4mm solid {GRN};padding-bottom:1mm">
        <div style="font-size:9pt;letter-spacing:2.5pt;text-transform:uppercase;color:{BRN}">Britain’s verdict</div><div style="font-family:'Diplomata SC',Georgia,serif;color:{GRN};font-size:13pt">1920</div></div>
      <div style="display:flex;gap:4mm;margin-top:3mm;flex:1;min-height:0">
        <div style="flex:1;display:flex;flex-direction:column;gap:2.5mm">
          {clip('gz20_masthead.png')}
          <div style="font-size:9.5pt;font-style:italic;color:{BRN}">Second Supplement to <i>The London Gazette</i>, issue 31931, page 6313 · Birthday Honours: Knights Bachelor</div></div>
        <div style="width:86mm;flex:none;align-self:flex-start;position:relative">{clip('gz20_col.png')}
          <div style="position:absolute;left:1.8mm;right:1.8mm;top:1.8mm;bottom:1.8mm">{hl(2,79.1,96,9.9)}</div></div></div>
      <div style="margin-top:3mm">{label("“For services in connection with the rubber plantation industry in the Far East”",
            "1920 · Knighthood, <i>The London Gazette</i>, 5 June 1920, p. 6315 · Reproduction from thegazette.co.uk",
            "Britain’s verdict: the official notice knighting Henry Alexander Wickham. It names the industry his seeds began. It does not mention Brazil.",
            mcolor=BRN, tsize=11.5, dsize=10)}</div></div>"""
    doc("BOARD_R3_Britains-verdict_London-Gazette-1920_185x190mm", F, 185, 190, body)

    # R4 · Brazil's verdict: Pesquisa FAPESP no. 158, April 2009 (real print pages)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:{VINK};font-family:{UNNA};padding:5mm 6mm;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:.4mm solid {GRN};padding-bottom:1mm">
        <div style="font-size:9pt;letter-spacing:2.5pt;text-transform:uppercase;color:{BRN}">Brazil’s verdict</div><div style="font-family:'Diplomata SC',Georgia,serif;color:{GRN};font-size:13pt">2009</div></div>
      <div style="display:flex;gap:4mm;margin-top:3mm">
        <div style="width:84mm;flex:none;display:flex;flex-direction:column;gap:2.5mm">
          {clip('fap_title.png')}
          <div style="position:relative">{clip('fap_col.png')}<div style="position:absolute;left:1.5mm;right:1.5mm;top:1.5mm;bottom:1.5mm">{hl(3.5,71.0,93.3,16.5)}{hl(3.5,87.7,69.3,5.4)}</div></div></div>
        <div style="flex:1;display:flex;flex-direction:column;gap:3mm">
          {clip('fap_photo.png', 'height:52mm;object-fit:cover;object-position:top')}
          <div style="font-size:8.5pt;font-weight:700;letter-spacing:1.5pt;text-transform:uppercase;color:{BRN}">In English</div>
          <div style="font-size:11pt;line-height:1.35;border-left:1.2mm solid {GRN};padding-left:3mm">“For decades there were discussions, with no satisfactory conclusion being reached, as to whether he behaved like a common thief or whether he was a ‘man of his time’; either way, he earned the moniker ‘the father of bio-piracy’.”</div>
          <div style="font-size:8pt;font-style:italic;color:{BRN}">Translation from the magazine’s own English edition. The Portuguese says <i>justo ou injusto</i>: ‘fair or unfair’.</div></div></div>
      <div style="margin-top:auto">{label("“As sementes da discórdia” (The seeds of discord)",
            "April 2009 · <i>Pesquisa FAPESP</i> no. 158, pp. 22–25, Brazil · Extract in Portuguese, with English",
            "A Brazilian research magazine on the long debate over whether Wickham was a thief or a man of his time. Its photo caption asks: <i>ladrão ou herói?</i> Thief or hero?",
            mcolor=BRN, tsize=11, dsize=9.5)}
        <div class="credit" style="margin-top:1.5mm">Pages: Carlos Haag, Pesquisa FAPESP (revistapesquisa.fapesp.br), CC BY-NC-ND. The full article is on the desk.</div></div></div>"""
    doc("BOARD_R4_Brazils-verdict_Pesquisa-FAPESP-2009_185x190mm", F, 185, 190, body)

    # R5 · Map: a real (unmarked) world map; the route is drawn on by hand
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:{VINK};font-family:{UNNA};padding:5mm 6mm;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2.5mm">
        <div style="font-family:'Diplomata SC',Georgia,serif;color:{GRN};font-size:14pt">From the Tapajós to Asia</div>
        <div style="font-size:10pt;font-style:italic;color:{BRN}">1876 to the 1890s</div></div>
      <img src="{u(A/'worldmap_1897_rubber.jpg')}" style="width:100%;flex:1;min-height:0;object-fit:cover;border:.4mm solid {GRN}">
      <div class="credit" style="margin-top:1.5mm">Map: Hermann Berghaus, <i>Chart of the World on Mercator’s Projection</i> (Gotha: Justus Perthes, 1897), detail. Public domain, via Wikimedia Commons.</div></div>"""
    doc("BOARD_R5_map_Tapajos-to-Asia_Berghaus-1897_297x210mm", F, 297, 210, body)

    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};border-top:3.5mm solid {GRN};padding:5mm;font-family:{UNNA};color:{VINK}">
      {label("From the Tapajós to Asia (map)", "1876 to the 1890s · Map printed 1897",
             "The seeds’ route: the Tapajós river, Belém, Liverpool, Kew Gardens, then Ceylon and Malaya. The route is drawn by hand on a world map of the time.",
             mcolor=BRN, tsize=14, dsize=12.5)}</div>"""
    doc("BOARD_R6_map-label_72x110mm", F, 72, 110, body)
    qr_panel("BOARD_R7_QR-audio_72x86mm", F, "08_Seventy_Thousand_Seeds.png", 72, 86, bg=GRN, fg="#f1e8d4", accent="#e2b98a",
             font=UNNA, line1="Listen &amp; see the sources", line2="Audio guide · Story 1", qr_mm=46)

    # Desk
    tent_card("DESK_R9_tent-card_rubber-seed_100x120mm-fold", F, "Seed of the Pará rubber tree (<i>Hevea brasiliensis</i>)", "Present day · Real seed",
              "A seed of the Pará rubber tree, like the 70,000 Wickham shipped from the Amazon in 1876.",
              bg="#f6efdf", color=VINK, mcolor=BRN, font=UNNA, rule=GRN)
    OS = F / "original-sources"
    copy_pdf(OS / "Pesquisa-FAPESP_158_2009-04_As-sementes-da-discordia_pp22-25.pdf", F / "DESK_R10_magazine_Pesquisa-FAPESP-2009_As-sementes-da-discordia_pp22-25.pdf")
    copy_pdf(OS / "London-Gazette_1920-06-04_issue-31931-supplement_pp6313-6315_Wickham-knighthood.pdf", F / "DESK_R11_government-document_London-Gazette-1920_pp6313-6315.pdf")


# =====================================================================================
# STORY 2 · WHAT THE BLOOD WAS FOR (permission-slip template)
# =====================================================================================
def tube(size, col):
    return f"""<svg width="{size}mm" height="{size}mm" viewBox="0 0 40 40"><rect x="15" y="3" width="10" height="6" rx="1.2" fill="{col}"/>
      <path d="M16 9 H24 V31 A4 4 0 0 1 16 31 Z" fill="none" stroke="{col}" stroke-width="2"/>
      <line x1="18" y1="14" x2="22" y2="14" stroke="{col}" stroke-width="1.4"/><line x1="18" y1="18" x2="22" y2="18" stroke="{col}" stroke-width="1.4"/><line x1="18" y1="22" x2="22" y2="22" stroke="{col}" stroke-width="1.4"/></svg>"""


def flow_icon(kind, c=SINK):
    if kind == "blood":
        return tube(17, c)
    if kind == "dna":
        return f"""<svg width="17mm" height="17mm" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="2"><path d="M12 4 C28 12 12 28 28 36"/><path d="M28 4 C12 12 28 28 12 36"/>
          <line x1="15" y1="9" x2="25" y2="9"/><line x1="17" y1="15" x2="23" y2="15"/><line x1="17" y1="25" x2="23" y2="25"/><line x1="15" y1="31" x2="25" y2="31"/></svg>"""
    if kind == "data":
        cells = "".join(f'<rect x="{7+j*7}" y="{7+i*7}" width="5" height="5" opacity="{((i*3+j*5)%4)/4+.25}"/>' for i in range(4) for j in range(4))
        return f'<svg width="17mm" height="17mm" viewBox="0 0 40 40" fill="{c}">{cells}</svg>'
    return f"""<svg width="17mm" height="17mm" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="2"><path d="M20 36 C20 36 9 24 9 16 A11 11 0 0 1 31 16 C31 24 20 36 20 36 Z"/><circle cx="20" cy="16" r="4"/></svg>"""


def build_havasupai():
    F = CASE["v"]
    body = f"""<div style="position:absolute;inset:0;background:{SCOUT};color:{SINK};font-family:{MONT}">
      <div style="position:absolute;left:0;top:0;width:30mm;height:30mm;background:{KHAKI};display:flex;align-items:center;justify-content:center">
        <div style="width:21mm;height:21mm;border-radius:50%;background:{SCOUT};display:flex;align-items:center;justify-content:center">{tube(15, SINK)}</div></div>
      <div style="position:absolute;left:36mm;right:10mm;top:8mm">
        <div style="font-weight:700;font-size:8pt;letter-spacing:2pt;text-transform:uppercase;color:{SMUTE}">Section 2 · Story 2</div>
        <div style="font-family:'League Spartan';font-weight:700;font-size:25pt;line-height:1.02;margin-top:1.5mm">WHAT THE BLOOD<br>WAS FOR</div></div>
      <div style="position:absolute;left:10mm;right:10mm;top:38mm;font-size:8.5pt;font-weight:600;color:{SMUTE};padding-bottom:2mm;border-bottom:.4mm solid {KHAKI}">The Havasupai Tribe and Arizona State University · Grand Canyon, USA · 1990–2010</div>
      <div class="fit" style="position:absolute;left:10mm;right:10mm;top:48mm;bottom:38mm;font-size:22pt;line-height:1.48;overflow:hidden">{paras(HAV,'margin-bottom:.6em')}</div>
      <div style="position:absolute;left:10mm;right:10mm;bottom:10mm;border-top:.5mm dashed {SINK};padding-top:3mm;font-family:'League Spartan';font-weight:700;font-size:15pt;line-height:1.15">They gave blood for a health study.<br><span style="color:{SMUTE}">How much permission travelled with it?</span></div></div>"""
    doc("BOARD_H1_wall-text_What-the-Blood-Was-For_210x297mm", F, 210, 297, body)

    # H2 · From blood to ancestry (diagram) + 23 outputs
    flow = [("blood", "BLOOD", "Given for a diabetes study"), ("dna", "DNA", "Read from the stored samples"),
            ("data", "DATA", "Copied, shared, analysed"), ("pin", "ANCESTRY", "A claim about where a people came from")]
    steps = "".join(f"""<div style="display:flex;align-items:center;gap:4mm"><div style="width:24mm;height:24mm;border-radius:50%;background:#efe6cc;display:flex;align-items:center;justify-content:center;flex:none">{flow_icon(k)}</div>
        <div><div style="font-family:'League Spartan';font-weight:700;font-size:18pt">{t}</div><div style="font-size:12pt;color:{SMUTE};font-weight:600;line-height:1.25">{d}</div></div></div>
        {'<div style="padding-left:9mm;font-size:9pt;color:'+SMUTE+'">▼</div>' if i < 3 else ''}""" for i, (k, t, d) in enumerate(flow))
    waffle = "".join(f'<div style="width:13.5mm;height:13.5mm;border-radius:1mm;background:{KHAKI if i < 8 else SINK}"></div>' for i in range(23))
    body = f"""<div style="position:absolute;inset:0;background:{SCOUT};color:{SINK};font-family:{MONT};padding:9mm 9mm 7mm;display:flex;flex-direction:column">
      <div style="font-weight:700;font-size:8pt;letter-spacing:2pt;text-transform:uppercase;color:{SMUTE}">Diagram</div>
      <div style="font-family:'League Spartan';font-weight:700;font-size:22pt;line-height:1.05;margin:1mm 0 7mm">FROM BLOOD<br>TO ANCESTRY</div>
      <div style="display:flex;flex-direction:column;gap:3.5mm">{steps}</div>
      <div style="border-top:.4mm solid {KHAKI};margin-top:7mm;padding-top:4mm;font-family:'League Spartan';font-weight:700;font-size:15pt">23 PAPERS &amp; DISSERTATIONS</div>
      <div style="display:grid;grid-template-columns:repeat(8,13.5mm);gap:2.3mm;margin-top:3mm">{waffle}</div>
      <div style="font-size:12pt;margin-top:3mm;line-height:1.5"><span style="display:inline-block;width:3mm;height:3mm;background:{KHAKI};vertical-align:middle"></span> 8 on diabetes<br>
        <span style="display:inline-block;width:3mm;height:3mm;background:{SINK};vertical-align:middle"></span> 15 on schizophrenia, inbreeding or the tribe’s origins</div>
      <div style="margin-top:auto">{label("From blood to ancestry (diagram)", "Made for this exhibition",
            "Blood becomes DNA, DNA becomes data, and data can answer questions no one asked when the blood was given.", mcolor=SMUTE, tsize=13, dsize=11.5)}</div></div>"""
    doc("BOARD_H2_diagram_From-Blood-to-Ancestry_155x297mm", F, 155, 297, body)

    # H3 · What did "yes" mean? Three versions + the court record
    cards = [("What tribal leaders were told", "Diabetes research", "The project was described to the Tribal Council again and again as a study of diabetes."),
             ("What the written form said", "“…to study the causes of behavioral/medical disorders.”", "The consent form signed by some of the early donors."),
             ("What later donors heard", "Diabetes research", "From 1991 to 1994 some blood was taken with spoken, not written, consent, explained as diabetes research.")]
    cardh = "".join(f"""<div style="flex:1;border:.4mm solid {SINK};background:#fffaf0;padding:3mm 4mm">
        <div style="font-weight:700;font-size:9pt;letter-spacing:1.3pt;text-transform:uppercase;color:{SMUTE}">{i+1}. {h}</div>
        <div style="font-family:'League Spartan';font-weight:700;font-size:{'18' if len(b) < 30 else '14'}pt;line-height:1.15;margin:2mm 0 1.5mm;{'font-style:italic' if i == 1 else ''}">{b}</div>
        <div style="font-size:11pt;line-height:1.35">{s}</div></div>""" for i, (h, b, s) in enumerate(cards))
    body = f"""<div style="position:absolute;inset:0;background:{SCOUT};color:{SINK};font-family:{MONT}">
      <div style="position:absolute;left:0;top:0;width:16mm;height:14mm;background:{KHAKI}"></div>
      <div style="position:absolute;left:22mm;top:4mm;right:8mm;display:flex;justify-content:space-between;align-items:baseline">
        <div style="font-family:'League Spartan';font-weight:700;font-size:16pt">WHAT DID “YES” MEAN?</div>
        <div style="font-weight:700;font-size:7.5pt;letter-spacing:1.5pt;text-transform:uppercase;color:{SMUTE}">Three versions of one permission · 1990–1994</div></div>
      <div style="position:absolute;left:8mm;right:8mm;top:18mm;height:47mm;display:flex;gap:4mm">{cardh}</div>
      <div style="position:absolute;left:8mm;right:8mm;top:68mm;text-align:center;font-size:8.5pt;letter-spacing:1pt;color:{SMUTE}">- - - - - - - - - - - - - - - - - - - - - - - - -  ✂ IN COURT, BOTH SIDES QUOTED THE SAME YEARS  - - - - - - - - - - - - - - - - - - - - - - - - -</div>
      <div style="position:absolute;left:8mm;right:8mm;top:75mm;height:80mm;display:flex;gap:5mm">
        <div style="flex:1;display:flex;flex-direction:column;gap:2mm">
          <div style="font-weight:700;font-size:7.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:{SMUTE}">The Tribe’s claim, as summarised in the brief</div>
          {clip('brief_allegation.png', border='#bbb')}</div>
        <div style="flex:1;display:flex;flex-direction:column;gap:2mm">
          <div style="font-weight:700;font-size:7.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:{SMUTE}">The researcher’s answer: the script donors were read</div>
          {clip('brief_footnote.png', border='#bbb')}{clip('brief_script.png', border='#bbb')}</div></div>
      <div style="position:absolute;left:8mm;width:178mm;bottom:6mm;display:flex;gap:6mm;align-items:flex-end">
        <div style="flex:1">{label("What did “yes” mean? (consent panel)",
            "1990–2007 · Cards made for this exhibition · Court record: Joint Answering Brief, <i>Havasupai Tribe v. Arizona Board of Regents</i>, Arizona Court of Appeals, No. 1 CA-CV 07-0454, pp. 3–4 · Reproduction",
            "Three versions of one permission. Below them, the two sides in court: the Tribe said it was told only about diabetes; Dr Markow said donors were read a script naming ‘diabetes, schizophrenia, depression’. No court ruled on which was true.",
            mcolor=SMUTE, tsize=11.5, dsize=10)}</div></div></div>"""
    doc("BOARD_H3_consent-panel_What-did-yes-mean_with-court-record_380x190mm", F, 380, 190, body)

    # H4 · Map: real National Park Service map (unmarked)
    body = f"""<div style="position:absolute;inset:0;background:{SCOUT};color:{SINK};font-family:{MONT};padding:6mm 7mm;display:flex;flex-direction:column">
      <div style="font-weight:700;font-size:8pt;letter-spacing:2pt;text-transform:uppercase;color:{SMUTE}">Map</div>
      <div style="font-family:'League Spartan';font-weight:700;font-size:16pt;margin:1mm 0 3mm">SUPAI, ARIZONA</div>
      <img src="{u(A/'nps_grandcanyon_havasupai.jpg')}" style="width:100%;height:135mm;object-fit:cover;border:.4mm solid {KHAKI}">
      <div style="margin-top:3mm">{label("Supai, Arizona (map)", "Grand Canyon National Park map, US National Park Service · Detail",
            "The Havasupai Reservation lies on the canyon’s south side, west of Grand Canyon Village. Supai, its village, is reachable only on foot, by mule or by helicopter.",
            mcolor=SMUTE, tsize=13, dsize=11)}</div>
      <div class="credit" style="margin-top:auto">Map: National Park Service, Harpers Ferry Center (public domain), via Wikimedia Commons.</div></div>"""
    doc("BOARD_H4_map_Supai-Arizona_NPS_185x210mm", F, 185, 210, body)

    # H5 · What came back (checklist) + the Tribe's own words from the settlement press release
    yes = ["151 remaining blood samples", "Lab notebooks and family-tree records", "$700,000 to 41 tribe members", "A formal apology", "No new ASU research with the samples"]
    no = ["23 papers and dissertations, still published", "Copies and data already passed to other researchers"]
    body = f"""<div style="position:absolute;inset:0;background:{SCOUT};color:{SINK};font-family:{MONT}">
      <div style="height:11mm;background:{KHAKI};padding:0 6mm;display:flex;align-items:center;font-family:'League Spartan';font-weight:700;font-size:13pt">WHAT CAME BACK IN 2010</div>
      <div style="position:absolute;left:6mm;top:16mm;width:84mm;font-size:12.5pt;line-height:1.55">
        {''.join(f'<div>☑ {t}</div>' for t in yes)}
        <div style="font-weight:700;font-size:9pt;letter-spacing:1.3pt;text-transform:uppercase;color:{SMUTE};margin-top:3mm">Not returned</div>
        {''.join(f'<div>☐ {t}</div>' for t in no)}
        <div style="font-family:'League Spartan';font-weight:700;font-size:15pt;margin-top:4mm;line-height:1.2">The blood went home.<br>The published papers did not.</div></div>
      <div style="position:absolute;left:93mm;right:6mm;top:15mm;display:flex;flex-direction:column;gap:2mm">
        {clip('pr_head.png', border='#bbb', pad=1)}
        {clip('pr_tilousi.png', border='#bbb', pad=1)}
        {clip('pr_jones.png', border='#bbb', pad=1)}
        <div style="font-size:9.5pt;line-height:1.3;color:{SMUTE};font-weight:600">Joint press release, Havasupai Tribe and Arizona Board of Regents, 21 April 2010 · Reproduction</div></div>
      <div class="credit" style="position:absolute;left:6mm;bottom:4mm">What came back (checklist) · 2010 settlement · Made for this exhibition; quotations from the 2010 press release.</div></div>"""
    doc("BOARD_H5_checklist_What-Came-Back-2010_185x136mm", F, 185, 136, body)
    qr_panel("BOARD_H6_QR-audio_185x58mm", F, "09_What_the_Blood_Was_For.png", 185, 58, bg=SINK, fg="#fdf6e3", accent=KHAKI,
             font=MONT, line1="Listen &amp; see the sources", line2="Audio guide · Story 2 · What the Blood Was For", qr_mm=46)

    # Desk
    tent_card("DESK_H9_tent-card_blood-collection-tube_100x120mm-fold", F, "Blood-collection tube", "Present day · Unused demonstration object",
              "An unused, empty tube; no Havasupai blood, image or genetic information is shown in this exhibition.",
              bg=SCOUT, color=SINK, mcolor=SMUTE, font=MONT, rule=KHAKI)
    OS = F / "original-sources"
    copy_pdf(OS / "ABOR-Havasupai_press-release_2010-04-21.pdf", F / "DESK_H10_press-release_Havasupai-Tribe-and-ABOR_2010-04-21.pdf")
    copy_pdf(OS / "Havasupai-v-ABOR_Ariz-Ct-App_1-CA-CV-07-0454_Joint-Answering-Brief_2007.pdf",
             F / "DESK_H11_court-record_Joint-Answering-Brief_cover-and-pp3-4.pdf", pages=[1, 10, 11])
    webprint("DESK_H12_news_Inside-Higher-Ed_2010-04-21_A4", F, "Arizona Regents Settle Dispute Over Use of Indian Blood",
             "https://www.insidehighered.com/quicktakes/2010/04/22/arizona-regents-settle-dispute-over-use-indian-blood", NEWS / "ihe_2010.png")


# =====================================================================================
# STORY 3 · A SEARCH ENGINE FOR FACES (content-table template)
# =====================================================================================
def asterisk(size, col):
    bars = "".join(f'<rect x="-3.6" y="-19" width="7.2" height="38" rx="3.6" transform="rotate({a})"/>' for a in (0, 45, 90, 135))
    return f'<svg width="{size}mm" height="{size}mm" viewBox="-20 -20 40 40"><g fill="{col}">{bars}</g></svg>'


def face_mesh():
    pts = [[50,12],[34,16],[66,16],[24,28],[76,28],[20,44],[80,44],[22,60],[78,60],[28,74],[72,74],[38,85],[62,85],[50,89],
           [32,38],[42,36],[58,36],[68,38],[34,46],[40,45],[46,46],[54,46],[60,45],[66,46],[50,52],[46,61],[54,61],[50,64],[40,72],[50,70],[60,72],[50,76]]
    tri = [[0,1,2],[1,3,14],[2,4,17],[3,5,14],[4,6,17],[5,7,18],[6,8,23],[7,9,28],[8,10,30],[9,11,28],[10,12,30],[11,13,31],[12,13,31],
           [14,15,19],[15,16,24],[16,17,22],[14,18,19],[17,22,23],[19,20,24],[21,22,24],[20,25,24],[21,26,24],[25,27,24],[26,27,24],[25,28,29],[26,29,30],[28,29,31],[29,30,31],[18,7,28],[23,8,30],[1,14,15],[2,16,17],[0,15,16]]
    lines = "".join(f'<polygon points="{pts[a][0]},{pts[a][1]} {pts[b][0]},{pts[b][1]} {pts[c][0]},{pts[c][1]}" fill="none" stroke="{RUST}" stroke-width=".45" opacity=".7"/>' for a, b, c in tri)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="{FINK}"/>' for x, y in pts)
    return f'<svg viewBox="10 4 80 92" width="100%" height="100%"><ellipse cx="50" cy="50" rx="31" ry="41" fill="#efe1d6"/>{lines}{dots}</svg>'


def build_clearview():
    F = CASE["c"]
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS}">
      <div style="position:absolute;left:0;right:0;top:0;height:52mm;background:{TAN}"></div>
      <div style="position:absolute;left:-5mm;top:-5mm">{asterisk(28, RUST)}</div>
      <div style="position:absolute;right:9mm;top:9mm;width:18mm;height:18mm;background:radial-gradient(circle,#8b4a2b 0 1.7mm,transparent 1.8mm) 0 0/6mm 6mm"></div>
      <div style="position:absolute;left:26mm;right:30mm;top:14mm">
        <div style="font-family:Poppins;font-weight:700;font-size:8pt;color:{FINK}">Section 2 · Story 3</div>
        <div style="font-family:Poppins;font-weight:700;font-size:22pt;line-height:1.08;margin-top:2mm">A Search Engine<br>for Faces</div></div>
      <div style="position:absolute;left:10mm;right:10mm;top:56mm;font-size:8.5pt;color:{RUST};padding-bottom:2mm;border-bottom:.3mm solid {TAN}">Clearview AI · New York, USA · 2017 to today</div>
      <div class="fit" style="position:absolute;left:10mm;right:10mm;top:65mm;bottom:44mm;font-size:21pt;line-height:1.45;overflow:hidden">{paras(CLV,'margin-bottom:.6em')}
        <div style="font-size:.6em;color:{RUST};font-weight:700">Status as of October 2026.</div></div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:36mm;background:{TAN};padding:6mm 10mm;font-family:Poppins;font-weight:700;font-size:13pt;line-height:1.25">Nobody lost a photograph.<br><span style="color:#5b3422">So what, if anything, was taken when the people in them became searchable?</span></div></div>"""
    doc("BOARD_C1_wall-text_A-Search-Engine-for-Faces_210x297mm", F, 210, 297, body)

    # C2 · A face as numbers (illustrative values)
    import random
    rnd = random.Random(4242)
    rows = "".join(f'<div style="display:flex;justify-content:space-between"><span style="color:#7d6a5e">{i+1:03d}</span><span>{"−" if v < 0 else "+"}{abs(v):.4f}</span></div>'
                   for i, v in enumerate(rnd.uniform(-.2, .2) for _ in range(11)))
    rows += '<div style="display:flex;justify-content:space-between"><span style="color:#7d6a5e">⋮ 512</span><span>+0.0731</span></div>'
    bars = "".join(f"""<div style="display:flex;align-items:center;gap:2mm;font-size:11pt;margin-top:2mm"><span style="width:12mm">{y}</span>
        <div style="height:5mm;width:{w*.8:.0f}mm;background:{RUST}"></div><span>{n}</span></div>""" for y, n, w in [("2020", "3 billion+", 4), ("2022", "20 billion", 22), ("2026", "100 billion+", 95)])
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS};padding:8mm 8mm 7mm;display:flex;flex-direction:column">
      <div style="font-family:Poppins;font-weight:700;font-size:8pt;color:{RUST}">Faceprint</div>
      <div style="font-family:Poppins;font-weight:700;font-size:19pt;margin-bottom:3mm">A face as numbers</div>
      <div style="height:105mm">{face_mesh()}</div>
      <div style="text-align:center;color:{RUST};font-size:10pt">▼</div>
      <div style="background:#1e1714;color:#e9dccf;font-family:'DM Sans',monospace;font-size:11pt;line-height:1.45;padding:3mm 6mm;border-radius:1mm">{rows}</div>
      <div style="font-family:Poppins;font-weight:700;font-size:13pt;margin-top:6mm">Images in the database</div>{bars}
      <div style="font-size:10pt;color:#7d6a5e;margin-top:2mm">Images, not people. The 2026 figure is Clearview’s own claim.</div>
      <div style="margin-top:auto">{label("A face as numbers (faceprint)", "Made for this exhibition · Values are illustrative",
            "Canada’s privacy commissioners described each Clearview faceprint as a ‘vector’ of 512 data points.", mcolor=RUST, tsize=12.5, dsize=11)}</div></div>"""
    doc("BOARD_C2_faceprint_A-Face-as-Numbers_155x297mm", F, 155, 297, body)

    # C3 · One face, four places: stills from the exhibition's own video (staged, consenting volunteer)
    posts = [("card1.png", "A. A friend’s post: she is beside the friend", "Public post"), ("card2.png", "B. “Best coffee spots this winter”", "Public post"),
             ("card3.png", "C. Her own post", "Public post"), ("street_c.png", "D. The photo that gets searched", "Not posted anywhere")]
    cells = "".join(f"""<div style="flex:1;display:flex;flex-direction:column;gap:2mm">
        <div style="height:88mm;background:#fff;border:.3mm solid {TAN};display:flex;align-items:center;justify-content:center;overflow:hidden"><img src="{u(A/f)}" style="max-width:100%;max-height:100%;object-fit:contain"></div>
        <div style="font-size:9pt;font-weight:700;letter-spacing:1pt;text-transform:uppercase;color:{RUST}">{tag}</div>
        <div style="font-size:12.5pt;line-height:1.25">{cap}</div></div>""" for f, cap, tag in posts)
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS};padding:5mm 7mm;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font-family:Poppins;font-weight:700;font-size:16pt">One face, four places</div>
        <div style="font-size:10pt;color:{RUST}">Staged photographs · 2026 · Made for this exhibition with a consenting volunteer</div></div>
      <div style="display:flex;gap:4mm;margin-top:3mm">{cells}</div>
      <div style="font-size:11pt;margin-top:auto;color:#5b3422">One volunteer in four settings, each photo shared with a different audience. The same stills appear in the face-search video on the desk.</div></div>"""
    doc("BOARD_C3_photos_One-Face-Four-Places_380x134mm", F, 380, 134, body)

    steps = [("01", "POSTED", "Visible online"), ("02", "COLLECTED", "Copied by Clearview"), ("03", "FACE DATA", "Turned into a faceprint"), ("04", "SEARCHABLE", "Found from a new photo")]
    st = "".join(f"""<div style="flex:1;background:#fff;border-radius:1.5mm;padding:2mm 3.5mm"><div style="font-size:9pt;color:{RUST}">{n}</div>
        <div style="font-family:Poppins;font-weight:700;font-size:16pt;line-height:1.1">{t}</div><div style="font-size:11pt">{d}</div></div>
        {'<div style="font-size:20pt;color:#5b3422">→</div>' if i < 3 else ''}""" for i, (n, t, d) in enumerate(steps))
    body = f"""<div style="position:absolute;inset:0;background:{TAN};color:{FINK};font-family:{DMS};padding:3.5mm 7mm">
      <div style="display:flex;align-items:stretch;gap:3mm;height:30mm">{st}</div>
      <div style="font-size:9pt;margin-top:2mm"><b>Posted → collected → face data → searchable (diagram)</b> · Made for this exhibition · The four steps that turn someone visible online into someone searchable.</div></div>"""
    doc("BOARD_C4_diagram_Posted-to-Searchable_380x52mm", F, 380, 52, body)

    # C5 · Canada's privacy commissioners (real report + news release)
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS};padding:6mm 7mm;display:flex;flex-direction:column">
      <div style="font-family:Poppins;font-weight:700;font-size:8pt;color:{RUST}">Document</div>
      <div style="font-family:Poppins;font-weight:700;font-size:13pt;margin-bottom:3mm">Canada’s privacy commissioners</div>
      <div style="width:80%">{clip('opc_rep_head.png', border='#d8cfc7')}</div>
      <div style="height:3mm"></div>
      {clip('opc_quote.png', border='#d8cfc7')}
      <div style="margin-top:3mm">{label("Canada’s privacy commissioners",
            "2–3 February 2021 · PIPEDA Findings #2021-001 and news release · Office of the Privacy Commissioner of Canada · Extracts printed from priv.gc.ca",
            "The joint investigation by Canada’s federal commissioner and three provincial commissioners found that Clearview’s scraping was mass surveillance and broke Canadian law. Clearview disputed the findings and withdrew from Canada.",
            mcolor=RUST, tsize=12.5, dsize=10.8)}</div>
      <div class="credit" style="margin-top:auto">Source: priv.gc.ca. The full news release is on the desk.</div></div>"""
    doc("BOARD_C5_government-document_Canada-OPC-2021_185x210mm", F, 185, 210, body)

    rulings = [("2021", "Canada", "Mass surveillance; illegal", "Clearview disputed it"), ("2021", "Australia", "Stop collecting; destroy Australians’ data", "Order issued"),
               ("2022", "USA", "Most private companies barred", "Settlement, no fault admitted"), ("2024", "Netherlands", "€30.5 million fine", "Fine issued"),
               ("2025", "EU", "AI Act bans scraping faces to build such databases", "In force"), ("2026", "Clearview", "“More than 100 billion images”", "Still operating")]
    trs = "".join(f'<tr><td><b>{a}</b></td><td><b>{b}</b></td><td>{c}</td><td style="color:{RUST}">{d}</td></tr>' for a, b, c, d in rulings)
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS}">
      <div style="padding:5mm 6mm 2mm;display:flex;justify-content:space-between"><div style="font-family:Poppins;font-weight:700;font-size:16pt">Rulings so far</div>
        <div style="width:12mm;height:4mm;background:radial-gradient(circle,#8b4a2b 0 1.4mm,transparent 1.5mm) 0 0/4.5mm 4mm"></div></div>
      <table style="width:100%;border-collapse:collapse;font-size:11pt;line-height:1.3">
        <tr style="background:{FINK};color:#fff;font-weight:700"><td style="padding:1.5mm 2mm 1.5mm 6mm">Year</td><td>Where</td><td>Decision</td><td>Status</td></tr>
        {trs}</table>
      <style>td{{padding:2.6mm 2mm;border-bottom:.2mm solid #e3d6cc;vertical-align:top}} tr td:first-child{{padding-left:6mm}}</style>
      <div style="padding:4mm 6mm;font-size:11pt;line-height:1.35">Clearview admits no wrongdoing and has not paid several European fines. Status as of October 2026.</div>
      <div class="credit" style="padding:0 6mm">Rulings so far (table) · 2021–2026 · Made for this exhibition. Dutch decision: Autoriteit Persoonsgegevens, 3 Sept. 2024 (on the desk).</div></div>"""
    doc("BOARD_C6_table_Rulings-So-Far_185x146mm", F, 185, 146, body)
    qr_panel("BOARD_C7_QR-audio_185x58mm", F, "10_A_Search_Engine_for_Faces.png", 185, 58, bg="#1e1714", fg="#fbf6f2", accent=TAN,
             font=DMS, line1="Listen &amp; see the sources", line2="Audio guide · Story 3 · A Search Engine for Faces", qr_mm=46)

    # Desk
    object_labels("DESK_C9_object-label_face-search-simulation_200x56mm", F, [("Face search (simulation)",
                  "Video, 32-second loop · Made for this exhibition · Not Clearview software",
                  "A simulation built by the exhibition team, not Clearview software: one new photo finds the same face in three earlier posts.")],
                  bg=FEED, color=FINK, mcolor=RUST, font=DMS, rule=RUST)
    side = lambda kick, big, txt, bg: f"""<div style="flex:1;background:{bg};padding:6mm 8mm"><div style="font-family:Poppins;font-weight:700;font-size:8pt;letter-spacing:1pt;color:{RUST}">{kick}</div>
        <div style="font-family:Poppins;font-weight:700;font-size:17pt;margin:1.5mm 0 2mm">{big}</div><div style="font-size:11.5pt;line-height:1.38">{txt}</div></div>"""
    body = f"""<div style="position:absolute;inset:0;display:flex;font-family:{DMS};color:{FINK}">
      {side("WHAT I DID", "“I posted this publicly”", "Friends, followers and strangers can see the photo. People who already know me can recognise me.", "#fff")}
      <div style="width:24mm;background:{TAN};display:flex;align-items:center;justify-content:center;font-family:Poppins;font-weight:700;font-size:22pt">=?</div>
      {side("WHAT HAPPENED NEXT", "“I agreed to this use”", "The photo is copied, my face becomes a faceprint, and a stranger’s photo of me can lead back to it.", "#f6ebe4")}</div>"""
    doc("DESK_C13_card_Posted-publicly-vs-Agreed_320x66mm", F, 320, 66, body)
    webprint("DESK_C14_government-document_Canada-OPC-news-release_2021-02-03_A4", F,
             "News release: Clearview AI’s unlawful practices represented mass surveillance of Canadians, commissioners say - Office of the Privacy Commissioner of Canada",
             "https://www.priv.gc.ca/en/opc-news/news-and-announcements/2021/nr-c_210203/", NEWS / "opc_newsrelease_2021.png")
    webprint("DESK_C15_government-document_Dutch-DPA-fine_2024-09-03_A4", F,
             "Dutch DPA imposes a fine on Clearview because of illegal data collection for facial recognition | Autoriteit Persoonsgegevens",
             "https://www.autoriteitpersoonsgegevens.nl/en/current/dutch-dpa-imposes-a-fine-on-clearview-because-of-illegal-data-collection-for-facial-recognition",
             NEWS / "dutchdpa_2024.png")


def build_shared():
    voting(CASE["s"], "Section 2", [("Story 1", "Seventy Thousand Seeds", GRN), ("Story 2", "What the Blood Was For", SINK),
                                    ("Story 3", "A Search Engine for Faces", RUST)])


if __name__ == "__main__":
    build_header(); build_rubber(); build_havasupai(); build_clearview(); build_shared()
    print(f"\n{len(BUILT)} PDFs built.")
