"""Manim scenes for "Eigenvalues and Eigenvectors: The Directions That Survive".

Renders one video per act, each carrying its own narration track from audio/.
Numbers, wording and durations all come from scenes.py, so the visuals and the
voice can never disagree.

    manim -ql eigenvideo.py Scene1Hook        # one act, low quality
    manim -qh eigenvideo.py                   # first act, high quality
    manim -ql eigenvideo.py Scene1Hook Scene2Concept Scene3Intuition Scene4Worked Scene5Interpret Scene6Summary

Colour code (from the storyboard):
    ordinary vectors -> BLUE,  lambda = 3 -> YELLOW, lambda = 1 -> GREEN,
    matrix A -> WHITE,  answers -> RED.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np
from manim import *

from generate_narration import slug
from scenes import MATRIX_A, SCENES, VOICE  # noqa: F401  (VOICE kept for reference)

A = np.array(MATRIX_A, dtype=float)

# --- colour code ------------------------------------------------------------
C_NORMAL = BLUE
C_EIG3 = YELLOW
C_EIG1 = GREEN
C_MATRIX = WHITE
C_RESULT = RED

E3 = np.array([1.0, 1.0, 0.0]) / np.sqrt(2)  # direction of the lambda = 3 eigenvector
E1 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)  # direction of the lambda = 1 eigenvector

AUDIO_DIR = Path("audio")

STUDENT_NAME = "OM ASHISH"
STUDENT_ID = "E25B070524"


# --- helpers ----------------------------------------------------------------
def audio_file(number: int) -> Path | None:
    scene = next((s for s in SCENES if s["number"] == number), None)
    if scene is None:
        return None
    path = AUDIO_DIR / f"scene_{number:02d}_{slug(scene['title'])}.mp3"
    return path if path.exists() else None


def media_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def attach_narration(scene, number: int) -> None:
    """Place this act's narration at the start of the scene (t = 0)."""
    path = audio_file(number)
    if path is not None:
        scene.add_sound(str(path))


def hold_for_narration(scene, number: int) -> None:
    """Hold the last frame so the animation never cuts the narration short."""
    path = audio_file(number)
    if path is None:
        return
    remaining = media_duration(path) - scene.time
    if remaining > 0.05:
        scene.wait(remaining)


def subtitle_cues(number: int) -> list[float]:
    """Start time (seconds) of every narration sentence, from the .srt file."""
    path = audio_file(number)
    if path is None:
        return []
    srt = path.with_suffix(".srt")
    if not srt.exists():
        return []

    cues = []
    for block in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        match = re.match(r"(\d+):(\d+):(\d+),(\d+)", lines[1])
        if match:
            h, m, s, ms = (int(g) for g in match.groups())
            cues.append(h * 3600 + m * 60 + s + ms / 1000)
    return cues


def wait_until(scene, t: float) -> None:
    """Hold until the scene clock reaches t."""
    remaining = t - scene.time
    if remaining > 0.02:
        scene.wait(remaining)


def span(start: float, end: float, floor: float = 0.5) -> float:
    """Animation run_time between two cues, never shorter than floor."""
    return max(floor, end - start)


def vec(x, y):
    return np.array([x, y, 0.0])


def arrow(vector, color=C_NORMAL, width=6, opacity=1.0, tip=0.16):
    return Arrow(
        ORIGIN,
        np.array(vector, dtype=float),
        buff=0,
        color=color,
        stroke_width=width,
        max_tip_length_to_length_ratio=tip,
    ).set_opacity(opacity)


def label_vector(start, end, text, color=WHITE, font_size=26, buff=0.2):
    mid = (np.array(start, dtype=float) + np.array(end, dtype=float)) / 2
    return MathTex(text, font_size=font_size, color=color).move_to(mid + buff * RIGHT)


def plane(**kwargs):
    defaults = dict(
        x_range=[-7, 7, 1],
        y_range=[-4, 4, 1],
        background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.45,
                               "stroke_width": 1.2},
        axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.7},
    )
    defaults.update(kwargs)
    return NumberPlane(**defaults)


def matrix_card(font_size=38, corner=UL):
    return MathTex(
        r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}",
        font_size=font_size,
        color=C_MATRIX,
    ).to_corner(corner, buff=0.4)


def cross_at(point, size=0.22, color=C_RESULT, width=7):
    point = np.array(point, dtype=float)
    d = np.array([size, size, 0.0])
    return VGroup(
        Line(point - d, point + d, color=color, stroke_width=width),
        Line(point + d * np.array([1, -1, 1]), point + d * np.array([-1, 1, 1]),
             color=color, stroke_width=width),
    )


