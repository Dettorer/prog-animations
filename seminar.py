# pylint: disable=missing-module-docstring
from typing import List

import manim as m

m.Rectangle.CONFIG["stroke_width"] = 2
m.Line.CONFIG["stroke_width"] = 2

INDENT = m.RIGHT


def replace_expr(scene: m.Scene, expr: m.Mobject, text: str, **kwargs) -> None:
    """Play an animation that transforms an expression in an other

    kwargs are given to the new Mobject creation function
    """
    scene.play(m.Transform(expr, m.TextMobject(text).move_to(expr, **kwargs)))


class CallContext:
    """
    A renderable list of name-value associations representing the context of
    a function call, plus some helper functions that uses the context.
    """

    def __init__(self, origin: m.Mobject, scene: m.Scene):
        self.entries = m.Group(
            m.TextMobject("Contexte~:", color=m.GRAY).next_to(
                origin, m.UP * 2, aligned_edge=m.LEFT
            )
        )
        scene.play(m.FadeInFrom(self.entries, direction=m.DOWN))

    # pylint: disable=too-many-arguments
    # pylint: disable=dangerous-default-value
    def add(
        self,
        name: str,
        val_orig: m.Mobject,
        scene: m.Scene,
        highlight: m.Mobject = None,
        extra_animations: List[m.Animation] = [],
    ) -> None:
        """Add an name-value association to the context and return animations

        name -- the name part of the association
        val_orig -- a Mobject that is the value part of the association
        highlight -- a Mobject that should be highlighted before other animations are
            played, defaults to val_orig
        extra_animations -- animations to be played along the others during the last
            step

        This creates a copy of `val_orig` and sets its target to the position of
        the value in the context, the returned animations will make the copy
        move to this position.
        """
        scene.play(m.Indicate(highlight if highlight else val_orig))

        association = m.VDict(
            ("name", m.TextMobject(name, color=m.GRAY)),
            ("eq", m.TextMobject("=", color=m.GRAY)),
            ("val", val_orig.copy()),
        )
        association["name"].move_to(self.entries[-1], aligned_edge=m.LEFT)
        association["eq"].next_to(association["name"], m.RIGHT)
        association["val"].generate_target().next_to(
            association["eq"], m.RIGHT
        ).set_color(m.GRAY)

        scene.play(
            m.ApplyMethod(self.entries.shift, m.UP * 0.5),
            m.FadeInFrom(association["name"], direction=m.DOWN),
            m.FadeInFrom(association["eq"], direction=m.DOWN),
            m.MoveToTarget(association["val"]),
            *extra_animations,
        )
        self.entries.add(association)
        scene.remove(association)  # The previous line created a copy

    def replace_occurrence(
        self, index: int, occurrence: m.Mobject, scene: m.Scene
    ) -> None:
        """
        Replace an occurrence of a name by the value store in the context,
        highlighting the link between them through animations
        """
        entry = self.entries[index]

        # Highlight what's going to happen with little linked rectangles around
        # the entry and the occurrence
        entry_rect = m.Rectangle(color=m.GREEN).surround(entry, stretch=True)
        occurrence_rect = m.Rectangle(color=m.GREEN).surround(occurrence, stretch=True)
        link = m.Line(
            entry_rect.get_corner(m.DOWN),
            occurrence_rect.get_corner(m.UP),
            color=m.GREEN,
        )
        scene.play(
            m.ShowCreationThenFadeOut(entry_rect),
            m.ShowCreationThenFadeOut(occurrence_rect),
            m.ShowCreationThenFadeOut(link),
        )

        # Actually replace the occurrence
        scene.play(
            m.Transform(
                occurrence, entry["val"].copy().move_to(occurrence).set_color(m.WHITE)
            )
        )


