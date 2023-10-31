#!/usr/bin/python3
"""
Defines CRUD actions for Place objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
import json

@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for Place objects based on JSON request body"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    all_places = storage.all(Place).values()

    if not states and not cities and not amenities:
        return jsonify([place.to_dict() for place in all_places])

    if states:
        states_places = set()
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    states_places.update(city.places)
        places.extend(states_places)

    if cities:
        cities_places = set()
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                cities_places.update(city.places)
        places.extend(cities_places)

    if amenities:
        amenities_places = set()
        for place in places:
            if all(amenity_id in place.amenities_id for amenity_id in amenities):
                amenities_places.add(place)
        places = list(amenities_places)

    return jsonify([place.to_dict() for place in places])
