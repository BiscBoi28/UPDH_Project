"""
Shared helpers for the Section 2 and Section 3 builds. Re-uses the page/PDF
machinery of build_section1.py (doc, label, webprint ...) and points it at a
per-section HTML folder and a font set that also includes Poppins.
"""
import pathlib
import build_section1 as S1

HERE = S1.HERE
ROOT = S1.ROOT
REPO = S1.REPO
QR = S1.QR
u = S1.u
doc = S1.doc
paras = S1.paras
label = S1.label
webprint = S1.webprint
BUILT = S1.BUILT

FONTS3 = REPO / "Section3_Full_Layout" / "assets" / "fonts"   # superset: + Poppins
ORN = REPO / "Section2_Full_Layout" / "assets" / "ornament_band.png"

S1.FONT_CSS = S1.FONT_CSS.replace(str(S1.FONTS.resolve().as_uri()), str(FONTS3.resolve().as_uri())) + f"""
@font-face {{ font-family:"Poppins"; font-weight:400; src:url("{u(FONTS3/'Poppins.ttf')}"); }}
@font-face {{ font-family:"Poppins"; font-weight:700; src:url("{u(FONTS3/'Poppins_Bold.ttf')}"); }}
"""


def use_section(n):
    """Write intermediate HTML to _build/html/section-n."""
    S1.HTMLDIR = HERE / "html" / f"section-{n}"
    S1.HTMLDIR.mkdir(parents=True, exist_ok=True)


def copy_pdf(src, dst, pages=None):
    """Put an original PDF (or selected pages of it) on the desk unchanged."""
    import shutil, subprocess, tempfile
    dst = pathlib.Path(dst)
    if pages is None:
        shutil.copy(src, dst)
    else:
        with tempfile.TemporaryDirectory() as t:
            outs = []
            for p in pages:
                o = pathlib.Path(t) / f"p{p}.pdf"
                subprocess.run(["pdfseparate", "-f", str(p), "-l", str(p), str(src), str(o)], check=True)
                outs.append(str(o))
            subprocess.run(["pdfunite", *outs, str(dst)], check=True)
    BUILT.append(dst)
    print("copied", dst.relative_to(ROOT))
    return dst


def image_pages(name, folder, items, w=210, h=297):
    """Reading copies: one scanned page per A4 sheet, with a source line."""
    pg = lambda f, cap: f"""<div style="position:absolute;inset:0;background:#fff;padding:10mm;display:flex;flex-direction:column;align-items:center">
        <img src="{u(f)}" style="max-width:100%;max-height:{h-29}mm;object-fit:contain;border:.3mm solid #ccc">
        <div class="credit" style="margin-top:auto">{cap}</div></div>"""
    return doc(name, folder, w, h, None, pages=[pg(f, c) for f, c in items])


def qr_panel(name, folder, qr_file, w, h, *, bg, fg, accent, font, line1, line2, qr_mm=None):
    qr_mm = qr_mm or min(w, h) - 30
    horizontal = w > h * 1.6
    if horizontal:
        body = f"""<div style="position:absolute;inset:0;background:{bg};color:{fg};display:flex;align-items:center;gap:6mm;padding:3.5mm 6mm;font-family:{font}">
          <div style="background:#fff;padding:1.5mm;flex:none"><img src="{u(QR/qr_file)}" style="width:{qr_mm}mm;height:{qr_mm}mm"></div>
          <div style="font-size:16pt;line-height:1.3">{line1}<br><span style="color:{accent};font-size:13pt">{line2}</span></div></div>"""
    else:
        body = f"""<div style="position:absolute;inset:0;background:{bg};color:{fg};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4mm;padding:5mm;text-align:center;font-family:{font}">
          <div style="background:#fff;padding:1.5mm"><img src="{u(QR/qr_file)}" style="width:{qr_mm}mm;height:{qr_mm}mm"></div>
          <div style="font-size:13pt;line-height:1.3">{line1}<br><span style="color:{accent};font-size:11pt">{line2}</span></div></div>"""
    return doc(name, folder, w, h, body)


def section_header(name, folder, *, kicker, title, sub, intro, qr_file, qr_caption, cols=3):
    body = f"""<div style="position:absolute;inset:0;background:#1f262e;color:#efe6d2;padding:7mm 9mm;display:flex;gap:11mm;font-family:'DM Sans',Arial,sans-serif">
      <div style="width:250mm;flex:none">
        <div style="font-family:Montserrat;font-weight:600;font-size:12pt;letter-spacing:2.4pt;text-transform:uppercase;color:#c9a36a">{kicker}</div>
        <div style="font-family:Georgia,'Noticia Text',serif;font-size:{44 if len(title) > 24 else 50}pt;line-height:1.05;margin:1.5mm 0 2mm">{title}</div>
        <div style="font-size:14pt;color:#c9b998">{sub}</div></div>
      <div class="fit" style="flex:1;column-count:{cols};column-gap:11mm;font-size:30pt;line-height:1.38;color:#e9e0cc;height:76mm;overflow:hidden">{paras(intro,'margin-bottom:.45em')}</div>
      <div style="width:46mm;flex:none;text-align:center;font-size:10pt;color:#c9b998"><div style="background:#fff;padding:2mm"><img src="{u(QR/qr_file)}" style="width:42mm;height:42mm"></div><div style="margin-top:2mm">{qr_caption}<br>Scan to listen</div></div>
    </div>"""
    return doc(name, folder, 1180, 90, body)


