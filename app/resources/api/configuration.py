from os import abort
from flask import jsonify, Blueprint, abort
from app.models.configuration import Configuration
from app.schemas.configuration import (
    configuration_schema
)

configuration_api = Blueprint("configuration", __name__,
                          url_prefix="/configuration")


@configuration_api.get("/")
def index():
    # validate(request.args)
    actual_configuration = Configuration.query.first()
    try:
        config = configuration_schema.dump(actual_configuration)
        return jsonify(config)
    except:
        return abort(500)
