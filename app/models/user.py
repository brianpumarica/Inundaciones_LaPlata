from flask.helpers import flash
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from app.db import db
from app.helpers.filters import order_converter
from flask import request
from app.models.configuration import Configuration
from app.models.permission import Permission
from app.models.role import Role
import hashlib

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True)
    password = Column(String(254))
    active = Column(Boolean)
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(100), unique=True)
    roles = db.relationship(
        "Role",
        secondary="user_roles",
    )

    # Sobreescribo el constructor, para que acepte estos parametros. Se ejecuta al hacer new_user = User()

    # def __init__(
    #     self,
    #     first_name=None,
    #     last_name=None,
    #     username=None,
    #     active=1,
    #     email=None,
    #     password=None,
    # ):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.username = username
    #     self.active = active
    #     self.email = email
    #     self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    #     # hashlib.sha256("a".encode('utf-8')).hexdigest()
    #     # self.password = hashlib.md5(password.encode(
    #     #     'utf-8')).hexdigest()  # guarda la password hasheada


    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        username=None,
        active=1,
        email=None,
        # password=None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.active = active
        self.email = email
        # self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        # hashlib.sha256("a".encode('utf-8')).hexdigest()
        # self.password = hashlib.md5(password.encode(
        #     'utf-8')).hexdigest()  # guarda la password hasheada

    
    # Métodos de clase

    # Obtener el usuario

    @classmethod
    def obtener_user(self, email, password):
        """Metodo que permite obtener un usuario a partir de un email
        y una contraseña ingresados

        Args:
            email ([string]): [email ingresado por el usuario y enviado por parametro]
            password ([string]): [contraseña ingresada por el usuario y enviada por parametro]

        Returns:
            [User]: [Usuario buscado en la base de datos coincidente con la búsqueda]
        """
        user = User.query.filter(
            (User.email == email), (User.password == password)
        ).first()
        return user

    # Ordenación de la lista de usuarios según criterio de orden establecido por el módulo de configuración

    @classmethod
    def order(cls):
        """Método que permite la ordenación de la lista de usuarios segun
        el criterio de orden establecido en el modulo de configuracion

        Returns:
            [list]: [Retorna una lista de usuarios segun los resultados
            de la busqueda realizada]
        """
        if order_converter(Configuration.query.one().order, 0, "desc") == 0:
            users = User.query.order_by(User.username.asc()).all()
        else:
            users = User.query.order_by(User.username.desc()).all()
        if not users:
            flash("En estos momentos no hay usuarios en el sistema")
        return users

    # Chequeo de permisos
    @classmethod
    def has_permission(cls, user_id, permission):
        """Metodo que realiza el chequeo de permisos

        Args:
            user_id ([integer]): [id del usuario]
            permission ([string]): [nombre del permiso del cual se desea
            saber si lo posee un usuario]

        Returns:
            [boolean]: [Retorna true en caso de que el usuario indicado
            por parametro tenga el permiso indicado por parametro, false caso contrario]
        """
        permission_query = (
            db.session.query(User, Role, Permission)
            .join(User.roles)
            .join(Role.permissions)
            .where(Permission.name == permission)
            .where(User.id == user_id)
            .first()
        )
        return permission_query is not None

    # Creación de usuario nuevo

    @classmethod
    def create(cls):
        new_user = User(**request.form)
        if User.validateForm():
            db.session.add(new_user)
            try:
                db.session.commit()
                return True
            except:
                flash("El usuario no se pudo crear. Vuelva a intentar.", category="danger")
        return False

    @classmethod
    def create(cls, email, name, lastname, username):
        new_user = User()
        new_user.email = email
        new_user.first_name = name
        new_user.last_name = lastname
        new_user.username = email

        db.session.add(new_user)
        try:
            db.session.commit()
            flash("El usuario fue creado correctamente", category="success")
            return True
        except:
            flash("El usuario no se pudo crear. Vuelva a intentar.", category="danger")
        return False

    @classmethod
    def createNew(cls, email, name, lastname, username):
        new_user = User()
        new_user.email = email
        new_user.first_name = name
        new_user.last_name = lastname
        new_user.username = email

        db.session.add(new_user)
        try:
            db.session.commit()
            flash("El usuario fue creado correctamente", category="success")
            return new_user
        except:
            flash("El usuario no se pudo crear. Vuelva a intentar.")
        return False

    # Edición de un usuario

    @classmethod
    def update(cls, usr, kwargs):
        """Metodo para actualizar los distintos campos de la informacion
        del usuario segun los parametros recibidos a traves del formulario

        Args:
            usr ([User]): [Usuario del cual se desea modificar los datos]
            kwargs ([array]): [Informacion del formulario recibida]

        Returns:
            [Usuario]: [Usuario el cual fue editado]
        """
        usr.first_name = kwargs["first_name"]
        usr.last_name = kwargs["last_name"]
        usr.username = kwargs["username"]
        usr.email = kwargs["email"]
        usr.password = kwargs["password"]
        return usr

    @classmethod
    def get(cls, users_email):
        user = User.query.filter(
            (User.email == users_email)).first()
        return user        
        # return ("id", "name", "email", "profile_pic")



class UserRoles(db.Model):
    """es la tabla intermedia entre usuarios y roles"""

    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    @classmethod
    def createNew(cls, usr, role):
        new_ur = UserRoles(usr, role)

        db.session.add(new_ur)
        try:
            db.session.commit()
            return new_ur
        except:
            print("Error en la asignación de roles")
        return False