#!/usr/bin/env python3
"""
Builds every printable document for Section 3 ("Who Names the Act and Who Owns
the Story?") of the Museum of Theft into ../section-3/. Same method as
build_section1.py: HTML at real millimetre size, printed with headless Chrome.

Run:  python3 build_section3.py
"""
from common import (S1, ROOT, u, doc, paras, label, webprint, BUILT, ORN, use_section, copy_pdf,
                    image_pages, qr_panel, section_header, voting, object_labels)

use_section(3)
HERE = S1.HERE
OUT = ROOT / "section-3"
A = HERE / "assets" / "section-3"
NEWS = A / "news"
CASE = {"h": OUT / "00_section-header", "d": OUT / "01_the-dawes-act", "a": OUT / "02_the-hasdeo-arand-forest", "s": OUT / "shared-desk-items"}
for p in CASE.values():
    p.mkdir(parents=True, exist_ok=True)

# =====================================================================================
# TEXT (Phase 4 text, as on the Section 3 layout mock-up)
# =====================================================================================
INTRO = [
    "When land changes hands, the conflict begins long before the first surveyor’s peg or industrial excavator strikes the earth; it begins with language. Those in power wield bureaucratic terminology to sanitize dispossession. Communal heritage is branded “surplus,” ancestral forests are classified as “mine blocks,” and systemic exploitation is reframed under the banner of “development,” “national progress,” or “corporate stewardship.”",
    "This section sets state and corporate archives directly against the counter-archives preserved by indigenous communities. Comparing the 1887 Dawes Act in the United States with ongoing coal extraction in India’s Hasdeo Arand forest reveals identical institutional playbooks separated by over a century. Official records: statutes, clearance certificates, and glossy sustainability brochures, depict an orderly, legal redistribution of resources. In contrast, tribal petitions, forged consent controversies, and grassroots resistance tell a story of existential survival and broken treaties. By laying official claims alongside community realities, this exhibit asks: Who gets to decide what is legal, what is theft, and whose memory becomes history?",
]
DAW = [
    "Before 1887, Native American tribes held and cared for their lands communally: no single person “owned” a plot; the entire tribe shared it. The U.S. government passed the Dawes General Allotment Act to end this system.",
    "The government surveyed reservations and split the shared land into small, individual private plots given to Native families. Any leftover territory was labeled “surplus” and sold off to non-Native settlers, railroads, and corporations.",
    "Under the guise of “civilizing” tribes through private ownership, this legal sleight of hand stripped Native Americans of roughly 90 million acres, two-thirds of their entire land base. The following exhibits trace how simple administrative labels transformed sacred communal homelands into commercial real estate, and how indigenous leaders fought to preserve their treaties.",
]
HAS = [
    "Spanning over 1650 square kilometres in Chhattisgarh, Hasdeo Arand is known as the “lungs of central India”, a biodiversity hotspot, elephant corridor, and home to indigenous Adivasi communities whose culture and survival rely on the forest. Under Indian law, village councils (Gram Sabhas) have the constitutional right to decide what happens to their ancestral land.",
    "Beneath this ancient canopy, however, lie billions of tons of coal. Over the past decade, state agencies and corporate developers have systematically cleared vast tracts of the forest, designating them as open-cast coal blocks.",
    "Official reports describe this extraction as essential national development and responsible stewardship. In response, local communities argue that clearances bypass their consent and destroy their watershed. The following exhibits document this unfolding clash: official environmental clearances and corporate brochures on one side, and village resolutions, forest blockades, and community defense on the other.",
]

NEU, NINK = "#f7f5f0", "#22252b"
SIDE_A, SIDE_B = "#2c3e5c", "#6b3f17"
VIC_BG = "linear-gradient(160deg,#f6efdf 0%,#f1e8d4 60%,#ebdfc6 100%)"
JOUR, JINK, JBRN = "#efe4d0", "#2b2016", "#8a5a2e"
FEED, TAN, RUST, FINK = "#fbf6f2", "#d5b7a3", "#9b5a3c", "#241a15"
NOT, UNNA, DMS, MONT = "'Noticia Text',Georgia,serif", "Unna,Georgia,serif", "'DM Sans',Arial,sans-serif", "Montserrat,Arial,sans-serif"

clip = lambda f, extra="", pad=1.5, border="#c9c2b0": f'<div style="background:#fff;border:.3mm solid {border};padding:{pad}mm;box-shadow:.4mm .6mm 1.4mm rgba(0,0,0,.18)"><img src="{u(A/f)}" style="width:100%;display:block;{extra}"></div>'
script = lambda t, col: f'<div style="font-family:Unna,Georgia,serif;font-style:italic;font-size:17pt;color:{col}">{t}</div>'


