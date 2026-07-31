"""
Flask API for the Solar System backend.

This file is deliberately thin: every route just calls a function from
analysis.py and returns the result as JSON. All the real logic lives in
analysis.py, which keeps the web layer simple and the logic testable.

Run it:
    python3 app.py
Then open http://127.0.0.1:5000/ in a browser. Flask serves index.html itself,
so the page and the API come from the same address and there is nothing else to
start. Visit /api for a list of the JSON endpoints.
"""

import os

from flask import Flask, jsonify, request, abort, send_from_directory
import analysis
from planets_data import PLANETS

# Serve index.html, fp.css and fp.js straight out of this folder, so the whole
# project runs from one command instead of needing a second web server.
HERE = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)


# Allow the static HTML page (opened from a file:// or a different port) to
# call this API from the browser. Fine for a local project; tighten the
# origin before putting anything like this on the public internet.
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def _resolve(name):
    """Match a planet name case-insensitively, or 404."""
    for key in PLANETS:
        if key.lower() == name.lower():
            return key
    abort(404, description="Unknown planet: " + name)


@app.route("/")
def home():
    """Serve the interactive page."""
    return send_from_directory(HERE, "index.html")


@app.route("/<path:filename>")
def static_file(filename):
    """Serve fp.css, fp.js and anything else sitting next to this file."""
    if filename.startswith("api"):
        abort(404, description="Unknown endpoint: /" + filename)
    return send_from_directory(HERE, filename)


@app.route("/api")
def api_index():
    """A small self-describing index so the API is easy to explore."""
    return jsonify({
        "name": "Solar System Analysis API",
        "endpoints": {
            "GET /api/planets": "All planets with derived properties",
            "GET /api/planets/<name>": "One planet (e.g. /api/planets/mars)",
            "GET /api/analysis/summary": "Min / max / mean of each metric",
            "GET /api/analysis/rankings": "Planets ranked by several metrics",
            "GET /api/analysis/correlation": "Distance vs temperature relationship",
            "GET /api/compare?a=Earth&b=Mars": "Compare two planets",
        },
    })


@app.route("/api/planets")
def get_planets():
    return jsonify(analysis.all_planets())


@app.route("/api/planets/<name>")
def get_planet(name):
    return jsonify(analysis.derived_properties(_resolve(name)))


@app.route("/api/analysis/summary")
def get_summary():
    return jsonify(analysis.summary())


@app.route("/api/analysis/rankings")
def get_rankings():
    return jsonify(analysis.rankings())


@app.route("/api/analysis/correlation")
def get_correlation():
    return jsonify(analysis.distance_temp_correlation())


@app.route("/api/compare")
def get_compare():
    a = request.args.get("a", "")
    b = request.args.get("b", "")
    if not a or not b:
        abort(400, description="Provide ?a=<planet>&b=<planet>")
    return jsonify(analysis.compare(_resolve(a), _resolve(b)))


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(err):
    return jsonify({"error": err.description}), err.code


if __name__ == "__main__":
    app.run(debug=True, port=5000)
