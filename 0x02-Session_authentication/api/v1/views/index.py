#!/usr/bin/env python3
""" Module of Index views
"""
from api.v1.auth.basic_auth import BasicAuth
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/api/v1/unauthorized',  methods=['GET'])
def not_auth() -> str:
    """raise unauthorized when one is unauthorized
    """
    abort(401)

@app_views.route('/users/me', methods=['GET'])
def current_user() -> str:
    user = request.current_user
    return jsonify(user)
    
@app_views.route('/api/v1/forbidden',  methods=['GET'])
def forbidden() -> str:
    """raise when one is forbidden to access resource
    """
    abort(403)
