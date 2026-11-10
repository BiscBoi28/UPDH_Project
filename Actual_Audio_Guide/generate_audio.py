"""
Museum of Theft: build the audio guide from the transcript.

Reads   Transcript/tracks/*.txt        (one plain-text script per track)
Writes  Audio/wav/NN_Title.wav         (masters, 24 kHz mono)
        Audio/mp3/NN_Title.mp3         (for phones / QR codes)
        Audio/Museum_of_Theft_Complete_Audio_Guide.(wav|mp3)
        Audio/Clearview_Video_Voiceover.(wav|mp3)   (32 s, timed to the video)
        Video/Clearview_Face_Search_Narrated.mp4    (video + voiceover)
        Transcript/Audio_Guide_Transcript.md        (full transcript with real durations)

Run it with the Kokoro environment:
    ..\\Audio_Guide\\venv-main\\Scripts\\python.exe generate_audio.py
To change wording, edit the .txt files in Transcript/tracks and run it again.
"""
import io
import re
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import soundfile as sf

warnings.filterwarnings("ignore")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = Path(__file__).resolve().parent
TRACK_DIR = HERE / "Transcript" / "tracks"
AUDIO = HERE / "Audio"
VIDEO_OUT = HERE / "Video" / "Clearview_Face_Search_Narrated.mp4"
VIDEO_IN = HERE.parent / "Clearview_Face_Search_Loop.mp4"

# ----------------------------------------------------------------- settings
VOICE = "af_heart"
SPEED = 0.90            # Kokoro's 1.0 is about 180 words a minute: too fast for a guide
SR = 24000
LEAD_IN = 0.35          # silence before the first word of a track (seconds)
PARA_GAP = 0.60         # silence between paragraphs
TAIL = 0.80             # silence after the last word
TRACK_GAP = 1.50        # silence between tracks in the complete file
TARGET_RMS_DB = -18.0   # speech level every track is matched to
PEAK_LIMIT_DB = -1.0

# Video voiceover: where each line starts (seconds), from suggestion_video.md
VIDEO_LEN = 32.0
BEATS = [0.5, 6.0, 13.0, 18.0, 25.0]
VO_SPEED = 0.95

# (file stem, title, section, where the QR code is)
TRACKS = [
    ("01_welcome", "Welcome to the Museum of Theft", "Entrance", "Entrance, beside the entry poll"),
    ("02_section1_who_is_the_thief", "Who Is the Thief?", "Section 1: Who Is the Thief?", "Section 1 header"),
    ("03_ordinary_theft", "A Wallet on a Crowded Street", "Section 1: Who Is the Thief?", "Case 1 · Ordinary Theft"),
    ("04_kleptomania_and_class", "Two Shoplifters, One Counter", "Section 1: Who Is the Thief?", "Case 2 · Kleptomania and Class"),
    ("05_robbing_the_rich", "Robbing the Rich", "Section 1: Who Is the Thief?", "Case 3 · Robin Hood"),
    ("06_benin_bronzes", "The Benin Bronzes", "Section 1: Who Is the Thief?", "Case 4 · The Benin Bronzes"),
    ("07_section2_what_can_be_taken", "What Can Be Taken?", "Section 2: What Can Be Taken?", "Section 2 header"),
    ("08_seventy_thousand_seeds", "Seventy Thousand Seeds", "Section 2: What Can Be Taken?", "Story 1 · Rubber, beside the seed"),
    ("09_what_the_blood_was_for", "What the Blood Was For", "Section 2: What Can Be Taken?", "Story 2 · Havasupai"),
    ("10_a_search_engine_for_faces", "A Search Engine for Faces", "Section 2: What Can Be Taken?", "Story 3 · Clearview AI, beside the laptop"),
    ("11_section3_who_names_the_act", "Who Names the Act?", "Section 3: Who Names the Act and Who Owns the Story?", "Section 3 header"),
    ("12_the_dawes_act", "The Dawes Act", "Section 3: Who Names the Act and Who Owns the Story?", "Case 1 · The Dawes Act"),
    ("13_the_hasdeo_arand_forest", "The Hasdeo Arand Forest", "Section 3: Who Names the Act and Who Owns the Story?", "Case 2 · Hasdeo Arand, beside the two jars"),
    ("14_exit_has_your_definition_changed", "Has Your Definition Changed?", "Exit", "Exit, beside the exit poll"),
]
VO_STEM = "V1_clearview_video_voiceover"

