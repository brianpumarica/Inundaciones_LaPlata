from flask import session, abort
from sqlalchemy.sql.functions import user
from app.models.user import User

def login_required(view_function):
    """Si no esta logueado  muestra el error 401.
    Si esta logueado sigue con la ejecucion del programa
    """

    def decorator(*args, **kwargs):
        if not session.get("user"):
            return abort(401)
        return view_function(*args, **kwargs)

    return decorator


def has_permission(permiso):
    """Si no tiene el permiso muestra el error 403.
    Si lo tiene sigue con la ejecucion del programa
    """

    def wrapper(view_function):
        def decorator(*args, **kwargs):
            try:
                if not User.has_permission(session["user"]["id"], permiso):
                    return abort(401)
                return view_function(*args, **kwargs)
            except:
                return abort(401)

        return decorator

    return wrapper
