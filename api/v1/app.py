#!/usr/bin/python3
"""
Script contains the Airbnb Clone API.
"""
from os import getenv
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


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
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = int(getenv("HBNB_API_PORT") or 5000)

    app.run(host=host, port=port, debug=True, threaded=True)
