"""Compose each section's printed board PDFs into one full-wall PDF.

Positions come from SectionN_Full_Layout/sectionN_layout.html (1 rem = 1 cm on a
120 x 90 cm wall). Chrome draws the cork wall, frame, shadows and caption; the
real board PDFs are then laid on top as vectors with pypdf, so nothing is
rasterised. Output: one A2 and one A3 landscape PDF per section, saved in
section-N/00_full-board/.

Run from Exhibit_Documents/:  python3 _build/build_full_boards.py
"""
import os, re, glob, subprocess, tempfile
from pypdf import PdfReader, PdfWriter, Transformation, PageObject

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MM = 72 / 25.4
CHROME = "google-chrome"

# Board positions in cm on the 120 x 90 cm wall (top-left corner), from the layouts.
POS = {
 1: dict(H=(1, 1), O1=(1, 11.5), O2=(1, 39), O3=(1, 53.1), O4=(1, 74.1), O5=(1, 84),
         K1=(30.83, 11.5), K2=(30.83, 39), K3=(30.83, 57.5), K4=(45.43, 57.5), K5=(30.83, 84),
         RH1=(60.67, 11.5), RH2=(60.67, 39), RH3=(60.67, 52.1), RH4=(60.67, 69.2), RH5=(60.67, 84),
         B1=(90.5, 11.5), B2=(90.5, 39), B3=(90.5, 54.4), B4=(102.1, 54.4), B5=(90.5, 73.3), B6=(90.5, 84)),
 2: dict(H=(1, 1), R1=(1, 11.5), R2=(23.5, 11.5), R3=(1, 43), R4=(20.5, 43), R5=(1, 64), R6=(31.8, 64), R7=(31.8, 76.4),
         H1=(41, 11.5), H2=(63.5, 11.5), H3=(41, 43), H4=(41, 64), H5=(60.5, 64), H6=(60.5, 79.2),
         C1=(81, 11.5), C2=(103.5, 11.5), C3=(81, 43), C4=(81, 57.4), C5=(81, 64), C6=(100.5, 64), C7=(100.5, 79.2)),
 3: dict(H=(1, 1), D1=(1, 11.5), D2=(1, 34.6), D3=(1, 58.4), D4=(31, 34.6), D5=(31, 48.8), D6=(1, 72.8), D7=(47, 72.8),
         HA1=(60.5, 11.5), HA2=(60.5, 34.6), HA3=(60.5, 52.8), HA4=(90.5, 34.6), HA5=(90.5, 47.4), HA6=(90.5, 60.2),
         HA7=(60.5, 72.8), HA8=(100.5, 72.8),
         # side-header strips: page 1 = official record, page 2 = community record
         **{"D1ab:0": (1, 32.4), "D1ab:1": (31, 32.4), "HA1ab:0": (60.5, 32.4), "HA1ab:1": (90.5, 32.4)}),
}
TITLES = {1: "Who Is the Thief?", 2: "What Can Be Taken?", 3: "Who Names the Act and Who Owns the Story?"}
# dashed dividers between the official and community columns (Section 3)
DIVIDERS = {3: [(30.0, 32.4, 72.0), (89.75, 32.4, 72.0)]}

WALL_W, WALL_H, FRAME = 120.0, 90.0, 0.9          # cm
PAPERS = {"A2": (594, 420), "A3": (420, 297)}     # landscape, mm


def board_files(sec):
    out = {}
    for p in glob.glob(f"{ROOT}/section-{sec}/*/BOARD_*.pdf"):
        code = re.match(r"BOARD_([A-Z]+\d*(?:ab)?)_", os.path.basename(p)).group(1)
        out[code] = p
    return out


def geometry(paper):
    pw, ph = PAPERS[paper]
    top, bottom = 0.03 * ph, 0.06 * ph               # margins; caption sits in the bottom one
    k = (ph - top - bottom) / ((WALL_H + 2 * FRAME) * 10)   # paper mm per real mm
    fw = (WALL_W + 2 * FRAME) * 10 * k
    ox = (pw - fw) / 2 + FRAME * 10 * k              # wall origin (inside the frame), mm on paper
    oy = top + FRAME * 10 * k
    return pw, ph, k, ox, oy


