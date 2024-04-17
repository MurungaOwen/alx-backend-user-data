#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")
auth = Auth() if AUTH_TYPE == "auth" else None
auth = BasicAuth() if AUTH_TYPE == "basic_auth" else None



@app.errorhandler(401)
def not_authorized(error) -> str:
    """When someone is not authenticated
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def not_allowed(error) -> str:
    """Not allowed to access the resource
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_func():
    """run before each request is processed"""
    my_url_list =['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']
    if auth and auth.require_auth(request.path, my_url_list):
        if not auth.authorization_header(request):
            abort(401)
        if not auth.current_user(request):
            abort(403)
    if not auth:
        abort(401)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