def voting(folder, section, cases):
    """Voting card (instructions) and one 0–10 pin strip per case (same design as Section 1)."""
    body = """<div style="position:absolute;inset:0;background:#1f262e;color:#efe6d2;padding:6mm 7.5mm;font-family:'DM Sans',Arial,sans-serif">
      <div style="font-family:Georgia,serif;font-size:24pt;color:#c9a36a">Theft or not?</div>
      <div style="font-size:16.5pt;line-height:1.42;margin-top:3mm">Place one pin on the line where you think this case belongs. 0 means ‘not theft’; 10 means ‘theft’. The line is continuous because many cases here do not fit a yes-or-no answer. The first few pins were placed by the exhibition team at the opening. Each evening, the strip is photographed and added to the digital catalogue.</div></div>"""
    doc(f"DESK_voting-card_Theft-or-not_195x96mm_print-x{len(cases)}", folder, 195, 96, body)
    L, R = 22, 258
    step = (R - L) / 10

    def strip(num, name, col):
        ticks = ""
        for i in range(21):
            x = L + i * step / 2
            major = i % 2 == 0
            ticks += f'<div style="position:absolute;left:{x-.2:.2f}mm;top:41mm;width:.4mm;height:{4.2 if major else 2.4}mm;background:#2b2a26"></div>'
            if major:
                n = i // 2
                ticks += f'<div style="position:absolute;left:{x-5:.2f}mm;top:46mm;width:10mm;text-align:center;font-family:Montserrat;font-weight:700;font-size:{13 if n in (0,5,10) else 10.5}pt;color:#2b2a26">{n}</div>'
        return f"""<div style="position:absolute;inset:0;background:#f4efe4;font-family:Montserrat,Arial,sans-serif;color:#2b2a26">
          <div style="position:absolute;left:0;top:0;bottom:0;width:4mm;background:{col}"></div>
          <div style="position:absolute;left:{L}mm;top:6mm;font-family:Georgia,'Noticia Text',serif;font-size:17pt;line-height:1">Theft or not?</div>
          <div style="position:absolute;right:{280-R}mm;top:6.5mm;text-align:right;font-size:8pt;font-weight:700;letter-spacing:1.4pt;text-transform:uppercase;color:{col}">{section} · {num}<br><span style="font-family:Georgia,serif;font-weight:400;font-style:italic;letter-spacing:0;text-transform:none;font-size:11pt;color:#2b2a26">{name}</span></div>
          <div style="position:absolute;left:{L}mm;top:17mm;font-size:8pt;color:#6b6457">Place one pin on the bar where you think this case belongs.</div>
          <div style="position:absolute;left:{L}mm;width:{R-L}mm;top:25mm;height:15mm;border-radius:7.5mm;background:linear-gradient(90deg,#d9e7d5 0%,#efe6c8 50%,#f0c7bd 85%,#e3a294 100%);box-shadow:inset 0 .4mm 1mm rgba(0,0,0,.18)"></div>
          <div style="position:absolute;left:{L+(R-L)/2-.15}mm;top:25mm;height:15mm;width:.3mm;background:rgba(43,42,38,.35)"></div>
          <div style="position:absolute;left:{L+(R-L)/2-6}mm;top:28.5mm;width:12mm;text-align:center;font-family:Georgia,serif;font-size:15pt;color:rgba(43,42,38,.45)">?</div>
          {ticks}
          <div style="position:absolute;left:5mm;top:28mm;width:15mm;text-align:right;font-size:7.5pt;font-weight:700;letter-spacing:.8pt;line-height:1.2;color:#2f6b3a">NOT<br>THEFT</div>
          <div style="position:absolute;left:{R+2}mm;top:28mm;width:18mm;font-size:7.5pt;font-weight:700;letter-spacing:.8pt;line-height:1.2;color:#b3261e">THEFT</div>
        </div>"""
    doc(f"DESK_voting-scale-strips_one-per-{'story' if 'Story' in cases[0][0] else 'case'}_280x60mm", folder, 280, 60, None,
        pages=[strip(*c) for c in cases])


def tent_card(name, folder, title, meta, desc, *, bg, color, mcolor, font, rule):
    """Folded tent card, 100 x 120 mm flat: the top half prints upside down so both faces read after folding."""
    face = lambda rot: f"""<div style="position:absolute;left:0;right:0;{'top:0' if rot else 'bottom:0'};height:60mm;background:{bg};color:{color};font-family:{font};padding:7mm 7mm 5mm;border-top:2mm solid {rule};{'transform:rotate(180deg)' if rot else ''}">
        {label(title, meta, desc, mcolor=mcolor, tsize=14, dsize=11.5)}</div>"""
    body = face(True) + face(False) + '<div style="position:absolute;left:0;right:0;top:60mm;border-top:.3mm dashed #999"></div>'
    return doc(name, folder, 100, 120, body)


def object_labels(name, folder, items, *, bg, color, mcolor, font, rule, w=200, h=56):
    pages = [f"""<div style="position:absolute;inset:0;background:{bg};border-top:2.5mm solid {rule};padding:5mm 7mm;font-family:{font};color:{color}">
        {label(t, m, d, mcolor=mcolor, tsize=14, dsize=11.5)}</div>""" for t, m, d in items]
    return doc(name, folder, w, h, None, pages=pages)
