import json
from flask import redirect, request, url_for, session, flash
from flask import (
    redirect,
    url_for,
    request,
    session,
    session,
    flash,
    Blueprint,
)
from app.models.user import User, UserRoles
import hashlib
import requests
from os import environ
from oauthlib.oauth2 import WebApplicationClient
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
auth = Blueprint("auth", __name__)

# Oauth Configuration
GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Redirección a la página de login

def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://127.0.0.1:5000/login/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

# Autenticacion de usuario


def authenticate():
    if request.method == "POST":
        params = request.form

        user = User.query.filter(
            User.email == params["email"],
            User.password == hashlib.sha256(params["password"].encode("utf-8")).hexdigest(),
        ).first()
       
        if user is not None:  # Si matcheó en la base de datos guardo la info en sesión
            if user.active:
                usuario = {
                    "id": user.id,
                    "nombre": user.first_name,
                }
                session["user"] = usuario
                flash("Bienvenido. Has iniciado sesión", category="success")
                return redirect(url_for("home"))
            else:
                flash(
                    "El usuario esta bloquado y no podrá acceder a la página",
                    category="danger",
                )
                return redirect(url_for("auth_login"))
        else:
            flash("No se pudo iniciar sesión, verifique sus datos", category="error")
            return redirect(url_for("auth_login"))


# Logout de usuario


def logout():
    session.clear()
    flash("La sesión se cerró correctamente.", category="success")

    return redirect(url_for("home"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

client = WebApplicationClient(GOOGLE_CLIENT_ID)



# @app.route("/login/callback")
def callback():

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        users_familyame = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400
        
    # Create a user in your db with the information provided
    # by Google

    # user = User(
    #     first_name=users_name, last_name=users_familyame, username=unique_id, email=users_email
    # )
    # Doesn't exist? Add it to the database.
    current_user = User.get(users_email)
    is_new = False
    if not current_user:
        is_new = True
        User.createNew(users_email, users_name, users_familyame, users_email)
        current_user = User.get(users_email)
        # UserRoles.createNew(current_user.id, 2)
    if current_user.active:
            usuario = {
                "id": current_user.id,
                "nombre": users_name,
            }
            session["user"] = usuario
            if (not is_new):
                flash("Bienvenido. Has iniciado sesión", category="success")
            return redirect(url_for("home"))
    else:
        flash(
            "El usuario esta bloquado y no podrá acceder a la página",
            category="danger",
        )
        return redirect(url_for("auth_login"))
    # Begin user session by logging the user in
    # login_user(user)

    # Send user back to homepage
    return redirect(url_for("auth_bienvenido"))


def bienvenido():
    return redirect(url_for("home"))
