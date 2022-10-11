from flask import abort, jsonify, Blueprint, request
from app.db import db
from app.models.locations import Location
from app.models.configuration import Configuration
from app.schemas.location import (
    location_pagination_schema
)

location_api = Blueprint("locations", __name__, url_prefix="/locations")

@location_api.get("/")
def index():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get(
            "per_page", Configuration.query.one().per_page))
    except:
        return abort(404)
    location_page = Location.query.paginate(page=page, per_page=per_page)
    # El objeto pagination tiene varios atributos como next, prev, total, page, etc.
    try:
        locations = location_pagination_schema.dump(location_page)
        return jsonify(locations)
    except:
        return abort(500)