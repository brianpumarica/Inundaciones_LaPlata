from flask import render_template, request
from flask.json import jsonify


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return make_response(kwargs, 404)


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return make_response(kwargs, 401)


def internal_error(e):
    kwargs = {
        "error_name": "500 Internal Server error",
        "error_description": "Algo salio mal!",
    }
    return make_response(kwargs, 500)


def make_response(data, status):
    if request.path.startswith("/api/"):
        return jsonify(data), status
    else:
        return render_template("error.html", **data), status
