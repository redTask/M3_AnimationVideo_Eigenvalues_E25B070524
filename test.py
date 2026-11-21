from manim import *


class Test(Scene):
    def construct(self):
        title = Text("Manim works!", font_size=64)
        equation = MathTex(r"e^{i\pi} + 1 = 0")
        group = VGroup(title, equation).arrange(DOWN, buff=0.8)

        self.play(Write(title))
        self.play(FadeIn(equation, shift=UP))
        self.wait(0.5)
        self.play(group.animate.scale(1.2).set_color(YELLOW))
        self.wait(1)
