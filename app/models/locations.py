from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    address = Column(String(30), nullable=False)
    status = Column(Boolean)
    telephone = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    coordinates = Column(String(30))

    def __init__(
        self,
        name=None,
        address=None,
        status=None,
        telephone=None,
        email=None,
        coordinates=None,
    ):
        self.name = name
        self.address = address
        self.status = status
        self.telephone = telephone
        self.email = email
        self.coordinates = coordinates

    @classmethod
    def update(cls, id, kwargs):
        loc = Location.query.filter_by(id=id).one()
        params = kwargs
        loc.name = params.get("name", loc.name)
        loc.address = params.get("address", loc.address)
        loc.coordinates = params.get("coordinates", loc.coordinates)
        loc.telephone = params.get("telephone", loc.telephone)
        loc.email = params.get("email", loc.email)
        return loc


    def set_attributes_default(loc):
        if loc.status == "on":
            loc.status = True