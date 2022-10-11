from os import abort
from flask import jsonify, Blueprint, request, abort, session
from app.db import db
from app.models.complaint import Complaint
from app.models.configuration import Configuration
from app.schemas.complaint import (
    complaints_schema,
    complaint_schema,
    complaint_pagination_schema,
)
from datetime import datetime, date

complaint_api = Blueprint("complaints", __name__, url_prefix="/complaints")


@complaint_api.get("/")
def index():
    # Validar lo que viene
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get(
        "per_page", Configuration.query.one().per_page))
    complaint_page = Complaint.query.paginate(page=page, per_page=per_page)
    # El objeto pagination tiene varios atributos como next, prev, total, page, etc.
    complaints = complaint_pagination_schema.dump(complaint_page)
    return jsonify(complaints)


@complaint_api.post("/")
def create():
    data = request.get_json()
    data["date_creation"] = datetime.now()
    data["status"] = 0
    data["count_calls"] = 0
    new_complaint = Complaint(**data)
    db.session.add(new_complaint)
    db.session.commit()
    complaint = complaint_schema.dump(new_complaint)
    return jsonify(complaint)

"""
example en postman
{
    "title": "NUEVITO98",
    "description": "Se inundo por falta de tapa",
    "category": 1,
    "surname_user": "Ele",
    "name_user": "Gante",
    "telephone": "2214377477",
    "email": "queloque@gmail.com",
    "coordinates": "-34.9187, -57.956"
}
"""