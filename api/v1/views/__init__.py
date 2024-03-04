#!/usr/bin/python3
"""
Package containing API view definitions.
"""

from flask import Blueprint

# Can also set static_folder and template_folder
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
