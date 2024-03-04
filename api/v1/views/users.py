#!/usr/bin/python3
"""
Module containing views for User objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users/')
@app_views.route('/users')
def list_users():
    """
    Retrieves a list of all User objects.
    """
    list_users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>')
def get_user(user_id):
    """
    Retrieves a User object by ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        JSON: A JSON representation of the User object.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object by ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        JSON: An empty JSON response with status code 200.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """
    Creates a User.

    Args:
        None (uses request.get_json()): The JSON payload containing user information.

    Returns:
        JSON: A JSON representation of the newly created User object with status code 201.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'email' not in data or 'password' not in data:
            abort(400, 'Missing email or password')

        new_user = User(email=data['email'], password=data['password'])
        storage.new(new_user)
        storage.save()

        return jsonify(new_user.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object by ID.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        JSON: A JSON representation of the updated User object with status code 200.
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        if 'first_name' in data:
            user_obj.first_name = data['first_name']

        if 'last_name' in data:
            user_obj.last_name = data['last_name']

        storage.save()

        return jsonify(user_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