def eigen_lines(extent=5.2):
    return VGroup(
        DashedLine(-extent * E3, extent * E3, color=C_EIG3, stroke_width=3,
                   dash_length=0.18).set_opacity(0.85),
        DashedLine(-extent * E1, extent * E1, color=C_EIG1, stroke_width=3,
                   dash_length=0.18).set_opacity(0.85),
    )


def apply_A(v):
    v = np.array(v, dtype=float)[:2]
    return np.array([A[0, 0] * v[0] + A[0, 1] * v[1],
                     A[1, 0] * v[0] + A[1, 1] * v[1], 0.0])


# --- opening frame ----------------------------------------------------------
class OpeningFrame(Scene):
    def construct(self):
        title = Text("Eigenvalues and Eigenvectors", font_size=54, weight=BOLD)
        subtitle = Text("The directions a matrix cannot turn", font_size=32,
                        slant=ITALIC, color=GREY_B)
        plate = VGroup(
            Text("M3 Internal Assessment", font_size=24, color=GREY_A),
            Text(f"{STUDENT_NAME}  |  {STUDENT_ID}", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18)

        VGroup(title, subtitle).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        plate.next_to(subtitle, DOWN, buff=0.9)

        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(plate), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(VGroup(title, subtitle, plate)), run_time=1.0)


# --- scene 1: hook ----------------------------------------------------------
class Scene1Hook(Scene):
    def construct(self):
        attach_narration(self, 1)
        self.construct_body()
        hold_for_narration(self, 1)

    def construct_body(self):
        grid = plane()
        seeds = [(1, 0), (0, 1), (1, 2), (-2, 1)]
        vectors = VGroup(*[arrow(vec(x, y)) for x, y in seeds])
        card = matrix_card()

        self.play(FadeIn(grid), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(v) for v in vectors], lag_ratio=0.2),
                  run_time=2.0)
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.8)
        self.wait(1.5)

        # Ghosts mark where every vector started; the originals swing away.
        ghosts = vectors.copy().set_opacity(0.25)
        self.add(ghosts)
        images = VGroup(*[arrow(apply_A(vec(x, y)), color=C_NORMAL) for x, y in seeds])
        self.play(
            grid.animate.apply_matrix(A),
            *[Transform(v, img) for v, img in zip(vectors, images)],
            run_time=3.0,
        )
        self.wait(1.0)

        # The two directions that refuse to turn.
        guides = VGroup(
            DashedLine(-4.2 * E3, 4.2 * E3, color=C_EIG3, stroke_width=2,
                       dash_length=0.16).set_opacity(0.6),
            DashedLine(-4.2 * E1, 4.2 * E1, color=C_EIG1, stroke_width=2,
                       dash_length=0.16).set_opacity(0.6),
        )
        yellow = arrow(vec(1, 1), color=C_EIG3, width=7)
        yellow_img = arrow(apply_A(vec(1, 1)), color=C_EIG3, width=4, opacity=0.55)
        green = arrow(vec(1, -1), color=C_EIG1, width=7)

        self.play(FadeIn(guides), run_time=1.0)
        self.play(GrowArrow(yellow), GrowArrow(green), run_time=1.6)
        self.wait(1.0)
        self.play(Transform(yellow, yellow_img), run_time=1.8)
        self.wait(0.8)

        question = Text("Which directions survive a transformation?",
                        font_size=32, color=C_RESULT)
        question.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.25), run_time=1.2)
        self.wait(1.0)


