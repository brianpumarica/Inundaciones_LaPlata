from app.db import db
from flask import redirect, render_template, request, url_for, flash
from app.models.routes import Route
from app.helpers.decorators import has_permission, login_required
from app.models.configuration import Configuration
from operator import and_





@has_permission("route_index")
@login_required
def index():
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        recorridos = Route.query.order_by(Route.name.asc()).paginate(
            page, int(criterion.per_page), False
        )
    else:
        recorridos = Route.query.order_by(Route.name.desc()).paginate(
            page, int(criterion.per_page), False
        )
    if (not recorridos):
        flash("En estos momentos no hay recorridos de evación disponibles", "danger")
    next_url = (
        url_for("route_index", page=recorridos.next_num) 
        if recorridos.has_next 
        else None
    )
    prev_url = (
        url_for("route_index", page=recorridos.prev_num) 
        if recorridos.has_prev 
        else None
    )
    return render_template(
        "route/index.html",
        routes=recorridos.items, 
        next_url=next_url, 
        prev_url=prev_url,)


# busqueda de puntos de encuentro
@has_permission("route_index")
@login_required
def search():
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if request.form["search_status"] == "any_status":
        routes, search_status, search_field = searchAll(
            page, int(criterion.per_page)
        )
    else:
        routes, search_status, search_field = searchByStatus(
            page, int(criterion.per_page)
        )
    if not routes.items:
        routes, search_status, search_field = emptyRouteList()
    next_url = (
        url_for("route_index", page=routes.next_num)
        if routes.has_next
        else None
    )
    prev_url = (
        url_for("route_index", page=routes.prev_num)
        if routes.has_prev
        else None
    )
    return render_template(
        "route/index.html",
        routes=routes.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field,
    )


# Busca entre todos los puntos de encuentro (tanto publicacidos como no pubicados)
def searchAll(page, elements):
    search_field = request.form["search_field"]

    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        routes = (
            Route.query.filter(Route.name.contains(search_field))
            .order_by(Route.name.asc())
            .paginate(page, elements, False)
        )
    else:
        routes = (
                Route.query.filter(Route.name.contains(search_field))
                .order_by(Route.name.desc())
                .paginate(page, elements, False)
            )

    if not routes:
        routes, search_status, search_field = emptyRouteList()
    else:
        search_status = request.form["search_status"]
    return routes, search_status, search_field


# Busca entre p.d.e publicacidos y no pubicados segun corresponda
def searchByStatus(page, elements):
    search_status = request.form["search_status"]
    search_field = request.form["search_field"]

    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        routes = (
            Route.query.filter(
                and_(Route.status == search_status, Route.name.contains(search_field))
            )
            .order_by(Route.name.asc())
            .paginate(page, elements, False)
        )
    else:
        routes = (
            Route.query.filter(
                and_(Route.status == search_status, Route.name.contains(search_field))
            )
            .order_by(Route.name.desc())
            .paginate(page, elements, False)
        )

    
    if not routes:
        routes, search_status, search_field = emptyRouteList()
    return routes, search_status, search_field


# un mensaje de que no encontro p.d.e y devuelte todos los puntos de encuentro
def emptyRouteList():
    flash("No se encontraron puntos de encuentro con esos requerimientos", "danger")
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    routes = Route.query.order_by(Route.name.asc()).paginate(
        page, int(criterion.per_page), False
    )
    return routes, None, None


@has_permission("route_show")
@login_required
def view(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("route/view.html", route=recorrido)


@has_permission("route_new")
@login_required
def new():
    return render_template("route/new.html")


@has_permission("route_new")
@login_required
def create():
    new_recorrido = Route(**request.form)
    Route.set_attributes_default(new_recorrido)
    db.session.add(new_recorrido)
    try:
        db.session.commit()
        flash("Se ha creado un recorrido de evacuación nuevo", "success")
    except:
        flash("No se pude crear el recorrido de evacuación", "danger")
    return redirect(url_for("route_index"))



@has_permission("route_destroy")
@login_required
def confirmDelete(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("route/delete.html", route=recorrido)



@has_permission("route_destroy")
@login_required
def delete(id):
    rec = Route.query.filter_by(id=id).one()
    db.session.delete(rec)
    try:
        db.session.commit()
        flash("Se ha eliminado el recorrido de evacuación", "success")
    except:
        flash("No se ha podido eliminar el recorrido de evacuación", "danger")
    return redirect(url_for("route_index"))



@has_permission("route_toggle")
@login_required
def toggle(id):
    recorrido = Route.query.filter_by(id=id).one()
    recorrido.status = not recorrido.status
    try:
        db.session.commit()
        flash("Se ha actualizado el estado del recorrido de evacuación.", "success")
    except:
        flash("No se ha podido actualizar el estado del recorrido de evacuación", "danger")
    return redirect(url_for("route_index"))



@has_permission("route_update")
@login_required
def edit(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("route/edit.html", route=recorrido)




@has_permission("route_update")
@login_required
def confirmEdited(id):
    Route.update(id, request.form)
    try:
        db.session.commit()
        flash("Se a modificado correctamente el recorrido de evacuación", "success")
    except:
        flash("No se ha podido modificar el recorrido de evacuación", "danger")
    return redirect(url_for("route_index"))