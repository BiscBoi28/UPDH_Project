#!/usr/bin/env python3
"""
Builds every printable document for Section 1 ("Who Is the Thief?") of the
Museum of Theft into ../section-1/.

Each item is written as an HTML page sized to its real mounted size (CSS @page
in millimetres) and printed to PDF with headless Google Chrome, so every PDF
prints 1:1 at the size it occupies on the board or the desk.

Run:  python3 build_section1.py
Needs: google-chrome, pdftoppm (poppler). Fonts come from
       ../../Section1_Full_Layout/assets/fonts (the same fonts as the layout mock-up).
"""
import html, json, os, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent                                   # Exhibit_Documents/
REPO = ROOT.parent                                   # UPDH_Project/
OUT = ROOT / "section-1"
ASSETS = HERE / "assets" / "section-1"
FONTS = REPO / "Section1_Full_Layout" / "assets" / "fonts"
ORN = REPO / "Section1_Full_Layout" / "assets" / "ornament_band.png"
QR = REPO.parent / "QR_codes" / "plain"              # Theft/QR_codes/plain (real QR codes)
HTMLDIR = HERE / "html" / "section-1"
HTMLDIR.mkdir(parents=True, exist_ok=True)

CASE = {
    "o": OUT / "01_ordinary-theft",
    "k": OUT / "02_kleptomania-and-class",
    "r": OUT / "03_robbing-the-rich",
    "b": OUT / "04_the-benin-bronzes",
    "h": OUT / "00_section-header",
    "s": OUT / "shared-desk-items",
}
for p in CASE.values():
    p.mkdir(parents=True, exist_ok=True)


def u(p):  # file URL for local assets
    return pathlib.Path(p).resolve().as_uri()


FONT_CSS = f"""
@font-face {{ font-family:"Diplomata SC"; src:url("{u(FONTS/'Diplomata_SC.ttf')}"); }}
@font-face {{ font-family:"Unna"; src:url("{u(FONTS/'Unna.ttf')}"); }}
@font-face {{ font-family:"Unna"; font-style:italic; src:url("{u(FONTS/'Unna_Italics.ttf')}"); }}
@font-face {{ font-family:"League Spartan"; src:url("{u(FONTS/'League_Spartan.ttf')}"); }}
@font-face {{ font-family:"Montserrat"; font-weight:400; src:url("{u(FONTS/'Montserrat.ttf')}"); }}
@font-face {{ font-family:"Montserrat"; font-weight:600; src:url("{u(FONTS/'Montserrat_Semi-Bold.ttf')}"); }}
@font-face {{ font-family:"Montserrat"; font-weight:700; src:url("{u(FONTS/'Montserrat_Bold.ttf')}"); }}
@font-face {{ font-family:"Roboto"; font-weight:400; src:url("{u(FONTS/'Roboto.ttf')}"); }}
@font-face {{ font-family:"Roboto"; font-weight:700; src:url("{u(FONTS/'Roboto_Bold.ttf')}"); }}
@font-face {{ font-family:"Noticia Text"; src:url("{u(FONTS/'Noticia_Text.ttf')}"); }}
@font-face {{ font-family:"DM Sans"; font-weight:400; src:url("{u(FONTS/'DM_Sans.ttf')}"); }}
@font-face {{ font-family:"DM Sans"; font-weight:700; src:url("{u(FONTS/'DM_Sans_Bold.ttf')}"); }}
"""

