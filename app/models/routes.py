from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db
from app.helpers.filters import from_string_to_bool


class Route(db.Model):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(30))
    coordinates = Column(String(30))
    status = Column(Boolean)

    def __init__(
        self,
        name=None,
        description=None,
        coordinates=None,
        status=None,
    ):
        self.name = name
        self.description = description
        self.coordinates = coordinates
        self.status = status

    @classmethod
    def update(cls, id, kwargs):
        rou = Route.query.filter_by(id=id).one()
        params = kwargs
        rou.name = params["name"]
        rou.description = params["description"]
        rou.coordinates = params["coordinates"]

    @classmethod
    def update(cls, id, kwargs):
        rou = Route.query.filter_by(id=id).one()
        params = kwargs
        rou.name = params["name"]
        rou.description = params["description"]
        rou.coordinates = params["coordinates"]


    def set_attributes_default(route):
        if route.status == "on":
            route.status = True