# --- scene 2: concept introduction -----------------------------------------
class Scene2Concept(Scene):
    def construct(self):
        attach_narration(self, 2)
        self.construct_body()
        hold_for_narration(self, 2)

    def construct_body(self):
        setup = Text("A is a 2x2 matrix.   v is a vector in the plane.",
                     font_size=32).to_edge(UP, buff=0.7)

        eq = MathTex("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}",
                     font_size=88).move_to(UP * 1.9)
        eq[0].set_color(C_MATRIX)
        eq[1].set_color(C_EIG3)
        eq[3].set_color(C_RESULT)
        eq[4].set_color(C_EIG3)

        self.play(FadeIn(setup, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.4)
        self.play(Write(eq), run_time=2.0)
        self.wait(0.8)

        # Annotate the two symbols.
        v_note = MathTex(r"\mathbf{v} \neq \mathbf{0}",
                         r"\ \text{(eigenvector)}", font_size=30)
        v_note[0].set_color(C_EIG3)
        v_note[1].set_color(GREY_A)
        v_note.move_to(LEFT * 3.3 + DOWN * 0.45)

        lam_note = MathTex(r"\lambda", r"\ \text{is a scalar (eigenvalue)}",
                           font_size=30)
        lam_note[0].set_color(C_RESULT)
        lam_note[1].set_color(GREY_A)
        lam_note.move_to(RIGHT * 2.9 + DOWN * 0.45)

        v_arrow = Arrow(v_note.get_top(), eq[1].get_bottom() + DOWN * 0.08,
                        buff=0.1, color=C_EIG3, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.12)
        lam_arrow = Arrow(lam_note.get_top(), eq[3].get_bottom() + DOWN * 0.08,
                          buff=0.1, color=C_RESULT, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.12)

        self.play(Create(v_arrow), FadeIn(v_note), run_time=0.9)
        self.play(Create(lam_arrow), FadeIn(lam_note), run_time=0.9)
        self.wait(1.0)

        # What lambda does to the vector.
        cases = VGroup(
            MathTex(r"|\lambda| > 1", r":\ \text{stretch}", font_size=32),
            MathTex(r"0 < |\lambda| < 1", r":\ \text{shrink}", font_size=32),
            MathTex(r"\lambda < 0", r":\ \text{flip direction}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        for row in cases:
            row[0].set_color(C_RESULT)
        cases.move_to(DOWN * 2.0)

        for row in cases:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
            self.wait(0.5)

        goal = MathTex(r"\text{Goal: find all pairs } (\lambda, \mathbf{v})",
                       font_size=32)
        goal.to_edge(DOWN, buff=0.45)
        box = SurroundingRectangle(goal, color=C_RESULT, buff=0.2, stroke_width=2.5)
        self.play(FadeIn(goal), Create(box), run_time=1.0)
        self.wait(1.0)


# --- scene 3: visual intuition ---------------------------------------------
class Scene3Intuition(Scene):
    """Cued to the narration: every visual beat starts on its own sentence."""

    def construct(self):
        attach_narration(self, 3)
        self.construct_body()
        hold_for_narration(self, 3)

    def construct_body(self):
        cue = subtitle_cues(3)

        grid = plane()
        card = matrix_card(font_size=34, corner=UL)

        # 1. "First, let's see what this matrix does."
        self.play(FadeIn(grid), FadeIn(card), run_time=1.3)

        i_vec = arrow(vec(1, 0), width=5)
        j_vec = arrow(vec(0, 1), width=5)
        i_img = arrow(apply_A(vec(1, 0)), color=GREY_A, width=4)
        j_img = arrow(apply_A(vec(0, 1)), color=GREY_A, width=4)
        col_note = Text("columns = where the basis vectors land", font_size=26,
                        color=GREY_A).to_edge(DOWN, buff=0.45)

        # 2. "The first column, two one, is where the vector one zero lands."
        wait_until(self, cue[1])
        self.play(GrowArrow(i_vec), run_time=1.2)
        self.play(GrowArrow(i_img), FadeIn(col_note), run_time=1.2)

        # 3. "The second column, one two, is where zero one lands."
        wait_until(self, cue[2])
        self.play(GrowArrow(j_vec), GrowArrow(j_img), run_time=1.6)

        # 4. "Now try the vector one zero."
        test = arrow(vec(1, 0), color=C_NORMAL, width=6)
        axis = Line(vec(-6.0, 0), vec(6.0, 0), color=GREY_B, stroke_width=2.5)
        wait_until(self, cue[3])
        self.play(Create(axis), GrowArrow(test), run_time=1.4)

        # 5. "It lands at two one, which is not on its original line."
        wait_until(self, cue[4])
        test_img = arrow(apply_A(vec(1, 0)), color=ORANGE, width=5)
        self.play(Transform(test, test_img), run_time=1.6)

        # 6. "So one zero is not an eigenvector."
        mark = cross_at(apply_A(vec(1, 0)))
        bad_note = Text("not an eigenvector", font_size=24, color=C_RESULT)
        bad_note.next_to(apply_A(vec(1, 0)), UR, buff=0.15)
        wait_until(self, cue[5])
        self.play(Create(mark), FadeIn(bad_note), run_time=1.0)

        # 7. "Let's rotate a test vector around the origin..."
        wait_until(self, cue[6] - 0.6)
        self.play(FadeOut(VGroup(axis, test, mark, bad_note, i_vec, j_vec,
                                 i_img, j_img, col_note)), run_time=0.8)

        theta = ValueTracker(0.0)

        def v_of_theta():
            t = theta.get_value()
            return np.array([np.cos(t), np.sin(t), 0.0])

        def gap_arc(v, w, radius=1.15):
            a1 = np.arctan2(v[1], v[0])
            a2 = np.arctan2(w[1], w[0])
            d = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
            if abs(d) < 0.02:
                return VMobject()
            return Arc(radius=radius, start_angle=a1, angle=d,
                       color=C_RESULT, stroke_width=4)

        # Image first and thinner, so the vector stays visible where the two coincide.
        img = always_redraw(lambda: arrow(apply_A(v_of_theta()), color=ORANGE,
                                          width=3, opacity=0.8, tip=0.12))
        def make_rot(color):
            # A plain wait() reuses manim's cached frame, so a colour held in a
            # mutable dict never appears; swapping the mobject does refresh it.
            return always_redraw(lambda: arrow(v_of_theta(), color=color, width=6))

        rot = make_rot(C_NORMAL)
        arc = always_redraw(lambda: gap_arc(v_of_theta(), apply_A(v_of_theta())))
        self.add(img, rot, arc)

        hint = Text("watch the angle between v and A v", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.45)

        # 8. "Most of the time there is a gap between them."
        wait_until(self, cue[7])
        self.play(FadeIn(hint), run_time=0.8)
        self.play(theta.animate.set_value(np.pi / 4),
                  run_time=span(self.time, cue[8] - 0.3, 1.0), rate_func=linear)

        # 9. "But watch what happens here, at one one." -- the gap closes.
        wait_until(self, cue[8])
        self.remove(rot)
        rot = make_rot(C_EIG3)
        self.add(rot)
        wait_until(self, cue[9])

        # 10. "The image is on the same line."
        gap_note = Text("the gap closes: A v is on the same line", font_size=26,
                        color=C_EIG3).to_edge(DOWN, buff=0.45)
        wait_until(self, cue[10] - 0.4)
        self.play(FadeIn(gap_note), FadeOut(hint), run_time=0.7)

        # 11. "And again here, at one minus one."
        wait_until(self, cue[11] - 0.9)
        self.play(FadeOut(gap_note), run_time=0.5)
        self.play(theta.animate.set_value(7 * np.pi / 4),
                  run_time=span(self.time, cue[12], 1.0), rate_func=linear)

        # 12. "These are our two special directions."
        wait_until(self, cue[12])
        self.remove(rot)
        rot = make_rot(C_EIG1)
        self.add(rot)
        gap_note2 = Text("the two special directions", font_size=26,
                         color=C_EIG1).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(gap_note2), run_time=0.7)

        # 13. "Now apply the matrix to the whole grid."
        wait_until(self, cue[13] - 0.8)
        self.play(FadeOut(VGroup(rot, img, arc, gap_note2)), run_time=0.8)

        lines = eigen_lines()
        yellow = arrow(vec(1, 1), color=C_EIG3, width=6)
        green = arrow(vec(1, -1), color=C_EIG1, width=6)
        self.play(FadeIn(lines), GrowArrow(yellow), GrowArrow(green), run_time=1.5)

        yellow_img = arrow(apply_A(vec(1, 1)), color=C_EIG3, width=4, opacity=0.6)
        self.play(grid.animate.apply_matrix(A),
                  Transform(yellow, yellow_img),
                  run_time=span(self.time, cue[14], 1.0))

        # 14. "Notice that both lines stay where they are."
        wait_until(self, cue[14])

        # 15. "Along the yellow line, everything is stretched."
        y_note = MathTex(r"\lambda = 3:\ \text{stretched } 3\times",
                         font_size=30, color=C_EIG3).next_to(vec(3, 3), LEFT, buff=0.35)
        wait_until(self, cue[15])
        self.play(FadeIn(y_note), Indicate(yellow, color=C_EIG3, scale_factor=1.08),
                  run_time=1.4)

        # 16. "Along the green line, everything keeps its length."
        g_note = MathTex(r"\lambda = 1:\ \text{same length}",
                         font_size=30, color=C_EIG1).next_to(vec(1, -1), RIGHT, buff=0.3)
        wait_until(self, cue[16])
        self.play(FadeIn(g_note), Indicate(green, color=C_EIG1, scale_factor=1.12),
                  run_time=1.4)

        # 17 and 18. "the skeleton of the transformation."
        skeleton = Text("eigen-lines = the skeleton of the transformation",
                        font_size=26, color=GREY_A).to_edge(DOWN, buff=0.45)
        wait_until(self, cue[17])
        self.play(FadeIn(skeleton), run_time=1.0)
        self.wait(1.2)


# --- scene 4: worked example -----------------------------------------------
class Scene4Worked(Scene):
    """One algebra step per narration sentence, with a live diagram alongside.

    Every `play` is anchored to a cue from audio/scene_04_worked_example.srt, so
    nothing ever freezes while the voice keeps talking.
    """

    def construct(self):
        attach_narration(self, 4)
        self.cue = subtitle_cues(4)
        self.construct_body()
        hold_for_narration(self, 4)

    # -- layout helpers ------------------------------------------------------
    def head(self, text):
        return Text(text, font_size=24, color=TEAL).to_corner(UL, buff=0.42)

    def stack(self, head, lines, width=7.0, height=4.9, buff=0.34):
        group = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=buff)
        if group.width > width:
            group.scale_to_fit_width(width)
        if group.height > height:
            group.scale_to_fit_height(height)
        return group.next_to(head, DOWN, aligned_edge=LEFT, buff=0.4)

    def diagram(self):
        """Small axes on the right where the geometry is illustrated."""
        return Axes(
            x_range=[-2, 4, 1], y_range=[-2, 4, 1],
            x_length=4.2, y_length=4.2, tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.75,
                         "stroke_width": 2, "include_ticks": False},
        ).move_to(np.array([4.5, -0.9, 0.0]))

    def dvec(self, ax, xy, color, width=6, opacity=1.0):
        return Arrow(
            ax.c2p(0, 0), ax.c2p(*xy), buff=0, color=color, stroke_width=width,
            max_tip_length_to_length_ratio=0.25, tip_length=0.18,
        ).set_opacity(opacity)

    def construct_body(self):
        c = self.cue
        mid = lambda a, b: a + (b - a) / 2  # noqa: E731

        # ---- step 1: rewrite the definition (cue 0 - cue 4) ----------------
        h1 = self.head("Step 1 - rewrite the definition")

        s1 = MathTex("A", r"\mathbf{v}", "=", r"\lambda", r"\mathbf{v}", font_size=44)
        s2 = MathTex("A", r"\mathbf{v}", "-", r"\lambda", r"\mathbf{v}", "=",
                     r"\mathbf{0}", font_size=44)
        s3 = MathTex("A", r"\mathbf{v}", "-", r"\lambda", "I", r"\mathbf{v}", "=",
                     r"\mathbf{0}", font_size=44)
        s4 = MathTex("(", "A", "-", r"\lambda", "I", ")", r"\mathbf{v}", "=",
                     r"\mathbf{0}", font_size=44)
        for line, ys, reds in ((s1, [1, 4], [3]), (s2, [1, 4], [3]),
                               (s3, [1, 5], [3]), (s4, [6], [])):
            for k in ys:
                line[k].set_color(C_EIG3)
            for k in reds:
                line[k].set_color(C_RESULT)
        s1[0].set_color(C_MATRIX)
        s2[0].set_color(C_MATRIX)
        s3[0].set_color(C_MATRIX)
        s3[4].set_color(C_MATRIX)
        s4[1].set_color(C_MATRIX)
        s4[4].set_color(C_MATRIX)
        s4.set_color(C_RESULT)
        s4[6].set_color(C_EIG3)

        g1 = VGroup(h1, self.stack(h1, [s1, s2, s3, s4]))

        wait_until(self, c[0])
        self.play(Write(h1), run_time=0.6)
        wait_until(self, c[1])
        self.play(Write(s1), run_time=0.9)
        wait_until(self, mid(c[1], c[2]))
        self.play(Write(s2), run_time=0.9)
        wait_until(self, c[2])
        self.play(Write(s3), run_time=0.9)
        wait_until(self, c[3])
        self.play(Write(s4), run_time=0.9)

        # ---- step 2: the characteristic equation (cue 4 - cue 10) ----------
        h2 = self.head("Step 2 - the characteristic equation")

        m1 = MathTex(r"\mathbf{v} \neq \mathbf{0} \;\Rightarrow\; A - \lambda I"
                     r"\ \text{is singular}", font_size=34)
        m2 = MathTex(r"\det(A - \lambda I) = 0", font_size=42, color=C_RESULT)
        # Built as prefix + matrix so the four entries can appear one at a
        # time, on the words that name them (cue 6 -> cue 7 is ~8 s long).
        m3p = MathTex(r"A - \lambda I =", font_size=34)
        m3b = Matrix([[r"2-\lambda", r"1"], [r"1", r"2-\lambda"]],
                     h_buff=1.7, v_buff=1.2, element_to_mobject=MathTex,
                     element_to_mobject_config={"font_size": 34})
        m3_entries = m3b.get_entries()
        for entry in m3_entries:          # layout stays fixed, ink fades in
            entry.set_opacity(0)
        m3 = VGroup(m3p, m3b).arrange(RIGHT, buff=0.2)
        m4 = MathTex(r"\det(A - \lambda I) = (2-\lambda)^2 - 1", font_size=32)
        m5 = MathTex(r"= \lambda^2 - 4\lambda + 3", font_size=32)
        m6 = MathTex(r"= (\lambda - 1)(\lambda - 3)", font_size=32)
        m7 = MathTex(r"\lambda = 1 \quad \text{or} \quad \lambda = 3", font_size=40,
                     color=C_RESULT)

        top = self.stack(h2, [m1, m2])               # first half of the panel
        low = self.stack(h2, [m3, m4, m5, m6, m7])   # determinant computation

        # illustration: A - lambda I sends both basis vectors onto one line
        ax = self.diagram()
        i_arrow = self.dvec(ax, (1, 0), C_NORMAL)
        j_arrow = self.dvec(ax, (0, 1), C_NORMAL)
        squash_caption = MathTex(r"\det = 0", font_size=26, color=C_RESULT)
        squash_caption.next_to(ax, DOWN, buff=0.28)

        wait_until(self, c[4])
        self.play(FadeOut(g1), Write(h2), Write(m1), run_time=0.9)
        self.play(FadeIn(ax), GrowArrow(i_arrow), GrowArrow(j_arrow), run_time=1.3)
        wait_until(self, c[5])
        self.play(Write(m2), run_time=0.8)
        self.play(
            Transform(i_arrow, self.dvec(ax, (-1, 1), C_NORMAL)),
            Transform(j_arrow, self.dvec(ax, (1, -1), C_NORMAL)),
            run_time=1.7,
        )
        self.play(FadeIn(squash_caption), run_time=0.6)
        wait_until(self, c[6] - 0.6)
        self.play(FadeOut(VGroup(ax, i_arrow, j_arrow, squash_caption, top)),
                  run_time=0.6)
        wait_until(self, c[6])
        self.play(Write(m3p), FadeIn(m3b.get_brackets()), run_time=0.9)
        wait_until(self, c[6] + 1.5)
        self.play(m3_entries[0].animate.set_opacity(1), run_time=0.7)
        wait_until(self, c[6] + 3.6)
        self.play(m3_entries[1].animate.set_opacity(1),
                  m3_entries[2].animate.set_opacity(1), run_time=0.7)
        wait_until(self, c[6] + 5.6)
        self.play(m3_entries[3].animate.set_opacity(1), run_time=0.7)
        wait_until(self, c[7])
        self.play(Write(m4), run_time=0.8)
        wait_until(self, c[8])
        self.play(Write(m5), run_time=0.7)
        wait_until(self, mid(c[8], c[9]))
        self.play(Write(m6), run_time=0.7)
        wait_until(self, c[9])
        self.play(Write(m7), run_time=0.9)
        self.wait(0.8)

        # ---- step 3: one eigenvector per eigenvalue (cue 10 - cue 13) ------
        h3 = self.head("Step 3 - one eigenvector per eigenvalue")

        n1 = MathTex(r"\lambda = 3:\quad A - 3I = \begin{bmatrix} -1 & 1 \\ 1 & -1"
                     r" \end{bmatrix}", font_size=31)
        n2 = MathTex(r"-x + y = 0 \;\Rightarrow\; y = x", font_size=31)
        n3 = MathTex(r"\mathbf{v} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}",
                     font_size=34, color=C_EIG3)
        n4 = MathTex(r"\lambda = 1:\quad A - I = \begin{bmatrix} 1 & 1 \\ 1 & 1"
                     r" \end{bmatrix}", font_size=31)
        n5 = MathTex(r"x + y = 0 \;\Rightarrow\; y = -x", font_size=31)
        n6 = MathTex(r"\mathbf{v} = \begin{bmatrix} 1 \\ -1 \end{bmatrix}",
                     font_size=34, color=C_EIG1)
        g3 = VGroup(h3, self.stack(h3, [n1, n2, n3, n4, n5, n6],
                                   height=4.6, buff=0.28))

        # illustration: the two eigen-lines, one arrow per direction
        ax2 = self.diagram()
        line3 = DashedLine(ax2.c2p(-1.6, -1.6), ax2.c2p(3.6, 3.6),
                           color=C_EIG3, stroke_width=2).set_opacity(0.5)
        line1 = DashedLine(ax2.c2p(-1.6, 1.6), ax2.c2p(3.6, -3.6),
                           color=C_EIG1, stroke_width=2).set_opacity(0.5)
        y_arr = self.dvec(ax2, (1, 1), C_EIG3)
        g_arr = self.dvec(ax2, (1, -1), C_EIG1)

        wait_until(self, c[10])
        self.play(FadeOut(VGroup(m3, m4, m5, m6, m7, h2)), Write(h3), Write(n1),
                  run_time=0.9)
        self.play(FadeIn(ax2), Create(line3), Create(line1), run_time=1.2)
        wait_until(self, c[11])
        self.play(Write(n2), run_time=0.8)
        wait_until(self, mid(c[11], c[12]))
        self.play(Write(n3), GrowArrow(y_arr), run_time=1.0)
        wait_until(self, c[12])
        self.play(Write(n4), run_time=0.8)
        wait_until(self, c[12] + 2.6)
        self.play(Write(n5), run_time=0.8)
        wait_until(self, c[12] + 5.2)
        self.play(Write(n6), GrowArrow(g_arr), run_time=1.0)

        # ---- step 4: check the answers (cue 13 - end) ----------------------
        h4 = self.head("Step 4 - check the answers")

        q1 = MathTex(r"A\begin{bmatrix}1\\1\end{bmatrix} = "
                     r"\begin{bmatrix}3\\3\end{bmatrix} = 3"
                     r"\begin{bmatrix}1\\1\end{bmatrix}",
                     font_size=31, color=C_EIG3)
        q2 = MathTex(r"A\begin{bmatrix}1\\-1\end{bmatrix} = "
                     r"\begin{bmatrix}1\\-1\end{bmatrix} = 1"
                     r"\begin{bmatrix}1\\-1\end{bmatrix}",
                     font_size=31, color=C_EIG1)
        q3 = MathTex(r"\checkmark \quad \text{both check out}", font_size=32,
                     color=C_MATRIX)
        q4 = MathTex(r"\operatorname{tr}(A) = 2 + 2 = 4 = 3 + 1", font_size=31)
        q5 = MathTex(r"\det(A) = 4 - 1 = 3 = 3 \times 1", font_size=31)
        g4 = self.stack(h4, [q1, q2, q3, q4, q5], height=4.6, buff=0.3)

        stretched = self.dvec(ax2, (3, 3), C_EIG3)
        x3 = MathTex(r"\times 3", font_size=26, color=C_EIG3)
        x3.next_to(ax2.c2p(3, 3), UP, buff=0.1)
        x1 = MathTex(r"\times 1", font_size=26, color=C_EIG1)
        x1.next_to(ax2.c2p(1, -1), RIGHT, buff=0.12)

        wait_until(self, c[13])
        self.play(FadeOut(g3), Write(h4), run_time=0.6)
        wait_until(self, c[14])
        self.play(Write(q1), Transform(y_arr, stretched), FadeIn(x3),
                  run_time=1.5)
        wait_until(self, c[15])
        self.play(Write(q2), Indicate(g_arr, color=C_EIG1, scale_factor=1.15),
                  FadeIn(x1), run_time=1.3)
        wait_until(self, c[16])
        self.play(Write(q3), run_time=0.8)
        wait_until(self, c[17])
        self.play(Write(q4), run_time=0.8)
        wait_until(self, c[17] + 3.6)
        self.play(Write(q5), run_time=0.8)


