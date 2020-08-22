# Programming animations

Animations for helping programming begginers understand some mechanisms, using
[manim](https://github.com/ManimCommunity/manim/#usage).

## Installing manim

Manim may be distributed for your system, but I suggest installing in a
virtualenv using the `requirements.txt` file:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

With a virtualenv, if you open a new terminal and want to use this project in
it, you need to run `source venv/bin/activate` again.

## Building the animations

After installing manim, you can run `manim [options] ocaml.py` to render the animations.
For example, `manim -p ocaml.py` will render and play your choosen animation, `manim
ocaml.py` will only render it.
