from sqlalchemy import false, true
from app.db import db
from app.models.role import Role
from app.models.user import User


def authenticated(session):
    return session.get("user")


def sameid(id, session):
    return session["user"]["id"] == id


def haspermission(id, permission):
    return User.has_permission(id, permission)


def isadmin(id):
    consulta = (
        db.session.query(User, Role)
        .join(User.roles)
        .where(Role.name == "ROL_ADMINISTRADOR")
        .where(User.id == id)
        .first()
    )
    return consulta is not None

def sinrol(id):
    if (not isoperador(id) and not isadmin(id)):
        return true
    return false


def isoperador(id):
    consulta = (
        db.session.query(User, Role)
        .join(User.roles)
        .where(Role.name == "ROL_OPERADOR")
        .where(User.id == id)
        .first()
    )
    return consulta is not None

def check():
    pass


def isnone(value):
    return value == None


def check():
    pass


def isnone(value):
    return value == None

# Devuelve el nombre de usuario de un usuario a partir de su ID


def getusername(id):
    consulta = User.query.where(User.id == id).first()
    if (consulta):
        return consulta.username
    else:
        return "-"
