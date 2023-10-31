#!/usr/bin/python3
"""
Defines API routes for status and object counts.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns a JSON response with the status "OK".
    """
    return jsonify(status="OK")


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """
    Retrieves the number of each object type and returns the counts as JSON.

    Returns:
        JSON response with the counts of each object type.
    """
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    count = {
        'Amenity': storage.count('Amenity'),
        'City': storage.count('City'),
        'Place': storage.count('Place'),
        'Review': storage.count('Review'),
        'State': storage.count('State'),
        'User': storage.count('User')
    }
    return jsonify(count)
