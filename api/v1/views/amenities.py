#!/usr/bin/python3
"""
Module containing views for Amenity objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/')
def list_amenities():
    """
    Retrieves a list of all Amenity objects.

    Returns:
        JSON: A JSON representation of the list of Amenity objects.
    """
    list_amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the amenity to retrieve.

    Returns:
        JSON: A JSON representation of the Amenity object.
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the amenity to delete.

    Returns:
        JSON: An empty JSON response with status code 200.
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """
    Creates an Amenity.

    Returns:
        JSON: A JSON representation of the newly created Amenity object with status code 201.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        new_amenity = Amenity(name=data['name'])
        storage.new(new_amenity)
        storage.save()

        return jsonify(new_amenity.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object by ID.

    Args:
        amenity_id (str): The ID of the amenity to update.

    Returns:
        JSON: A JSON representation of the updated Amenity object with status code 200.
    """
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        amenity_obj.name = data.get('name', amenity_obj.name)
        storage.save()

        return jsonify(amenity_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
