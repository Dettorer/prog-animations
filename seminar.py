# pylint: disable=missing-module-docstring
import manim as m

m.Rectangle.CONFIG["stroke_width"] = 2
m.Line.CONFIG["stroke_width"] = 2

INDENT = m.RIGHT


def get_square_of_pred(arg: str = "x", pred_val: str = "x-1") -> m.VDict:
    """Generate a renderable `square_of_pred` OCaml function"""
    fn_def = m.TextMobject(f"\\verb|let square_of_pred {arg} =|")

    pred_let = (
        m.TextMobject("\\verb|let|")
        .next_to(fn_def, m.DOWN, aligned_edge=m.LEFT)
        .shift(INDENT)
    )
    pred_def = m.VDict(
        (
            "name",
            m.TextMobject("\\verb|pred_x =|").next_to(
                pred_let, m.RIGHT, aligned_edge=m.UP
            ),
        )
    )
    pred_def.add(
        (
            "val",
            m.TextMobject(f"\\verb|{pred_val}|").next_to(
                pred_def["name"], m.RIGHT, aligned_edge=m.UP
            ),
        )
    )
    pred_end = m.TextMobject("\\verb|in|").next_to(pred_def, m.RIGHT, aligned_edge=m.UP)
    pred = m.VDict(("let", pred_let), ("def", pred_def), ("end", pred_end),)

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
        self.play(m.Write(call))

        # Shift the call and show instanciated definition of the function
        def_instance = self.def_box["function"].deepcopy().remove("fn")
        def_instance.generate_target().scale(1 / self.def_scale_ratio).next_to(
            call, m.RIGHT * 5
        )
        lines = m.VGroup(
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
        context = [
            m.TextMobject("Contexte~:", color=m.GRAY).move_to(
                def_instance, aligned_edge=m.LEFT
            )
        ]
        context[0].generate_target().shift(m.UP * 3.5)
        self.play(m.FadeIn(context[0]), m.MoveToTarget(context[0]))
        # add x=val to context
        context.append(
            m.VDict(
                ("name", m.TextMobject("x =", color=m.GRAY)),
                ("val", call["val"].copy().set_color(m.GRAY)),
            )
        )
        context[-1]["name"].next_to(context[-2], m.DOWN, aligned_edge=m.LEFT)
        context[-1]["val"].generate_target().next_to(context[-1]["name"], m.RIGHT)
        self.play(m.Indicate(call["val"]))
        self.play(
            m.ShowCreation(context[-1]["name"]), m.MoveToTarget(context[-1]["val"])
        )

        # Replace x by its value
        self.wait()
        self.play(
            m.Indicate(def_instance["pred"]["def"]["val"]), m.Indicate(context[-1])
        )
        self.play(
            m.Transform(
                def_instance["pred"]["def"]["val"],
                m.TextMobject(f"\\verb|{val}-1|").move_to(
                    def_instance["pred"]["def"]["val"]
                ),
            )
        )
        self.wait()

        # Evaluate pred_x
        self.play(
            m.Transform(
                def_instance["pred"]["def"]["val"],
                m.TextMobject(f"\\verb|{val-1}|").move_to(
                    def_instance["pred"]["def"]["val"]
                ),
            )
        )
        self.wait()
        # add pred_x=val-1 to context
        context.append(def_instance["pred"]["def"])
        context[-1].generate_target().next_to(context[-2], m.DOWN, aligned_edge=m.LEFT)
        context[-1].target.set_color(m.GRAY)
        self.play(m.Indicate(context[-1]))
        self.play(
            m.FadeOut(def_instance["pred"]["let"]),
            m.FadeOut(def_instance["pred"]["end"]),
            m.MoveToTarget(context[-1]),
            m.ApplyMethod(def_instance["res"].move_to, def_instance),
        )
        self.wait()

        # Replace pred_x by its value
        op1 = m.TextMobject(f"\\verb|{val-1}|").move_to(
            def_instance["res"], aligned_edge=m.LEFT
        )
        def_instance["res"]["mul"].generate_target().next_to(op1, m.RIGHT)
        op2 = op1.copy().next_to(def_instance["res"]["mul"].target, m.RIGHT)
        self.play(
            m.Indicate(def_instance["res"]["op1"]),
            m.Indicate(def_instance["res"]["op2"]),
            m.Indicate(context[-1]),
        )
        self.play(
            m.Transform(def_instance["res"]["op1"], op1),
            m.Transform(def_instance["res"]["op2"], op2),
            m.MoveToTarget(def_instance["res"]["mul"]),
        )

        # Evaluate the result
        self.wait()
        self.play(
            m.Transform(
                def_instance["res"],
                m.TextMobject(f"\\verb|{(val-1) * (val-1)}|").move_to(
                    def_instance["res"], aligned_edge=m.LEFT
                ),
            )
        )

        # Wrap up
        self.wait()
        self.play(
            *[m.FadeOut(l) for l in context],
            m.FadeOut(call),
            m.ApplyMethod(def_instance["res"].center),
            m.Uncreate(lines),
        )

    def construct(self) -> None:
        self.construct_def_box()

        self.construct_call(5)

        self.wait()