# --- scene 5: interpretation ------------------------------------------------
class Scene5Interpret(Scene):
    def construct(self):
        attach_narration(self, 5)
        self.construct_body()
        hold_for_narration(self, 5)

    def construct_body(self):
        grid = plane()
        lines = eigen_lines()
        self.play(FadeIn(grid), FadeIn(lines), run_time=1.2)

        # What the two eigenvalues mean.
        yellow = arrow(vec(1, 1), color=C_EIG3, width=6)
        green = arrow(vec(1, -1), color=C_EIG1, width=6)
        self.play(GrowArrow(yellow), GrowArrow(green), run_time=1.2)

        yellow_img = arrow(apply_A(vec(1, 1)), color=C_EIG3, width=4, opacity=0.55)
        y_note = MathTex(r"\lambda = 3:\ \text{stretched } 3\times",
                         font_size=30, color=C_EIG3).next_to(vec(3, 3), UR, buff=0.1)
        g_note = MathTex(r"\lambda = 1:\ \text{unchanged}",
                         font_size=30, color=C_EIG1).next_to(vec(1, -1), DR, buff=0.1)

        self.play(Transform(yellow, yellow_img), FadeIn(y_note), run_time=1.6)
        self.play(FadeIn(g_note), run_time=0.8)
        self.wait(1.8)

        # Decompose an ordinary vector into the two eigen-directions.
        self.play(FadeOut(VGroup(yellow, y_note, g_note)), run_time=0.7)

        a, b, total = vec(1, 1), vec(1, -1), vec(2, 0)
        para = Polygon(ORIGIN, a, total, b, color=GREY_B, fill_opacity=0.15,
                       stroke_width=2)
        comp_y = arrow(a, color=C_EIG3, width=4, opacity=0.9)
        comp_g = arrow(b, color=C_EIG1, width=4, opacity=0.9)
        plain = arrow(total, color=C_NORMAL, width=6)
        decomp = MathTex(r"\begin{bmatrix}2\\0\end{bmatrix} = "
                         r"1\begin{bmatrix}1\\1\end{bmatrix} + "
                         r"1\begin{bmatrix}1\\-1\end{bmatrix}", font_size=34)
        decomp.to_corner(UL, buff=0.5)

        self.play(GrowArrow(plain), run_time=1.0)
        self.play(Create(para), GrowArrow(comp_y), GrowArrow(comp_g),
                  FadeIn(decomp), run_time=1.8)
        self.wait(2.0)

        # Apply A: each eigen-component scales by its own eigenvalue.
        result = MathTex(r"A\begin{bmatrix}2\\0\end{bmatrix} = "
                         r"3\begin{bmatrix}1\\1\end{bmatrix} + "
                         r"1\begin{bmatrix}1\\-1\end{bmatrix} = "
                         r"\begin{bmatrix}4\\2\end{bmatrix}",
                         font_size=34, color=C_RESULT)
        result.to_corner(UL, buff=0.5)
        img_plain = arrow(apply_A(total), color=C_NORMAL, width=5)
        img_y = arrow(apply_A(a), color=C_EIG3, width=4, opacity=0.85)
        img_para = Polygon(ORIGIN, apply_A(a), apply_A(total), apply_A(b),
                           color=C_RESULT, fill_opacity=0.12, stroke_width=2)

        self.play(
            Transform(comp_y, img_y),
            Transform(para, img_para),
            Transform(plain, img_plain),
            FadeTransform(decomp, result),
            run_time=2.2,
        )
        self.wait(2.0)

        closing = Text("Eigenvectors turn a messy transformation into simple\n"
                       "stretching along two directions.",
                       font_size=26, color=GREY_A, line_spacing=0.9)
        closing.to_edge(DOWN, buff=0.35)
        area = MathTex(r"\text{areas scale by } \det(A) = 3 \times 1 = 3",
                       font_size=28, color=C_RESULT).next_to(closing, UP, buff=0.25)
        self.play(FadeIn(closing), FadeIn(area), run_time=1.2)
        self.wait(1.5)