BASE_CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
html, body { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.page { position:relative; overflow:hidden; page-break-after:always; break-after:page; }
.page:last-child { page-break-after:auto; break-after:auto; }
img { display:block; }
.chips { display:flex; gap:3mm; align-items:center; flex-wrap:wrap; }
.chip { font-family:Montserrat; font-weight:700; font-size:11pt; letter-spacing:.4pt; padding:1.6mm 4mm; border-radius:20mm; border:.6mm solid currentColor; line-height:1; }
.chip.yes { color:#2f6b3a; background:#e6f0e2; }
.chip.no  { color:#b3261e; background:#f8e2df; }
.verdict { font-family:Montserrat; font-weight:700; font-size:13pt; margin-left:2mm; }
.credit { font-family:"DM Sans",Arial,sans-serif; font-size:7pt; color:#555; line-height:1.3; }
"""

# Shrinks the text inside every .fit box until it no longer overflows.
FIT_JS = """
<script>
document.fonts.ready.then(()=>{
  document.querySelectorAll('.fit').forEach(el=>{
    let fs=parseFloat(getComputedStyle(el).fontSize), n=0;
    while((el.scrollHeight>el.clientHeight+1 || el.scrollWidth>el.clientWidth+1) && n<80){ fs*=0.98; el.style.fontSize=fs+'px'; n++; }
  });
  document.body.setAttribute('data-ready','1');
});
</script>
"""

BUILT = []


def doc(name, folder, w, h, body, css="", pages=None):
    """Write HTML and print it to <folder>/<name>.pdf at w x h millimetres."""
    if pages is None:
        pages = [body]
    inner = "".join(f'<div class="page" style="width:{w}mm;height:{h}mm">{p}</div>' for p in pages)
    src = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(name)}</title>
<style>@page {{ size:{w}mm {h}mm; margin:0; }} {FONT_CSS} {BASE_CSS} {css}</style></head>
<body>{inner}{FIT_JS}</body></html>"""
    hp = HTMLDIR / f"{name}.html"
    hp.write_text(src, encoding="utf-8")
    pdf = folder / f"{name}.pdf"
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", f"--user-data-dir={prof}",
                        "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        "--allow-file-access-from-files", f"--print-to-pdf={pdf}", hp.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    BUILT.append(pdf)
    print("built", pdf.relative_to(ROOT))
    return pdf


def pdf_to_png(pdf, png_stem, dpi=110):
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", "-f", "1", "-l", "1", str(pdf), str(png_stem)], check=True)
    return pathlib.Path(str(png_stem) + ".png")


def conditions(o, l, w, verdict, color="#222"):
    c = lambda t, ok: f'<span class="chip {"yes" if ok else "no"}">{t} {"✓" if ok else "✗"}</span>'
    return f'<div class="chips">{c("OWNER",o)}{c("LOSS",l)}{c("LAW",w)}<span class="verdict" style="color:{color}">{verdict}</span></div>'


def paras(ps, style=""):
    return "".join(f'<p style="{style}">{p}</p>' for p in ps)


def qr_strip(name, folder, qr_file, bg, fg, accent, font, line1, line2):
    body = f"""<div style="position:absolute;inset:0;background:{bg};color:{fg};display:flex;align-items:center;gap:6mm;padding:3.5mm 6mm;font-family:{font}">
      <div style="background:#fff;padding:1.5mm;flex:none"><img src="{u(QR/qr_file)}" style="width:36mm;height:36mm"></div>
      <div style="font-size:17pt;line-height:1.3">{line1}<br><span style="color:{accent};font-size:14pt">{line2}</span></div></div>"""
    return doc(name, folder, 285, 46, body)


# =====================================================================================
# TEXT (Phase 4 text, as on the layout mock-up; facts re-checked against sources)
# =====================================================================================
INTRO = [
    "Most people can picture a thief: someone who takes what belongs to another, without permission. The thief is usually the easiest person in the story to identify. The label seems to follow from the act. This section tests that idea through four cases.",
    "Each case is checked against three conditions: an owner, a loss, and a law that names the taking as a crime. In an ordinary theft, all three are present, and so is the thief. Each case that follows keeps the taking in plain sight and changes something else.",
    "Two women take the same goods from the same counter, but only one is called a thief. An outlaw robs travellers at knifepoint, and centuries of retelling turn him into a hero. A palace is looted, and its treasures pass through so many lawful hands that no single person seems to have taken them.",
    "The taking stays visible throughout. What changes is who the taker is, who the victim is, where the goods end up, and how much time has passed. The label ‘thief’ turns out to depend on more than the act.",
]
ORD = [
    "On a crowded street, a hand slips into a pocket and leaves with a wallet. The owner notices only later. A complaint is filed, and if the pickpocket is caught, the law takes its course. Cash, cards and jewellery are taken the same way.",
    "In India, that law is Section 303 of the Bharatiya Nyaya Sanhita, 2023. It defines theft as dishonestly taking someone’s movable property out of their possession, without consent. The pickpocket’s act fits every part of that definition.",
    "Owner, loss, law: all three are present, and the thief is obvious. Note the word <i>movable</i>. Under this section, land cannot be stolen at all — a limit Section 3 of this exhibition returns to.",
]
KLE = [
    "From the 1870s, large department stores spread through American and British cities. Goods sat on open counters, and shoppers could handle them freely. Shoplifting rose with them. Many of those caught were middle-class women, the stores’ best customers, taking things they could easily afford. Doctors offered an explanation. Since the early nineteenth century, they had described ‘kleptomania’, an urge to steal. Applied to these women, it turned a crime into an illness. Stores, unwilling to lose respectable customers, often settled such cases quietly.",
    "The diagnosis did not reach everyone. In New York in 1882, Ellen Sardy was caught in a Sixth Avenue department store with three pairs of hosiery and five pieces of silk. Her lawyer admitted the theft and asked for clemency because she had been ‘of weak mind’. The court accepted it and she went free. Historian Elaine Abelson, who recovered the case, writes that only middle-class women seemed to suffer from kleptomania: ‘stealing by members of other classes was simple theft’.",
    "Owner and loss are identical in both cases, and so is the law. Only the person differs. The act did not decide the label; class did.",
]
ROB = [
    "Robin Hood is first mentioned in the 1370s, when the poem <i>Piers Plowman</i> refers to ‘rhymes of Robin Hood’. The poem says nothing about who he was or what he did; it tells us only that such rhymes already circulated.",
    "The earliest surviving ballads, from about 1450, describe an outlaw living in the forest with a band of followers, in conflict with a corrupt sheriff. He stops wealthy travellers on the road and takes what they carry at the point of a weapon. The ballads are frank about the violence, and they are also frank about what they do not say: they do not describe him giving to the poor. That line is first set down plainly by John Stow in 1592, roughly a century after <i>A Gest of Robyn Hode</i>, and it is the version that has lasted.",
    "Owner, loss and law are all present. The travellers owned what they carried, they lost it, and Robin lived outside the law’s protection as a declared outlaw. Nothing is missing. What changed was not the robbery but the story told about it afterwards — and each retelling gave the robberies a better reason.",
]
BEN = [
    "In 1897, a British punitive expedition captured Benin City, burned the royal palace and removed thousands of brass plaques, ivories and commemorative heads. Many were auctioned in London to defray the cost of the expedition itself. Others entered Western museums over the following decades through purchase, donation and transfer. These were not currency or raw material: the plaques were the palace’s own record of its dynasty, an archive kept in place.",
    "Owner and loss are not in doubt. What is missing is the third condition. Each transfer was lawful where it took place, and every person in the chain can point to someone earlier. With no act the law named as a crime, the chain has no obvious thief — only a sequence of people who each acted correctly, and a benefit that passed down the line with the objects.",
    "The question has since moved from who took the objects to who holds them now. In 2022 the Smithsonian transferred ownership of 29 objects to Nigeria’s National Commission for Museums and Monuments. In 2023 Nigeria’s outgoing president declared the Oba of Benin the owner of returned bronzes, and who should hold, keep and display them within Nigeria remains disputed. Returning an object settles ownership. It does not settle who is answerable for how it left.",
]


# Common wall-text panel (285 x 260 mm), one per case
def wall_panel(name, folder, *, header_html, sub, body_ps, cond_html, bg, color, font, body_pt, rule):
    body = f"""<div style="position:absolute;inset:0;background:{bg};color:{color};font-family:{font}">
      {header_html}
      <div style="position:absolute;left:14mm;right:14mm;top:58mm;bottom:28mm;display:flex;flex-direction:column">
        <div style="font-size:12.5pt;font-style:italic;opacity:.85;padding-bottom:3mm;border-bottom:.4mm solid {rule};margin-bottom:5mm">{sub}</div>
        <div class="fit" style="flex:1;font-size:{body_pt}pt;line-height:1.42;overflow:hidden">{paras(body_ps,'margin-bottom:.55em')}</div>
      </div>
      <div style="position:absolute;left:14mm;right:14mm;bottom:9mm;border-top:.5mm solid {rule};padding-top:3.5mm">{cond_html}</div>
    </div>"""
    return doc(name, folder, 285, 260, body)


def label(title, meta, desc, *, tcolor="#222", mcolor="#7a4e26", tsize=12, dsize=10.5, font="inherit"):
    return f"""<div style="font-family:{font}"><div style="font-weight:700;font-size:{tsize}pt;line-height:1.2">{title}</div>
      <div style="font-size:{tsize-3}pt;font-style:italic;color:{mcolor};margin:1mm 0 1.5mm">{meta}</div>
      <div style="font-size:{dsize}pt;line-height:1.35;color:{tcolor}">{desc}</div></div>"""


# =====================================================================================
# 00 · SECTION HEADER  (118 x 9 cm strip across the top of the board)
# =====================================================================================
def build_header():
    body = f"""<div style="position:absolute;inset:0;background:#1f262e;color:#efe6d2;padding:7mm 9mm;display:flex;gap:11mm;font-family:'DM Sans',Arial,sans-serif">
      <div style="width:250mm;flex:none">
        <div style="font-family:Montserrat;font-weight:600;font-size:12pt;letter-spacing:2.4pt;text-transform:uppercase;color:#c9a36a">Section 1</div>
        <div style="font-family:Georgia,'Noticia Text',serif;font-size:50pt;line-height:1.05;margin:1.5mm 0 2mm">Who Is the Thief?</div>
        <div style="font-size:14pt;color:#c9b998">Four cases · owner, loss, law</div></div>
      <div class="fit" style="flex:1;column-count:3;column-gap:11mm;font-size:30pt;line-height:1.38;color:#e9e0cc;height:76mm;overflow:hidden">{paras(INTRO,'margin-bottom:.45em')}</div>
      <div style="width:46mm;flex:none;text-align:center;font-size:10pt;color:#c9b998"><div style="background:#fff;padding:2mm"><img src="{u(QR/'02_Who_Is_the_Thief.png')}" style="width:42mm;height:42mm"></div><div style="margin-top:2mm">Audio guide · Section 1<br>Scan to listen</div></div>
    </div>"""
    doc("BOARD_H_section-header_Who-Is-the-Thief_1180x90mm", CASE["h"], 1180, 90, body)


# =====================================================================================
# CASE 1 · ORDINARY THEFT
# =====================================================================================
def build_ordinary():
    F = CASE["o"]
    hdr = """<div style="position:absolute;left:0;right:0;top:0;height:46mm;display:flex">
        <div style="width:46mm;background:#1d3b6a;color:#fff;display:flex;align-items:center;justify-content:center;font-family:'League Spartan';font-weight:700;font-size:64pt">1</div>
        <div style="flex:1;padding:9mm 12mm 0;border-bottom:1mm solid #1d3b6a">
          <div style="font-family:Montserrat;font-weight:700;font-size:10pt;letter-spacing:2pt;text-transform:uppercase;color:#1d3b6a">Section 1 · Case 1</div>
          <div style="font-family:'League Spartan';font-weight:700;font-size:40pt;line-height:1.05;margin-top:2mm">ORDINARY THEFT</div></div></div>"""
    wall_panel("BOARD_O1_wall-text_Ordinary-Theft_285x260mm", F, header_html=hdr,
               sub="A wallet, taken on a crowded street · Present day", body_ps=ORD,
               cond_html=conditions(True, True, True, "→ Thief: obvious", "#1d3b6a"),
               bg="#fbfbf8", color="#1e2430", font="Roboto,Arial,sans-serif", body_pt=30, rule="#1d3b6a")

    # O2 · Government document: clipped from the Gazette of India
    # yellow marks over the two occurrences of "movable" (positions from pdftotext -bbox, see SOURCES.md)
    hl = lambda l, t, w, h: f'<div style="position:absolute;left:{l}%;top:{t}%;width:{w}%;height:{h}%;background:rgba(253,224,71,.55);mix-blend-mode:multiply"></div>'
    body = f"""<div style="position:absolute;inset:0;background:#fbfbf8;padding:6mm 7mm;font-family:Roboto,Arial,sans-serif;color:#1e2430;display:flex;gap:6mm">
      <div style="width:52mm;flex:none;display:flex;flex-direction:column;gap:3mm">
        <div style="border:.3mm solid #c9cfd9;background:#fff;padding:1.5mm"><img src="{u(ASSETS/'bns_masthead.png')}" style="width:100%"></div>
        <div style="border:.3mm solid #c9cfd9;background:#fff;padding:1.5mm"><img src="{u(ASSETS/'bns_title.png')}" style="width:100%"></div>
        <div style="font-family:Montserrat;font-weight:700;font-size:7pt;letter-spacing:1pt;color:#1d3b6a;text-transform:uppercase">The Gazette of India · Extraordinary · No. 53 · 25 Dec 2023 · page 1</div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column">
        <div style="font-family:Montserrat;font-weight:700;font-size:8.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:#1d3b6a">Government document · clipped from the official Gazette, page 78</div>
        <div style="position:relative;margin:2mm 0 3mm;border:.3mm solid #c9cfd9;border-left:2mm solid #1d3b6a;background:#fff">
          <div style="position:relative"><img src="{u(ASSETS/'bns_s303.png')}" style="width:100%">{hl(62.5,27.3,7.2,9.8)}{hl(79.0,54.2,7.2,9.8)}</div></div>
        {label("Section 303, Bharatiya Nyaya Sanhita, 2023",
               "2023 · The Gazette of India, Extraordinary, Part II — Section 1 · Clipped from the official Gazette",
               "India’s criminal code defines theft as dishonestly taking <b>movable</b> property from someone’s possession without consent. Explanation 1 spells out the limit: a thing attached to the earth ‘is not the subject of theft’. Under this section, land cannot be stolen.",
               mcolor="#1d3b6a", tsize=12, dsize=10)}
      </div></div>"""
    doc("BOARD_O2_government-document_BNS-2023-s303_Gazette-of-India_285x126mm", F, 285, 126, body)

    # O3 · Incident report: clips from a real, police-published FIR (Nagpur Railway Police, FIR 0038/2026)
    clip = lambda f: f'<div style="background:#fff;border:.3mm solid #c9cfd9;padding:1.5mm;box-shadow:.4mm .6mm 1.4mm rgba(0,0,0,.18)"><img src="{u(ASSETS/f)}" style="width:100%"></div>'
    body = f"""<div style="position:absolute;inset:0;background:#fbfbf8;padding:6mm 7mm;font-family:Roboto,Arial,sans-serif;color:#1e2430;display:flex;gap:6mm">
      <div style="width:136mm;flex:none;display:flex;flex-direction:column;gap:4mm">
        <div style="font-family:Montserrat;font-weight:700;font-size:8.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:#1d3b6a">Incident report · First Information Report, page 1</div>
        {clip('fir_p1_head.png')}
        {label("First Information Report No. 0038/2026","P.S. Gondia (Railway), Nagpur Railway Police District · 1 April 2026 · Published by Nagpur Railway Police · Reproduction",
               "Filed at a railway police station in Maharashtra. A traveller fell asleep on a bench opposite the booking office at Gondia station; when he woke, his phone was gone from his trouser pocket, and so was his purse with his ID cards and ₹1,500. Accused: ‘unknown’. Section: BNS 303(2), theft. Every later case in this section is checked against the same three lines: owner, loss, law.",
               mcolor="#1d3b6a", tsize=14, dsize=12)}
        <div style="margin-top:auto;border-top:.4mm dashed #1d3b6a;padding-top:3mm">{conditions(True, True, True, "→ Thief: obvious", "#1d3b6a")}
          <div style="font-size:10pt;color:#555;margin-top:2.5mm">The full six-page FIR, with an English translation of the complaint, is on the desk below.</div></div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:3mm">
        <div style="font-family:Montserrat;font-weight:700;font-size:8.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:#1d3b6a">Page 3 · Item 9: property stolen</div>
        {clip('fir_p3_property.png')}
        <div style="font-size:9.5pt;line-height:1.35;color:#333">Mobile phone ₹17,000 · PAN card · Aadhaar card · ATM card · licence · cash ₹1,500 · <b>total ₹18,500</b></div>
      </div></div>"""
    doc("BOARD_O3_incident-report_FIR-0038-2026_clips_285x194mm", F, 285, 194, body)

    # O4 · How to read this section
    body = f"""<div style="position:absolute;inset:0;background:#fbfbf8;border-top:2.5mm solid #1d3b6a;padding:5mm 8mm;font-family:Roboto,Arial,sans-serif;color:#1e2430">
      <div style="font-family:'League Spartan';font-weight:700;font-size:15pt;margin-bottom:2.5mm">HOW TO READ THIS SECTION</div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:3mm 5mm;align-items:center;font-size:17pt">
        <span class="chip yes">OWNER ✓</span><span>Someone the thing belongs to</span>
        <span class="chip yes">LOSS ✓</span><span>They no longer have it</span>
        <span class="chip yes">LAW ✓</span><span>A law names the taking as a crime</span></div>
      <div style="font-size:11pt;margin-top:2.5mm;color:#555">Each case has this strip. Watch which one changes.</div></div>"""
    doc("BOARD_O4_how-to-read-this-section_285x84mm", F, 285, 84, body)

    qr_strip("BOARD_O5_QR-audio-strip_285x46mm", F, "03_A_Wallet_on_a_Crowded_Street.png", "#1d3b6a", "#fff", "#c8d6ee",
             "Roboto,Arial,sans-serif", "Listen &amp; see the sources", "Audio guide · Case 1 · A Wallet on a Crowded Street")

    import shutil
    OS = F / "original-sources"
    shutil.copy(OS / "FIR_0038-2026_PS-Gondia-Railway_Nagpur-Railway-Police_BNS-303(2).pdf",
                F / "DESK_O6_incident-report_FIR-0038-2026_Gondia-Railway-PS_6pp_A4.pdf")
    BUILT.append(F / "DESK_O6_incident-report_FIR-0038-2026_Gondia-Railway-PS_6pp_A4.pdf")
    tr = [
        "On 31/03/2026 the complainant came to Gondia railway station to travel from Balaghat to Raipur. He was going to Raipur with his friends, and because they were arriving on another train he waited for them.",
        "He fell asleep on the bench opposite the main booking office at Gondia station, sleeping deeply after his journey. When he woke a few hours later, his Realme mobile phone (Jio SIM, worth ₹17,000), kept in his trouser pocket, was gone — and so was his black money purse, holding his Aadhaar card, PAN card, voter card, licence and ₹1,500 in cash. Property worth ₹18,500 in all.",
        "He asked the people around him, but the phone and the purse were not found. Taking advantage of his sleep, some unknown thief had stolen them.",
        "He came to the police station and gave a written complaint. On the orders of the officer in charge, Crime No. 38/2026 was registered under Section 303(2) of the Bharatiya Nyaya Sanhita, and the investigation was handed to PSI Meshram.",
    ]
    body = f"""<div style="position:absolute;inset:0;background:#fbfbf8;padding:11mm 12mm;font-family:Roboto,Arial,sans-serif;color:#1e2430">
      <div style="font-family:Montserrat;font-weight:700;font-size:8.5pt;letter-spacing:1.3pt;text-transform:uppercase;color:#1d3b6a">English translation · FIR 0038/2026 · Item 12, ‘First Information contents’</div>
      <div style="font-family:'League Spartan';font-weight:700;font-size:20pt;margin:3mm 0 4mm;line-height:1.1">What the complainant told the police</div>
      <div style="font-size:11.5pt;line-height:1.5">{paras(tr,'margin-bottom:.7em')}</div>
      <div class="credit" style="position:absolute;left:12mm;right:12mm;bottom:9mm;border-top:.2mm solid #bbb;padding-top:1.5mm">Translated from the Marathi for this exhibition. Source: FIR No. 0038/2026, P.S. Gondia (Railway), published by Nagpur Railway Police at nagpurrailwaypolice.gov.in.</div></div>"""
    doc("DESK_O6b_FIR-0038-2026_English-translation_A5", F, 148, 210, body)
    shutil.copy(OS / "Gazette-of-India_2023-12-25_BNS-2023_pages-1-78-79-102.pdf",
                F / "DESK_O9_government-document_Gazette-of-India_BNS-2023_flip-through_pp1-78-79-102_A4.pdf")
    BUILT.append(F / "DESK_O9_government-document_Gazette-of-India_BNS-2023_flip-through_pp1-78-79-102_A4.pdf")

    body = f"""<div style="position:absolute;inset:0;background:#fbfbf8;border-top:2.5mm solid #1d3b6a;padding:5mm 7mm;font-family:Roboto,Arial,sans-serif;color:#1e2430">
      {label("Wallet, cash, cards and jewellery","Present day · Props","Everyday objects of the kind taken in street theft. They are here to fix the familiar case in mind before the rest of the exhibition takes it apart. The First Information Report beside them lists the same kinds of things: a phone, a purse, ID cards and cash.", mcolor="#1d3b6a", tsize=14, dsize=11.5)}</div>"""
    doc("DESK_O7_object-label_props_200x56mm", F, 200, 56, body)
    body = "".join(f"""<div style="position:absolute;left:{(i%2)*100+10}mm;top:{(i//2)*60+10}mm;width:80mm;height:45mm;border:.3mm dashed #999">
        <div style="position:absolute;inset:0;bottom:50%;background:#f5c518;border-bottom:.3mm dashed #8a6d00;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:700;font-size:40pt;color:#1e2430;transform:rotate(180deg)">{i+1}</div>
        <div style="position:absolute;inset:0;top:50%;background:#f5c518;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:700;font-size:40pt;color:#1e2430">{i+1}</div></div>""" for i in range(4))
    body += '<div class="credit" style="position:absolute;left:10mm;bottom:8mm">Evidence number tents 1–4 · cut along the dashed lines, fold along the middle · 1 wallet · 2 cash · 3 cards · 4 jewellery</div>'
    doc("DESK_O8_evidence-number-tents_1-4_A4", F, 210, 297, body)


# =====================================================================================
# CASE 2 · KLEPTOMANIA AND CLASS
# =====================================================================================
VIC_BG = "linear-gradient(160deg,#f6efdf 0%,#f1e8d4 60%,#ebdfc6 100%)"


def build_klepto():
    F = CASE["k"]
    hdr = f"""<div style="position:absolute;left:12mm;right:12mm;top:9mm">
        <div style="height:9mm;background:url('{u(ORN)}') repeat-x center/auto 100%;margin-bottom:4mm"></div>
        <div style="font-size:11pt;letter-spacing:3pt;text-transform:uppercase;color:#8a5a2e">Section 1 · Case 2</div>
        <div style="font-family:'Diplomata SC',Georgia,serif;color:#2f4a3a;font-size:24pt;line-height:1.2;margin-top:2mm">Kleptomania and Class</div></div>
      <div style="position:absolute;inset:4.5mm;border:.5mm solid #2f4a3a;pointer-events:none"></div>"""
    wall_panel("BOARD_K1_wall-text_Kleptomania-and-Class_285x260mm", F, header_html=hdr,
               sub="Two shoplifters, one counter, two verdicts · Department stores in the United States and Britain, 1870s–1900s",
               body_ps=KLE, cond_html=conditions(True, True, True, "→ Thief: depends on who you are", "#2f4a3a"),
               bg=VIC_BG, color="#2b2a26", font="Unna,Georgia,serif", body_pt=30, rule="#2f4a3a")

    # K2 · Same goods, two verdicts (comparison, now with a real court record on the right)
    card = lambda kick, name, txt, verdict, vcol, outcome: f"""<div style="flex:1;background:#fbf8f0;border:.4mm solid #c08a4f;padding:4mm 5mm;position:relative">
        <div style="font-size:9pt;letter-spacing:2pt;text-transform:uppercase;color:#8a5a2e">{kick}</div>
        <div style="font-size:22pt;font-weight:700;margin:1mm 0 2mm;line-height:1.15">{name}</div>
        <div style="font-size:16pt;line-height:1.38">{txt}</div>
        <div style="position:absolute;left:5mm;right:5mm;bottom:4mm;text-align:center"><div style="font-family:'Diplomata SC',Georgia,serif;font-size:15pt;color:{vcol}">{verdict}</div><div style="font-size:12pt">{outcome}</div></div></div>"""
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};padding:6mm 7mm;font-family:Unna,Georgia,serif;color:#2b2a26;display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:.4mm solid #2f4a3a;padding-bottom:1.5mm">
        <div style="font-family:'Diplomata SC',Georgia,serif;color:#2f4a3a;font-size:14pt">Same goods · Two verdicts</div><div style="font-size:9pt;letter-spacing:2pt;text-transform:uppercase;color:#8a5a2e">Comparison</div></div>
      <div style="display:flex;gap:5mm;margin-top:4mm;flex:1">
        {card("New York · January 1882","Ellen Sardy","Caught in Simpson, Crawford &amp; Simpson’s Sixth Avenue store with three pairs of stockings and five pieces of silk. Her lawyer admitted the theft and pleaded that she had been ‘of weak mind’.","Kleptomania","#2f6b3a","She went free.")}
        {card("London · May 1895","Hannah Wilson &amp; Ann Hanstead","Caught at a City silk warehouse with eighty-six yards of silk rolled under a skirt. Wilson told the court she was ‘a respectable woman, of Hackney’. No doctor spoke for them; both had a previous conviction.","Theft","#b3261e","Guilty. Three years’ penal servitude.")}
      </div>
      <div style="font-size:12pt;font-style:italic;margin-top:3mm;color:#2f4a3a">A Paris newspaper of the period suggested defining a thief as ‘a kind of kleptomaniac, but of the lower social class’ — and a kleptomaniac as ‘a kind of thief, but of the better class’.</div>
      <div style="font-size:9pt;margin-top:2mm"><b>Two verdicts (comparison)</b> · <i style="color:#8a5a2e">Made for this exhibition · Based on Elaine S. Abelson, ‘The Invention of Kleptomania’, <i>Signs</i> 15:1 (1989), citing the <i>New York Times</i>, 18 Jan 1882; and the Proceedings of the Old Bailey, trial t18950520-454</i></div>
    </div>"""
    doc("BOARD_K2_two-verdicts-comparison_285x170mm", F, 285, 170, body)

    # K3 · Journal of Mental Science, 1862 (real page, reproduction)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};padding:5mm;font-family:Unna,Georgia,serif;color:#2b2a26;display:flex;flex-direction:column">
      <div style="background:#fbf8f0;border:.3mm solid #bbb;padding:2mm"><img src="{u(ASSETS/'jms_p262_article.png')}" style="width:100%"></div>
      <div style="margin-top:3mm">{label("‘Kleptomania’, <i>The Journal of Mental Science</i>","July 1862 · Vol. 8, pp. 262–275 · British psychiatric journal · Reproduction of page 262",
            "The article opens with ‘the injudicious defence of two lady thieves’ on the plea of kleptomania. Writing like this gave families and courts a medical account of shoplifting to set against a criminal one. The full article is on the desk.",
            mcolor="#8a5a2e", tsize=12.5, dsize=10.5)}</div>
      <div class="credit" style="margin-top:auto">Scan: Wellcome Library / Internet Archive (public domain).</div></div>"""
    doc("BOARD_K3_Journal-of-Mental-Science_1862_Kleptomania_139x250mm", F, 139, 250, body)

    # K4 · Court records: two trials at the Old Bailey (fills the "authentic court record" slot)
    img = lambda f, w="100%": f'<div style="background:#fff;border:.3mm solid #bbb;padding:1mm"><img src="{u(ASSETS/f)}" style="width:{w}"></div>'
    tag = lambda t, c: f'<div style="font-family:\'Diplomata SC\',Georgia,serif;font-size:10pt;color:{c};margin:2mm 0 1mm">{t}</div>'
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};padding:5mm;font-family:Unna,Georgia,serif;color:#2b2a26;display:flex;flex-direction:column">
      <div style="font-family:'Diplomata SC',Georgia,serif;color:#2f4a3a;font-size:11pt;margin-bottom:1mm">Two trials at the Old Bailey</div>
      {tag("1885 · Whiteley’s, Westbourne Grove","#2f6b3a")}
      {img('ob_ryan_head.png')}
      <div style="font-size:8.5pt;text-align:center;margin:.5mm 0">· · ·</div>
      {img('ob_ryan_verdict.png')}
      {tag("1895 · De Selincourt’s silk warehouse","#b3261e")}
      {img('ob_wilson_head.png')}
      <div style="font-size:8.5pt;text-align:center;margin:.5mm 0">· · ·</div>
      {img('ob_wilson_respectable.png')}
      <div style="font-size:8.5pt;text-align:center;margin:.5mm 0">· · ·</div>
      {img('ob_wilson_verdict.png')}
      <div style="margin-top:3mm">{label("Proceedings of the Central Criminal Court, London","September 1885 and May 1895 · Printed court record · Reproduction",
            "Georgina Ryan, a long-standing Whiteley’s customer who banked at the store, was defended by a Queen’s Counsel and ‘received an excellent character’: not guilty. Wilson and Hanstead, with a past conviction: three years.",
            mcolor="#8a5a2e", tsize=10.5, dsize=9)}</div>
      <div class="credit" style="margin-top:auto">Images: Old Bailey Proceedings Online (oldbaileyonline.org), t18850914-845 and t18950520-454. Non-commercial use.</div></div>"""
    doc("BOARD_K4_court-records_Old-Bailey-1885-1895_139x250mm", F, 139, 250, body)

    qr_strip("BOARD_K5_QR-audio-strip_285x46mm", F, "04_Two_Shoplifters_One_Counter.png", "#2f4a3a", "#f1e8d4", "#e2b98a",
             "Unna,Georgia,serif", "Listen &amp; see the sources", "Audio guide · Case 2 · Two Shoplifters, One Counter")

    # Desk: two luggage-style verdict tags + object label
    tagcard = lambda x, verdict, sub, col: f"""<div style="position:absolute;left:{x}mm;top:20mm;width:85mm;height:45mm;background:{VIC_BG};border:.4mm solid #8a7a5a;border-left:4mm solid {col};border-radius:2mm 8mm 8mm 2mm;padding:6mm 6mm 0 9mm;font-family:Unna,Georgia,serif;color:#2b2a26">
        <div style="position:absolute;left:5mm;top:19mm;width:5mm;height:5mm;border-radius:50%;border:.5mm solid #8a7a5a;background:#fff"></div>
        <div style="font-size:9pt;letter-spacing:2pt;text-transform:uppercase;color:#8a5a2e;padding-left:6mm">Verdict</div>
        <div style="font-family:'Diplomata SC',Georgia,serif;font-size:12.5pt;letter-spacing:-.2pt;color:{col};padding-left:6mm;margin-top:1.5mm;white-space:nowrap">{verdict}</div>
        <div style="font-size:14pt;padding-left:6mm;margin-top:1mm">{sub}</div></div>"""
    body = tagcard(12, "Kleptomania", "Settled privately", "#2f6b3a") + tagcard(110, "Theft", "Prosecuted", "#b3261e") + \
        '<div class="credit" style="position:absolute;left:12mm;top:72mm">Cut out each tag, punch the hole, tie to its tray with string.</div>'
    doc("DESK_K6_verdict-tags_x2_A4-landscape", F, 210, 100, body)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};padding:4mm 6mm;font-family:Unna,Georgia,serif;color:#2b2a26">
      <div style="height:5mm;background:url('{u(ORN)}') repeat-x center/auto 100%;margin-bottom:2mm"></div>
      {label("Two pieces of silk","Props · Made for this exhibition","The same goods, as in the Ellen Sardy case and the 1895 Old Bailey trial. One taker was called ill; the other, a thief.", mcolor="#8a5a2e", tsize=14, dsize=12)}</div>"""
    doc("DESK_K7_object-label_two-pieces-of-silk_200x56mm", F, 200, 56, body)

    # Desk reading copies: the article pages and the full trial pages
    pg = lambda f, cap: f"""<div style="position:absolute;inset:0;background:#fff;padding:10mm;display:flex;flex-direction:column;align-items:center">
        <img src="{u(f)}" style="max-width:100%;max-height:268mm;object-fit:contain;border:.3mm solid #ccc">
        <div class="credit" style="margin-top:auto">{cap}</div></div>"""
    doc("DESK_K8_reading-copy_Journal-of-Mental-Science_1862_pp262-266_A4", F, 210, 297, None, pages=[
        pg(ASSETS / "jms_p262.png", "‘Kleptomania’, The Journal of Mental Science, vol. 8 (July 1862), p. 262 · Scan: Wellcome Library / Internet Archive · Reproduction"),
        pg(ASSETS / "jms_p266.png", "‘Kleptomania’, The Journal of Mental Science, vol. 8 (July 1862), p. 266 — on ‘that new and peculiar duty of life called shopping’ · Reproduction")])
    OS = F / "original-sources"
    doc("DESK_K9_court-records_Old-Bailey_full-pages_A4", F, 210, 297, None, pages=[
        pg(OS / "OldBailey_t18850914-845_Ryan_188509140068.jpg", "Old Bailey Proceedings, September 1885, p. 588 · Trial of Georgina Louisa Ryan (t18850914-845) · oldbaileyonline.org"),
        pg(OS / "OldBailey_t18850914-845_Ryan_188509140069.jpg", "Old Bailey Proceedings, September 1885, p. 589 · Trial of Georgina Louisa Ryan (t18850914-845)"),
        pg(OS / "OldBailey_t18850914-845_Ryan_188509140070.jpg", "Old Bailey Proceedings, September 1885, p. 590 · ‘The prisoner received an excellent character. NOT GUILTY.’"),
        pg(OS / "OldBailey_t18950520-454_Wilson-Hanstead_189505200015.jpg", "Old Bailey Proceedings, May 1895, p. 637 · Trial of Hannah Wilson and Ann Hanstead (t18950520-454) · oldbaileyonline.org"),
        pg(OS / "OldBailey_t18950520-454_Wilson-Hanstead_189505200016.jpg", "Old Bailey Proceedings, May 1895, p. 638 · ‘GUILTY … Three Years’ Penal Servitude’")])


# =====================================================================================
# CASE 3 · ROBBING THE RICH
# =====================================================================================
JOUR = "#efe4d0"


def build_robin():
    F = CASE["r"]
    hdr = """<div style="position:absolute;left:0;right:0;top:0;height:48mm;background:#dccbb0;padding:8mm 14mm 0">
        <div style="font-family:Montserrat;font-weight:700;font-size:10pt;letter-spacing:2pt;color:#1f3b44">SECTION 1 · CASE 3</div>
        <div style="font-family:'Noticia Text',Georgia,serif;font-size:38pt;color:#1f3b44;line-height:1.1;margin-top:3mm"><i>Robbing</i> the Rich</div></div>"""
    wall_panel("BOARD_RH1_wall-text_Robbing-the-Rich_285x260mm", F, header_html=hdr,
               sub="Robin Hood and six centuries of retelling · England, 1370s to today", body_ps=ROB,
               cond_html=conditions(True, True, True, "→ Thief, retold as hero", "#1f3b44"),
               bg=JOUR, color="#22343a", font="'Noticia Text',Georgia,serif", body_pt=30, rule="#1f3b44")

    steps = [("1370s", "<i>Piers Plowman</i>", "MENTIONED", "#8a8a8a", "‘Rhymes of Robin Hood’ exist. Nothing more."),
             ("c.1450", "<i>Robin Hood and the Monk</i>", "VIOLENT OUTLAW", "#8e3b2e", "His men kill a monk and his page."),
             ("c.1500", "<i>A Gest of Robyn Hode</i>", "HELPS A POOR KNIGHT", "#b07a2a", "Lends money. No ‘rich to poor’."),
             ("1592", "John Stow, <i>Annales</i>", "ROBS THE RICH, SPARES THE POOR", "#2f6b3a", "The line that lasts."),
             ("1922 · 1938", "Fairbanks, Flynn", "WRONGED NOBLEMAN", "#1f3b44", "Fights injustice on screen.")]
    cols = "".join(f"""<div style="flex:1">
        <div style="font-family:Montserrat;font-weight:700;font-size:16pt;color:#1f3b44">{s[0]}</div>
        <div style="width:4mm;height:4mm;border-radius:50%;background:#1f3b44;margin:2.2mm 0 2.5mm 1mm;position:relative;z-index:2"></div>
        <div style="font-size:14pt;line-height:1.2;height:13mm">{s[1]}</div>
        <div style="font-family:Montserrat;font-weight:700;font-size:10pt;letter-spacing:.4pt;padding:1.3mm 2.8mm;border-radius:10mm;color:#fff;background:{s[3]};display:inline-block;margin:1.5mm 0 2mm;line-height:1.15">{s[2]}</div>
        <div style="font-size:14.5pt;line-height:1.3">{s[4]}</div></div>""" for s in steps)
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};padding:6mm 7mm;font-family:'Noticia Text',Georgia,serif;color:#22343a">
      <div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font-size:18pt;font-weight:700">Each retelling gave him a better reason</div>
        <div style="font-family:Montserrat;font-weight:700;font-size:8pt;letter-spacing:1.5pt;color:#8a6a3a">TIMELINE</div></div>
      <div style="position:relative;margin-top:5mm;display:flex;gap:4mm">
        <div style="position:absolute;left:0;right:0;top:12mm;height:.8mm;background:#1f3b44"></div>{cols}</div></div>"""
    doc("BOARD_RH2_timeline_retellings_285x116mm", F, 285, 116, body)

    ext = lambda imgs, title, meta, desc, fl=1: f"""<div style="flex:{fl};display:flex;flex-direction:column;min-width:0">
        <div style="height:82mm;background:#fbf6ea;border:.3mm solid #b9a582;padding:1.5mm;display:flex;flex-direction:column;gap:1mm;justify-content:center;overflow:hidden">{imgs}</div>
        <div style="margin-top:2.5mm">{label(title, meta, desc, mcolor="#8a6a3a", tsize=10.5, dsize=9)}</div></div>"""
    im = lambda f, extra="": f'<img src="{u(ASSETS/f)}" style="width:100%;{extra}">'
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};padding:5mm 6mm;font-family:'Noticia Text',Georgia,serif;color:#22343a;display:flex;gap:4mm">
      {ext(im('child_monk.png','max-height:80mm;object-fit:contain'), "<i>Robin Hood and the Monk</i>",
           "About 1450 · Ballad, stanzas 48–52 · Original: Cambridge University Library MS Ff.5.48 · Text as printed by F. J. Child, 1888",
           "The oldest surviving Robin Hood ballad, and an openly violent one: Little John beheads the monk who betrayed Robin, and Much kills the monk’s young page ‘for ferd lest he wolde tell’.")}
      {ext(im('gest.png','max-height:80mm;object-fit:contain'), "<i>A Gest of Robyn Hode</i>",
           "Printed in Edinburgh by Chepman &amp; Myllar, c.1508 · Opening page · Reproduction; original in the National Library of Scotland",
           "The longest early ballad: ‘Lythe and listin, gentilmen…’. Robin helps a poor knight with a loan, but never robs the rich to give to the poor.")}
      {ext(im('stow_head.png')+im('stow_passage.png'), "John Stow, <i>The Annales of England</i>",
           "London, 1592 · Page 227 · Reproduction from the Early English Books scan",
           "‘…poore mens goodes hee spared, aboundantly releeuing them with that, which by thefte hee gote from Abbeyes and the houses of riche Carles.’ The best-known part of the story is the latest addition.", 1.5)}
    </div>"""
    doc("BOARD_RH3_ballad-and-chronicle-extracts_285x156mm", F, 285, 156, body)

    body = f"""<div style="position:absolute;inset:0;background:{JOUR};padding:5mm 6mm;font-family:'Noticia Text',Georgia,serif;color:#22343a;display:flex;gap:5mm">
      <div style="flex:none;width:78mm;height:123mm;background:#fbf6ea;padding:2mm;box-shadow:0 .5mm 1.5mm rgba(0,0,0,.35)"><img src="{u(ASSETS/'poster1922_art.jpg')}" style="width:74mm;height:119mm;object-fit:cover"></div>
      <div style="flex:none;width:78mm;height:123mm;background:#fbf6ea;padding:2mm;box-shadow:0 .5mm 1.5mm rgba(0,0,0,.35)"><img src="{u(ASSETS/'poster1938_art.jpg')}" style="width:74mm;height:119mm;object-fit:cover"></div>
      <div style="flex:1;padding-top:4mm;display:flex;flex-direction:column">{label("Robin Hood on screen","1922 and 1938 · Film posters · Reproductions",
            "Posters for the Douglas Fairbanks (1922) and Errol Flynn (1938) films. In both, Robin is a wronged nobleman fighting injustice rather than an outlaw robbing travellers at knifepoint.",
            mcolor="#8a6a3a", tsize=13, dsize=11)}
        <div class="credit" style="margin-top:auto">Posters: United Artists (1922), Warner Bros. (1938). Public domain; via Wikimedia Commons.</div></div></div>"""
    doc("BOARD_RH4_film-posters_1922-1938_285x133mm", F, 285, 133, body)

    qr_strip("BOARD_RH5_QR-audio-strip_285x46mm", F, "05_Robbing_the_Rich.png", "#1f3b44", "#efe4d0", "#dccbb0",
             "'Noticia Text',Georgia,serif", "Hear the ballads &amp; see the sources", "Audio guide · Case 3 · Robbing the Rich")

    body = f"""<div style="position:absolute;inset:0;background:{JOUR};padding:4mm 6mm;text-align:center;font-family:'Noticia Text',Georgia,serif;color:#1f3b44">
      <div style="font-size:30pt;font-style:italic;line-height:1.1">Take a hat</div>
      <div style="font-size:11pt;color:#22343a;margin-top:1mm">Free · made by the exhibition team</div></div>"""
    doc("DESK_RH6_sign_take-a-hat_180x36mm", F, 180, 36, body)
    OS = F / "original-sources"
    pg = lambda f, cap: f"""<div style="position:absolute;inset:0;background:#fff;padding:10mm;display:flex;flex-direction:column;align-items:center">
        <img src="{u(f)}" style="max-width:100%;max-height:268mm;object-fit:contain;border:.3mm solid #ccc"><div class="credit" style="margin-top:auto">{cap}</div></div>"""
    doc("DESK_RH7_reading-copies_Stow-1592-p227_Child-1888-p99_A4", F, 210, 297, None, pages=[
        pg(OS / "Stow_Annales-of-England_1592_p227.jpg", "John Stow, The Annales of England (London: Ralfe Newbery, 1592), p. 227 · Early English Books scan via Internet Archive · Reproduction"),
        pg(OS / "Child_ESPB_vol3_1888_p99_Robin-Hood-and-the-Monk.jpg", "‘Robin Hood and the Monk’ (Child 119), in F. J. Child, The English and Scottish Popular Ballads, vol. 3 (1888), p. 99 · Internet Archive · Reproduction")])


# =====================================================================================
# CASE 4 · THE BENIN BRONZES
# =====================================================================================
ARC = "#f6f1e8"


NEWSIMG = ASSETS / "news"
ARTICLES = [  # (key, outlet, date, headline, url, png)
    ("aj", "Al Jazeera", "12 October 2022", "US returns Benin Bronzes stolen by British colonial forces",
     "https://www.aljazeera.com/news/2022/10/12/us-returns-african-bronzes-stolen-by-british-colonial-forces", "aljazeera_2022.png"),
    ("td", "THISDAY", "13 April 2023", "FG Issues Gazette Recognising Ownership, Vesting Custody of Repatriated Looted Artefacts in Oba of Benin",
     "https://www.thisdaylive.com/2023/04/13/breaking-fg-issues-gazette-recognising-ownership-vesting-custody-of-repatriated-looted-artefacts-in-oba-of-benin/", "thisday_2023.png"),
    ("rt", "Reuters, via The Star", "11 May 2023", "Return of Benin Bronzes delayed after Nigerian president's decree",
     "https://www.thestar.com.my/news/world/2023/05/11/return-of-benin-bronzes-delayed-after-nigerian-president039s-decree", "reuters_thestar_2023.png"),
]


def slice_rows(png, page_ratio):
    """Cut points for splitting a tall article screenshot into pages, at blank rows."""
    from PIL import Image
    im = Image.open(png).convert("L"); w, h = im.size
    target = int(w * page_ratio); cuts = [0]
    while h - cuts[-1] > target:
        y = cuts[-1] + target
        for yy in range(y, max(cuts[-1] + target // 2, y - 400), -1):
            row = im.crop((0, yy, w, yy + 1)).getextrema()
            if row[0] > 245:
                y = yy; break
        cuts.append(y)
    cuts.append(h)
    return w, h, cuts


def webprint(name, folder, art_title, url, png):
    """A4 'printed from the browser' copy of a captured article (Chrome's print header/footer)."""
    W_MM, H_MM = 186, 265
    w, h, cuts = slice_rows(png, H_MM / W_MM)
    pages = []
    for i in range(len(cuts) - 1):
        top, bot = cuts[i], cuts[i + 1]
        scale = W_MM / w
        pages.append(f"""<div style="position:absolute;inset:0;background:#fff;font-family:Arial,Helvetica,sans-serif;color:#000">
          <div style="position:absolute;left:12mm;right:12mm;top:5mm;display:flex;justify-content:space-between;font-size:7.5pt"><span>12/11/2026, 10:42</span><span style="max-width:120mm;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{html.escape(art_title)}</span><span></span></div>
          <div style="position:absolute;left:12mm;top:14mm;width:{W_MM}mm;height:{(bot-top)*scale:.2f}mm;overflow:hidden">
            <img src="{u(png)}" style="position:absolute;left:0;top:{-top*scale:.2f}mm;width:{W_MM}mm"></div>
          <div style="position:absolute;left:12mm;right:12mm;bottom:5mm;display:flex;justify-content:space-between;font-size:7.5pt"><span style="max-width:160mm;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{html.escape(url)}</span><span>{i+1}/{len(cuts)-1}</span></div></div>""")
    return doc(name, folder, 210, 297, None, pages=pages)


def build_benin():
    F = CASE["b"]
    hdr = """<div style="position:absolute;left:0;right:0;top:0;height:46mm;background:#7a4e26;color:#f6ead8;padding:9mm 14mm 0">
        <div style="font-family:Montserrat;font-weight:700;font-size:10pt;letter-spacing:2.5pt;color:#e8cfa6">SECTION 1 · CASE 4</div>
        <div style="font-family:'Noticia Text',Georgia,serif;font-size:38pt;line-height:1.1;margin-top:3mm">The Benin Bronzes</div></div>"""
    wall_panel("BOARD_B1_wall-text_The-Benin-Bronzes_285x260mm", F, header_html=hdr,
               sub="Who exactly is the thief? · Benin City (now in Nigeria), 1897 to today", body_ps=BEN,
               cond_html=conditions(True, True, False, "→ Thief: no one?", "#7a4e26"),
               bg=ARC, color="#2e2118", font="'Noticia Text',Georgia,serif", body_pt=30, rule="#7a4e26")

    hands = [("Soldier", "Carried a plaque out of the palace, following orders."), ("Officer", "Led an expedition authorised in London."),
             ("Auction, London", "Sold objects to pay for the expedition."), ("Dealer", "Bought at auction. Lawful."),
             ("Museum", "Bought from the dealer. Lawful."), ("Curator, 1950", "Catalogued it. Took nothing.")]
    nodes = "".join(f"""<div style="background:#fff;border:.4mm solid #b39b7e;padding:2mm 3mm;height:28mm">
        <div style="font-family:Montserrat;font-weight:700;font-size:8pt;color:#7a4e26">{i+1}</div>
        <div style="font-weight:700;font-size:13pt;line-height:1.1">{h[0]}</div><div style="font-size:10.5pt;line-height:1.25;margin-top:1mm">{h[1]}</div></div>""" for i, h in enumerate(hands))
    body = f"""<div style="position:absolute;inset:0;background:{ARC};padding:5mm 7mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118">
      <div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font-size:14pt;font-weight:700">The chain of hands</div>
        <div style="font-family:Montserrat;font-weight:700;font-size:8pt;letter-spacing:2pt;text-transform:uppercase;color:#7a4e26">Diagram</div></div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm 5mm;margin-top:3mm">{nodes}</div>
      <div style="font-size:11pt;font-style:italic;margin-top:2.5mm;color:#7a4e26">Each was lawful where it took place. Each can point to someone earlier.</div>
      <div style="display:flex;gap:3mm;margin-top:2mm">
        <div style="flex:1;background:#7a4e26;color:#f6ead8;padding:1.8mm 3mm;font-size:10pt;line-height:1.25"><b>2022</b> · Smithsonian transfers ownership of 29 objects to Nigeria’s NCMM</div>
        <div style="flex:1;background:#7a4e26;color:#f6ead8;padding:1.8mm 3mm;font-size:10pt;line-height:1.25"><b>2023</b> · Oba of Benin declared owner; who holds them is disputed</div></div>
      <div style="font-size:9pt;margin-top:1.5mm;color:#6b5a48"><b>The chain of hands (diagram)</b> · Made for this exhibition</div></div>"""
    doc("BOARD_B2_chain-of-hands-diagram_285x139mm", F, 285, 139, body)

    body = f"""<div style="position:absolute;inset:0;background:{ARC};padding:4.5mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118;display:flex;flex-direction:column">
      <img src="{u(ASSETS/'plaque_fill.jpg')}" style="width:100%;height:112mm;object-fit:cover;object-position:center">
      <div style="margin-top:3mm">{label("Brass plaque from the royal palace of Benin (image)","Edo peoples, c.1540–70 · Enlarged image · Original: The Metropolitan Museum of Art, New York (1990.332)",
            "Cast by Benin’s royal guild of brass casters and fixed to the palace’s pillars, plaques like this recorded kings, warriors and court ceremonies. They were the palace’s archive, not decoration.",
            mcolor="#7a4e26", tsize=10.5, dsize=9)}</div>
      <div class="credit" style="margin-top:auto">Image: The Met, Plaque with Warrior and Attendants, 1990.332, Gift of Mr. and Mrs. Klaus G. Perls, 1990. Open Access (CC0).</div></div>"""
    doc("BOARD_B3_plaque-image_Met-1990.332_110x174mm", F, 110, 174, body)

    build_map(F)

    # Real news articles: full browser printouts on the desk, clippings on the board
    titles = {"aj": "US returns Benin Bronzes stolen by British colonial forces | News | Al Jazeera",
              "td": "Breaking: FG Issues Gazette Recognising Ownership, Vesting Custody of Repatriated Looted Artefacts in Oba of Benin – THISDAYLIVE",
              "rt": "Return of Benin Bronzes delayed after Nigerian president's decree | The Star"}
    names = {"aj": "DESK_B8_news_Al-Jazeera_2022-10-12_A4", "td": "DESK_B9_news_ThisDay_2023-04-13_Nigeria-gazette_A4",
             "rt": "DESK_B10_news_Reuters-in-The-Star_2023-05-11_A4"}
    for key, outlet, date, head, url, png in ARTICLES:
        webprint(names[key], F, titles[key], url, NEWSIMG / png)
    rot = [-1.6, 1.1, -0.7]
    clips = "".join(f"""<div style="flex:none;width:60mm;display:flex;flex-direction:column;align-items:center">
        <div style="width:60mm;height:72mm;overflow:hidden;background:#fff;transform:rotate({rot[i]}deg);box-shadow:.6mm .9mm 2mm rgba(0,0,0,.35)">
          <img src="{u(NEWSIMG/a[5])}" style="width:100%;display:block"></div>
        <div style="font-family:Montserrat;font-weight:700;font-size:7pt;letter-spacing:.6pt;text-transform:uppercase;color:#7a4e26;margin-top:2.2mm;text-align:center">{a[1]} · {a[2]}</div></div>""" for i, a in enumerate(ARTICLES))
    body = f"""<div style="position:absolute;inset:0;background:{ARC};padding:4.5mm 5.5mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118;display:flex;gap:4.5mm;align-items:flex-start">
      {clips}
      <div style="flex:1;padding-top:1mm">{label("Returning the bronzes","2022–2023 · News reports · Clippings",
            "October 2022: 29 objects go back from the Smithsonian. March 2023: Nigeria’s president names the Oba of Benin owner. May 2023: returns stall over who should receive them. Full articles are on the desk.",
            mcolor="#7a4e26", tsize=11, dsize=9.2)}</div></div>"""
    doc("BOARD_B5_news-clippings_2022-2023_285x92mm", F, 285, 92, body)

    qr_strip("BOARD_B6_QR-audio-strip_285x46mm", F, "06_The_Benin_Bronzes.png", "#3b2a1e", "#f6ead8", "#e8cfa6",
             "'Noticia Text',Georgia,serif", "Listen &amp; see the sources", "Audio guide · Case 4 · The Benin Bronzes")

    # Government document: The London Gazette, 7 May 1897 (the official account)
    body = f"""<div style="position:absolute;inset:0;background:{ARC};padding:9mm 10mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118;display:flex;flex-direction:column">
      <div style="font-family:Montserrat;font-weight:700;font-size:8.5pt;letter-spacing:1.5pt;text-transform:uppercase;color:#7a4e26">Government document · the official account, 1897</div>
      <div style="background:#fff;border:.3mm solid #b39b7e;padding:2mm;margin-top:2mm"><img src="{u(ASSETS/'gz_masthead.png')}" style="width:100%"></div>
      <div style="display:flex;gap:4mm;margin-top:3mm">
        <div style="width:72mm;flex:none;display:flex;flex-direction:column;gap:3mm">
          <div style="background:#fff;border:.3mm solid #b39b7e;padding:2mm"><img src="{u(ASSETS/'gz_despatch.png')}" style="width:100%"></div>
          {label("<i>The London Gazette</i>, 7 May 1897","Issue 26850, pp. 2516–2534 · Published by authority · Reproduction",
             "Rear-Admiral Rawson’s despatches on ‘operations against the King of Benin, and the capture of Benin City’, printed in the government’s official newspaper. The report of the column’s commander (right) describes the palace altars, ‘carved ivory tusks’ set in ‘brass heads’, and the fire that ‘destroyed the King’s and all surrounding quarters’.",
             mcolor="#7a4e26", tsize=12, dsize=10)}
          <div style="font-size:10.5pt;line-height:1.38;border-left:1.2mm solid #7a4e26;padding-left:3mm">The official record describes the objects. It does not say that they were taken, or where they went next.</div>
          <div class="credit" style="margin-top:auto">Source: thegazette.co.uk, issue 26850, pages 2516 and 2532 (Crown copyright; Open Government Licence).</div></div>
        <div style="flex:1;background:#fff;border:.3mm solid #b39b7e;padding:2mm"><img src="{u(ASSETS/'gz_2532_col.png')}" style="width:100%"></div>
      </div></div>"""
    doc("BOARD-OR-DESK_B7_government-document_London-Gazette_1897-05-07_A4", F, 210, 297, body)

    body = f"""<div style="position:absolute;inset:0;background:{ARC};border-top:2.5mm solid #7a4e26;padding:4mm 7mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118">
      {label("Handmade plaque (replica)","Made for this exhibition · Not an original","A copy made by the exhibition team, so visitors can see a plaque’s size and depth of relief. The plaque in the photograph on the wall is about 48 × 38 cm.", mcolor="#7a4e26", tsize=14, dsize=12)}</div>"""
    doc("DESK_B11_object-label_replica-plaque_200x52mm", F, 200, 52, body)


def benin_route_svg():
    """Movements of the Benin objects drawn over the 1897 Berghaus map detail (1420 x 900 px, Mercator)."""
    import math
    SC = 10.4; X0 = 880 + SC*0.1; K = SC*180/math.pi
    YEQ = 262 + K*math.log(math.tan(math.pi/4 + math.radians(51.5)/2))
    xy = lambda lo, la: (X0 + SC*lo, YEQ - K*math.log(math.tan(math.pi/4 + math.radians(la)/2)))
    def path(pts):
        P = [xy(*p) for p in pts]
        d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
        for i in range(len(P)-1):
            p0 = P[i-1] if i else P[i]; p1, p2 = P[i], P[i+1]; p3 = P[i+2] if i+2 < len(P) else p2
            c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6); c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
            d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
        return d
    RED, BRN, GRN = "#9b3b22", "#5b3a1e", "#2f5d46"
    taken = path([(5.62,6.34),(3.5,4.6),(-3,4.4),(-11,5.5),(-19,11),(-22,18),(-20,26),(-15,33),(-11.5,40),(-8.5,45.5),(-5.5,48.6),(-1.5,50.3),(-0.13,51.5)])
    to_ny = path([(-0.13,51.5),(-8,51.2),(-25,50),(-45,46.5),(-62,43),(-74,40.7)])
    to_dc = path([(-0.13,51.5),(-9,50.4),(-27,47.5),(-47,43),(-64,39.5),(-77,38.9)])
    to_eu = path([(-0.13,51.5),(4,52.2),(9,52.5)])
    back = path([(-77,38.9),(-62,31),(-45,20),(-28,8),(-12,0.5),(1,1.2),(5.62,6.34)])
    halo = 'fill="none" stroke="#f4efe6" stroke-opacity=".85" stroke-linecap="round" stroke-linejoin="round" stroke-width="15"'
    line = lambda d, c, extra="": f'<path d="{d}" fill="none" stroke="{c}" stroke-width="6.5" stroke-linecap="round" {extra}/>'
    o = ['<svg viewBox="0 0 1420 900" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%">',
         '<defs><marker id="bh" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="context-stroke"/></marker>'
         f'<marker id="bhb" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{BRN}"/></marker>'
         f'<marker id="bhr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{RED}"/></marker>'
         f'<marker id="bhg" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="{GRN}"/></marker></defs>']
    for d in (taken, to_ny, to_dc, to_eu, back): o.append(f'<path d="{d}" {halo}/>')
    o += [line(back, GRN, 'stroke-dasharray="2 13" marker-end="url(#bhg)"'),
          line(taken, RED, 'stroke-dasharray="18 11" marker-end="url(#bhr)"'),
          line(to_ny, BRN, 'marker-end="url(#bhb)"'), line(to_dc, BRN, 'marker-end="url(#bhb)"'), line(to_eu, BRN, 'marker-end="url(#bhb)"')]
    lab = lambda x, y, t, anc="start", sz=30: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" font-family="Noticia Text,Georgia,serif" font-weight="700" font-size="{sz}" '
                                              f'fill="#2e2118" stroke="#f4efe6" stroke-width="8" paint-order="stroke" stroke-linejoin="round">{t}</text>')
    for n, ll, col, (dx, dy, anc, t) in [(1,(5.62,6.34),RED,(26,-14,"start","Benin City")),(2,(-0.13,51.5),RED,(-24,-22,"end","London")),
                                         (3,(-74,40.7),BRN,(22,-16,"start","New York")),(4,(-77,38.9),BRN,(22,34,"start","Washington"))]:
        x, y = xy(*ll)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="{col}" stroke="#f4efe6" stroke-width="4"/>'
                 f'<text x="{x:.1f}" y="{y+7:.1f}" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="20" fill="#f4efe6">{n}</text>' + lab(x+dx, y+dy, t, anc))
    ex, ey = xy(9.5, 52.5); o.append(lab(ex+14, ey+8, "Europe", "start", 26))
    o.append('</svg>')
    return "".join(o)


