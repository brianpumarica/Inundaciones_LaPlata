from os import path, environ, urandom
from flask import Flask, render_template, Blueprint
from app.models.user import User
from flask_session import Session
from config import config
from app import db
from flask_cors import CORS
from app.resources import (
    configuration,
    user,
    auth,
    location,
    complaint,
    inundable,
    route,
)
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import filters
import logging
from app.resources.api.inundables import inundable_api
from app.resources.api.complaints import complaint_api
from app.resources.api.locations import location_api
from app.resources.api.routes import route_api
from app.resources.api.configuration import configuration_api

#Oauth
from oauthlib.oauth2 import WebApplicationClient
from flask_login import (LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    )

# Oauth Configuration
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

UPLOAD_FOLDER = "/static/uploaded"

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    CORS(app)
    #CORS(app, resources={r"/api/": {"origins": ''}}, support_credentials=True)
    
    #Oauth
    app.secret_key = environ.get("SECRET_KEY") or urandom(24)
    
    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


    ###fin oauth#### 


    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Server Side session
    app.secret_key = "llavesecreta"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2 - FILTROS
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(same_id=helper_auth.sameid)
    app.jinja_env.globals.update(has_permission=helper_auth.haspermission)
    app.jinja_env.globals.update(is_admin=helper_auth.isadmin)
    app.jinja_env.globals.update(sin_rol=helper_auth.sinrol)
    app.jinja_env.globals.update(is_operador=helper_auth.isoperador)
    app.jinja_env.globals.update(get_username=helper_auth.getusername)
    app.jinja_env.filters["boolean_converter"] = filters.boolean_converter
    app.jinja_env.filters["int_converter"] = filters.int_converter
    app.jinja_env.filters["none_converter"] = filters.none_converter
    app.jinja_env.filters["list_converter"] = filters.list_converter
    app.jinja_env.filters["list_counter"] = filters.list_counter
    app.jinja_env.globals.update(is_none=helper_auth.isnone)
    

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )
    app.add_url_rule(
        "/login/callback", "auth_callback", auth.callback, methods=["GET"]
    )

    app.add_url_rule(
        "/login/bienvenido", "auth_bienvenido", auth.bienvenido, methods=["GET"]
    )

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios/search", "user_search", user.search, methods=["GET"])
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule(
        "/usuarios/confirm_delete/<id>", "user_confirm_delete", user.confirm_delete
    )
    app.add_url_rule("/usuarios/delete/<id>", "user_delete", user.delete)
    app.add_url_rule("/usuarios/toggle/<id>", "user_toggle", user.toggle)
    app.add_url_rule("/usuarios/edit/<id>", "user_edit", user.edit)
    app.add_url_rule(
        "/usuarios/edit_confirmed/<id>",
        "user_edit_confirmed",
        user.edit_confirmed,
        methods=["POST"],
    )
    app.add_url_rule(
        "/usuarios/profile/<id>", "user_show", user.show
    )

    ########## RUTAS DE DENUNCIAS #####################
    # index
    app.add_url_rule("/complaint", "complaint_index", complaint.index)
    # view
    app.add_url_rule("/complaint/view/<id>", "complaint_view", complaint.view)
    # new
    app.add_url_rule("/complaint/nuevo", "complaint_new", complaint.new)
    app.add_url_rule("/complaint", "complaint_create",
                     complaint.create, methods=["POST"])
    # delete
    app.add_url_rule("/complaint/<id>", "complaint_delete", complaint.delete)
    app.add_url_rule(
        "/complaint/confirm_delete/<id>",
        "complaint_confirmDelete",
        complaint.confirmDelete,
    )
    # edit
    app.add_url_rule("/complaint/edit/<id>", "complaint_edit", complaint.edit)
    app.add_url_rule(
        "/complaint/confirmEdited/<id>",
        "complaint_confirmEdited",
        complaint.confirmEdited,
        methods=["POST"],
    )
    # search
    app.add_url_rule(
        "/complaint/search", "complaint_search", complaint.search, methods=["POST"]
    )
    #toggle
    app.add_url_rule("/complaint/toggle/<id>", "complaint_toggle", complaint.toggle)

    #follow
    app.add_url_rule("/complaint/index_follow/<id>", "complaint_index_follow", complaint.index_follow)
    app.add_url_rule("/complaint/complaint_new_follow/<id>", "complaint_new_follow", complaint.new_follow)
    app.add_url_rule("/complaint/create_follow", "create_follow",
                     complaint.create_follow, methods=["POST"])


    # Rutas de Zonas inundables
    app.add_url_rule("/inundable/view/<id>", "inundable_view", inundable.view)
    app.add_url_rule("/inundable", "inundable_index", inundable.index)
    app.add_url_rule(
        "/inundable/search", "inundable_search", inundable.search, methods=["GET"]
    )
    app.add_url_rule(
        "/inundable/nuevo", "inundable_new", inundable.new, methods=["GET", "POST"]
    )
    # app.add_url_rule("/inundable/edit/<id>", "inundable_edit", inundable.edit)
    app.add_url_rule(
        "/inundable/confirm_delete/<id>",
        "inundable_confirm_delete",
        inundable.confirm_delete,
    )
    app.add_url_rule("/inundable/delete/<id>",
                     "inundable_delete", inundable.delete)
    # app.add_url_rule(
    #     "/inundable/inundable_confirmed/<id>",
    #     "inundable_edit_confirmed",
    #     inundable.edit_confirmed,
    #     methods=["POST"],
    # )
    app.add_url_rule("/inundable/toggle/<id>", "inundable_toggle", inundable.toggle)


    ########## RUTAS DE PUNTO DE ENCUENTRO #####################
    # index
    app.add_url_rule("/location", "location_index", location.index)
    # view
    app.add_url_rule("/location/view/<id>", "location_view", location.view)
    # new
    app.add_url_rule("/location/nuevo", "location_new", location.new)
    app.add_url_rule("/location", "location_create", location.create, methods=["POST"])
    # delete
    app.add_url_rule(
        "/location/confirm_delete/<id>",
        "location_confirmDelete",
        location.confirmDelete,
    )
    app.add_url_rule("/location/<id>", "location_delete", location.delete)
    # toggle
    app.add_url_rule("/location/toggle/<id>",
                     "location_toggle", location.toggle)
    # edit
    app.add_url_rule("/location/edit/<id>", "location_edit", location.edit)
    app.add_url_rule(
        "/location/confirmEdited/<id>",
        "location_confirmEdited",
        location.confirmEdited,
        methods=["POST"],
    )
    # search
    app.add_url_rule(
        "/location/search", "location_search", location.search, methods=["POST"]
    )

    ########## RUTAS DE EVACUACIÓN #####################

    app.add_url_rule("/route", "route_index", route.index)
    app.add_url_rule("/route/view/<id>", "route_view", route.view)
    app.add_url_rule("/route/nuevo", "route_new", route.new)
    app.add_url_rule(
        "/route", "route_create", route.create, methods=["POST"]
    )
    # delete
    app.add_url_rule(
        "/route/confirmDelete/<id>",
        "route_confirmDelete",
        route.confirmDelete,
    )
    app.add_url_rule("/route/<id>", "route_delete", route.delete)
    app.add_url_rule("/route/toggle/<id>",
                     "route_toggle", route.toggle)
    app.add_url_rule("/route/edit/<id>", "route_edit", route.edit)
    app.add_url_rule(
        "/route/confirmEdited/<id>",
        "route_confirmEdited",
        route.confirmEdited,
        methods=["POST"],
    )
    # search
    app.add_url_rule(
        "/route/search", "route_search", route.search, methods=["POST"]
    )

    # Rutas de Configuración
    app.add_url_rule("/configuration", "configuration_index", configuration.index)
    app.add_url_rule("/configuration", "configuration_update", configuration.update, methods=["POST"])

    # Ruta para el Home (usando decorator)

    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(inundable_api)
    api.register_blueprint(complaint_api)
    api.register_blueprint(route_api)
    api.register_blueprint(location_api)
    api.register_blueprint(configuration_api)
    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(500, handler.internal_error)

    # Retornar la instancia de app configurada
    return app