# --- scene 6: summary and credits ------------------------------------------
class Scene6Summary(Scene):
    def construct(self):
        attach_narration(self, 6)
        self.construct_body()
        hold_for_narration(self, 6)

    def construct_body(self):
        takeaways = VGroup(
            VGroup(Text("1.  An eigenvector keeps its direction:",
                        font_size=30, color=GREY_A),
                   MathTex(r"A\mathbf{v} = \lambda\mathbf{v}", font_size=36)),
            VGroup(Text("2.  Eigenvalues solve:", font_size=30, color=GREY_A),
                   MathTex(r"\det(A - \lambda I) = 0", font_size=36)),
            VGroup(Text("3.  Each eigenvalue is the scaling factor",
                        font_size=30, color=GREY_A),
                   Text("along its eigenvector.", font_size=30, color=GREY_A)),
        )
        for group in takeaways:
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        takeaways.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(UP * 0.55)

        self.play(Write(takeaways[0]), run_time=1.4)
        self.wait(1.6)
        self.play(Write(takeaways[1]), run_time=1.2)
        self.wait(1.4)
        self.play(Write(takeaways[2]), run_time=1.2)
        self.wait(2.0)

        credits = VGroup(
            Text("Eigenvalues and Eigenvectors", font_size=34, weight=BOLD),
            Text(f"{STUDENT_NAME}  |  {STUDENT_ID}", font_size=24, color=GREY_A),
            Text("References: M3 course notes; Strang, Introduction to "
                 "Linear Algebra;", font_size=20, color=GREY_B),
            Text("Manim Community documentation.", font_size=20, color=GREY_B),
            Text("Music: track / artist / licence (if used)", font_size=20,
                 color=GREY_B),
            Text("AI disclosure: AI assisted with script and Manim code; "
                 "reviewed and tested by the author.", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.28)

        if credits.width > 12:
            credits.scale_to_fit_width(12)
        credits.move_to(ORIGIN)

        self.play(FadeOut(takeaways), run_time=0.9)
        self.play(FadeIn(credits, shift=UP * 0.2), run_time=1.4)
        self.wait(2.0)
