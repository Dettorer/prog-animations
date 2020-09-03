"""Animations showing some OCaml mechanisms"""

from typing import List, Tuple

import manim as m

m.Rectangle.CONFIG["stroke_width"] = 2
m.Line.CONFIG["stroke_width"] = 2

INDENT = m.RIGHT


def replace_expr(scene: m.Scene, expr: m.Mobject, text: str, **kwargs) -> None:
    """Play an animation that transforms an expression in an other

    kwargs are given to a call to the new Mobject's `move_to` method
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

        self.scene = scene

    def add(
        self,
        name: str,
        val_orig: m.Mobject,
        highlight: m.Mobject = None,
        extra_animations: List[m.Animation] = None,
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
        self.scene.play(m.Indicate(highlight if highlight else val_orig))

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

        self.scene.play(
            m.ApplyMethod(self.entries.shift, m.UP * 0.5),
            m.FadeInFrom(association["name"], direction=m.DOWN),
            m.FadeInFrom(association["eq"], direction=m.DOWN),
            m.MoveToTarget(association["val"]),
            *(extra_animations if extra_animations else []),
        )
        self.entries.add(association)
        self.scene.remove(association)  # The previous line created a copy

    def replace_occurrence(self, index: int, occurrence: m.Mobject) -> None:
        """ Replace an occurrence of a name by the value stored in the context,
        highlighting the link between them through animations.

        Warning: index `0` in the context entries is the title line ("Contexte :")
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
        self.scene.play(
            m.ShowCreationThenFadeOut(entry_rect),
            m.ShowCreationThenFadeOut(occurrence_rect),
            m.ShowCreationThenFadeOut(link),
        )

        # Actually replace the occurrence
        self.scene.play(
            m.Transform(
                occurrence, entry["val"].copy().move_to(occurrence).set_color(m.WHITE)
            )
        )


