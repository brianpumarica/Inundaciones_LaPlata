from flask import abort, jsonify, Blueprint, request
from app.models.configuration import Configuration
from app.models.routes import Route
from app.schemas.route import (
    route_pagination_schema
)

route_api = Blueprint("routes", __name__, url_prefix="/routes")

@route_api.get("/")
def index():
    # validate(request.args)
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get(
            "per_page", Configuration.query.one().per_page))
    except:
        return abort(404)
    route_page = Route.query.paginate(page=page, per_page=per_page)
    # El objeto pagination tiene varios atributos como next, prev, total, page, etc.
    try:
        routes = route_pagination_schema.dump(route_page)
        return jsonify(routes)
    except:
        return abort(500)