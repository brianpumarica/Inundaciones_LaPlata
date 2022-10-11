import re
from sqlalchemy import Column, Integer, String, DateTime
from app.db import db
from flask import session
from datetime import datetime
from flask.helpers import flash


class FollowComplaint(db.Model):
    __tablename__ = "follow_complaint"
    id = Column(Integer, primary_key=True)
    id_complaint = Column(Integer, nullable=False)
    date_creation = Column(DateTime) 
    description = Column(String(3000), nullable=False)
    author = Column(Integer)

    def __init__(
        self,
        id_complaint=None,
        date_creation=None,
        description=None,
        author=None,
    ):
        self.id_complaint = id_complaint
        self.date_creation = date_creation
        self.description = description
        self.author = author
 
    @classmethod   
    def set_attributes_default(cls, follow_complaint):
         # poner en date_creation, la fecha de creacion (actual)
        follow_complaint.date_creation = datetime.now()
        follow_complaint.author =   session["user"]["id"]
        return follow_complaint