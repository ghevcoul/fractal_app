#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)


@app.route("/hello")
def hello_world():
    """
    Simple Hello, World to test if server is up.
    """
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