def get_square_of_pred() -> m.VDict:
    """Generate a renderable `square_of_pred` OCaml function"""
    # first line: `let square_of_pred x =`
    fn_def = m.TextMobject("\\verb|let square_of_pred x =|")

    # second line: `let pred_x = x - 1 in`
    # -> let
    pred_let = (
        m.TextMobject("\\verb|let|")
        .next_to(fn_def, m.DOWN, aligned_edge=m.LEFT)
        .shift(INDENT)
    )
    # -> pred_x = x - 1
    # ---> pred_x =
    pred_def = m.VDict(
        (
            "name",
            m.TextMobject("\\verb|pred_x =|").next_to(
                pred_let, m.RIGHT, aligned_edge=m.UP
            ),
        )
    )
    # ---> x - 1
    # -----> x
    pred_def_val = m.VDict(
        ("x", m.TextMobject("\\verb|x|").next_to(pred_def["name"], m.RIGHT),)
    )
    # -----> - 1
    pred_def_val.add(
        (
            "min",
            m.TextMobject("\\verb|- 1|").next_to(
                pred_def_val["x"], m.RIGHT, aligned_edge=m.DOWN
            ),
        )
    )
    pred_def.add(("val", pred_def_val))
    ## in
    pred_end = m.TextMobject("\\verb|in|").next_to(pred_def, m.RIGHT, aligned_edge=m.UP)
    pred = m.VDict(("let", pred_let), ("def", pred_def), ("end", pred_end),)

    ### Last line: `pred_x * pred_x`
    res = m.VDict(
        (
            "op1",
            m.TextMobject("\\verb|pred_x|").next_to(pred, m.DOWN, aligned_edge=m.LEFT),
        )
    )
    res.add(("mul", m.TextMobject("\\verb|*|").next_to(res["op1"], m.RIGHT)))
    res.add(("op2", res["op1"].copy().next_to(res["mul"], m.RIGHT)))

    return m.VDict(("fn", fn_def), ("pred", pred), ("res", res))


class SquareOfPred(m.Scene):
    """An animation to illustrate the evaluation of a simple OCaml function

    The function:
    ```ocaml
    let square_of_pred x =
        let pred_x = x-1 in
        pred_x * pred_x
    ```
    """

    def_box = None
    def_scale_ratio = 0.5

    def construct_def_box(self) -> None:
        """Show the creation of the OCaml definiton, with a box"""
        # Create the function definition and its rectangular box
        self.def_box = m.VDict(("function", get_square_of_pred()))
        self.def_box.add(
            ("box", m.Rectangle(height=1.5).surround(self.def_box["function"]))
        )

        # Animate the creations
        self.play(m.Write(self.def_box["function"]))
        self.play(m.ShowCreation(self.def_box["box"]))

        # Move and scale down to up-left corner of the scene
        self.def_box.generate_target()
        self.def_box.target.scale(self.def_scale_ratio).to_corner(m.UL)
        self.play(m.MoveToTarget(self.def_box))

    def construct_call(self, val: int) -> None:
        """Show how a call to the OCaml function is evaluated

        val: the argument given to square_of_pred
        """
        call = m.VDict(
            ("name", m.TextMobject("\\verb|square_of_pred|").shift(m.LEFT * 2)),
            ("val", m.TextMobject(f"\\verb|{val}|")),
        )
        call["val"].next_to(call["name"], m.RIGHT, aligned_edge=m.UP)
        self.play(m.FadeIn(call))

        # Shift the call and show instanciated definition of the function
        def_instance = self.def_box["function"].deepcopy().remove("fn")
        def_instance.generate_target().scale(1 / self.def_scale_ratio).next_to(
            call, m.RIGHT * 5
        )
        lines = m.Group(
            m.Line(
                call.get_corner(m.RIGHT) + m.RIGHT * 0.2,
                def_instance.target.get_corner(m.LEFT) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
            m.Line(
                def_instance.target.get_corner(m.DL) + m.LEFT * 0.2,
                def_instance.target.get_corner(m.UL) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
        )
        self.play(m.Indicate(self.def_box))
        self.play(
            m.MoveToTarget(def_instance), m.ShowCreation(lines),
        )
        self.wait()

        # Show context
        context = CallContext(def_instance, self)
        # add x=val to context
        context.add("x", call["val"], self)

        # Replace x by its value
        self.wait()
        context.replace_occurrence(-1, def_instance["pred"]["def"]["val"]["x"], self)
        self.wait()

        # Evaluate pred_x
        replace_expr(self, def_instance["pred"]["def"]["val"], f"\\verb|{val-1}|")
        self.wait()
        # add pred_x=val-1 to context
        context.add(
            "pred\\_x",
            def_instance["pred"]["def"]["val"],
            self,
            highlight=def_instance["pred"],
            extra_animations=[
                m.FadeOutAndShift(def_instance["pred"], direction=m.UP),
                m.ApplyMethod(def_instance["res"].next_to, lines[1], m.RIGHT),
            ],
        )
        self.wait()

        # Replace pred_x by its value
        context.replace_occurrence(-1, def_instance["res"]["op2"], self)
        context.replace_occurrence(-1, def_instance["res"]["op1"], self)

        # Evaluate the result
        self.wait()
        replace_expr(
            self,
            def_instance["res"],
            f"\\verb|{(val-1) * (val-1)}|",
            aligned_edge=m.LEFT,
        )

        # Wrap up
        self.wait()
        self.play(
            m.FadeOut(context.entries),
            m.FadeOut(call),
            m.ApplyMethod(def_instance["res"].center),
            m.Uncreate(lines),
        )

    def construct(self) -> None:
        self.construct_def_box()

        self.construct_call(5)

        self.wait()
