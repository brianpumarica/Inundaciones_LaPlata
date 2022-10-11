from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db
from flask import session
from datetime import datetime
from app.models.follow_complaint import FollowComplaint
from flask.helpers import flash


class Complaint(db.Model):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    date_creation = Column(DateTime) 
    date_closed = Column(DateTime, nullable=True)
    description = Column(String(30), nullable=False)
    status = Column(Integer)
    from_user = Column(Integer)
    surname_user = Column(String(30), nullable=False)
    name_user = Column(String(30), nullable=False)
    telephone = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    category = Column(Integer, nullable=False)
    coordinates = Column(String(30))
    count_calls = Column(Integer)


    def __init__(
        self,
        title=None,
        date_creation=None,
        date_closed=None,
        description=None,
        status=None,
        from_user=None,
        surname_user=None,
        name_user=None,
        telephone=None,
        email=None,
        category=None,
        coordinates=None,
        count_calls=None,
    ):
        self.title = title
        self.date_creation = date_creation
        self.date_closed = date_closed
        self.description = description
        self.status = status
        self.from_user = from_user
        self.surname_user = surname_user
        self.name_user = name_user
        self.telephone = telephone
        self.email = email
        self.category = category
        self.coordinates = coordinates
        self.count_calls = count_calls

    @classmethod
    def set_attributes_default(cls, complaint):
        # poner en from_user, el id del usuario logueado
        complaint.from_user = session["user"]["id"]
        # poner en date_creation, la fecha de creacion (actual)
        """datetime.now() o datetime.today().strftime('%Y-%m-%d') """
        complaint.date_creation = datetime.now()
        # pasar en status, el string de status a int
        complaint.status = 1
        # pasar en category, el string de category a int
        complaint.category = int(complaint.category)
        # Setear en count_calls, 0, ya que recien se crea la denuncia
        complaint.count_calls = 0

    @classmethod
    def update(cls, id, kwargs):
        complaint = Complaint.query.filter_by(id=id).one()
        params = kwargs
        complaint.title = params.get("title", complaint.title)
        complaint.category = params.get("category", complaint.category)
        complaint.description = params.get("description", complaint.description)
        complaint.surname_user = params.get("surname_user", complaint.surname_user)
        complaint.name_user = params.get("name_user", complaint.name_user)
        complaint.coordinates = params.get("coordinates", complaint.coordinates)
        complaint.telephone = params.get("telephone", complaint.telephone)
        complaint.email = params.get("email", complaint.email)
        complaint.status = params.get("status", complaint.status)
        complaint.from_user = session["user"]["id"]
        if complaint.status == '3':
            complaint.date_closed = datetime.now()

    @classmethod
    def not_call(cls, complaint):
        complaint.count_calls = complaint.count_calls + 1
        complaint.from_user = session["user"]["id"]
        if(complaint.count_calls==3):
            complaint.status = 3
            complaint.date_closed = datetime.now()
            description = 'No fue posible contactar al denunciante'
            new_follow = FollowComplaint(complaint.id,complaint.date_closed, description, session["user"]["id"])
            db.session.add(new_follow)
            try:
                db.session.commit()
                flash("El seguimiento de denuncia fue creado correctamente", "success")
            except:
                flash("El seguimiento de denuncia no se pudo crear. Vuelva a intentar.", "danger")
