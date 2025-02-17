"""The Flask app that serves the web interface and controls."""

import threading
from flask import Flask, render_template, request, jsonify
from core.AppController import AppController
from core.utils import get_foreground_window


app = Flask(__name__)

controller = AppController("Stremio", auto_connect=False)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/run_action", methods=["POST"])
def run_action():
    """Run the selected action(s) on the foreground window."""
    actions_list = request.form.getlist("action")
    threading.Thread(target=process_actions, args=(actions_list,)).start()
    return "", 204


@app.route("/foreground_window", methods=["GET"])
def foreground_window():
    """Return the title of the foreground window."""
    return jsonify({"title": get_foreground_window()})


@app.route("/state", methods=["GET"])
def state():
    """Return the current state of the app."""
    print(get_foreground_window())
    return jsonify({"fullscreen": controller.is_fullscreen})


def process_actions(actions_list):
    """Process the selected actions on the foreground window."""
    print(get_foreground_window())
    if not controller.app:
        controller.connect_app()
    for action in actions_list:
        controller.send_action(action)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
