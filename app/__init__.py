#!/usr/bin/env python3

from flask import Flask, Markup, render_template, url_for

from . import fractal_tree

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    """
    Simple Hello, World to test if server is up.
    """
    return "Hello, World!"

@app.route("/")
@app.route("/tree")
def display_tree():
    """
    Make a random fractal tree and display it.
    """
    tree = fractal_tree.build_tree()
    svg_string = fractal_tree.get_tree_xml(tree)

    return render_template("fractal.html", image=Markup(svg_string))


if __name__ == "__main__":
    app.run(debug=True)