def build_map(F):
    body = f"""<div style="position:absolute;inset:0;background:{ARC};padding:4.5mm 5.5mm;font-family:'Noticia Text',Georgia,serif;color:#2e2118;display:flex;flex-direction:column">
      <div style="font-size:13pt;font-weight:700;margin-bottom:2mm">From Benin City to the world</div>
      <div style="position:relative;width:100%;height:100mm;border:.3mm solid #b39b7e;overflow:hidden">
        <img src="{u(ASSETS/'worldmap_1897_atlantic.jpg')}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">{benin_route_svg()}</div>
      <div style="margin-top:2.5mm;font-size:9pt;line-height:1.5">
        <div style="display:flex;align-items:center;gap:2.5mm"><svg width="13mm" height="2.6mm" viewBox="0 0 52 10"><line x1="2" y1="5" x2="50" y2="5" stroke="#9b3b22" stroke-width="3.5" stroke-dasharray="9 5"/></svg><span><b>1897</b> · Taken from ① Benin City to ② London, where many were auctioned</span></div>
        <div style="display:flex;align-items:center;gap:2.5mm"><svg width="13mm" height="2.6mm" viewBox="0 0 52 10"><line x1="2" y1="5" x2="50" y2="5" stroke="#5b3a1e" stroke-width="3.5"/></svg><span><b>After 1897</b> · Sold on to collections in Europe and North America, among them ③ the Met and ④ the Smithsonian</span></div>
        <div style="display:flex;align-items:center;gap:2.5mm"><svg width="13mm" height="2.6mm" viewBox="0 0 52 10"><line x1="2" y1="5" x2="50" y2="5" stroke="#2f5d46" stroke-width="3.5" stroke-dasharray="1.5 5" stroke-linecap="round"/></svg><span><b>2022</b> · The Smithsonian transfers ownership of 29 objects back to Nigeria</span></div></div>
      <div style="margin-top:3mm">{label("From Benin City to the world (map)","Map: Hermann Berghaus, <i>Chart of the World on Mercator’s Projection</i>, Gotha: Justus Perthes, 1897 · Detail",
            "A world map printed in the year of the raid, with the objects’ journeys drawn on for this exhibition. Objects taken from Benin City were auctioned in London and passed to collections across Europe and North America. More than a century later, most of them are still outside Nigeria.",
            mcolor="#7a4e26", tsize=11, dsize=9.2)}</div>
      <div class="credit" style="margin-top:auto">Map: public domain, via Wikimedia Commons (from Barry Lawrence Ruderman Antique Maps).</div></div>"""
    doc("BOARD_B4_map_Benin-City-to-the-world_169x174mm", F, 169, 174, body)


