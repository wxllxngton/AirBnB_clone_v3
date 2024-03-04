#!/usr/bin/python3
"""
Module containing views for City objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities')
@app_views.route('/states/<state_id>/cities/')
def list_cities_of_state(state_id):
    """Retrieves a list of all City objects in a specific State"""
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    list_cities = [city.to_dict() for city in storage.all("City").values()
                   if state_id == city.state_id]
    return jsonify(list_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a City in a specific State"""
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        state_obj = storage.get("State", state_id)
        if state_obj is None:
            abort(404)

        new_city = City(name=data['name'], state_id=state_id)
        storage.new(new_city)
        storage.save()

        return jsonify(new_city.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """Retrieves a City object by ID"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object by ID"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object by ID"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        city_obj.name = data.get('name', city_obj.name)
        storage.save()

        return jsonify(city_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
