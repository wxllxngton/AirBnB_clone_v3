#!/usr/bin/python3
"""
Module containing views for Place objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places')
@app_views.route('/cities/<city_id>/places/')
def list_places_of_city(city_id):
    """Retrieves a list of all Place objects in a specific City"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)

    list_places = [place.to_dict() for place in storage.all("Place").values()
                   if city_id == place.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    """Retrieves a Place object by ID"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place in a specific City"""
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data or 'name' not in data:
            abort(400, 'Missing user_id or name')

        city_obj = storage.get("City", city_id)
        if city_obj is None:
            abort(404)

        user_obj = storage.get("User", data['user_id'])
        if user_obj is None:
            abort(404)

        new_place = Place(city_id=city_id, **data)
        storage.new(new_place)
        storage.save()

        return jsonify(new_place.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object by ID"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key in ['name', 'description', 'number_rooms', 'number_bathrooms',
                    'max_guest', 'price_by_night', 'latitude', 'longitude']:
            if key in data:
                setattr(place_obj, key, data[key])

        storage.save()
        return jsonify(place_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
