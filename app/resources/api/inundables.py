from os import abort
from flask import jsonify, Blueprint, request, abort
from app.db import db
from app.models.inundable import Inundable
from app.models.configuration import Configuration
from app.schemas.inundable import (
    inundables_schema,
    inundable_schema,
    inundable_pagination_schema,
)

inundable_api = Blueprint("zonas-inundables", __name__,
                          url_prefix="/zonas-inundables")


@inundable_api.get("/")
def index():
    # validate(request.args)
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get(
            "per_page", Configuration.query.one().per_page))
    except:
        return abort(404)
    inundable_page = Inundable.query.paginate(page=page, per_page=per_page)
    # El objeto pagination tiene varios atributos como next, prev, total, page, etc.
    try:
        inundables = inundable_pagination_schema.dump(inundable_page)
        return jsonify(inundables)
    except:
        return abort(500)


@inundable_api.get("/<int:id>")
def indexID(id):
    # Si no se ingresa un numero, error 404
    inundable = Inundable.query.filter(Inundable.id == id).first()
    if inundable == None:
        return abort(404)
    else:
        try:
            inundables = inundable_schema.dump(inundable)
            return {"inundable": inundables}
        except:
            return abort(500)


@inundable_api.post("/")
def create():
    new_inundable = Inundable(**request.get_json())
    db.session.add(new_inundable)
    db.session.commit()
    inundable = inundable_schema.dump(new_inundable)
    return jsonify(inundable)
