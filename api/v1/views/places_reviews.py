#!/usr/bin/python3
"""
Module containing views for Place Reviews objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews')
@app_views.route('/places/<place_id>/reviews/')
def list_reviews_of_place(place_id):
    """
    Retrieves a list of all Review objects of a Place.

    Args:
        place_id (str): The ID of the place for which to list reviews.

    Returns:
        JSON: A JSON representation of the list of Review objects.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)

    list_reviews = [review.to_dict() for review in storage
                    .all("Review")
                    .values()
                    if place_id == review.place_id]
    return jsonify(list_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a Review for a Place.

    Args:
        place_id (str): The ID of the place for which to create a review.

    Returns:
        JSON: A JSON representation of the newly created
        Review object with status code 201.
    """
    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data or 'text' not in data:
            abort(400, 'Missing user_id or text')

        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)

        user_obj = storage.get("User", data['user_id'])
        if user_obj is None:
            abort(404)

        new_review = Review(place_id=place_id, **data)
        storage.new(new_review)
        storage.save()

        return jsonify(new_review.to_dict()), 201
    except ValueError:
        abort(400, 'Invalid JSON')


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """
    Retrieves a Review object by ID.

    Args:
        review_id (str): The ID of the review to retrieve.

    Returns:
        JSON: A JSON representation of the Review object.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object by ID.

    Args:
        review_id (str): The ID of the review to delete.

    Returns:
        JSON: An empty JSON response with status code 200.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object by ID.

    Args:
        review_id (str): The ID of the review to update.

    Returns:
        JSON: A JSON representation of the updated
        Review object with status code 200.
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        if 'text' in data:
            review_obj.text = data['text']

        storage.save()
        return jsonify(review_obj.to_dict()), 200
    except ValueError:
        abort(400, 'Invalid JSON')
