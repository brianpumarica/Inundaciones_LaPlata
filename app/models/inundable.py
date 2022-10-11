from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db


class Inundable(
    db.Model
):  # Mi clase hereda de db.Model necesariamente para poder referenciar con cada clase a una tabla por medio del ORM
    # Nombre de la tabla que quiero que se una con este modelo
    __tablename__ = "inundables"
    id = Column(Integer, primary_key=True)
    code = Column(String(30))
    name = Column(String(30))
    coordinates = Column(Text)
    status = Column(Boolean)
    color = Column(String(30))

    # Sobreescribo el constructor, para que acepte estos parametros. Se ejecuta al hacer new_user = User()
    def __init__(
        self,
        code=None,
        name=None,
        coordinates=None,
        status=None,
        color=None,
    ):
        self.code = code
        self.name = name
        self.coordinates = coordinates
        self.status = status
        self.color = color

    # Edición de una zona inundable

    @classmethod
    def update(cls, inundable, kwargs):
        inundable.code = kwargs["code"]
        inundable.name = kwargs["name"]
        inundable.coordinates = kwargs["coordinates"]
        inundable.status = kwargs["status"]
        inundable.color = kwargs["color"]
        return inundable
