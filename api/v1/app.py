#!/usr/bin/python3
"""
Script containing the Airbnb Clone API.
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app,
     resources={r"/api/*": {"origins": "0.0.0.0"}})  # Directly initialize CORS

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    """
    Teardown method to close the storage session.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Resource not found error handler.
    """
    return jsonify({'error': 'Not found'})


if __name__ == "__main__":
    """
    Run the Flask server.
    """
    # Get environment variables with default values
    HBNB_API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
