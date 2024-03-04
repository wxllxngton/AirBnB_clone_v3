#!/usr/bin/python3
"""
Script contains the Airbnb Clone API.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

import os

app = Flask(__name__)

@app.teardown_appcontext
def close_session(exception):
    """
    Teardown method to close the storage session.
    """
    storage.close()

if __name__ == "__main__":
    """
    Run the Flask server.
    """
    # Get environment variables
    host = os.getenv("HBNB_API_HOST") or '0.0.0.0'
    port = int(os.getenv("HBNB_API_PORT") or 5000)

    app.run(host=host, port=port, debug=True, threaded=True)