# Pronunciations Kokoro gets wrong on its own: word -> (phonemes, plain-letters cue)
PRON = {
    "303": ("θɹˈi ˈO θɹˈi", "three-oh-three"),
    "Bharatiya": ("bˈɑɹətijə", "BHAA-ruh-tee-yuh"),
    "Nyaya": ("njˈɑjə", "NYAA-yuh"),
    "Sanhita": ("sˈʌnhɪtɑ", "SUN-hi-taa"),
    "Oba": ("ˈObɑ", "OH-bah"),
    "Wickham": ("wˈɪkəm", "WICK-um"),
    "Lanka": ("lˈɑŋkə", "LAHNG-kuh"),
    "Havasupai": ("hˌɑvəsˈupI", "hah-vuh-SOO-pie"),
    "Tilousi": ("tɪlˈusi", "tih-LOO-see"),
    "Keetoowah": ("kitˈuwɑ", "kee-TOO-wah"),
    "Hasdeo": ("hˈʌsdAˌO", "HUS-day-oh"),
    "Arand": ("ˈɑɹənd", "AH-rund"),
    "Chhattisgarh": ("ʧˈʌtisɡˌʌɹ", "CHUT-tees-gur"),
    "Adivasi": ("ˌɑdivˈɑsi", "aa-dee-VAA-see"),
    "Adani": ("ədˈɑni", "uh-DAA-nee"),
    "Ghatbarra": ("ɡɑtbˈʌɹɑ", "ghaat-BUR-raa"),
}


def tts_text(text: str) -> str:
    """Mark the words in PRON with Kokoro's [word](/phonemes/) syntax."""
    for word, (ph, _) in PRON.items():
        def sub(m, ph=ph):
            poss = m.group(2) or ""
            return f"[{m.group(1)}{poss}](/{ph}{'z' if poss else ''}/)"
        text = re.sub(rf"(?<![\w\[])({re.escape(word)})(['’]s)?(?![\w\]])", sub, text)
    return text


def db(x):
    return 20 * np.log10(max(float(x), 1e-9))


def trim(x, thresh_db=-45.0, keep=0.03):
    """Cut silence from both ends so the pauses are the ones set above."""
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(1))
    loud = np.where(20 * np.log10(rms + 1e-9) > thresh_db)[0]
    if len(loud) == 0:
        return x
    a = max(loud[0] * win - int(keep * SR), 0)
    b = min((loud[-1] + 1) * win + int(keep * SR), len(x))
    return x[a:b]


def silence(seconds):
    return np.zeros(int(round(seconds * SR)), dtype=np.float32)


def speech_rms_db(x):
    win = int(0.05 * SR)
    n = len(x) // win
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(1))
    level = 20 * np.log10(rms + 1e-9)
    active = rms[level > level.max() - 30]
    return db(np.sqrt((active ** 2).mean()))


