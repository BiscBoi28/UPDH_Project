# Museum of Theft — exhibit documents: sources and curation notes

This file records **every source used for the printed board and desk documents**: where each one came from, how it was obtained, and what was done to it. Update it as each section is built.

- `section-1/` — **done**, revised 12 Nov 2026 (real FIR, real news pages, 1897 map, Gazette flip-through)
- `section-2/` — **done** 12 Nov 2026 (`_build/build_section2.py`)
- `section-3/` — **done** 12 Nov 2026 (`_build/build_section3.py`)

## How the folders work

```
Exhibit_Documents/
  SOURCES.md                ← this file
  _build/build_section1.py  ← regenerates every Section 1 PDF (python3 build_section1.py)
  _build/build_section2.py  ← Section 2 (uses _build/common.py, which re-uses the Section 1 helpers)
  _build/build_section3.py  ← Section 3
  _build/assets/section-1/  ← cropped clips of the original documents used on the mounts (also section-2/, section-3/)
  _build/data/              ← news text used for the clipping reproductions
  section-1/
    00_section-header/
    01_ordinary-theft/  02_kleptomania-and-class/  03_robbing-the-rich/  04_the-benin-bronzes/
      BOARD_…pdf            ← goes on the wall board
      DESK_…pdf             ← goes on the table
      BOARD-OR-DESK_…pdf    ← either (see notes)
      original-sources/     ← untouched downloads of the primary documents
    shared-desk-items/      ← voting card (print 4) + 0–10 scale strips (one page per case)
```

- **Every PDF is sized to its real mounted size** (in the file name, e.g. `285x260mm`), matching `Section1_Full_Layout/section1_layout.html`. Print at **100% / "actual size"**, not "fit to page". Items bigger than A4 (the 285 mm-wide panels) print on A3 and get trimmed. The 1180 × 90 mm header strip needs a plotter or banner print, or two A3s tiled.
- The tags (O1, K2, RH3, B5…) match the numbered tags on the layout mock-up.
- Wall text is set at about 18–24 pt in the layout's fonts (Roboto / Unna / Noticia Text), so it can be read standing about 1 m from the board.
- QR strips use the **real** QR codes from `../QR_codes/plain/` (tracks 02–06 of the live audio guide).

## What is real, and what was made for the exhibition

| Kind | Items |
|---|---|
| **Real primary document (clipped or reproduced, unaltered)** | BNS s.303 (Gazette of India) + desk flip-through; Case 1 FIR 0038/2026 (Nagpur Railway Police); Journal of Mental Science 1862; Old Bailey trial pages 1885 and 1895; Stow's *Annales* 1592; the Gest c.1508 print; the Monk ballad (Child's 1888 printing); the 1922 and 1938 posters; the Met plaque photo; the 1897 Berghaus world map; the London Gazette 1897 |
| **Real web pages, captured** (screenshots of the live article, site menus and ads removed) | Al Jazeera 2022; THISDAY 2023; Reuters (in The Star) 2023 |
| **Translation** (made for the exhibition) | English translation of item 12 of the Case 1 FIR |
| **Exhibition graphics** | wall texts, comparison panel, timeline, chain-of-hands diagram, labels, tags, voting card and scales |

---

## Section 1 · Who Is the Thief?

### 00 · Section header
- `BOARD_H_section-header_Who-Is-the-Thief_1180x90mm.pdf` — the Phase 4 intro text from the layout, plus QR 02.

### 01 · Ordinary theft

