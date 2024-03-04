#!/usr/bin/python3
"""
Module containing views for State objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def list_states():
    """
    Retrieves a list of all State objects.

    Returns:
        JSON: A JSON representation of the list of State objects.
    """
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Retrieves a State object by ID.

    Args:
        state_id (str): The ID of the state to retrieve.

    Returns:
        JSON: A JSON representation of the State object.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object by ID.

    Args:
        state_id (str): The ID of the state to delete.

    Returns:
        JSON: An empty JSON response with status code 200.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """
    Creates a State.

    Returns:
        JSON: A JSON representation of the newly created
        State object with status code 201.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        new_state = State(name=data['name'])
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Updates a State object by ID.

    Args:
        state_id (str): The ID of the state to update.

    Returns:
        JSON: A JSON representation of the updated
        State object with status code 200.
    """
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, key, value)

        storage.save()

        return jsonify(state_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
