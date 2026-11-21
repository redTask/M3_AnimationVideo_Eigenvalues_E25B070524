"""Render the narration for every scene to audio with edge-tts.

Usage:
    .venv/bin/python generate_narration.py                # all scenes
    .venv/bin/python generate_narration.py 4              # only scene 4
    .venv/bin/python generate_narration.py --voice en-GB-RyanNeural

Outputs, in audio/:
    scene_01_hook.mp3 (+ .srt)      one audio file and one subtitle file per act
    narration_full.mp3              all acts joined with short gaps, for review
"""

import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

from scenes import RATE, SCENES, VOICE, total_words

AUDIO_DIR = Path("audio")
GAP = 0.5  # seconds of silence between acts in the joined file
WORDS_PER_MIN = 130.0  # storyboard target


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def probe_duration(path):
    """Duration in seconds via ffprobe."""
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "json", str(path),
        ],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


async def synth(scene, voice, rate, attempts=4):
    """Synthesise one scene. The endpoint occasionally returns no audio for a
    valid request, so retry with backoff before giving up."""
    import edge_tts

    stem = AUDIO_DIR / f"scene_{scene['number']:02d}_{slug(scene['title'])}"
    mp3, srt = stem.with_suffix(".mp3"), stem.with_suffix(".srt")

    for attempt in range(1, attempts + 1):
        audio = bytearray()
        submaker = edge_tts.SubMaker()
        try:
            communicate = edge_tts.Communicate(scene["narration"], voice, rate=rate)
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    submaker.feed(chunk)
        except Exception as exc:  # noqa: BLE001 - retry any transient failure
            error = exc
        else:
            if audio:
                mp3.write_bytes(audio)
                srt.write_text(submaker.get_srt(), encoding="utf-8")
                return mp3
            error = RuntimeError("empty audio stream")

        if attempt < attempts:
            wait = 2 * attempt
            print(f"  retry {attempt}/{attempts - 1} in {wait}s ({error})")
            await asyncio.sleep(wait)

    raise SystemExit(f"Scene {scene['number']} failed after {attempts} attempts: {error}")


def join_audio(tracks, out_path):
    """Concatenate mp3s with GAP seconds of silence between them."""
    if not tracks:
        return None
    silence = AUDIO_DIR / "_gap.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "lavfi",
            "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP),
            "-c:a", "libmp3lame", "-b:a", "48k", str(silence),
        ],
        check=True,
    )

    # One distinct input per stream: every gap needs its own ffmpeg input,
    # otherwise the concat filter consumes a shared stream only once.
    files = []
    for i, track in enumerate(tracks):
        files.append(track)
        if i < len(tracks) - 1:
            files.append(silence)

    inputs = [arg for f in files for arg in ("-i", str(f))]
    graph = (
        "".join(f"[{idx}:a]" for idx in range(len(files)))
        + f"concat=n={len(files)}:v=0:a=1[out]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph,
         "-map", "[out]", str(out_path)],
        check=True,
    )
    silence.unlink(missing_ok=True)
    return out_path


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", type=int, help="scene numbers to render")
    parser.add_argument("--voice", default=VOICE)
    parser.add_argument("--rate", default=RATE)
    parser.add_argument("--no-join", action="store_true", help="skip narration_full.mp3")
    args = parser.parse_args()

    AUDIO_DIR.mkdir(exist_ok=True)
    wanted = [s for s in SCENES if not args.scenes or s["number"] in args.scenes]

    print(f"voice={args.voice}  rate={args.rate}\n")
    tracks = []
    for scene in wanted:
        mp3 = await synth(scene, args.voice, args.rate)
        tracks.append(mp3)
        actual = probe_duration(mp3)
        words = len(scene["narration"].split())
        wpm = words / (actual / 60)
        target = scene["duration"]
        flag = "" if abs(actual - target) <= target * 0.12 else "  <-- off target"
        print(
            f"Scene {scene['number']}: {scene['title']:<24} "
            f"{actual:6.1f}s actual / {target:>3}s planned  "
            f"{wpm:5.1f} wpm  -> {mp3.name}{flag}"
        )

    print()
    if not args.scenes and not args.no_join:
        joined = join_audio(tracks, AUDIO_DIR / "narration_full.mp3")
        total = probe_duration(joined)
        print(
            f"Joined: {joined}  {total:.1f}s "
            f"({total / 60:.2f} min) for {total_words()} words  "
            f"= {total_words() / (total / 60):.1f} wpm"
        )
    print(f"\nDone: {len(tracks)} track(s) in {AUDIO_DIR}/")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