# =====================================================================================
# SHARED DESK ITEMS (one set per case quarter: print x4)
# =====================================================================================
def build_shared():
    F = CASE["s"]
    body = """<div style="position:absolute;inset:0;background:#1f262e;color:#efe6d2;padding:6mm 7.5mm;font-family:'DM Sans',Arial,sans-serif">
      <div style="font-family:Georgia,serif;font-size:24pt;color:#c9a36a">Theft or not?</div>
      <div style="font-size:16.5pt;line-height:1.42;margin-top:3mm">Place one pin on the line where you think this case belongs. 0 means ‘not theft’; 10 means ‘theft’. The line is continuous because many cases here do not fit a yes-or-no answer. The first few pins were placed by the exhibition team at the opening. Each evening, the strip is photographed and added to the digital catalogue.</div></div>"""
    doc("DESK_voting-card_Theft-or-not_195x96mm_print-x4", F, 195, 96, body)
    cases = [("Case 1", "Ordinary theft", "#1d3b6a"), ("Case 2", "Kleptomania and class", "#2f4a3a"),
             ("Case 3", "Robbing the rich", "#1f3b44"), ("Case 4", "The Benin Bronzes", "#7a4e26")]
    L, R = 22, 258                      # bar ends (mm)
    step = (R - L) / 10
    def strip(num, name, col):
        ticks = ""
        for i in range(21):
            x = L + i * step / 2
            major = i % 2 == 0
            ticks += f'<div style="position:absolute;left:{x-.2:.2f}mm;top:{41 if major else 41}mm;width:.4mm;height:{4.2 if major else 2.4}mm;background:#2b2a26"></div>'
            if major:
                n = i // 2
                ticks += f'<div style="position:absolute;left:{x-5:.2f}mm;top:46mm;width:10mm;text-align:center;font-family:Montserrat;font-weight:700;font-size:{13 if n in (0,5,10) else 10.5}pt;color:#2b2a26">{n}</div>'
        return f"""<div style="position:absolute;inset:0;background:#f4efe4;font-family:Montserrat,Arial,sans-serif;color:#2b2a26">
          <div style="position:absolute;left:0;top:0;bottom:0;width:4mm;background:{col}"></div>
          <div style="position:absolute;left:{L}mm;top:6mm;font-family:Georgia,'Noticia Text',serif;font-size:17pt;line-height:1">Theft or not?</div>
          <div style="position:absolute;right:{280-R}mm;top:6.5mm;text-align:right;font-size:8pt;font-weight:700;letter-spacing:1.4pt;text-transform:uppercase;color:{col}">Section 1 · {num}<br><span style="font-family:Georgia,serif;font-weight:400;font-style:italic;letter-spacing:0;text-transform:none;font-size:11pt;color:#2b2a26">{name}</span></div>
          <div style="position:absolute;left:{L}mm;top:17mm;font-size:8pt;color:#6b6457">Place one pin on the bar where you think this case belongs.</div>
          <div style="position:absolute;left:{L}mm;width:{R-L}mm;top:25mm;height:15mm;border-radius:7.5mm;background:linear-gradient(90deg,#d9e7d5 0%,#efe6c8 50%,#f0c7bd 85%,#e3a294 100%);box-shadow:inset 0 .4mm 1mm rgba(0,0,0,.18)"></div>
          <div style="position:absolute;left:{L+(R-L)/2-.15}mm;top:25mm;height:15mm;width:.3mm;background:rgba(43,42,38,.35)"></div>
          <div style="position:absolute;left:{L+(R-L)/2-6}mm;top:28.5mm;width:12mm;text-align:center;font-family:Georgia,serif;font-size:15pt;color:rgba(43,42,38,.45)">?</div>
          {ticks}
          <div style="position:absolute;left:5mm;top:28mm;width:15mm;text-align:right;font-size:7.5pt;font-weight:700;letter-spacing:.8pt;line-height:1.2;color:#2f6b3a">NOT<br>THEFT</div>
          <div style="position:absolute;left:{R+2}mm;top:28mm;width:18mm;font-size:7.5pt;font-weight:700;letter-spacing:.8pt;line-height:1.2;color:#b3261e">THEFT</div>
        </div>"""
    doc("DESK_voting-scale-strips_one-per-case_280x60mm", F, 280, 60, None, pages=[strip(*c) for c in cases])


if __name__ == "__main__":
    build_header(); build_ordinary(); build_klepto(); build_robin(); build_benin(); build_shared()
    print(f"\n{len(BUILT)} PDFs built.")