def match_level(x):
    """Bring the speech to the same level in every track, then hold the few stray peaks under the limit."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    x = x * 10 ** ((TARGET_RMS_DB - speech_rms_db(x)) / 20)
    ceiling = 10 ** (PEAK_LIMIT_DB / 20)
    win = int(0.005 * SR)                                   # 5 ms look-ahead
    need = np.minimum(1.0, ceiling / np.maximum(np.abs(x), 1e-9))
    gain = uniform_filter1d(minimum_filter1d(need, size=2 * win + 1), size=win)
    return (x * gain).astype(np.float32)


def say(pipe, text, speed):
    """Speak one paragraph. Returns (audio, phoneme string)."""
    audio, phon = [], []
    for r in pipe(tts_text(text), voice=VOICE, speed=speed, split_pattern=None):
        if r.audio is None or len(r.audio) == 0:
            raise RuntimeError(f"Kokoro returned no audio for: {r.graphemes[:60]!r}")
        audio.append(r.audio.detach().cpu().numpy().astype(np.float32))
        phon.append(r.phonemes)
    return trim(np.concatenate(audio)), " ".join(phon)


def paragraphs(stem):
    text = (TRACK_DIR / f"{stem}.txt").read_text(encoding="utf-8").strip()
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def n_words(text):
    return len(re.findall(r"[A-Za-z0-9$’'-]+", text))


def mmss(seconds):
    return f"{int(seconds // 60)}:{int(round(seconds % 60)):02d}"


def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ffmpeg(args):
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)


def write_pair(wav_path: Path, mp3_path: Path, x):
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(wav_path, x, SR, subtype="PCM_16")
    run_ffmpeg(["-i", str(wav_path), "-ar", "44100", "-ac", "1",
                "-c:a", "libmp3lame", "-b:a", "96k", str(mp3_path)])


def file_title(stem, title):
    return stem[:2] + "_" + re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")


# ----------------------------------------------------------------- build
def build_tracks(pipe):
    rows, parts = [], []
    for stem, title, section, where in TRACKS:
        paras = paragraphs(stem)
        chunks, checks = [silence(LEAD_IN)], []
        for i, p in enumerate(paras):
            audio, phon = say(pipe, p, SPEED)
            rate = len(phon.replace(" ", "")) / (len(audio) / SR)   # phonemes per second
            checks.append(rate)
            chunks.append(audio)
            chunks.append(silence(PARA_GAP if i < len(paras) - 1 else TAIL))
        x = match_level(np.concatenate(chunks))
        name = file_title(stem, title)
        write_pair(AUDIO / "wav" / f"{name}.wav", AUDIO / "mp3" / f"{name}.mp3", x)
        dur = len(x) / SR
        words = sum(n_words(p) for p in paras)
        rows.append(dict(stem=stem, title=title, section=section, where=where, name=name,
                         dur=dur, words=words, paras=paras,
                         wpm=words / dur * 60, peak=db(np.abs(x).max()),
                         rate_min=min(checks), rate_max=max(checks)))
        parts.append(x)
        print(f"{name:45s} {mmss(dur)}  {words:3d} words  {words / dur * 60:5.0f} wpm  "
              f"peak {db(np.abs(x).max()):5.1f} dB  phonemes/s {min(checks):.1f}-{max(checks):.1f}")
    joined = []
    for i, x in enumerate(parts):
        joined.append(x)
        if i < len(parts) - 1:
            joined.append(silence(TRACK_GAP))
    complete = np.concatenate(joined)
    write_pair(AUDIO / "Museum_of_Theft_Complete_Audio_Guide.wav",
               AUDIO / "Museum_of_Theft_Complete_Audio_Guide.mp3", complete)
    print(f"{'COMPLETE GUIDE':45s} {mmss(len(complete) / SR)}")
    return rows, len(complete) / SR


def build_voiceover(pipe):
    lines = [l.strip() for l in (TRACK_DIR / f"{VO_STEM}.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == len(BEATS), "the voiceover needs one line per beat"
    speed = VO_SPEED
    while True:
        clips = [say(pipe, l, speed)[0] for l in lines]
        starts, ok = [], True
        for i, c in enumerate(clips):
            start = BEATS[i]
            length = len(c) / SR
            limit = (BEATS[i + 1] - 0.25) if i < len(clips) - 1 else VIDEO_LEN - 0.3
            if start + length > limit:
                if i == len(clips) - 1:
                    # last line: start earlier, but keep a clear pause after the line before it
                    prev_end = starts[-1] + len(clips[i - 1]) / SR
                    start = max(limit - length, prev_end + 0.8)
                    ok = ok and (start + length <= limit)
                else:
                    ok = False
            starts.append(start)
        if ok or speed >= 1.15:
            break
        speed = round(speed + 0.03, 2)
    track = np.zeros(int(VIDEO_LEN * SR), dtype=np.float32)
    for s, c in zip(starts, clips):
        a = int(s * SR)
        track[a:a + len(c)] += c[: len(track) - a]
    track = match_level(track)
    write_pair(AUDIO / "Clearview_Video_Voiceover.wav", AUDIO / "Clearview_Video_Voiceover.mp3", track)
    timing = [(s, s + len(c) / SR, l) for s, c, l in zip(starts, clips, lines)]
    for s, e, l in timing:
        print(f"  voiceover {s:5.2f}-{e:5.2f}s  {l[:60]}")
    print(f"  voiceover speed {speed}, fits: {ok}")
    made_video = False
    if VIDEO_IN.exists():
        VIDEO_OUT.parent.mkdir(parents=True, exist_ok=True)
        run_ffmpeg(["-i", str(VIDEO_IN), "-i", str(AUDIO / "Clearview_Video_Voiceover.wav"),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", str(VIDEO_OUT)])
        made_video = True
        print(f"  wrote {VIDEO_OUT.name}")
    return timing, speed, ok, made_video


def write_transcript(rows, total, timing, vo_speed):
    guide_words = sum(r["words"] for r in rows)
    out = []
    out.append("# Museum of Theft: Audio Guide Transcript\n")
    out.append("Team Biscuit · November 2026 · updated from the October 2026 draft\n")
    out.append("## About this script\n")
    out.append(f"- **{len(rows)} tracks**: an entrance welcome, one introduction per section, one track per case, and an exit. "
               "Each QR code opens one track, so visitors move at their own pace.")
    out.append(f"- **Length:** {mmss(sum(r['dur'] for r in rows))} of narration in total ({guide_words} words). "
               "Case tracks run from about 55 seconds to 1 minute 40; the others run under a minute.")
    out.append("- **Each case track** opens with a hook, tells what happened and what it turned into, gives both sides, "
               "and ends on an open question. It does not walk the listener through the objects; "
               "at most one line points at something beside the QR code.")
    out.append("- **Sections 1 and 2** leave the verdict to the visitor. **Section 3** keeps the stance of its wall panels.")
    out.append(f"- **Voice:** Kokoro `{VOICE}` at speed {SPEED}, about "
               f"{round(guide_words / sum(r['dur'] for r in rows) * 60)} words a minute including pauses.")
    out.append("- **No sound effects.** The October draft's sound cues (shop bell, drum, forest and chainsaw) are not recorded. "
               "Places where they could be mixed in later are marked *[Sound cue]* below; those lines are not read aloud.")
    out.append("- The text of each track lives in `tracks/*.txt`. To change the audio, edit that file and run `generate_audio.py` again.\n")
    out.append("## Tracks\n")
    out.append("| # | Track | Where | Length | Words | Audio file |")
    out.append("|---|---|---|---|---|---|")
    for r in rows:
        out.append(f"| {r['stem'][:2]} | {r['title']} | {r['where']} | {mmss(r['dur'])} | {r['words']} | `{r['name']}.mp3` |")
    out.append(f"| | **Complete guide** (all 14, in order) | | {mmss(total)} | {guide_words} | `Museum_of_Theft_Complete_Audio_Guide.mp3` |\n")
    cues = {
        "04_kleptomania_and_class": "*[Sound cue, not recorded: a shop bell and the murmur of a busy store, fading under the voice.]*",
        "05_robbing_the_rich": "*[Sound cue, not recorded: a single drum under the opening verse. The verse is the opening of "
                               "A Gest of Robyn Hode, read here in modern spelling.]*",
        "13_the_hasdeo_arand_forest": "*[Sound cue, not recorded: about ten seconds of forest canopy, then a chainsaw fading in. "
                                      "Use only recordings made with consent and credited in the catalogue.]*",
    }
    section = None
    for r in rows:
        if r["section"] != section:
            section = r["section"]
            out.append(f"## {section}\n")
        out.append(f"### Track {r['stem'][:2]} · {r['title']}\n")
        out.append(f"{r['where']} · {mmss(r['dur'])} · {r['words']} words\n")
        if r["stem"] in cues:
            out.append(cues[r["stem"]] + "\n")
        for p in r["paras"]:
            out.append(p + "\n")
    out.append("## Clearview video voiceover\n")
    out.append(f"For `Clearview_Face_Search_Loop.mp4` (32 seconds). Audio: `Clearview_Video_Voiceover.mp3`. "
               f"Video with the voice built in: `Video/Clearview_Face_Search_Narrated.mp4`. "
               f"Same voice, speed {vo_speed}. It is not part of the complete guide file.\n")
    out.append("| Voice starts | Voice ends | Line |")
    out.append("|---|---|---|")
    for s, e, l in timing:
        out.append(f"| 0:{s:04.1f} | 0:{e:04.1f} | {l} |")
    out.append("")
    out.append("## Pronunciations set by hand\n")
    out.append("Kokoro mispronounced these on its own, so the generator spells them out for it.\n")
    out.append("| Word | Said as |")
    out.append("|---|---|")
    for w, (_, cue) in PRON.items():
        out.append(f"| {w} | {cue} |")
    out.append("")
    (HERE / "Transcript" / "Audio_Guide_Transcript.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    rows, total = build_tracks(pipe)
    timing, vo_speed, fits, made_video = build_voiceover(pipe)
    write_transcript(rows, total, timing, vo_speed)
    print("done")
