# Eigenvalues and Eigenvectors: The Directions That Survive

**M3 Internal Assessment, Project Option 1: Animation Video** Student name: \_\_\_\_\_\_\_\_  |  Student ID: \_\_\_\_\_\_\_\_ Tool: Manim Community Edition (Python)  |  Target length: about 5:15 (hard limit 7:00)

## Learning objective

By the end of this video, the viewer will be able to explain what an eigenvector and eigenvalue of a 2×2 matrix are, interpret them geometrically, and compute them for a given matrix.

## The one example used throughout

A = \[\[2, 1\], \[1, 2\]\] (columns are (2, 1) and (1, 2)).

- Characteristic equation: det(A − λI) = (2 − λ)² − 1 = λ² − 4λ + 3 = (λ − 1)(λ − 3) = 0, so λ = 3 or λ = 1.
- λ = 3: (A − 3I)v = 0 gives −x + y = 0, so v = (1, 1).
- λ = 1: (A − I)v = 0 gives x + y = 0, so v = (1, −1).
- Check by substitution: A(1, 1) = (3, 3) = 3(1, 1). A(1, −1) = (1, −1) = 1(1, −1).
- Contrast vector: A(1, 0) = (2, 1), which is not a multiple of (1, 0), so (1, 0) is not an eigenvector.
- Extra checks: trace = 4 = 3 + 1, det = 3 = 3 × 1, and the unit square's area is scaled by det(A) = 3.

**Colour code (keep it the same in every scene):** ordinary vectors = blue, eigenvector for λ = 3 = yellow, eigenvector for λ = 1 = green, matrix A = white, results/answers = red.

## Timing overview

| Scene | Title | Time | Approx. words |
| --- | --- | --- | --- |
| Opening frame | Title card | 0:05 | 0 |
| 1 | Hook | 0:30 | 60 |
| 2 | Concept introduction | 0:45 | 95 |
| 3 | Visual intuition | 1:15 | 150 |
| 4 | Worked example | 1:30 | 185 |
| 5 | Interpretation | 0:45 | 95 |
| 6 | Summary and credits | 0:30 | 60 |

Narration pace is about 120 to 130 words per minute. Leave short pauses so each animation step can finish before the next sentence starts.

## Opening frame (0:00 to 0:05)

**On screen:** Title "Eigenvalues and Eigenvectors", subtitle "The directions a matrix cannot turn", then your name, student ID and "M3 Internal Assessment". Soft fade in and out.

**Narration:** none (optional soft music starts, kept low).

## Scene 1: Hook (0:05 to 0:35)

**Purpose:** spark curiosity with a guiding question.

**Visuals:**

1. A plain coordinate grid with a few blue vectors, e.g. (1, 0), (0, 1), (1, 2), (−2, 1).
2. The matrix A appears in the corner. The whole grid smoothly warps under A. Each blue vector swings away from its original line, and faint "ghost" copies stay behind to show where it started.
3. Two vectors, (1, 1) in yellow and (1, −1) in green, are highlighted. They stretch or stay but never leave their lines.
4. Question text fades in: "Which directions survive a transformation?"

**Narration:**

> Take any vector in the plane and apply this matrix to it. Watch the grid. It stretches, it tilts, and almost every vector is knocked off the line it started on. Almost. A few special directions refuse to turn. They only get longer, shorter, or flipped. Which directions are these, and why do they matter? Let's find out.

**Manim notes:** `LinearTransformationScene` with `add_vector` and `apply_matrix`; ghost copies via `add_transformable_label` or by keeping a copy of each vector before the transform.

## Scene 2: Concept introduction (0:35 to 1:20)

**Purpose:** state the definition, the notation, and the goal.

**Visuals:**

1. Clear the screen. Write "A is a 2×2 matrix. v is a vector in R²".
2. Show the equation **Av = λv** in large text, with colour: A white, v yellow, λ red.
3. Annotate with arrows and labels: "v ≠ 0 (eigenvector)" and "λ is a scalar (eigenvalue)".
4. Three short lines appear one by one: "|λ| > 1: stretch", "0 < |λ| < 1: shrink", "λ < 0: flip direction".
5. Last, the goal box: "Goal: find all pairs (λ, v)".

**Narration:**

