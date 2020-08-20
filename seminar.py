import manim as m

m.Rectangle.CONFIG["stroke_width"] = 2
m.Line.CONFIG["stroke_width"] = 2

INDENT = m.RIGHT


def get_square_of_pred(x="x", pred_val="x-1", res="pred_x * pred_x"):
    fn_def = m.TextMobject(f"\\verb|let square_of_pred {x} =|")

    pred_def = (
        m.TextMobject(f"\\verb|let pred_x =|")
        .next_to(fn_def, m.DOWN, aligned_edge=m.LEFT)
        .shift(INDENT)
    )
    pred_value = m.TextMobject(f"\\verb|{pred_val}|").next_to(
        pred_def, m.RIGHT, aligned_edge=m.UP
    )
    pred_end = m.TextMobject("\\verb|in|").next_to(
        pred_value, m.RIGHT, aligned_edge=m.UP
    )
    pred = m.VDict(("def", pred_def), ("val", pred_value), ("end", pred_end),)

    res_def = m.TextMobject(f"\\verb|{res}|").next_to(pred, m.DOWN, aligned_edge=m.LEFT)

    return m.VDict(("fn", fn_def), ("pred", pred), ("res", res_def))


class SquareOfPred(m.Scene):
    def_box = None

    def construct_def_box(self):
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
        self.def_box.target.scale(0.5).to_corner(m.UL)
        self.play(m.MoveToTarget(self.def_box))

    def construct_call(self, val):
        """val: the argument given to square_of_pred"""

        call = m.TextMobject(f"\\verb|square_of_pred {val}|")
        self.play(m.Write(call))

        # Shift the call and show instanciated definition of the function
        self.play(m.ApplyMethod(call.shift, m.LEFT * 2 + m.DOWN))
        def_instance = get_square_of_pred().remove("fn")
        def_instance.next_to(call, m.RIGHT * 5)
        lines = m.VGroup(
            m.Line(
                call.get_corner(m.RIGHT) + m.RIGHT * 0.2,
                def_instance.get_corner(m.LEFT) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
            m.Line(
                def_instance.get_corner(m.DL) + m.LEFT * 0.2,
                def_instance.get_corner(m.UL) + m.LEFT * 0.2,
                color=m.BLUE,
            ),
        )
        def_copy = m.VDict(
            ("pred", self.def_box["function"]["pred"].deepcopy()),
            ("res", self.def_box["function"]["res"].deepcopy()),
        )
        self.play(
            m.Transform(def_copy, def_instance), m.ShowCreation(lines),
        )
        def_instance = def_copy

        # Show context
        context = [
            m.TextMobject("Contexte~:", color=m.GRAY).move_to(
                def_instance, aligned_edge=m.LEFT
            )
        ]
        context[0].generate_target().shift(m.UP * 4)
        self.play(m.FadeIn(context[0]), m.MoveToTarget(context[0]))
        # add x=val to context
        context.append(call.deepcopy())
        self.play(
            m.Transform(
                context[-1],
                m.TextMobject(f"x = {val}", color=m.GRAY).next_to(
                    context[-2], m.DOWN, aligned_edge=m.LEFT
                ),
            )
        )

        # Replace x by its value
        self.wait()
        self.play(
            m.Transform(
                def_instance["pred"]["val"],
                m.TextMobject(f"\\verb|{val}-1|").move_to(def_instance["pred"]["val"]),
            )
        )

        # Evaluate pred_x
        def_instance_3 = (
            get_square_of_pred(pred_val=f" {val-1} ")
            .remove("fn")
            .next_to(call, m.RIGHT * 5)
        )
        self.remove(def_instance)
        self.play(m.Transform(def_instance, def_instance_3))
        # add pred_x=val-1 to context
        self.wait()
        context.append(def_instance["pred"])
        self.play(
            m.Transform(
                context[-1],
                m.TextMobject(f"pred\\_x = {val-1}", color=m.GRAY).next_to(
                    context[-2], m.DOWN, aligned_edge=m.LEFT
                ),
            ),
            m.ApplyMethod(def_instance["res"].move_to, def_instance),
        )

        # Replace pred_x by its value
        self.wait()
        self.play(
            m.Transform(
                def_instance["res"],
                m.TextMobject(f"\\verb|{val-1} * {val-1}|").move_to(
                    def_instance["res"], aligned_edge=m.LEFT
                ),
            )
        )

        # Evaluate the result
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
            m.Transform(
                call, m.TextMobject(f"\\verb|{(val-1) * (val-1)}|").move_to(call)
            ),
            m.Uncreate(def_instance["res"]),
            m.Uncreate(lines),
        )
        self.play(m.ApplyMethod(call.move_to, m.ORIGIN))

    def construct(self):
        self.construct_def_box()

        self.construct_call(5)

        self.wait()
