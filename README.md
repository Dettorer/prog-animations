# Programming animations

Animations for helping programming begginers understand some mechanisms, using
[manim](https://github.com/ManimCommunity/manim/#usage).

## Installing manim

Manim may be distributed for your system, but I suggest installing in a
virtualenv using the `requirements.txt` file:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

With a virtualenv, if you open a new terminal and want to use this project in
it, you need to run `source venv/bin/activate` again.

### With Nix

Alternatively, if using [nix](https://nixos.org/manual/nix/stable/), you can
simply run `nix-shell` in this repository. I suggest using direnv to
automatically load the environment:

```shell
echo "use_nix" > .direnvrc
direnv allow
```

## Building the animations

After installing manim, you can run `manim [options] ocaml.py` to render the
animations.  For example, `manim -p ocaml.py` will render and play your choosen
animation, `manim ocaml.py` will only render it.

## Current animations

- `manim ocaml.py SquareOfPred`: visualize a simple function call evaluation
  with emphasis on the "context" of the evaluation (current name-value
  associations).
- `manim ocaml.py Fact`: visualize a call to a recursive factorial
  implementation to illustrate how different calls have different contexts that
  may be reused when going back up the call stack.