def case_panel(name, F, num, title, sub, ps, off, com, accent):
    chip = lambda w, bg, fg: f'<span style="display:inline-block;font-family:Montserrat;font-weight:700;font-size:11pt;padding:1.2mm 3.5mm;border-radius:10mm;margin:0 1.5mm 1.5mm 0;background:{bg};color:{fg};border:.4mm solid {fg}">{w}</span>'
    body = f"""<div style="position:absolute;inset:0;background:{NEU};color:{NINK};font-family:{NOT}">
      <div style="position:absolute;left:0;right:0;top:0;height:36mm;display:flex">
        <div style="width:36mm;background:{accent};color:#fff;display:flex;align-items:center;justify-content:center;font-family:'League Spartan';font-weight:700;font-size:54pt">{num}</div>
        <div style="flex:1;padding:6mm 10mm 0;border-bottom:.8mm solid {accent}">
          <div style="font-family:Montserrat;font-weight:700;font-size:9pt;letter-spacing:2pt;text-transform:uppercase;color:{accent}">Section 3 · Case {num} · {sub}</div>
          <div style="font-size:30pt;line-height:1.1;margin-top:3mm">{title}</div></div></div>
      <div class="fit" style="position:absolute;left:10mm;right:10mm;top:44mm;bottom:30mm;column-count:2;column-gap:12mm;font-size:36pt;line-height:1.42;overflow:hidden">{paras(ps,'margin-bottom:.5em')}</div>
      <div style="position:absolute;left:10mm;right:10mm;bottom:6mm;border-top:.4mm solid #c9c2b0;padding-top:3mm;display:flex;align-items:center;gap:5mm">
        <div style="font-family:Montserrat;font-weight:700;font-size:9pt;letter-spacing:1pt;line-height:1.15;flex:none">SAME ACT,<br>TWO NAMES</div>
        <div style="flex:1">{''.join(chip(w, '#e3e7ee', SIDE_A) for w in off)}</div>
        <div style="font-family:Montserrat;font-size:10pt;color:#777">vs</div>
        <div style="flex:1;text-align:right">{''.join(chip(w, '#efe2c8', SIDE_B) for w in com)}</div></div></div>"""
    doc(name, F, 585, 194, body)


def side_heads(name, F):
    head = lambda t, bg, fg, al: f'<div style="position:absolute;inset:0;background:{bg};color:{fg};display:flex;align-items:center;justify-content:{al};padding:0 6mm;font-family:Montserrat;font-weight:700;font-size:12pt;letter-spacing:3pt;text-transform:uppercase">{t}</div>'
    doc(name, F, 285, 15, None, pages=[head("Side A · The official record", SIDE_A, "#e9eef6", "flex-start"),
                                        head("The community’s record · Side B", SIDE_B, "#f5e9d4", "flex-end")])


def build_header():
    section_header("BOARD_H_section-header_Who-Names-the-Act_1180x90mm", CASE["h"], kicker="Section 3",
                   title="Who Names the Act and Who Owns the Story?", sub="Two cases · two records each", intro=INTRO,
                   qr_file="11_Who_Names_the_Act.png", qr_caption="Audio guide · Section 3")


