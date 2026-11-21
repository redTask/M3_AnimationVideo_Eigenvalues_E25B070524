# Eigenvalues and Eigenvectors — The Directions That Survive

An animated explainer built with [Manim](https://www.manim.community/) and narrated
with [edge-tts](https://github.com/rany2/edge-tts). Six acts, **5:11**, rendered at
1920×1080 / 60 fps.

**OM ASHISH — E25B070524** · M3 Internal Assessment

The finished video is in the repo at
[`media/videos/eigenvideo/1080p60/eigenvideo_full.mp4`](media/videos/eigenvideo/1080p60/eigenvideo_full.mp4).

## The story

One matrix is used the whole way through:

```
A = [2 1]
    [1 2]
```

with eigenvalues **λ = 3** and **λ = 1**, and eigenvectors **(1, 1)** and **(1, −1)**.

| Act | File | Length | What it does |
|---|---|---|---|
| Opening | `OpeningFrame` | 0:05 | Title card, name and student ID |
| 1 — Hook | `Scene1Hook` | 0:24 | A vector lands off its own line when the matrix acts; asks which directions survive |
| 2 — Concept | `Scene2Concept` | 0:41 | `Av = λv` defined, then animated so the parallel case is obvious |
| 3 — Intuition | `Scene3Intuition` | 1:04 | A rotation sweeps vectors off their directions; two directions refuse to move |
| 4 — Worked example | `Scene4Worked` | 1:40 | `det(A − λI) = 0`, the algebra step by step, then the answers checked |
| 5 — Interpretation | `Scene5Interpret` | 0:47 | What the eigenvalues mean: scaling, trace and determinant |
| 6 — Summary | `Scene6Summary` | 0:29 | Recap and credits |

Colour code, identical in every act:

| Meaning | Colour |
|---|---|
| Ordinary vectors | blue |
| Eigenvector for λ = 3 | yellow |
| Eigenvector for λ = 1 | green |
| Matrix **A** | white |
| Results / answers | red |

## Requirements

- Python 3.10+ (developed on 3.13)
- FFmpeg on the `PATH` (audio joining, duration probing)
- A LaTeX installation — TeX Live or MacTeX

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install manim edge-tts
```

If `/Library/TeX/texbin` is missing on macOS, either link it:

```bash
sudo mkdir -p /Library/TeX
sudo ln -s /usr/local/texlive/2026/bin/universal-darwin /Library/TeX/texbin
```

or prepend TeX Live to the `PATH` for each render:

```bash
export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"
```

## Regenerating the narration

`scenes.py` holds the script. `generate_narration.py` turns it into one MP3 plus
one SRT per act, and a joined file for review:

```bash
python generate_narration.py                  # every act
python generate_narration.py 4                # only act 4
python generate_narration.py --voice en-GB-RyanNeural
```

Outputs land in `audio/`. The `.srt` files are not just subtitles — the scenes
read their cue timestamps to time each animation to the sentence being spoken,
so a re-generated track automatically re-syncs the visuals.

## Rendering

```bash
manim -qh eigenvideo.py Scene4Worked          # one act, 1080p60
manim -ql eigenvideo.py Scene4Worked          # quick 480p preview
manim -qh eigenvideo.py OpeningFrame Scene1Hook Scene2Concept \
    Scene3Intuition Scene4Worked Scene5Interpret Scene6Summary
```

Adjust the `PATH` first if LaTeX is not linked (see above). Each act renders to
`media/videos/eigenvideo/<quality>/<SceneName>.mp4`.

## Joining the acts

The acts are separate files, and the title card has no narration, so it gets a
silent stereo track. Manim's MP4 timestamps make the concat *demuxer* mis-sum the
duration, so join with the concat **filter**:

```bash
cd media/videos/eigenvideo/1080p60

ffmpeg -y -i OpeningFrame.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo \
  -map 0:v -map 1:a -t 5.6 -c:v copy -c:a aac _opening.mp4

ffmpeg -y -i _opening.mp4 -i Scene1Hook.mp4 -i Scene2Concept.mp4 \
  -i Scene3Intuition.mp4 -i Scene4Worked.mp4 -i Scene5Interpret.mp4 \
  -i Scene6Summary.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a][5:v][5:a][6:v][6:a]concat=n=7:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k eigenvideo_full.mp4
```

The result is 1920×1080, 60 fps, 5:11.

## Layout

```
eigenvideo.py                                all seven scenes and shared helpers
scenes.py                                    script, timings and matrix numbers
generate_narration.py                        edge-tts narration + SRT cues
Eigenvalues and Eigenvectors ....md          the original storyboard
audio/                                       narration per act, SRT cues, full mix
media/videos/eigenvideo/1080p60/             rendered acts + the joined video
test.py                                      early LaTeX smoke test
```

`scenes.py` is the single source of truth: the scene text, the durations and the
numbers on screen all come from it, so the narration and the animation cannot
drift apart. `media/` and `.venv/` are gitignored apart from the final video.