> Let A be a two by two matrix, and v a vector in the plane. Usually A v points somewhere new. But sometimes A v lands on the same line as v. Then A v is just a scalar multiple of v. We write this as A v equals lambda v. The vector v, which must not be zero, is called an eigenvector. The number lambda is its eigenvalue. If lambda is bigger than one, the vector stretches. Between zero and one, it shrinks. If lambda is negative, it flips. Our goal: find all such pairs, lambda and v.

**Manim notes:** `MathTex("A", "\\mathbf{v}", "=", "\\lambda", "\\mathbf{v}")` with `set_color_by_tex`.

## Scene 3: Visual intuition (1:20 to 2:35)

**Purpose:** build geometric understanding before any heavy algebra.

**Visuals:**

1. Return to the grid with A = \[\[2, 1\], \[1, 2\]\] shown at the top.
2. Show where the basis vectors go: i = (1, 0) goes to (2, 1), j = (0, 1) goes to (1, 2). Label the columns of A to show "columns are where the basis vectors land".
3. **Non-example:** draw the line through (1, 0). Apply A. The vector lands at (2, 1), off the line. Flash a red cross: "not an eigenvector".
4. **Rotating test:** a blue vector rotates slowly around the origin, with its image A v drawn beside it. A thin angle arc shows the gap between v and A v. Most of the time the arc is open.
5. When the blue vector passes (1, 1), the arc closes to zero. Freeze, turn the vector yellow, and show a label "A v is on the same line". Repeat when it reaches (1, −1) in green. Together, they flag the two special directions.
6. Draw the two lines through the origin along (1, 1) and (1, −1), then apply A to the whole grid again. Both lines stay in place while the grid slides along them: the yellow line stretches by 3, the green one stays the same length.
7. Optional: the unit square becomes a parallelogram, with area counter going from 1 to 3.

**Narration:**

> First, let's see what this matrix does. The first column, two one, is where the vector one zero lands. The second column, one two, is where zero one lands. Now try the vector one zero. It lands at two one, which is not on its original line. So one zero is not an eigenvector. Let's rotate a test vector around the origin and compare it with its image. Most of the time, the image points in a different direction, and there's a gap between them. But watch what happens here, at one one. The gap closes. The image is on the same line. And again here, at one minus one. These are our two special directions. Now apply the matrix to the whole grid. Notice that both lines stay where they are. Along the yellow line, everything is stretched. Along the green line, everything keeps its length. These lines are the skeleton of the transformation. The rest of the plane is just mixing the two.

**Manim notes:** use a `ValueTracker` for the rotating vector angle and `always_redraw` for the image vector and the angle arc.

## Scene 4: Worked example (2:35 to 4:05)

**Purpose:** show every step of finding the eigenvalues and eigenvectors, then verify.

**Visuals (one step at a time, equations stay on screen and slide up as new lines appear):**

1. **Rewrite:** Av = λv becomes Av − λv = 0, then (A − λI)v = 0. Highlight I, the identity.
2. **Key idea:** "We need v ≠ 0, so A − λI must squash the plane. Hence it is singular: det(A − λI) = 0."
3. **Compute A − λI:** \[\[2 − λ, 1\], \[1, 2 − λ\]\].
4. **Determinant:** (2 − λ)² − 1 = λ² − 4λ + 3 = (λ − 1)(λ − 3) = 0. Highlight the roots **λ = 1 and λ = 3** in red.
5. **Eigenvector for λ = 3:** A − 3I = \[\[−1, 1\], \[1, −1\]\]. Both rows give −x + y = 0, so y = x. Choose x = 1: **v = (1, 1)**, in yellow.
6. **Eigenvector for λ = 1:** A − I = \[\[1, 1\], \[1, 1\]\]. Both rows give x + y = 0, so y = −x. Choose x = 1: **v = (1, −1)**, in green.
7. **Verify by substitution:** A(1, 1) = (2 + 1, 1 + 2) = (3, 3) = 3(1, 1). A(1, −1) = (2 − 1, 1 − 2) = (1, −1) = 1(1, −1).
8. **Sanity check:** trace = 2 + 2 = 4 = 3 + 1, det = 4 − 1 = 3 = 3 × 1.

**Narration:**