# =====================================================================================
# CASE 1 · THE DAWES ACT
# =====================================================================================
def build_dawes():
    F = CASE["d"]
    case_panel("BOARD_D1_case-panel_The-Dawes-Act_585x194mm", F, 1, "The Dawes Act", "Allotment of Native American land · United States, 1887–1934",
               DAW, ["“surplus”", "allotment", "“civilizing”", "land for sale"], ["treaty land", "communal homeland", "two-thirds lost"], SIDE_A)
    side_heads("BOARD_D1ab_side-headers_Official-vs-Community_285x15mm_2pp", F)

    # D2 · The broadside (Side A)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:#2b2a26;font-family:{UNNA};padding:6mm;display:flex;gap:6mm">
      <div style="width:150mm;flex:none">{clip('landsale.jpg', border='#999')}</div>
      <div style="flex:1;display:flex;flex-direction:column;padding-top:2mm">
        <div style="height:6mm;background:url('{u(ORN)}') repeat-x center/auto 100%;margin-bottom:5mm"></div>
        {label("“Indian Land for Sale”", "1911 · US Department of the Interior · Poster · Reproduction",
               "A federal poster advertising allotted tribal land by sealed bid: ‘For the year 1911 it is estimated that 350,000 acres will be offered for sale.’ Signed by the Secretary of the Interior and the Commissioner of Indian Affairs.",
               mcolor="#8a5a2e", tsize=15, dsize=12.5)}
        <div style="font-family:'Diplomata SC',Georgia,serif;color:#2f4a3a;font-size:17pt;line-height:1.5;margin-top:10mm">The state<br>names it:<br>for sale</div>
        <div class="credit" style="margin-top:auto">Original: Library of Congress. Public domain; image via Wikimedia Commons. The man pictured is a Yankton Sioux named Not Afraid of Pawnee.</div></div></div>"""
    doc("BOARD_D2_government-poster_Indian-Land-for-Sale_1911_285x224mm", F, 285, 224, body)

    # D3 · The statute and the rolls (Side A)
    body = f"""<div style="position:absolute;inset:0;background:{VIC_BG};color:#2b2a26;font-family:{UNNA};padding:5.5mm;display:flex;gap:4mm">
      <div style="width:88mm;flex:none">{clip('dawes_act_p1.jpg', 'height:110mm;object-fit:cover;object-position:top', border='#999')}</div>
      <div style="width:80mm;flex:none">{clip('frL_300.jpg', 'height:110mm;object-fit:cover;object-position:top', border='#999')}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("The Dawes Act and the allotment rolls", "1887 and 1907 · Reproductions; originals in the US National Archives",
               "Left: the signed Act of 8 February 1887, ‘to provide for the allotment of lands in severalty to Indians’. Right: a page of the 1907 index to the final Dawes Rolls, ‘Cherokees by Blood’. A roll number decided who belonged, and who received land.",
               mcolor="#8a5a2e", tsize=12.5, dsize=10.5)}
        <div class="credit" style="margin-top:auto">Act: NARA, Enrolled Acts and Resolutions of Congress (via DPLA / Wikimedia Commons). Index to the Final Rolls (1907), p. 297, via Internet Archive. Public domain.</div></div></div>"""
    doc("BOARD_D3_government-documents_Dawes-Act-1887_Final-Rolls-1907_285x128mm", F, 285, 128, body)

    # D4 · Cherokee protest to Congress, 1896 (Side B)
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};color:{JINK};font-family:{NOT};padding:5.5mm;display:flex;gap:4mm">
      <div style="width:70mm;flex:none">{clip('cp_cover.png', border='#b9a582')}</div>
      <div style="width:100mm;flex:none;display:flex;flex-direction:column;gap:2mm">{clip('cp_allot.png', border='#b9a582')}{clip('cp_force.png', border='#b9a582')}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("Protest of the Cherokee Nation to Congress", "Washington, 5 March 1896 · Printed petition · Reproduction",
               "Cherokee delegates protest a bill to bring tribal land under federal courts and allotment: ‘Congress has no more right to force a division of the use of the lands of the Cherokees than it has to compel heirs to an estate to individualize their interest.’",
               mcolor=JBRN, tsize=12, dsize=10)}
        <div style="margin-top:3mm">{script('The people name it', JBRN)}</div>
        <div class="credit" style="margin-top:auto">Library of Congress copy, via Internet Archive (protestofcheroke00cher). Public domain.</div></div></div>"""
    doc("BOARD_D4_petition_Protest-of-the-Cherokee-Nation_1896_285x128mm", F, 285, 128, body)

    # D5 · Redbird Smith, in his own words (Side B)
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};color:{JINK};font-family:{NOT};padding:7mm 8mm;display:flex;flex-direction:column">
      <div style="font-family:Montserrat;font-weight:700;font-size:9pt;letter-spacing:2pt;color:{SIDE_B}">IN HIS OWN WORDS</div>
      <div style="font-size:20pt;line-height:1.3;font-style:italic;color:{SIDE_B};margin:3mm 0 2mm;border-left:2mm solid {SIDE_B};padding-left:5mm">“I never consented to any agreement to divide up my land, and I don’t want it divided up. I want the old treaty.”</div>
      <div style="font-size:11pt;margin-bottom:4mm">— Redbird Smith, Cherokee (Keetoowah) leader, testimony to a US Senate select committee, Muskogee, November 1906</div>
      <div style="display:flex;gap:4mm;flex:1;min-height:0">
        <div style="width:62mm;flex:none">{clip('rs_title.jpg', 'height:100mm;object-fit:cover;object-position:top', border='#b9a582')}</div>
        <div style="flex:1;display:flex;flex-direction:column;gap:1.5mm">{clip('rs_head.png', border='#b9a582')}{clip('rs_p98.png', border='#b9a582')}</div></div>
      <div style="margin-top:3mm">{label("Testimony of Redbird Smith", "November 1906 to January 1907 · Senate Report 5013, vol. 1, pp. 97–98 · Reproduction",
            "Arrested for refusing to enrol, he told the committee he was ‘made to enroll against my will’. The committee’s answer, on the next page: take your allotment, or ‘you will soon find yourself without land altogether’.",
            mcolor=JBRN, tsize=12, dsize=10)}</div></div>"""
    doc("BOARD_D5_testimony_Redbird-Smith_Senate-1906_285x224mm", F, 285, 224, body)

    # D6 · Shrinking land base: a dated official map + blocks drawn to scale
    import math
    k = 9.0
    a1, a2 = math.sqrt(138) * k, math.sqrt(48) * k
    body = f"""<div style="position:absolute;inset:0;background:{NEU};color:{NINK};font-family:{NOT};padding:5mm 6mm;display:flex;gap:6mm">
      <div style="width:190mm;flex:none;display:flex;flex-direction:column">
        <div style="font-size:14pt;font-weight:700;margin-bottom:2mm">The shrinking land base, 1887–1934</div>
        <img src="{u(A/'map1894.jpg')}" style="width:100%;height:118mm;object-fit:cover;border:.3mm solid #999">
        <div class="credit" style="margin-top:1mm">Map showing Indian reservations within the limits of the United States, 1894 (Office of Indian Affairs, for the Eleventh Census). Public domain, via Internet Archive / Wikimedia Commons.</div></div>
      <div style="flex:1;display:flex;flex-direction:column">
        <div style="font-family:Montserrat;font-weight:700;font-size:8pt;letter-spacing:2pt;color:#777;text-align:right">AREAS DRAWN TO SCALE</div>
        <div style="display:flex;align-items:flex-end;gap:6mm;margin-top:3mm">
          <div style="width:{a1:.1f}mm;height:{a1:.1f}mm;background:#7a5230;color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Montserrat;font-weight:700;font-size:12pt;line-height:1.3">1887<br>≈138 million acres</div>
          <div style="font-size:20pt;padding-bottom:{a2/2:.0f}mm">→</div>
          <div style="position:relative;width:{a1:.1f}mm;height:{a1:.1f}mm;border:.5mm dashed #7a5230">
            <div style="position:absolute;left:0;bottom:0;width:{a2:.1f}mm;height:{a2:.1f}mm;background:#7a5230;color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Montserrat;font-weight:700;font-size:10pt;line-height:1.3">1934<br>≈48 million</div>
            <div style="position:absolute;right:2mm;top:2mm;text-align:right;font-family:Montserrat;font-weight:700;font-size:10pt;color:#7a5230">≈90 million<br>acres lost</div></div></div>
        <div style="margin-top:auto">{label("The shrinking land base, 1887–1934 (map and diagram)", "Map 1894 · Diagram made for this exhibition",
            "An official map of reservations seven years into allotment, beside two squares drawn to scale: Native land in 1887 and the third that remained in 1934, when allotment ended.",
            tsize=12, dsize=10.5, mcolor="#555")}</div></div></div>"""
    doc("BOARD_D6_map-and-diagram_Shrinking-land-base_445x156mm", F, 445, 156, body)
    qr_panel("BOARD_D7_QR-audio_125x156mm", F, "12_The_Dawes_Act.png", 125, 156, bg=SIDE_A, fg="#e9eef6", accent="#c9d4e6",
             font=MONT, line1="Listen &amp; see the sources", line2="Audio guide · Case 1 · The Dawes Act", qr_mm=80)

    # Desk: the mock ledger (reconstruction), stamp artwork, labels, reading copies
    rows = "".join(f"""<tr><td>Tract {101+i}</td><td>{['160 ac','80 ac','160 ac','40 ac','160 ac','80 ac','80 ac','40 ac','160 ac','80 ac','160 ac','40 ac','80 ac','160 ac'][i]}</td>
        <td>{['Sec. 4, T. 21 N.','Sec. 4, T. 21 N.','Sec. 5, T. 21 N.','Sec. 5, T. 21 N.','Sec. 8, T. 21 N.','Sec. 8, T. 21 N.','Sec. 9, T. 21 N.','Sec. 9, T. 21 N.','Sec. 16, T. 21 N.','Sec. 16, T. 21 N.','Sec. 17, T. 21 N.','Sec. 17, T. 21 N.','Sec. 20, T. 21 N.','Sec. 20, T. 21 N.'][i]}</td>
        <td>{'' if i in (4,5,7,8,10,11,13) else 'allotted'}</td><td></td></tr>""" for i in range(14))
    body = f"""<div style="position:absolute;inset:0;background:#efe6d0;font-family:Unna,Georgia,serif;color:#2b2a26;display:flex">
      <div style="flex:1;padding:12mm 12mm 10mm 14mm;border-right:1mm solid #8a7a5a">
        <div style="font-family:'Diplomata SC',Georgia,serif;font-size:16pt;color:#2f4a3a">Allotment Ledger</div>
        <div style="font-size:10pt;font-style:italic;color:#8a5a2e;margin:1mm 0 4mm">Schedule of allotments · Township 21 North</div>
        <table style="width:100%;border-collapse:collapse;font-size:12pt"><tr style="font-weight:700;border-bottom:.5mm solid #2b2a26"><td>Tract</td><td>Acres</td><td>Location</td><td>Status</td><td>Allottee / roll no.</td></tr>{rows}</table>
        <style>td{{padding:2.2mm 1.5mm;border-bottom:.2mm solid #b8a888}}</style></div>
      <div style="flex:1;padding:12mm 14mm 10mm 12mm">
        <div style="font-family:'Diplomata SC',Georgia,serif;font-size:13pt;color:#2f4a3a">Unallotted tracts</div>
        <div style="font-size:10pt;font-style:italic;color:#8a5a2e;margin:1mm 0 4mm">To be stamped by the visitor</div>
        {''.join('<div style="height:11.6mm;border-bottom:.2mm solid #b8a888"></div>' for _ in range(18))}</div>
      <div class="credit" style="position:absolute;left:14mm;bottom:4mm">Mock allotment ledger · Reconstruction made for this exhibition, after the layout of Dawes-era allotment schedules. Not a historical document.</div></div>"""
    doc("DESK_D8_prop_mock-allotment-ledger_A3-landscape", F, 420, 297, body)
    body = """<div style="position:absolute;inset:0;background:#fff;display:flex;align-items:center;justify-content:center;gap:12mm;font-family:'Diplomata SC',Georgia,serif">
      <div style="border:1.2mm solid #000;padding:2mm 5mm;font-size:24pt;letter-spacing:2pt">SURPLUS</div>
      <div style="border:1.2mm solid #000;padding:2mm 5mm;font-size:24pt;letter-spacing:2pt;transform:scaleX(-1)">SURPLUS</div></div>
      <div class="credit" style="position:absolute;left:5mm;bottom:3mm">Artwork for the rubber stamp: readable (left) and mirrored for the stamp maker (right).</div>"""
    doc("DESK_D9_stamp-artwork_SURPLUS_120x40mm", F, 120, 40, body)
    object_labels("DESK_D11_object-labels_ledger-stamp-chain_200x56mm_3pp", F, [
        ("Mock allotment ledger", "Made for this exhibition · Reconstruction", "A ledger where tracts are listed, allotted, or stamped ‘surplus’."),
        ("“SURPLUS” rubber stamp", "Prop made for this exhibition", "The administrative word that turned leftover tribal territory into public land for sale. Visitors may stamp the ledger."),
        ("Surveyor’s chain", "Representative object", "A 66-foot chain of the kind used to split ancestral territory into rectangular, saleable parcels.")],
        bg=VIC_BG, color="#2b2a26", mcolor="#8a5a2e", font=UNNA, rule="#2f4a3a")
    OS = F / "original-sources"
    copy_pdf(OS / "Dawes-Act_1887-02-08_enrolled-original_NARA-via-Commons.pdf", F / "DESK_D15_government-document_Dawes-Act-1887_full-2pp.pdf")
    image_pages("DESK_D16_reading-copy_Senate-Report-5013_1907_Redbird-Smith_pp97-98_A4", F, [
        (A / "rs_title.jpg", "Report of the Select Committee to Investigate Matters Connected with Affairs in the Indian Territory, Senate Report No. 5013, 59th Cong., 2d sess. (1907), vol. 1 · Internet Archive (cu31924097702090)"),
        (A / "rs_112.jpg", "p. 97 · Statement of Redbird Smith (Mr. John R. Smith, interpreter)"),
        (A / "rs_113.jpg", "p. 98 · ‘I never consented to any agreement to divide up my land, and I don’t want it divided up. I want the old treaty.’")])
    image_pages("DESK_D17_reading-copy_Protest-of-the-Cherokee-Nation_1896_A4", F, [
        (A / "cherokee_protest_leaf6.jpg", "Protest of the Cherokee Nation against the passage of House Bill (6309), 1896 · Library of Congress copy via Internet Archive"),
        (A / "cherokee_protest_leaf8.jpg", "p. 1 · Washington, D.C., March 5th, 1896. To the Senate and House of Representatives"),
        (A / "cherokee_protest_leaf14.jpg", "p. 9 · ‘Allotment of lands’"),
        (A / "cherokee_protest_leaf15.jpg", "p. 10 · ‘Congress has no more right to force a division of the use of the lands of the Cherokees…’")])
    image_pages("DESK_D18_reading-copy_Index-to-the-Final-Rolls_1907_A4", F, [
        (A / "frL_0.jpg", "Index to the Final Rolls of Citizens and Freedmen of the Five Civilized Tribes in Indian Territory (1907) · Internet Archive"),
        (A / "frL_300.jpg", "p. 297 · Cherokees by Blood")])


# =====================================================================================
# CASE 2 · THE HASDEO ARAND FOREST
# =====================================================================================
def build_hasdeo():
    F = CASE["a"]
    case_panel("BOARD_HA1_case-panel_The-Hasdeo-Arand-Forest_585x194mm", F, 2, "The Hasdeo Arand Forest",
               "Coal mining and forest rights · Chhattisgarh, India, 2010 to today", HAS,
               ["coal blocks", "“development”", "“stewardship”", "clearance"], ["ancestral forest", "consent refused", "our watershed"], "#3d5a2a")
    side_heads("BOARD_HA1ab_side-headers_Official-vs-Community_285x15mm_2pp", F)

    # HA2 · Forest clearance (Side A): the Stage-II approval, 15 March 2012
    body = f"""<div style="position:absolute;inset:0;background:{NEU};color:{NINK};font-family:{NOT};padding:5.5mm;display:flex;gap:5mm">
      <div style="width:150mm;flex:none">{clip('lett_head.png', 'height:155mm;object-fit:cover;object-position:top', border='#999')}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("Forest clearance, Parsa East and Kete Basan coal mine", "15 March 2012 · Union Ministry of Environment and Forests, F. No. 8-31/2010-FC · Stage-II approval · Reproduction",
               "Final approval to divert 1,898.328 hectares of forest land for an open-cast coal mine, in two phases. In 2014 the National Green Tribunal set this clearance aside; the area had earlier been classed a ‘No Go’ area for mining. The Supreme Court stayed the Tribunal’s order, and mining continued.",
               mcolor="#555", tsize=13, dsize=11)}
        <div style="font-family:Poppins;font-weight:700;font-size:15pt;color:{RUST};margin-top:7mm;line-height:1.25">The state names it:<br>a coal block</div>
        <div class="credit" style="margin-top:auto">Copy: ‘True copy’ filed as Annexure R-2 by RRVUNL before the National Green Tribunal, O.A. No. 59 of 2024 (greentribunal.gov.in). Full letter on the desk.</div></div></div>"""
    doc("BOARD_HA2_government-document_Forest-clearance-PEKB_2012_285x168mm", F, 285, 168, body)

    # HA3 · Company reports (Side A, glossy)
    body = f"""<div style="position:absolute;inset:0;background:{FEED};color:{FINK};font-family:{DMS}">
      <div style="height:30mm;background:{TAN};padding:6mm 8mm;position:relative">
        <div style="font-family:Poppins;font-weight:700;font-size:8pt">Company report · 2023–24</div>
        <div style="font-family:Poppins;font-weight:700;font-size:17pt;line-height:1.1;margin-top:1.5mm">The official story,<br>in a glossy brochure</div>
        <div style="position:absolute;right:8mm;top:7mm;width:16mm;height:16mm;background:radial-gradient(circle,#8b4a2b 0 1.6mm,transparent 1.7mm) 0 0/5.5mm 5.5mm"></div></div>
      <div style="position:absolute;left:6mm;right:6mm;top:35mm;bottom:5mm;display:flex;gap:4mm">
        <div style="width:72mm;flex:none">{clip('adani_esg_cover.png', border='#d8cfc7')}</div>
        <div style="width:118mm;flex:none">{clip('adani_pekb.png', border='#d8cfc7')}</div>
        <div style="flex:1;display:flex;flex-direction:column">
          {label("Company report", "2023–24 · Adani Natural Resources, ESG Report 2023-24, ‘Crafting Contours: Sustainable Mining’ · Cover and p. 57 · Extract",
                 "The company that develops and operates the PEKB mine reports ‘3,37,960’ trees planted and a ‘Sal Regeneration’ initiative at the coal block, which it describes as ‘environmental stewardship’.",
                 mcolor=RUST, tsize=11.5, dsize=10, font="Poppins")}
          <div class="credit" style="margin-top:auto">Source: adanienterprises.com (Adani-ESG-Report-202324). Extract reproduced for comment and review.</div></div></div></div>"""
    doc("BOARD_HA3_company-report_Adani-Natural-Resources-ESG-2023-24_285x184mm", F, 285, 184, body)

    # HA4 · The gram sabhas speak (Side B): the movement's own statement
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};color:{JINK};font-family:{NOT};padding:5mm;display:flex;gap:4mm">
      <div style="width:132mm;flex:none;display:flex;flex-direction:column;gap:2mm">{clip('si_head.png', border='#b9a582')}{clip('si_2015.png', border='#b9a582')}</div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("The gram sabhas’ record", "Hasdeo Aranya Bachao Sangharsh Samiti · Call for a gathering of gram sabhas and a march from Fattepur to Raipur · Statement · Reproduction",
               "The village movement’s own account: ‘In 2015, 20 gram sabhas of the Hasdeo Aranya region had passed motions’ against any coal block in the area, and the consent later used for mining was obtained ‘by forging gram sabha resolutions’.",
               mcolor=JBRN, tsize=11, dsize=9.5)}
        <div style="margin-top:2mm">{script('The people name it', JBRN)}</div>
        <div class="credit" style="margin-top:auto">English version published by Survival International. Full statement on the desk.</div></div></div>"""
    doc("BOARD_HA4_community-record_Gram-sabhas-statement_285x114mm", F, 285, 114, body)

    # HA5 · Ghatbarra's forest rights: granted 2013, cancelled 2016, upheld 2025
    step = lambda y, t, c, stamp="": f"""<div style="flex:1;border:.5mm solid {c};background:#fbf6ea;padding:3mm;text-align:center;position:relative">
        <div style="font-family:Montserrat;font-weight:700;font-size:16pt;color:{c}">{y}</div><div style="font-size:10.5pt;line-height:1.25;margin-top:1mm">{t}</div>{stamp}</div>"""
    stamp = '<div style="position:absolute;left:50%;top:84%;transform:translate(-50%,-50%) rotate(-8deg);border:.8mm solid #b3261e;color:#b3261e;font-family:Montserrat;font-weight:700;font-size:11pt;padding:.3mm 2.5mm;opacity:.9;background:#fbf6ea">CANCELLED</div>'
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};color:{JINK};font-family:{NOT};padding:5mm;display:flex;gap:4mm">
      <div style="width:132mm;flex:none;display:flex;flex-direction:column;gap:3mm">
        <div style="display:flex;gap:2mm;align-items:stretch;height:40mm">
          {step("2013", "Community forest title granted to Ghatbarra village (810 ha)", "#3d5a2a")}<div>→</div>
          {step("2016", "Titles cancelled by the district, for coal mining", "#b3261e", stamp)}<div>→</div>
          {step("2025", "High Court dismisses the village’s challenge", JINK)}</div>
        <div style="height:58mm;overflow:hidden">{clip('wire_head.png', 'height:55mm;object-fit:cover;object-position:top', border='#b9a582')}</div></div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("Ghatbarra’s forest rights: granted and cancelled", "September 2013, January 2016, October 2025 · District forest rights committee; Chhattisgarh High Court · News report: The Wire, 17 Feb 2016",
               "Under the Forest Rights Act, Ghatbarra’s gram sabha received community title over its forest in 2013. On 8 January 2016 the district cancelled it, because the coal block had been cleared in 2012. The Act has no provision for revoking such titles; the High Court still upheld the cancellation.",
               mcolor=JBRN, tsize=11, dsize=9.3)}
        <div class="credit" style="margin-top:auto">Full reports on the desk: The Wire (2016), Down To Earth (2025).</div></div></div>"""
    doc("BOARD_HA5_community-record_Ghatbarra-rights-granted-and-cancelled_285x114mm", F, 285, 114, body)

    # HA6 · Protest photograph (news photo, credited)
    body = f"""<div style="position:absolute;inset:0;background:{JOUR};color:{JINK};font-family:{NOT};padding:5mm;display:flex;gap:5mm">
      <div style="width:150mm;flex:none"><img src="{u(A/'mongabay_parsa_photo.png')}" style="width:100%;height:100mm;object-fit:cover;box-shadow:.5mm .8mm 2mm rgba(0,0,0,.35)"></div>
      <div style="flex:1;display:flex;flex-direction:column">
        {label("Felling in the Parsa coal block", "2024 · Photograph: Ramlal Kariyam · Published by Mongabay India, 28 November 2024",
               "Villagers and police face each other as trees are felled in the Parsa block, next to PEKB. Days later, Chhattisgarh’s Scheduled Tribes Commission reported that the gram sabha consent behind the clearance had been forged.",
               mcolor=JBRN, tsize=11.5, dsize=10)}
        <div class="credit" style="margin-top:auto">Image © Ramlal Kariyam, from ‘Chhattisgarh tribal body says consent for mining in Hasdeo Arand was forged’, india.mongabay.com. Full article on the desk. Print permission to be confirmed with the photographer.</div></div></div>"""
    doc("BOARD_HA6_photograph_Parsa-block-felling_2024_285x110mm", F, 285, 110, body)

    # HA7 · Map (real, unmarked)
    body = f"""<div style="position:absolute;inset:0;background:{NEU};color:{NINK};font-family:{NOT};padding:5mm;display:flex;gap:6mm">
      <div style="width:240mm;flex:none;display:flex;flex-direction:column">
        <div style="font-size:13pt;font-weight:700;margin-bottom:2mm">Forest and coal blocks</div>
        <img src="{u(A/'osm_hasdeo.png')}" style="width:100%;flex:1;min-height:0;object-fit:cover;object-position:center 40%;border:.3mm solid #999"></div>
      <div style="flex:1;display:flex;flex-direction:column;padding-top:8mm">
        {label("Forest cover and coal blocks (map)", "Map data © OpenStreetMap contributors (ODbL) · Northern Chhattisgarh: Surguja, Surajpur and Korba districts",
               "Green is forest; the blue water is the Hasdeo Bango reservoir. The grey patches near Udaypur are the existing open-cast pits. The coal blocks and the villages of Ghatbarra, Salhi and Hariharpur are marked by hand.",
               mcolor="#555", tsize=12, dsize=10.5)}
        <div class="credit" style="margin-top:auto">Map: openstreetmap.org, tiles at zoom 11, retrieved November 2026.</div></div></div>"""
    doc("BOARD_HA7_map_Hasdeo-forest-and-coal-blocks_OSM_385x156mm", F, 385, 156, body)
    qr_panel("BOARD_HA8_QR-audio_Voices-of-the-forest_185x156mm", F, "13_The_Hasdeo_Arand_Forest.png", 185, 156, bg="#3d5a2a", fg="#eef3e6", accent="#cfe0b0",
             font=MONT, line1="Listen · Voices of the forest", line2="+ audio guide · Case 2 · The Hasdeo Arand Forest", qr_mm=88)

    # Desk
    body = """<div style="position:absolute;inset:0;background:#e9dcc0;border-radius:3mm;font-family:'DM Sans',monospace;color:#222;padding:4mm 6mm 4mm 16mm">
      <div style="position:absolute;left:5mm;top:50%;width:6mm;height:6mm;margin-top:-3mm;border-radius:50%;border:.6mm solid #555;background:#fff"></div>
      <div style="font-size:7pt;letter-spacing:1pt">FOREST DEPT · ENUMERATION</div>
      <div style="font-size:20pt;font-weight:700;letter-spacing:1pt;margin-top:1mm">TREE #1279</div>
      <div style="font-size:8pt;margin-top:1mm">Species: Sal · Girth: 142 cm · Compt. no. —</div></div>"""
    doc("DESK_HA9_prop_felling-tag-Tree-1279_90x40mm", F, 90, 40, body)
    jar = lambda t: f'<div style="position:absolute;inset:0;background:#fffaf0;border:.4mm solid #6b3f17;display:flex;align-items:center;justify-content:center;text-align:center;font-family:{NOT};font-size:14pt;color:#2b2016">{t}</div>'
    doc("DESK_HA10_jar-labels_x2_90x40mm", F, 90, 40, None, pages=[jar("Forest topsoil<br>· clear water"), jar("Coal dust<br>· murky water")])
    object_labels("DESK_HA11_object-labels_tag-jars-tree_200x56mm_3pp", F, [
        ("Felling tag: Tree #1279", "Prop made for this exhibition", "Living trees are numbered and inventoried before clearing. A tag like this is how a forest becomes a list."),
        ("Two jars", "Made for this exhibition", "Forest topsoil and clear water set against dark coal dust and murky water."),
        ("Tree and embrace (cut-out)", "Made for this exhibition", "A potted plant and a paper figure hugging it, after the tree-hugging protests in Hasdeo.")],
        bg=JOUR, color=JINK, mcolor=JBRN, font=NOT, rule="#3d5a2a")
    OS = F / "original-sources"
    copy_pdf(OS / "MoEF_Stage-II-forest-approval_PEKB_2012-03-15_true-copy_from-NGT-OA-59-2024.pdf", F / "DESK_HA15_government-document_MoEF-Stage-II-approval_PEKB_2012-03-15.pdf")
    copy_pdf(OS / "NGT_Appeal-73-2012_Sudiep-Shrivastava_judgment_2014-03-24.pdf", F / "DESK_HA16_court-record_NGT-judgment_Appeal-73-2012_2014-03-24_first-6pp.pdf", pages=[1, 2, 3, 4, 5, 6])
    copy_pdf(OS / "Hasdeo-Aranya-Bachao-Sangharsh-Samiti_statement_gathering-and-march_via-Survival-International.pdf", F / "DESK_HA17_community-record_HABSS-statement_4pp.pdf")
    webprint("DESK_HA18_news_The-Wire_2016-02-17_Ghatbarra-rights-cancelled_A4", F, "Chhattisgarh Govt. Cancels Tribal Rights Over Forests to Facilitiate Coal Mining - The Wire",
             "https://m.thewire.in/article/agriculture/chhattisgarh-govt-cancels-tribal-rights-over-forests-to-facilitiate-coal-mining/amp", NEWS / "wire_2016.png")
    webprint("DESK_HA19_news_Mongabay-India_2024-11-28_consent-forged_A4", F, "Chhattisgarh tribal body says consent for mining in Hasdeo Arand was forged",
             "https://india.mongabay.com/2024/11/chhattisgarh-tribal-body-says-consent-for-mining-in-hasdeo-arand-was-forged/", NEWS / "mongabay_2024.png")
    webprint("DESK_HA20_news_Down-To-Earth_2025-11-17_Setback-in-Hasdeo_A4", F, "Chhattisgarh Court Ruling: Hasdeo Forest Rights Setback",
             "https://www.downtoearth.org.in/forests/setback-in-hasdeo", NEWS / "dte_2025.png")


def build_shared():
    voting(CASE["s"], "Section 3", [("Case 1", "The Dawes Act", SIDE_A), ("Case 2", "The Hasdeo Arand Forest", "#3d5a2a")])


if __name__ == "__main__":
    build_header(); build_dawes(); build_hasdeo(); build_shared()
    print(f"\n{len(BUILT)} PDFs built.")