def background_html(sec, paper, sizes):
    pw, ph, k, ox, oy = geometry(paper)
    c = lambda v: v * 10 * k                         # cm on the wall -> mm on paper
    f = FRAME * 10 * k
    shadows = "".join(
        f'<div class="sh" style="left:{ox + c(x)}mm;top:{oy + c(y)}mm;width:{c(w)}mm;height:{c(h)}mm"></div>'
        for (x, y), (w, h) in sizes)
    divs = "".join(
        f'<div style="position:absolute;left:{ox + c(x)}mm;top:{oy + c(y0)}mm;height:{c(y1 - y0)}mm;'
        f'border-left:{c(.12)}mm dashed #5a4330"></div>' for x, y0, y1 in DIVIDERS.get(sec, []))
    scale = 1 / k
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size:{pw}mm {ph}mm; margin:0 }}
html,body {{ margin:0; width:{pw}mm; height:{ph}mm; background:#f4f1ea; font-family:'DM Sans','Segoe UI',Arial,sans-serif;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; overflow:hidden }}
.frame {{ position:absolute; left:{ox - f}mm; top:{oy - f}mm; width:{c(WALL_W)}mm; height:{c(WALL_H)}mm;
  border:{f}mm solid #5a4330; box-sizing:content-box;
  background: radial-gradient(circle at 20% 30%, rgba(0,0,0,.06) 0 {c(.08)}mm, transparent {c(.09)}mm) 0 0/{c(.7)}mm {c(.7)}mm,
              radial-gradient(circle at 70% 60%, rgba(255,255,255,.08) 0 {c(.06)}mm, transparent {c(.07)}mm) 0 0/{c(.5)}mm {c(.5)}mm,
              #b98c5d; }}
.sh {{ position:absolute; box-shadow:{c(.12)}mm {c(.18)}mm {c(.35)}mm rgba(0,0,0,.35) }}
.cap {{ position:absolute; left:{ox - f}mm; width:{c(WALL_W) + 2 * f}mm; top:{oy + c(WALL_H) + f + ph * .012}mm;
  display:flex; justify-content:space-between; font-size:{ph * .016}mm; color:#3a2a1a; letter-spacing:.02em }}
.cap b {{ font-weight:700 }}
</style></head><body>
<div class="frame"></div>{shadows}{divs}
<div class="cap"><span><b>Museum of Theft · Section {sec}</b> · {TITLES[sec]} · full board</span>
<span>Wall 120 × 90 cm · printed on {paper} at 1 : {scale:.1f}</span></div>
</body></html>"""


def chrome_pdf(html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", "file://" + fh.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    os.unlink(fh.name)


def build(sec, paper):
    files = board_files(sec)
    items = []                                       # (page, (x,y) cm)
    for key, xy in POS[sec].items():
        code, _, idx = key.partition(":")
        page = PdfReader(files[code]).pages[int(idx or 0)]
        items.append((page, xy))
    sizes = [(xy, (float(p.mediabox.width) / MM / 10, float(p.mediabox.height) / MM / 10)) for p, xy in items]

    pw, ph, k, ox, oy = geometry(paper)
    with tempfile.TemporaryDirectory() as td:
        bg = os.path.join(td, "bg.pdf")
        chrome_pdf(background_html(sec, paper, sizes), bg)
        base = PdfReader(bg).pages[0]
        base.mediabox.upper_right = (pw * MM, ph * MM)
        for page, (x, y) in items:
            w, h = float(page.mediabox.width), float(page.mediabox.height)
            x0, y0 = float(page.mediabox.left), float(page.mediabox.bottom)
            left = (ox + x * 10 * k) * MM
            bottom = (ph - (oy + y * 10 * k)) * MM - h * k  # PDF y runs upward
            t = Transformation().translate(-x0, -y0).scale(k, k).translate(left, bottom)
            base.merge_transformed_page(page, t)
        w = PdfWriter()
        w.add_page(base)
        w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        d = f"{ROOT}/section-{sec}/00_full-board"
        os.makedirs(d, exist_ok=True)
        slug = re.sub(r"[^A-Za-z]+", "-", TITLES[sec]).strip("-")
        out = f"{d}/FULL-BOARD_Section-{sec}_{slug}_{paper}-landscape.pdf"
        with open(out, "wb") as fh:
            w.write(fh)
        print(out)


if __name__ == "__main__":
    for s in (1, 2, 3):
        for paper in ("A2", "A3"):
            build(s, paper)
