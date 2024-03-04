#!/usr/bin/python3
"""
Module defining API status route.
"""

from api.v1.views import app_views

@app_views.route("/status")
def index():
    """
    Returns a JSON with status "OK".
    """
    return {"status": "OK"}
