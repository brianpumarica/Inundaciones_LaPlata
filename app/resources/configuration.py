from flask.helpers import flash
from app.db import db
from flask import redirect, render_template, request, url_for
from app.helpers.decorators import has_permission, login_required
from app.models.configuration import Configuration

@has_permission("configuration_index")
@login_required
def index():
    try:
        actual_configuration = Configuration.query.first()
        return render_template("/configuration.html", config=actual_configuration)
    except:
        flash("Hubo un error en el modulo de configuración. Intente nuevamente.", "danger")
        return render_template("/home.html")

def validateForm(form): #Aca tambien se podria validar colores segun se requiera (por ejemplo, no elegir dos o tres colores iguales)
    if (form["pagination_input"]):
        return True
    return False

@has_permission("configuration_update")
@login_required
def update():
    try:
        new_configuration = Configuration.query.first()
    except:
        flash("Hubo un error en el modulo de configuración", "danger")
    new_configuration.per_page = request.form["pagination_input"]
    new_configuration.order = int(request.form["pagination_order"])
    color_public = []
    color_public.append(request.form["pub1"])
    color_public.append(request.form["pub2"])
    color_public.append(request.form["pub3"])
    new_configuration.color_public = ','.join(color_public)
    color_priv = []
    color_priv.append(request.form["priv1"])
    color_priv.append(request.form["priv2"])
    color_priv.append(request.form["priv3"])
    new_configuration.color_private = ','.join(color_priv)
    db.session.add(new_configuration)
    db.session.commit()
    # if validateForm(request.form):
    #     db.session.add(new_configuration)
    #     try:
    #         db.session.commit()
    #         flash("La configuración fue actualizada correctamente", "success")
    #         return True
    #     except:
    #         flash("La configuración no se pudo actualizar. Vuelva a intentar.", "danger")
    return redirect(url_for("configuration_index"))
