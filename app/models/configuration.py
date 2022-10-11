from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db


class Configuration(db.Model):
    __tablename__ = "configuration"
    id = Column(Integer, primary_key=True)
    order = Column(Boolean)
    per_page = Column(Integer)
    color_public = Column(String(255))
    color_private = Column(String(255))

def __init__(
    self, order=None, per_page=None, color_public=None, color_private=None
):
    self.order = order
    self.per_page = per_page
    self.color_public = color_public
    self.color_private = color_private