> Now let's actually compute them. Start with A v equals lambda v. Move everything to one side: A v minus lambda v equals zero. To factor v out, write lambda v as lambda I times v. So A minus lambda I, times v, equals zero. We want a nonzero v that this matrix sends to zero. That can only happen if the matrix squashes the plane, which means its determinant is zero. For our matrix, A minus lambda I is two minus lambda, one, one, two minus lambda. Its determinant is two minus lambda, squared, minus one. Expanding gives lambda squared minus four lambda plus three, which factors as lambda minus one, times lambda minus three. So the eigenvalues are one and three. For lambda equals three, the matrix becomes minus one, one, one, minus one. Both rows say y equals x, so v is one, one. For lambda equals one, both rows say x plus y equals zero, so v is one, minus one. Let's check. A times one, one is three, three, which is three times one, one. And A times one, minus one is one, minus one, which is one times itself. Both check out. One more sanity check: the eigenvalues add up to the trace, four, and multiply to the determinant, three.

**Manim notes:** `MathTex` plus `TransformMatchingTex` for each rewriting step; use `Indicate` to highlight the part that changes; put the matrices in `Matrix` or `bmatrix` MathTex.

## Scene 5: Interpretation (4:05 to 4:50)

**Purpose:** connect the numbers back to the geometry.

**Visuals:**

1. Return to the grid with the two eigen-lines drawn (yellow and green).
2. Show the yellow vector (1, 1) growing to (3, 3) with the label "λ = 3: stretched 3×". Show the green vector (1, −1) staying put with "λ = 1: unchanged".
3. Take a new, ordinary blue vector, e.g. (2, 0). Decompose it as (2, 0) = 1·(1, 1) + 1·(1, −1) with a parallelogram. Apply A: the yellow part triples, the green part stays: A(2, 0) = (3, 3) + (1, −1) = (4, 2). Check: A(2, 0) = (4, 2). ✓
4. Final line: "Eigenvectors turn a complicated transformation into simple stretching along two directions."
5. Brief mention: the area scale factor is det(A) = 3 × 1 = 3, which matches the area counter from Scene 3.

**Narration:**

> What do these numbers tell us? Along the direction one, one, the matrix stretches everything by three. Along one, minus one, it leaves everything alone. Now take any other vector, say two, zero. We can write it as one copy of the yellow vector plus one copy of the green one. Apply the matrix: the yellow part triples, the green part stays. Together that gives four, two, exactly what the matrix gives directly. So eigenvectors turn a messy transformation into simple stretching along two directions. And the area of any shape is scaled by three times one, which is three, the determinant.

**Manim notes:** `Polygon` for the decomposition parallelogram; `Transform` for the stretched components; reuse the colour code.

## Scene 6: Summary and credits (4:50 to 5:20)

**Purpose:** reinforce three takeaways and show references, music credit and AI disclosure.

**Visuals:**

1. Three takeaways appear one at a time:
   - An eigenvector keeps its direction: **Av = λv**.
   - Eigenvalues solve **det(A − λI) = 0**.
   - Each eigenvalue is the scaling factor along its eigenvector.
2. Fade to the closing frame:
   - Title, student name and ID.
   - **References:** (1) your M3 course notes; (2) Strang, *Introduction to Linear Algebra*; (3) the Manim Community documentation. Edit this list to match what you actually used.
   - **Music:** track title, artist, licence and source (if used).
   - **AI disclosure:** list exactly what AI helped with, for example "Claude (Anthropic) was used to help draft the script and Manim code; I reviewed, tested and can explain all of it. Narration was recorded by me."

**Narration:**

> To recap. One: an eigenvector is a direction that a matrix only stretches or flips, written A v equals lambda v. Two: we find the eigenvalues by solving the determinant of A minus lambda I equals zero. Three: each eigenvalue is the scaling factor along its eigenvector. Thanks for watching. References, music credit and AI disclosure are on screen.

## Final checklist for this storyboard

- [ ] Every number on screen matches the example above.
- [ ] Each symbol (A, v, λ, I, det) is defined before it is used.
- [ ] One step per animation, with enough pause to read at 1080p.
- [ ] Colour code is the same in every scene.
- [ ] Total runtime is under 7:00 (target about 5:15).
- [ ] Export this document as PDF and put it in the `Storyboard/` folder of the repo.

## Likely viva questions

1. Why must det(A − λI) = 0? Because a nonzero v is sent to 0 by A − λI, so that matrix is not invertible.
2. Why can an eigenvector be rescaled (e.g. (2, 2) instead of (1, 1))? Because A(cv) = cAv = cλv = λ(cv), so any nonzero multiple is also an eigenvector.
3. Can an eigenvalue be 0? Yes. Then A sends v to 0, so the matrix is singular.
4. What does the LinearTransformationScene in your code do? It draws the grid and basis vectors and animates applying the matrix to everything.