| File | Where | What |
|---|---|---|
| `BOARD_O1_wall-text_…` | board | Case text |
| `BOARD_O2_government-document_BNS-2023-s303_…` | board | **Clipped from the official Gazette of India** |
| `BOARD_O3_incident-report_FIR-0038-2026_clips_…` | board | **Clips of a real FIR**: page 1 header and page 3 property list |
| `BOARD_O4_how-to-read-this-section_…` | board | Owner / loss / law key |
| `BOARD_O5_QR-audio-strip_…` | board | QR 03 |
| `DESK_O6_incident-report_FIR-0038-2026_Gondia-Railway-PS_6pp_A4` | desk | **The real FIR, all 6 pages, untouched**, on the evidence mat |
| `DESK_O6b_FIR-0038-2026_English-translation_A5` | desk | English translation of the complaint (item 12) |
| `DESK_O7_object-label_props_…` | desk | Label for the wallet, cash, cards and ring |
| `DESK_O8_evidence-number-tents_1-4_A4` | desk | Yellow number tents 1–4 |
| `DESK_O9_government-document_Gazette-of-India_BNS-2023_flip-through_pp1-78-79-102_A4` | desk | **Unclipped Gazette pages** to flip through: p. 1 (masthead and enactment), pp. 78–79 (Section 303 and its illustrations), p. 102 (last page: Secretary's signature and the Government of India Press digital-signature stamp). Print double-sided and staple. |

**Government document — Bharatiya Nyaya Sanhita, 2023, Section 303**
- Source: *The Gazette of India, Extraordinary*, Part II — Section 1, No. 53, New Delhi, 25 December 2023 (CG-DL-E-25122023-250883), Ministry of Law and Justice (Legislative Department). Act No. 45 of 2023.
- URL: https://egazette.gov.in/WriteReadData/2023/250883.pdf (102 pages).
- How: India Code's PDF (`indiacode.nic.in/bitstream/123456789/20062/1/a202345.pdf`) returned an error page. egazette.gov.in serves an incomplete certificate chain, so the missing Let's Encrypt intermediate (YR1, from the certificate's own AIA URL) was downloaded and the PDF fetched **with** TLS verification.
- Section 303 is on **page 78**. Pages 1, 78, 79 and 102 are kept untouched in `original-sources/Gazette-of-India_2023-12-25_BNS-2023_pages-1-78-79-102.pdf` (this same file is the desk flip-through).
- Clip: page 78 rendered at 300 dpi and cropped from "CHAPTER XVII" to the end of Explanation 2. The masthead and Act title come from page 1. The yellow highlights on the two occurrences of *movable* are positioned from `pdftotext -bbox` coordinates.
- The quoted wording on the layout ("Whoever, intending to take dishonestly any movable property…") **matches the Gazette exactly**, so the layout's note "check wording against the official Gazette text" is resolved.
- Explanation 1 ("A thing so long as it is attached to the earth, not being movable property, is not the subject of theft") is now quoted on the label, because it is what Section 3 of the exhibition depends on.

**Incident report — a real First Information Report (FIR No. 0038/2026, P.S. Gondia Railway)**
- The first version was a reconstruction, which read as fake. It has been **replaced with a real FIR** that the police themselves published online.
- Source: Nagpur Railway Police, who publish their FIRs (791 listed at https://www.nagpurrailwaypolice.gov.in/en/fir). This one is https://www.nagpurrailwaypolice.gov.in/en/files/pdf/fir/0038%20-%202026.pdf
- How found: downloaded 260 of the 2025–26 FIRs and searched their text for the Marathi words for pocket, purse, wallet and cash. Then the closest matches were read; 0038/2026 fits the case best.
- What it is: the official CCTNS printout, N.C.R.B. Form I.I.F.-I, "FIRST INFORMATION REPORT (Under Section 173 B.N.S.S)", in English and Marathi. District: Nagpur Railway; P.S. Gondia; registered 01/04/2026 02:00; BNS **303(2)**; accused "unknown" (अनोळखी).
  - On 31/03/2026 at about 23:00 the complainant fell asleep on a bench opposite the booking office at Gondia railway station. A Realme mobile phone (₹17,000) was taken from his trouser pocket, along with a black purse holding his Aadhaar, PAN and voter cards, licence and ₹1,500 cash. Total ₹18,500.
- Saved untouched in `original-sources/FIR_0038-2026_PS-Gondia-Railway_Nagpur-Railway-Police_BNS-303(2).pdf`. The desk copy is the same file.
- Board clips: page 1 (header, items 1–2) and page 3 (item 9 property table), rendered at 200 dpi.
- Translation: item 12 (the complaint) translated from Marathi for the exhibition (`DESK_O6b`).
- **Not redacted**, at the team's request. The FIR is already public on the police website, but it includes the complainant's name, mobile number and address. Decide before the opening whether that is acceptable on display.
- Other police sites that publish FIRs (for Sections 2/3 if needed): Manipur Police (manipurpolice.gov.in/wp-content/uploads/…, scanned paper FIRs), Siliguri Police Commissionerate.

### 02 · Kleptomania and class

| File | Where | What |
|---|---|---|
| `BOARD_K1_wall-text_…` | board | Case text |
| `BOARD_K2_two-verdicts-comparison_…` | board | Sardy (1882) vs Wilson & Hanstead (1895) |
| `BOARD_K3_Journal-of-Mental-Science_1862_…` | board | **Real page 262** of the 1862 article |
| `BOARD_K4_court-records_Old-Bailey-1885-1895_…` | board | **Real court record clips** (replaces the layout's storyboard slot) |
| `BOARD_K5_QR-audio-strip_…` | board | QR 04 |
| `DESK_K6_verdict-tags_x2` | desk | Luggage tags for the two silk trays (lettering resized so "Kleptomania" fits) |
| `DESK_K7_object-label_two-pieces-of-silk` | desk | Label |
| `DESK_K8_reading-copy_Journal-of-Mental-Science_…` | desk | Pages 262 and 266, full |
| `DESK_K9_court-records_Old-Bailey_full-pages_A4` | desk | All 5 trial pages, full |

**Government / official document — Proceedings of the Central Criminal Court (Old Bailey)**
- These are the official printed court proceedings and serve as this case's actual incident reports.
- How found: Old Bailey Online API (`https://www.dhi.ac.uk/api/data/oldbailey_record?text=…&from=…`), searching "Whiteley" (London's big department store), "shopwalker", "shoplifter", and store names (Debenham, Shoolbred, Snelgrove…), then filtering to 1870–1900. Full records came from `oldbailey_record_single?idkey=…`; the page-scan URLs are in each record.
- **t18850914-845 — Georgina Louisa Ryan, September 1885.** Stole 1½ yards of ribbon at Whiteley's, Westbourne Grove.
  - She was a regular customer who banked at the store, defended by Edward Clarke QC, and had £6 10s 8d on her.
  - "The prisoner received an excellent character. NOT GUILTY."
  - Scans: `https://www.dhi.ac.uk/san/ccc/18850914/188509140068.jpg`, `…069.jpg`, `…070.jpg` (pp. 588–590).
- **t18950520-454 — Hannah Wilson (40) and Ann Hanstead (40), May 1895.** Stole 86 yards of silk at De Selincourt & Son, Cannon Street.
  - Wilson "said she was a respectable woman, of Hackney".
  - "GUILTY … previous conviction … Three Years' Penal Servitude."
  - Scans: `https://www.dhi.ac.uk/san/ccc/18950520/189505200015.jpg`, `…016.jpg` (pp. 637–638).
- Rights: "Non-commercial and fair use of this image is allowed without further consent" (Old Bailey Online project). Credit is on the mount.
- **Curatorial care:** the 1895 record does **not** state the women's occupation or class. The comparison panel therefore does not call them "working-class". It says only what the record shows: no doctor, a previous conviction, three years. Keep it that way.
- The layout's "Add an authentic court record of a working-class shoplifter, if found" placeholder is now filled by K4. The **storyboard (layout K4) was not made**: it needs drawings. If you still want it, it could go on the desk.

**Ellen Sardy, New York, 1882 (verified)**
- Source: Elaine S. Abelson, "The Invention of Kleptomania", *Signs* 15:1 (Autumn 1989), pp. 123–143, https://www.jstor.org/stable/3174709. A copy was read from the Freud Museum's PDF (https://www.freud.org.uk/wp-content/uploads/2019/04/Abelson-The-Invention-of-Kleptomania.pdf).
  - It is **not stored in this repo** (copyrighted).
- Confirmed details: 1882; Simpson, Crawford & Simpson, Sixth Avenue; "three pairs of stockings and five pieces of silk"; her lawyer pleaded she had "been of weak mind"; released.
- The wall-text quote "stealing by members of other classes was simple theft" and the Paris newspaper line ("a kind of thief, but of the better class") on K2 are both verbatim from p. 141 of the article.
- Abelson's source for Sardy is the ***New York Times*, 18 January 1882, p. 8, col. 6**. That page is public domain, but NYT TimesMachine needs a subscription, and the Library of Congress newspaper search sits behind a Cloudflare bot check.
  - **TODO (optional):** if anyone has NYT access, download that page as a PDF. It would be the actual 1882 incident report for Sardy.

**The Journal of Mental Science, July 1862 — "Kleptomania"**
- Vol. 8 (April 1862 – January 1863), pp. 262–275. The article opens: "The injudicious defence of two lady thieves on the plea that they were subject to that form of mental unsoundness… kleptomania".
- Scan: Internet Archive item `s5912id1397879` (Wellcome Library digitisation, public domain), https://archive.org/details/s5912id1397879.
- Article pages extracted untouched to `original-sources/Journal-of-Mental-Science_1862-07_Kleptomania_pp262-275.pdf` (scan pages 272–285).
- Page 266 is included on the desk because it ties kleptomania to "that new and peculiar duty of life called 'shopping'".
- Cambridge Core record: https://www.cambridge.org/core/journals/journal-of-mental-science/article/abs/kleptomania/46A448F8BBC0788878EB8B3C73627F5E

### 03 · Robbing the rich

| File | Where | What |
|---|---|---|
| `BOARD_RH1_wall-text_…` | board | Case text |
| `BOARD_RH2_timeline_retellings_…` | board | Timeline |
| `BOARD_RH3_ballad-and-chronicle-extracts_…` | board | **Monk, Gest, Stow: real page clips** |
| `BOARD_RH4_film-posters_1922-1938_…` | board | Real posters |
| `BOARD_RH5_QR-audio-strip_…` | board | QR 05 |
| `DESK_RH6_sign_take-a-hat` | desk | Sign for the hat basket |
| `DESK_RH7_reading-copies_Stow-1592-p227_Child-1888-p99_A4` | desk | Full pages |

- **John Stow, *The Annales of England* (London: Ralfe Newbery, 1592), p. 227.** "In this time were many robbers and out-lawes, among the which, Robert Hood, and litle John, renowmed theeues… poore mens goodes hee spared, aboundantly releeuing them with that, which by thefte hee gote from Abbeyes and the houses of riche Carles".
  - Internet Archive `bim_early-english-books-1475-1640_the-annales-of-england-_stow-john_1592` (Early English Books scan), page image `page/n250`.
  - Found by searching the item's OCR text index for "Hood" (the OCR uses the long s, ſ).
- ***Robin Hood and the Monk*, c.1450** (Child 119). The original is Cambridge University Library MS Ff.5.48, fols. 128v–135v. No free digital facsimile of the manuscript was found online. The extract is therefore **Child's 1888 printed transcription**: F. J. Child, *The English and Scottish Popular Ballads*, vol. 3 (Boston, 1888), p. 99, stanzas 48–52. Internet Archive `englishscottishp31chilrich`, page `n112`.
  - Content check: Little John beheads the monk, and Much kills the monk's page "for ferd lest he wolde tell". The timeline now says "His men kill a monk and his page."
- ***A Gest of Robyn Hode*, Chepman & Myllar print, Edinburgh, c.1508**, opening page ("Here begynneth a gest of Robyn Hode").
  - Wikimedia Commons `File:Here begynneth a gest of Robyn Hode.png`, from the National Library of Scotland's *First Scottish Books* site (folio 197). Public domain.
  - Only 350 × 581 px is available (the NLS viewer is behind a CAPTCHA), which is fine at the small size used on the mount.
- **Posters** (Wikimedia Commons, public domain in the US). Both are cropped to the printed art and shown at the same size. The 1922 file is a "window card" with a blank panel at the top for cinemas to write in; that panel is cut off.
  - `File:Douglas Fairbanks Robin Hood 1922 film poster.jpg` (United Artists; published before 1929)
  - `File:The Adventures of Robin Hood (1938 poster).jpg` (Warner Bros.)
- Not used: the 1225–26 Pipe Roll entry for "Robertus Hod, fugitivus" (The National Archives, E 372/71) would be a real government record, but no free image was found.

### 04 · The Benin Bronzes

| File | Where | What |
|---|---|---|
| `BOARD_B1_wall-text_…` | board | Case text |
| `BOARD_B2_chain-of-hands-diagram_…` | board | Diagram |
| `BOARD_B3_plaque-image_Met-1990.332_…` | board | Real plaque photo |
| `BOARD_B4_map_…` | board | **Real 1897 world map** (detail), unmarked so the team can add routes by hand |
| `BOARD_B5_news-clippings_2022-2023_…` | board | Clippings (top of each article) of the three real news articles |
| `BOARD_B6_QR-audio-strip_…` | board | QR 06 |
| `BOARD-OR-DESK_B7_government-document_London-Gazette_1897-05-07_A4` | **desk recommended** (the board has no A4 slot) | **The official 1897 account** |
| `DESK_B8_news_Al-Jazeera_2022-10-12_A4` | desk | Full article, as a browser printout |
| `DESK_B9_news_ThisDay_2023-04-13_Nigeria-gazette_A4` | desk | Full article: the Nigerian Gazette notice |
| `DESK_B10_news_Reuters-in-The-Star_2023-05-11_A4` | desk | Full article: returns delayed by the decree |
| `DESK_B11_object-label_replica-plaque` | desk | Label |

**Government document — *The London Gazette*, 7 May 1897, issue 26850**
- This is both the government document and the incident report for this case. It prints Rear-Admiral Harry Rawson's despatches "reporting operations against the King of Benin, and the capture of Benin City" (p. 2516), with the column commander's report (pp. 2531–2532).
- p. 2532 describes "carved ivory tusks… mounted at base, in hideously-constructed brass heads", says the compounds "commenced to be burnt", and says a fire "destroyed the King's and all surrounding quarters".
- **It never says the objects were removed.** That silence is the point of the mount.
- URLs: `https://www.thegazette.co.uk/London/issue/26850/page/2516/data.pdf` (and pages 2517–2520, 2531–2534).
- Pages 2516–2520 and 2531–2533 are kept untouched in `original-sources/`.
- Rights: Crown copyright, Open Government Licence.

**Image — brass plaque.** *Plaque with Warrior and Attendants*, Edo peoples, c.1540–70, brass, 47.6 × 38.1 cm, The Metropolitan Museum of Art, 1990.332, Gift of Mr. and Mrs. Klaus G. Perls, 1990. Open Access / CC0. https://www.metmuseum.org/art/collection/search/316393
- On the board the photo is cropped to the brass itself so it fills the frame (no studio backdrop).
- Found with the Met Collection API. The old `/v1/search` was retired on 2026-10-01, so `/public/collection/v1.1/search?q=Benin plaque` was used.
- The Met's object page did not return its provenance text to a script. The label therefore does **not** state this plaque's own 1897 history; it speaks about plaques generally.

**Map.** Hermann Berghaus, *Chart of the World on Mercator's Projection* (Gotha: Justus Perthes, **1897**), the year of the raid. Wikimedia Commons `File:1897 map of the world by Hermann Berghaus.jpg` (public domain; scan from Barry Lawrence Ruderman Antique Maps). The 6,000 px version was used, cropped to the Atlantic world (Washington DC, London, Berlin, Gulf of Guinea). No markings; the team will add routes by hand.

**News articles (real pages, captured from the live websites)**
- Captured with `_build/capture_article.mjs`. It loads the page in headless Chrome, finds the article (the block around the headline), hides site menus, ads, cookie and subscription boxes, and screenshots only the article at 2× resolution. The text and images are the publisher's own.
- Desk copies are laid out like Chrome's own "Print" output (date and page title at the top, URL and page number at the bottom), cut between paragraphs. Board clippings are the top of each article.
- **Al Jazeera, 12 Oct 2022**, "US returns Benin Bronzes stolen by British colonial forces": https://www.aljazeera.com/news/2022/10/12/us-returns-african-bronzes-stolen-by-british-colonial-forces
- **THISDAY, 13 Apr 2023**, "FG Issues Gazette Recognising Ownership, Vesting Custody of Repatriated Looted Artefacts in Oba of Benin": https://www.thisdaylive.com/2023/04/13/breaking-fg-issues-gazette-recognising-ownership-vesting-custody-of-repatriated-looted-artefacts-in-oba-of-benin/
  - It quotes Government Notice No. 25, Federal Republic of Nigeria Official Gazette No. 57, Vol. 110, 28 March 2023. The Nigerian gazette PDF itself was **not found online**.
- **Reuters, 11 May 2023**, by MacDonald Dzirutwe, "Return of Benin Bronzes delayed after Nigerian president's decree", as published by The Star (Malaysia): https://www.thestar.com.my/news/world/2023/05/11/return-of-benin-bronzes-delayed-after-nigerian-president039s-decree
  - reuters.com itself blocks automated browsers.
- Dropped: the re-typeset Smithsonian press release and Art Newspaper text, which read as fake.

---

## Section 2 · What Can Be Taken?

Layout source: `Section2_Full_Layout/section2_layout.html` (tags R1–R12, H1–H12, C1–C13). Wall text is the Phase 4 text from that file. Each story is styled in its own template, as on the mock-up: Victorian for rubber, permission slip for Havasupai, content table for Clearview.

### 00 · Section header
`BOARD_H` 1180 × 90 mm. QR code: `07_What_Can_Be_Taken.png`.

### 01 · Seventy Thousand Seeds (rubber)

**Government document: Britain's verdict (R3).** *The London Gazette*, Second Supplement of Friday 4 June 1920, published Saturday 5 June 1920, issue 31931.
- Page 6313 is the masthead. Page 6315 has the Knights Bachelor list: "Henry Alexander Wickham, Esq. For services in connection with the rubber plantation industry in the Far East."
- Found via Wikipedia's *1920 Birthday Honours* list, which cites issue 31931, pp. 6313–6320.
- Downloaded from `https://www.thegazette.co.uk/London/issue/31931/supplement/6313/data.pdf` and `/6315/data.pdf`. The Wickham entry was located with `pdftotext`.
- Clips were made at 300 dpi. The entry is highlighted on the board.
- Both pages are kept untouched in `original-sources/` and as desk copy `DESK_R11`. Crown copyright, Open Government Licence.

**Brazil's verdict (R4).** Carlos Haag, "As sementes da discórdia", *Pesquisa FAPESP* no. 158, April 2009, pp. 22–25.
- The real print pages come as a PDF linked from the article page: `https://revistapesquisa.fapesp.br/wp-content/uploads/2009/04/As-sementes-da-discórdia.pdf`. The web article is at `https://revistapesquisa.fapesp.br/as-sementes-da-discordia/`.
- The board shows the title and the opening column, with the passage "Por décadas discutiu-se … 'pai da biopirataria'" highlighted (positions from `pdftotext -bbox`). It also shows the photo "Henry Wickham: ladrão ou herói?".
- The English is the magazine's **own** English edition: `https://revistapesquisa.fapesp.br/en/the-seeds-of-discord/`. Printed unedited from that page (browser print, 12 Nov 2026) as `DESK_R10_magazine_Pesquisa-FAPESP-2009_The-seeds-of-discord_ENGLISH.pdf`, kept next to the Portuguese pages so visitors can read the whole article in English.
- Licence: CC BY-NC-ND (stated on the article page). It is reproduced unedited, with credit.
- The full 4-page PDF is the desk copy `DESK_R10`.
- Not found: Wickham's 1908 book (the "exceedingly delicate botanical specimens" account) has no free scan on the Internet Archive, BHL or Open Library. The FAPESP pages quote the same customs story.

**Map (R5).** The same Berghaus 1897 world map as Section 1, cropped from Brazil to Malaya. The route is printed over it (revised 12 Nov 2026): seeds, 1876, Tapajós (Santarém) → Belém → Liverpool → Kew, dashed; seedlings from 1876, Kew → Ceylon → Malaya (Singapore), solid. Stops are placed by latitude and longitude on the map's Mercator grid. The sea lanes are drawn schematically (the Kew–Ceylon line runs through Suez); the legend names only the stops.

**Made for the exhibition.** R1 (wall text), R2 (timeline drawn to scale), R6 (map label), R9 (seed tent card).

### 02 · What the Blood Was For (Havasupai)

**Wall text (H1), revised 12 Nov 2026.**
- "Type 2 diabetes was common in the tribe and growing, and its members wanted answers and help": Wikipedia, "Havasupai Tribe v. the Arizona Board of Regents" (high rates of type II diabetes; the tribe's concern about rising rates). Secondary source: check against Mello & Wolf, *NEJM* 362 (2010), or Amy Harmon, *New York Times*, 21 Apr 2010, before printing.
- "Proposed a diabetes project … help address diabetes … attend its classes for free": the Joint Answering Brief, p. 3 (the Tribe's complaint, ¶¶ 30–32), and the Tribe's notice of claim quoted in the brief ("a diabetes education, nutrition and genetics research project").
- "ASU's researchers say these studies belonged to the same research …": Dr Markow's declaration, quoted in the brief, footnote 3 and p. 4 (the script read to donors: "factors that cause some of the health problems experienced by the Havasupai … diabetes, schizophrenia, depression …").

**Court record (H3).** Joint Answering Brief of the defendants (Therese Markow and the Arizona Board of Regents), *Havasupai Tribe v. Arizona State University Board of Regents*, Arizona Court of Appeals, Division One, No. 1 CA-CV 07-0454 (2007).
- Original posted by Turtle Talk (turtletalk.blog), fetched through the Wayback Machine because the live site returns 403: `https://web.archive.org/web/20260901003820/https://turtletalk.blog/wp-content/uploads/2008/12/joint-answering-brief.pdf`.
- Clips come from page 3, the Tribe's allegations, and from footnote 3 and page 4, the script Dr Markow said donors were read: "…Many of these diseases, such as diabetes, schizophrenia, depression…". The board shows both sides in the court's own record.
- Desk copy `DESK_H11` is the cover plus pp. 3–4. The full 58-page brief is in `original-sources/`.
- Not obtained: the 2008 Court of Appeals opinion. Leagle and CourtListener refuse automated access (403 / empty), and the azcourts.gov PDF returns 403.

**Press release (H5, replaces the mock-up's placeholder).** "Havasupai Tribe and Arizona Board of Regents Resolve Lawsuit, Announce Future Collaborations", joint press release, 21 April 2010, 2 pages.
- Fetched through Wayback from turtletalk.blog: `…/wp-content/uploads/2010/04/havasupai-asu-press-release.pdf`.
- It carries the Havasupai members' own words at the 2010 return: Councilwoman Carletta Tilousi ("…helps us to rebuild what we have lost") and Chairwoman Bernadine Jones ("the restoration of hope for my people").
- Full copy on the desk: `DESK_H10`. It shows the press contacts' phone numbers as published; nothing is redacted.

**Map (H4).** US National Park Service, *Grand Canyon National Park* map (public domain), via Wikimedia Commons `File:NPS grand-canyon-national-park-map.jpg`.
- Cropped to the Havasupai Reservation and Grand Canyon Village. Nothing is added; Supai is printed on the NPS map.

**News (desk H12).** Inside Higher Ed, "Arizona Regents Settle Dispute Over Use of Indian Blood", 21 April 2010: https://www.insidehighered.com/quicktakes/2010/04/22/arizona-regents-settle-dispute-over-use-indian-blood
- Captured with `capture_article.mjs`; the site footer was cut.
- The NBC News copy of the NYT report ("Tribe wins fight over research on its DNA") rendered blank in headless Chrome, so it was dropped.

**Made for the exhibition.** H1 (wall text), H2 (diagram), the three "versions" cards in H3, the H5 checklist, H9 (tent card).

### 03 · A Search Engine for Faces (Clearview AI)

**Government documents (C5, desk C14).** Office of the Privacy Commissioner of Canada.
- *PIPEDA Findings #2021-001*, 2 February 2021: https://www.priv.gc.ca/en/opc-actions-and-decisions/investigations/investigations-into-businesses/2021/pipeda-2021-001/
- News release, 3 February 2021, "Clearview AI's unlawful practices represented mass surveillance of Canadians, commissioners say": https://www.priv.gc.ca/en/opc-news/news-and-announcements/2021/nr-c_210203/
- Both pages were captured with `capture_article.mjs`. The board shows the report's title block and the news release's quote from Daniel Therrien ("What Clearview does is mass surveillance and it is illegal…").
- The "512 data points" figure in C2 is from the report's own text.

**Government document (desk C15).** Autoriteit Persoonsgegevens (Dutch DPA), "Dutch DPA imposes a fine on Clearview because of illegal data collection for facial recognition", 3 September 2024: https://www.autoriteitpersoonsgegevens.nl/en/current/dutch-dpa-imposes-a-fine-on-clearview-because-of-illegal-data-collection-for-facial-recognition
- Captured; it backs the €30.5 million line in C6. TechCrunch was tried, but it redirected to a different article, so it was dropped.

**Photos (C3).** Stills from the exhibition's own video `Actual_Audio_Guide/Video/Clearview_Face_Search_Narrated.mp4`, at 4 s (the three posts) and 19.6 s (the street photo), taken with `ffmpeg`.
- These are the "same photos used in the video", as the mock-up asked: staged, with a consenting volunteer, on fictional `.example` sites.

**Made for the exhibition.** C1 (wall text), C2 (faceprint, illustrative numbers), C4 (pipeline), C6 (rulings table), C9 (label), C13 (card).

### Shared desk items (Section 2)
Voting card (print 3) and one 0–10 strip per story, in each story's colour.

---

## Section 3 · Who Names the Act and Who Owns the Story?

Layout source: `Section3_Full_Layout/section3_layout.html` (tags D1–D14, HA1–HA14). Each case has a case panel, then **Side A · the official record** and **Side B · the community's record**. The side-header strips are `…_side-headers_…_2pp.pdf`.

### 00 · Section header
QR code: `11_Who_Names_the_Act.png`.

### 01 · The Dawes Act

**Side A · D2. "Indian Land for Sale"**, US Department of the Interior poster, 1911 (signed Walter L. Fisher and Robert G. Valentine).
- Wikimedia Commons `File:Indian Land for Sale Advertisement.jpg` (1576 × 2031, public domain). The original is in the Library of Congress (loc.gov blocks scripts).

**Side A · D3. The Act and the rolls.**
- The Dawes Act, enrolled original signed 8 February 1887, 2 pages at 300 ppi: NARA via DPLA, Commons `File:Dawes Act of 1887 - DPLA - 7bacd2372092b028acda7a0524f7c388.pdf`. Full copy on the desk as `DESK_D15`.
- *Index to the Final Rolls of Citizens and Freedmen of the Five Civilized Tribes in Indian Territory* (1907), p. 297 "Cherokees by Blood", and the title page. Internet Archive `index-to-the-final-rolls-of-citizens-and-freedmen-of-the-five-civilized-tribes-in-indian-territory`, leaves 0 and 300. Desk copy: `DESK_D18`.
- A Commons "Dawes enrollment jacket" scan was checked, but it was a blank folder cover, so it is not used.

**Side B · D4. Cherokee protest to Congress.** *Protest of the Cherokee Nation against the passage of House Bill (6309)*, Washington, 5 March 1896.
- Library of Congress copy on the Internet Archive (`protestofcheroke00cher`, "NOT_IN_COPYRIGHT"). It replaces the mock-up's "Cherokee memorials c.1900" placeholder.
- Clips: the cover; p. 9, "Allotment of lands"; and p. 10, "Congress has no more right to force a division of the use of the lands of the Cherokees…". Desk copy: `DESK_D17`.

**Side B · D5. Redbird Smith.** *Report of the Select Committee to Investigate Matters Connected with Affairs in the Indian Territory, with Hearings, Nov. 11, 1906–Jan. 9, 1907*, Senate Report No. 5013, 59th Congress, 2nd session, vol. 1.
- Internet Archive `cu31924097702090` (Cornell copy). The testimony was found in the OCR text; the printed pages are 97–98 (leaves 112–113).
- Exact quotation on the board: "I never consented to any agreement to divide up my land, and I don't want it divided up. I want the old treaty."
- Desk copy `DESK_D16` is the title page plus pp. 97–98.

**D6. Map.** "Map showing Indian reservations within the limits of the United States", 1894 (Report on Indians Taxed and Not Taxed, Eleventh Census). Internet Archive `reportonindianst1894unit`, via Commons.
- Next to it are two squares drawn to scale: about 138 million acres in 1887 and about 48 million in 1934. These are the standard figures, the same as the wall text's "about 90 million acres".

**Made for the exhibition.** D1 (case panel); D8 (mock ledger, marked as a reconstruction); D9 (SURPLUS stamp artwork); D11 (labels).

### 02 · The Hasdeo Arand Forest

**Side A · HA2. Forest clearance.** Ministry of Environment & Forests, F. No. 8-31/2010-FC, Stage-II approval dated 15 March 2012, for diverting 1,898.328 ha for the Parsa East and Kete Basan coal block. Addressed to the Principal Secretary (Forests), Chhattisgarh.
- The original on forestsclearance.nic.in could not be located. The copy used is the **"True copy" filed as Annexure R-2** in RRVUNL's reply affidavit before the National Green Tribunal, O.A. No. 59 of 2024: `https://www.greentribunal.gov.in/sites/default/files/news_updates/AFFIDAVIT BY R-4 RRVUNL IN OA NO. 59 of 2024 NEWS ITEM TITLED DEFORESTATION FOR MINING RESUMES IN HASDEO LOCALS ACTIVISTS ALLEGE DETENTION.pdf`. It is PDF pages 63–66, extracted unchanged with `pdfseparate`.
- The scan is only about 150 ppi, so the board clip is enlarged and prints slightly soft.
- The same affidavit carries Annexure R-4: the NGT judgment of 24 March 2014 in Appeal 73/2012 (*Sudiep Shrivastava v. State of Chhattisgarh*), PDF pages 70–119. It is in `original-sources/`, and its first 6 pages are on the desk as `DESK_HA16`.

**Side A · HA3. Company report.** Adani Natural Resources, *ESG Report 2023-24: Crafting Contours, Sustainable Mining*. The board shows the cover and p. 57: "No. of Trees Planted 3,37,960" and "Sal Regeneration at PEKB Coal Block".
- Source: `https://www.adanienterprises.com/-/media/Project/Enterprises/Sustainability/Adani-ESG-Report-202324-24042025.pdf`
- Extract reproduced for comment and review. The full report is **not** copied into the repo; only the link is kept here, as with the Abelson article.

**Side B · HA4. The movement's own statement.** Hasdeo Aranya Bachao Sangharsh Samiti, call for a "gathering of gram sabhas" at Fattepur on 2 October and a 10-day march to Raipur, English version, 4 pages, published by Survival International: `https://assets.survivalinternational.org/documents/2018/notice-for-gathering-and-march.pdf`
- The text refers to a 75-day protest at Fattepur in 2019, so the statement is from after that, although the file sits in a "2018" folder.
- It replaces the mock-up's "gram sabha resolution" placeholder. The resolutions themselves (Hindi originals) were not found online; this document records them in the movement's own words ("In 2015, 20 gram sabhas … had passed motions"). Full copy: `DESK_HA17`.

**Side B · HA5. Ghatbarra.**
- Community forest titles were granted in 2013. The cancellation order is dated 8 January 2016.
- The Chhattisgarh High Court dismissed the village's petition (WPC 1346/2016) on 8 October 2025.
- Sources: The Wire, Nitin Sethi, 17 Feb 2016 (originally Business Standard): https://m.thewire.in/article/agriculture/chhattisgarh-govt-cancels-tribal-rights-over-forests-to-facilitiate-coal-mining/amp ; Down To Earth, Himanshu Nitnaware, 17 Nov 2025, "Setback in Hasdeo": https://www.downtoearth.org.in/forests/setback-in-hasdeo
- Both were captured. The Wire's donation box was removed, and DTE was cut at its paywall line. Desk copies: `DESK_HA18`, `DESK_HA20`.
- The order itself (a scan) was not found online.

**HA6. Photograph.** No openly licensed photo of the Hasdeo protests exists (Openverse and Commons were searched).
- The board uses Mongabay India's own photo of the Parsa block felling, credited "Image by Ramlal Kariyam", from Simrin Sirur, "Chhattisgarh tribal body says consent for mining in Hasdeo Arand was forged", 28 Nov 2024: https://india.mongabay.com/2024/11/chhattisgarh-tribal-body-says-consent-for-mining-in-hasdeo-arand-was-forged/ (full article on the desk: `DESK_HA19`).
- **TODO: confirm print permission with the photographer or Mongabay before the opening.**
- Mongabay's other image, a 2018 protest banner (GOI Monitor, CC BY-SA), is labelled "representational" and is *not* from Hasdeo, so it was not used.

**HA7. Map.** OpenStreetMap, zoom 11, 35 tiles from `tile.openstreetmap.org`, fetched once with a descriptive user agent and stitched.
- Area: about 82.15–83.15°E, 22.45–23.15°N, which shows the forest cover, the Hasdeo Bango reservoir and the existing open-cast pits near Udaypur.
- © OpenStreetMap contributors, ODbL. Unmarked: the team marks the coal blocks and villages by hand. It replaces the mock-up's "schematic only" drawing.

**Made for the exhibition.** HA1 (case panel), HA9 (felling tag prop), HA10 (jar labels), HA11 (labels).

### Shared desk items (Section 3)
Voting card (print 2) and one strip per case.

---

## Tools and method
- Downloads: `curl`; Internet Archive metadata, search, OCR index and page-image endpoints; the Old Bailey API; the Wikimedia Commons API; the Met API.
- PDF handling: `pdfseparate` / `pdfunite` (poppler) to extract untouched original pages; `pdftoppm -r 300` plus ImageMagick `convert -crop` for the clips; `pdftotext -bbox` to position highlights.
- Web articles: `_build/capture_article.mjs <url> <out.png> [css selector] [extra selectors to remove]`. It needs Node 22+ (built-in WebSocket) and Google Chrome.
- Layout: HTML/CSS at real millimetre size → headless Google Chrome `--print-to-pdf`. A small script shrinks text until it fits each box.
- Sites that blocked automated access (bot checks or CAPTCHAs): si.edu, loc.gov / Chronicling America, digital.nls.uk, edostate.gov.ng, smithsonianmag.com, nga.gov. Each was replaced by the alternative noted above.
- Also blocked or refused in Sections 2–3: leagle.com, courtlistener.com, azcourts.gov, turtletalk.blog (fetched via the Wayback Machine instead), nps.gov/carto (served HTML instead of PDFs; Commons used), the NBC News article page (renders blank), techcrunch.com (redirects).
- Video stills: `ffmpeg -ss <t> -i video.mp4 -frames:v 1 out.png`.
