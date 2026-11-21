"""Act-by-act breakdown of "Eigenvalues and Eigenvectors: The Directions That Survive".

Single source of truth for both the Manim scenes and the edge-tts narration,
so the timings, the numbers on screen and the spoken words can never drift apart.

Timing targets come from the storyboard: ~120-130 words per minute, total ~5:15.

Colour code (identical in every scene):
    ordinary vectors -> BLUE
    eigenvector for lambda = 3 -> YELLOW
    eigenvector for lambda = 1 -> GREEN
    matrix A -> WHITE
    results / answers -> RED
"""

# The one worked example used throughout the video.
MATRIX_A = [[2, 1], [1, 2]]
EIGENVALUE_1 = 3
EIGENVECTOR_1 = (1, 1)
EIGENVALUE_2 = 1
EIGENVECTOR_2 = (1, -1)

OPENING = {
    "number": 0,
    "title": "Opening frame",
    "start": "0:00",
    "duration": 5,
    "purpose": "Title card.",
    "on_screen": [
        'Title: "Eigenvalues and Eigenvectors"',
        'Subtitle: "The directions a matrix cannot turn"',
        'Student name, student ID, "M3 Internal Assessment"',
        "Soft fade in and out",
    ],
    "narration": "",  # none, optional low music
}

SCENES = [
    {
        "number": 1,
        "title": "Hook",
        "start": "0:05",
        "duration": 30,
        "purpose": "Spark curiosity with a guiding question.",
        "visuals": [
            "Plain coordinate grid with blue vectors (1,0), (0,1), (1,2), (-2,1).",
            "Matrix A appears in the corner; whole grid warps under A.",
            "Each blue vector swings off its line, ghost copies stay behind.",
            "(1,1) highlighted yellow and (1,-1) green: they never leave their lines.",
            'Question fades in: "Which directions survive a transformation?"',
        ],
        "manim_notes": "LinearTransformationScene with add_vector/apply_matrix; "
        "ghost copies by keeping a copy of each vector before the transform.",
        "narration": (
            "Take any vector in the plane and apply this matrix to it. Watch the grid. "
            "It stretches, it tilts, and almost every vector is knocked off the line it "
            "started on. Almost. A few special directions refuse to turn. They only get "
            "longer, shorter, or flipped. Which directions are these, and why do they "
            "matter? Let's find out."
        ),
    },
    {
        "number": 2,
        "title": "Concept introduction",
        "start": "0:35",
        "duration": 45,
        "purpose": "State the definition, the notation and the goal.",
        "visuals": [
            'Write "A is a 2x2 matrix. v is a vector in R2".',
            "Equation Av = lambda v large, colour coded (A white, v yellow, lambda red).",
            'Annotate: "v != 0 (eigenvector)" and "lambda is a scalar (eigenvalue)".',
            'Three lines one by one: "|lambda| > 1: stretch", "0 < |lambda| < 1: shrink", '
            '"lambda < 0: flip direction".',
            'Goal box: "Goal: find all pairs (lambda, v)".',
        ],
        "manim_notes": 'MathTex("A", "\\\\mathbf{v}", "=", "\\\\lambda", "\\\\mathbf{v}") '
        "with set_color_by_tex.",
        "narration": (
            "Let A be a two by two matrix, and v a vector in the plane. Usually A v points "
            "somewhere new. But sometimes A v lands on the same line as v. Then A v is just "
            "a scalar multiple of v. We write this as A v equals lambda v. The vector v, "
            "which must not be zero, is called an eigenvector. The number lambda is its "
            "eigenvalue. If lambda is bigger than one, the vector stretches. Between zero "
            "and one, it shrinks. If lambda is negative, it flips. Our goal: find all such "
            "pairs, lambda and v."
        ),
    },
    {
        "number": 3,
        "title": "Visual intuition",
        "start": "1:20",
        "duration": 75,
        "purpose": "Build geometric understanding before any heavy algebra.",
        "visuals": [
            "Return to the grid with A = [[2,1],[1,2]] at the top.",
            "Basis vectors: i -> (2,1), j -> (1,2); columns are where the basis vectors land.",
            "Non-example: line through (1,0), A lands at (2,1) off the line; red cross.",
            "Rotating blue test vector with its image Av and a thin angle arc.",
            "Arc closes at (1,1) -> turns yellow; closes again at (1,-1) -> turns green.",
            "Draw both eigen-lines, apply A: yellow line stretches 3x, green line unchanged.",
            "Optional: unit square -> parallelogram, area counter 1 -> 3.",
        ],
        "manim_notes": "ValueTracker for the rotating angle, always_redraw for the image "
        "vector and the angle arc.",
        "narration": (
            "First, let's see what this matrix does. The first column, two one, is where the "
            "vector one zero lands. The second column, one two, is where zero one lands. Now "
            "try the vector one zero. It lands at two one, which is not on its original line. "
            "So one zero is not an eigenvector. Let's rotate a test vector around the origin "
            "and compare it with its image. Most of the time, the image points in a different "
            "direction, and there's a gap between them. But watch what happens here, at one "
            "one. The gap closes. The image is on the same line. And again here, at one minus "
            "one. These are our two special directions. Now apply the matrix to the whole "
            "grid. Notice that both lines stay where they are. Along the yellow line, "
            "everything is stretched. Along the green line, everything keeps its length. "
            "These lines are the skeleton of the transformation. The rest of the plane is "
            "just mixing the two."
        ),
    },
    {
        "number": 4,
        "title": "Worked example",
        "start": "2:35",
        "duration": 90,
        "purpose": "Show every step of finding the eigenvalues and eigenvectors, then verify.",
        "visuals": [
            "Rewrite: Av = lambda v -> Av - lambda v = 0 -> (A - lambda I)v = 0.",
            "Key idea: v != 0 forces A - lambda I to be singular, so det(A - lambda I) = 0.",
            "Compute A - lambda I = [[2-lambda, 1], [1, 2-lambda]].",
            "det = (2-lambda)^2 - 1 = lambda^2 - 4lambda + 3 = (lambda-1)(lambda-3) = 0.",
            "Highlight roots lambda = 1 and lambda = 3 in red.",
            "lambda = 3: A - 3I = [[-1,1],[1,-1]] -> y = x -> v = (1,1) in yellow.",
            "lambda = 1: A - I = [[1,1],[1,1]] -> y = -x -> v = (1,-1) in green.",
            "Verify: A(1,1) = (3,3) = 3(1,1); A(1,-1) = (1,-1) = 1(1,-1).",
            "Sanity: trace 4 = 3 + 1, det 3 = 3 x 1.",
        ],
        "manim_notes": "MathTex plus TransformMatchingTex per rewriting step; Indicate the "
        "part that changes; Matrix/bmatrix for the matrices.",
        "narration": (
            "Now let's actually compute them. Start with A v equals lambda v. Move everything "
            "to one side: A v minus lambda v equals zero. To factor v out, write lambda v as "
            "lambda I times v. So A minus lambda I, times v, equals zero. We want a nonzero v "
            "that this matrix sends to zero. That can only happen if the matrix squashes the "
            "plane, which means its determinant is zero. For our matrix, A minus lambda I is "
            "two minus lambda, one, one, two minus lambda. Its determinant is two minus "
            "lambda, squared, minus one. Expanding gives lambda squared minus four lambda "
            "plus three, which factors as lambda minus one, times lambda minus three. So the "
            "eigenvalues are one and three. For lambda equals three, the matrix becomes minus "
            "one, one, one, minus one. Both rows say y equals x, so v is one, one. For lambda "
            "equals one, both rows say x plus y equals zero, so v is one, minus one. Let's "
            "check. A times one, one is three, three, which is three times one, one. And A "
            "times one, minus one is one, minus one, which is one times itself. Both check "
            "out. One more sanity check: the eigenvalues add up to the trace, four, and "
            "multiply to the determinant, three."
        ),
    },
    {
        "number": 5,
        "title": "Interpretation",
        "start": "4:05",
        "duration": 45,
        "purpose": "Connect the numbers back to the geometry.",
        "visuals": [
            "Grid with both eigen-lines drawn (yellow and green).",
            "(1,1) grows to (3,3), label 'lambda = 3: stretched 3x'; (1,-1) unchanged.",
            "Decompose (2,0) = 1*(1,1) + 1*(1,-1) with a parallelogram.",
            "Apply A: yellow part triples, green part stays -> (4,2), matches A(2,0).",
            'Final line: "Eigenvectors turn a complicated transformation into simple '
            'stretching along two directions."',
            "Area scale factor det(A) = 3 x 1 = 3, matching the Scene 3 counter.",
        ],
        "manim_notes": "Polygon for the decomposition parallelogram; Transform for the "
        "stretched components; reuse the colour code.",
        "narration": (
            "What do these numbers tell us? Along the direction one, one, the matrix "
            "stretches everything by three. Along one, minus one, it leaves everything alone. "
            "Now take any other vector, say two, zero. We can write it as one copy of the "
            "yellow vector plus one copy of the green one. Apply the matrix: the yellow part "
            "triples, the green part stays. Together that gives four, two, exactly what the "
            "matrix gives directly. So eigenvectors turn a messy transformation into simple "
            "stretching along two directions. And the area of any shape is scaled by three "
            "times one, which is three, the determinant."
        ),
    },
    {
        "number": 6,
        "title": "Summary and credits",
        "start": "4:50",
        "duration": 30,
        "purpose": "Reinforce three takeaways and show references, music credit, AI disclosure.",
        "visuals": [
            "Three takeaways one at a time:",
            "  1. An eigenvector keeps its direction: Av = lambda v.",
            "  2. Eigenvalues solve det(A - lambda I) = 0.",
            "  3. Each eigenvalue is the scaling factor along its eigenvector.",
            "Fade to closing frame: title, name, ID.",
            "References: M3 course notes; Strang, Introduction to Linear Algebra; Manim docs.",
            "Music credit, then AI disclosure.",
        ],
        "manim_notes": "Succession/Write for the three takeaways, then FadeOut to credits.",
        "narration": (
            "To recap. One: an eigenvector is a direction that a matrix only stretches or "
            "flips, written A v equals lambda v. Two: we find the eigenvalues by solving the "
            "determinant of A minus lambda I equals zero. Three: each eigenvalue is the "
            "scaling factor along its eigenvector. Thanks for watching. References, music "
            "credit and AI disclosure are on screen."
        ),
    },
]

# Narration defaults for edge-tts.
VOICE = "en-US-AndrewNeural"
RATE = "-15%"  # slowdown so the read lands near the 120-130 wpm target


def total_words():
    return sum(len(s["narration"].split()) for s in SCENES)


if __name__ == "__main__":
    total = 0
    for scene in SCENES:
        words = len(scene["narration"].split())
        total += scene["duration"]
        print(
            f"Scene {scene['number']}: {scene['title']:<24} "
            f"{scene['duration']:>3}s  {words:>3} words"
        )
    print(f"{'Total':<32} {total:>3}s  {total_words():>3} words")
