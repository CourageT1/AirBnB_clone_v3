#!/usr/bin/python3
"""
This module creates a Flask web application for the AirBnB clone project.
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the storage when the app context is torn down."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = '0.0.0.0' if not os.getenv(
'HBNB_API_HOST') else os.getenv('HBNB_API_HOST')
    port = 5000 if not os.getenv(
'HBNB_API_PORT') else int(os.getenv('HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)