class Fact(m.MovingCameraScene):
    """An animation to illustrate the evaluation of a simple recursive OCaml factorial
    function"""

    def_box = None
    def_scale_ratio = 0.4

    # pylint: disable=too-many-locals
    @staticmethod
    def get_def() -> m.Mobject:
        """Generate a renderable OCaml fact function

        The function:
        ```ocaml
        let rec fact n =
          if n = 0 then
            1
          else
            n * fact (n - 1)
        ```
        """
        # First line: `let rec fact n =`
        fn_line = m.TextMobject("\\verb|let rec fact n =|")

        # Second line: `if n = 0 then`
        # -> `if`
        if_if = (
            m.TextMobject("\\verb|if|")
            .next_to(fn_line, m.DOWN, aligned_edge=m.LEFT)
            .shift(INDENT)
        )
        # -> `n = 0`
        if_cond_n = m.TextMobject("\\verb|n|").next_to(  # `n`
            if_if, m.RIGHT, aligned_edge=m.DOWN
        )
        if_cond_eq = m.TextMobject("\\verb|=|").next_to(if_cond_n, m.RIGHT)  # `=`
        if_cond_zero = m.TextMobject("\\verb|0|").next_to(if_cond_eq, m.RIGHT)  # `0`
        if_cond = m.VDict(  # assembling
            ("n", if_cond_n), ("=", if_cond_eq), ("0", if_cond_zero)
        )
        # -> `then`
        if_then = m.TextMobject("\\verb|then|").next_to(
            if_cond, m.RIGHT, aligned_edge=m.UP
        )
        # <- assembling
        if_line = m.VDict(("if", if_if), ("cond", if_cond), ("then", if_then))

        # Third line: `1`
        base_line = (
            m.TextMobject("\\verb|1|")
            .next_to(if_line, m.DOWN, aligned_edge=m.LEFT)
            .shift(INDENT)
        )

        # Fourth line: `else`
        else_line = (
            m.TextMobject("\\verb|else|")
            .next_to(base_line, m.DOWN, aligned_edge=m.LEFT)
            .shift(-INDENT)
        )

        # Fifth line: `n * fact (n - 1)`
        # -> n
        rec_n = (
            m.TextMobject("\\verb|n|")
            .next_to(else_line, m.DOWN, aligned_edge=m.LEFT)
            .shift(INDENT)
        )
        # -> *
        rec_times = m.TextMobject("\\verb|*|").next_to(
            rec_n, m.RIGHT, aligned_edge=m.UP
        )
        # -> `fact (n - 1)`
        # ---> `fact`
        rec_call_name = m.TextMobject("\\verb|fact|").next_to(
            rec_times, m.RIGHT, aligned_edge=m.DOWN
        )
        # ---> `(n - 1)`
        rec_call_arg_ob = m.TextMobject("\\verb|(|").next_to(  # `(`
            rec_call_name, m.RIGHT, aligned_edge=m.UP
        )
        rec_call_arg_n = m.TextMobject("\\verb|n|").next_to(  # `n`
            rec_call_arg_ob, m.RIGHT * 0.3
        )
        rec_call_arg_min = m.TextMobject("\\verb|-|").next_to(  # `-`
            rec_call_arg_n, m.RIGHT
        )
        rec_call_arg_one = m.TextMobject("\\verb|1|").next_to(  # `1`
            rec_call_arg_min, m.RIGHT
        )
        rec_call_arg_cb = m.TextMobject("\\verb|)|").next_to(  # `)`
            rec_call_arg_one, m.RIGHT * 0.3
        )
        rec_call_arg = m.VDict(  # assembling
            ("(", rec_call_arg_ob),
            ("n", rec_call_arg_n),
            ("-", rec_call_arg_min),
            ("1", rec_call_arg_one),
            (")", rec_call_arg_cb),
        )
        # <--- assembling
        rec_call = m.VDict(("name", rec_call_name), ("arg", rec_call_arg))
        # <- assembling
        rec = m.VDict(("n", rec_n), ("*", rec_times), ("call", rec_call))

        return m.VDict(
            ("fn", fn_line),
            ("if", if_line),
            ("base", base_line),
            ("else", else_line),
            ("rec", rec),
        ).move_to(m.ORIGIN)

    def construct_def_box(self):
        """Construct the function's definition in a box"""
        fact = self.get_def()
        rect = m.Rectangle().surround(fact, stretch=True)

        self.play(m.Write(fact))
        self.play(m.ShowCreation(rect))

        self.def_box = m.VDict(("function", fact), ("box", rect))
        self.def_box.generate_target().scale(self.def_scale_ratio).to_corner(m.UL)

        self.play(m.MoveToTarget(self.def_box))

    def construct_call(self, val: int) -> None:
        """Show how a call to the function with the given argument is evaluated"""
        call = m.VDict(
            ("name", m.TextMobject("\\verb|fact|").shift(m.LEFT * 5 + m.DOWN * 0.7)),
            ("val", m.TextMobject(f"\\verb|{val}|")),
        )
        call["val"].next_to(call["name"], m.RIGHT, aligned_edge=m.UP)
        self.play(m.FadeIn(call))

        # Show the first call
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
        self.wait()
        self.play(m.Indicate(self.def_box))
        self.play(
            m.MoveToTarget(def_instance), m.ShowCreation(lines),
        )
        self.wait()

        _, res_mobject = self.eval_call(def_instance, val, call["val"])

        self.play(m.FadeOut(call), m.FadeOut(lines), m.ApplyMethod(res_mobject.center))

    def eval_call(
        self, call: m.Mobject, val: int, val_mobject: m.Mobject
    ) -> Tuple[int, m.Mobject]:
        """Show the evaluation of one function call, recursively

        call: the manim object representing the call, expected to be oneline
        val: the value of `n` for that call

        Returns the value and the corresponding Mobject of the result of the call
        """
        context = CallContext(call, self)
        context.add("n", val_mobject)
        self.wait()

        # Evaluate the if's condition
        context.replace_occurrence(-1, call["if"]["cond"]["n"])
        self.wait()
        replace_expr(self, call["if"]["cond"], f"\\verb|{str(val == 0).lower()}|")

        # Replace the expression with the correct if branch
        self.wait()
        self.play(m.Indicate(call["if"]["cond"]))
        if val == 0:
            bad = "rec"
            good = "base"
        else:
            good = "rec"
            bad = "base"
        strike_through = m.Line(
            call[bad].get_corner(m.DL) + m.DL * 0.1,
            call[bad].get_corner(m.UR) + m.UR * 0.1,
        )
        rect = m.Rectangle().surround(call[good], stretch=True)
        self.play(m.ShowCreation(strike_through), m.ShowCreation(rect))
        self.wait()
        self.play(
            *map(m.FadeOut, [strike_through, rect, call["if"], call[bad], call["else"]])
        )
        self.play(
            m.ApplyMethod(call[good].next_to, call.get_corner(m.LEFT), m.RIGHT * 0.1)
        )

        if val == 0:  # end of recursion
            self.play(*map(m.FadeOut, context.entries))
            return 1, call["base"]

        # Evaluate the expression containing the recursive call up to the call, starting
        # by the right-hand operand of the multiplication
        self.wait()
        self.play(m.Indicate(call["rec"]["call"]))
        context.replace_occurrence(-1, call["rec"]["call"]["arg"]["n"])
        self.wait(m.DEFAULT_WAIT_TIME / 2)
        replace_expr(
            self, call["rec"]["call"]["arg"], f"\\verb|{val - 1}|", aligned_edge=m.LEFT
        )
        # Evaluate the recursive call
        rect = m.Rectangle(color=m.BLUE).surround(call["rec"]["call"], stretch=True)
        def_instance = self.def_box["function"].deepcopy().remove("fn")
        def_instance.generate_target().scale(1 / self.def_scale_ratio).next_to(
            rect, m.RIGHT * 5
        )
        lines = m.Group(
            m.Line(
                rect.get_corner(m.RIGHT),
                def_instance.target.get_corner(m.LEFT) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
            m.Line(
                def_instance.target.get_corner(m.DL) + m.LEFT * 0.2,
                def_instance.target.get_corner(m.UL) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
        )
        self.play(m.ShowCreation(rect))
        self.wait(m.DEFAULT_WAIT_TIME / 2)
        self.play(m.Indicate(self.def_box))
        self.play(m.MoveToTarget(def_instance), m.ShowCreation(lines))
        self.wait()
        shift_vector = (
            call["rec"]["call"]["arg"].get_center() - val_mobject.get_center()
        )
        self.play(
            m.ApplyMethod(self.camera_frame.shift, shift_vector),
            m.ApplyMethod(self.def_box.shift, shift_vector),
        )
        recursive_call_res, recursive_call_res_mobject = self.eval_call(
            def_instance, val - 1, call["rec"]["call"]["arg"]
        )
        self.play(
            m.ApplyMethod(self.camera_frame.shift, -shift_vector),
            m.ApplyMethod(self.def_box.shift, -shift_vector),
        )
        self.play(
            m.FadeOut(lines),
            m.FadeOut(rect),
            m.FadeOut(call["rec"]["call"]),
            m.ApplyMethod(
                recursive_call_res_mobject.next_to, call["rec"]["*"], m.RIGHT
            ),
        )
        self.wait()
        call["rec"]["call"] = recursive_call_res_mobject
        # Evaluate the left-hand operand of the multiplication
        context.replace_occurrence(-1, call["rec"]["n"])
        res = val * recursive_call_res
        replace_expr(self, call["rec"], f"\\verb|{res}|", aligned_edge=m.LEFT)
        self.play(*map(m.FadeOut, context.entries))
        return res, call["rec"]

    def construct(self) -> None:
        self.construct_def_box()
        self.construct_call(4)
        self.wait()


class SquareOfPred(m.Scene):
    """An animation to illustrate the evaluation of a simple OCaml function"""

    def_box = None
    def_scale_ratio = 0.5

    @staticmethod
    def get_def() -> m.VDict:
        """Generate a renderable `square_of_pred` OCaml function

        The function:
        ```ocaml
        let square_of_pred x =
            let pred_x = x-1 in
            pred_x * pred_x
        ```
        """
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
        pred_end = m.TextMobject("\\verb|in|").next_to(
            pred_def, m.RIGHT, aligned_edge=m.UP
        )
        pred = m.VDict(("let", pred_let), ("def", pred_def), ("end", pred_end),)

        ### Last line: `pred_x * pred_x`
        res = m.VDict(
            (
                "op1",
                m.TextMobject("\\verb|pred_x|").next_to(
                    pred, m.DOWN, aligned_edge=m.LEFT
                ),
            )
        )
        res.add(("mul", m.TextMobject("\\verb|*|").next_to(res["op1"], m.RIGHT)))
        res.add(("op2", res["op1"].copy().next_to(res["mul"], m.RIGHT)))

        return m.VDict(("fn", fn_def), ("pred", pred), ("res", res))

    def construct_def_box(self) -> None:
        """Show the creation of the OCaml definiton, with a box"""
        # Create the function definition and its rectangular box
        self.def_box = m.VDict(("function", self.get_def()))
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
        self.wait()
        self.play(m.Indicate(self.def_box))
        self.play(
            m.MoveToTarget(def_instance), m.ShowCreation(lines),
        )
        self.wait()

        # Show context
        context = CallContext(def_instance, self)
        # add x=val to context
        context.add("x", call["val"])

        # Replace x by its value
        self.wait()
        context.replace_occurrence(-1, def_instance["pred"]["def"]["val"]["x"])
        self.wait()

        # Evaluate pred_x
        replace_expr(self, def_instance["pred"]["def"]["val"], f"\\verb|{val-1}|")
        self.wait()
        # add pred_x=val-1 to context
        context.add(
            "pred\\_x",
            def_instance["pred"]["def"]["val"],
            highlight=def_instance["pred"],
            extra_animations=[
                m.FadeOutAndShift(def_instance["pred"], direction=m.UP),
                m.ApplyMethod(def_instance["res"].next_to, lines[1], m.RIGHT),
            ],
        )
        self.wait()

        # Replace pred_x by its value
        context.replace_occurrence(-1, def_instance["res"]["op2"])
        context.replace_occurrence(-1, def_instance["res"]["op1"])

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
