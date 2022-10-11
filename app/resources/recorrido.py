from sqlalchemy.sql.elements import and_
from app.db import db
from flask import redirect, render_template, request, url_for, flash, session
from app.models.routes import Route
from app.helpers.decorators import has_permission, login_required
from app.models.configuration import config
from app.models.user import User
from app.helpers.auth import authenticated
from datetime import datetime
from operator import and_



from app.models.configuration import Configuration
from app.resources.inundable import emptyFloodedList

#region Auxiliary functions
def getConfig():
    """
    Funcion auxiliar que permite obtener las configuraciones de paginación

    Returns:
        page: número de página requerido por el usuario. Si no se indicó
            ninguno, por defecto es la número 1.
        per_page: cantidad de elementos por página según la configuración
            por defecto del módulo de configuración del sistema.
    """
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    per_page = int(criterion.per_page)
    order = criterion.order
    return page, per_page, order
#endregion

#region Search functions
def searchAll(page, per_page, order, search_field=None):
    """
    Funcion que permite realizar busquedas entre todos los
        puntos de encuentro (tanto publicados como no publicados)

    Args:
        page (integer): pagina requerida
        elements (integer): elementos por pagina requeridos para la
            paginacion

    Returns:
        list: Retorna una lista con los puntos de encuentro filtrados
            y con los valores de los inputs enviados por el usuario
                a traves del form
    """
    # Búsqueda por orden ascendente (publicados y despublicados)

    if order == 0:
        routes = searchAllAsc(page, per_page, search_field)
    
    # Búsqueda por orden descendente (publicadas y despublicadas)
    else:
        routes = searchAllDesc(page, per_page, search_field)
    if not routes:
        flash("No existen recorridos de evacuación para su búsqueda", "danger")
        routes = emptyRouteList(page, per_page, order, search_field)
    return routes

def searchAllAsc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todos los recorridos de evacuación
        paginando de manera ascendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todos los recorridos de evacuación filtrados de manera
            ascendente
    """
    if (search_field):
        return (
            Route.query.filter(Route.name.contains(search_field))
            .order_by(Route.name.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Route.query.order_by(Route.name.asc()).paginate(page, per_page, False)
        )
def searchAllDesc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todos los recorridos de evacuación
        paginando de manera descendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todos los recorridos de evacuación filtrados de manera
            descendente
    """
    if (search_field):
        return (
            Route.query.filter(Route.name.contains(search_field))
            .order_by(Route.name.desc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Route.query.order_by(Route.name.desc()).paginate(page, per_page, False)
        )

def emptyRouteList(page, per_page,order, search_field=None):
    """
    Función auxiliar utilizada cuando una query retorna una lista vacia
    Informa al usuario a través de un flash message y retorna la lista
    completa de los recorridos de evacuación.

    Returns:
        list: retorna una lista con una lista de todos los recorridos de
            evacuación y dos elementos None que limpian los campos de
                busqueda en el index.
    """
    if (search_field):
        # Obtengo los recorridos de evacuación segun el orden por defecto
        if order == 0:
            routes = searchAllAsc(page, per_page)
        else:
            routes = searchAllDesc(page, per_page)
        return routes
    else:
        return None

#endregion

#region Index
@has_permission("routes_index")
@login_required
def index():
    """
    Renderizacion del index del modulo de recorridos de evacuación.
        Lista todos los recorridos de evacuación del sistema de
            forma paginada.

    Returns:
        HTML: Pantalla del index de recorridos de evacuación
    """
    
    # Obtengo la configuración de paginado
    page, per_page, order = getConfig()

    # Obtengo las listas de recorridos de evacuación segun el orden por defecto
    routes = searchAll(page, per_page, order)

    # Configuro la paginación
    next_url = (
        url_for("recorrido_index", page=routes.next_num)
        if routes.has_next
        else None
    )
    prev_url = (
        url_for("recorrido_index", page=routes.prev_num)
        if routes.has_prev
        else None
    )

    # Retorno la vista con las variables
    return render_template(
        "recorrido/index.html",
        recorridos=routes.items,
        next_url=next_url,
        prev_url=prev_url,
    )
#endregion

@has_permission("routes_show")
@login_required
def view(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("recorrido/view.html", recorrido=recorrido)


@has_permission("routes_new")
@login_required
def new():
    return render_template("recorrido/new.html")


@has_permission("routes_new")
@login_required
def create():
    new_recorrido = Route(**request.form)
    # Route.statusClassFromStringToBool(new_recorrido)
    #new_recorrido.coordinates = request.form["latitud"] + \
     #   ","+request.form["longitud"]
    new_recorrido.coordinates = request.form["coordinates"]
    db.session.add(new_recorrido)
    try:
        db.session.commit()
        flash("Se ha creado un recorrido de evacuación nuevo", "info")
    except:
        flash("No se pude crear el recorrido de evacuación", "info")
    return redirect(url_for("recorrido_index"))



@has_permission("routes_destroy")
@login_required
def confirmDelete(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("recorrido/delete.html", recorrido=recorrido)



@has_permission("routes_destroy")
@login_required
def delete(id):
    rec = Route.query.filter_by(id=id).one()
    db.session.delete(rec)
    try:
        db.session.commit()
        flash("Se ha eliminado el recorrido de evacuación", "info")
    except:
        flash("No se ha podido eliminar el recorrido de evacuación", "info")
    return redirect(url_for("recorrido_index"))



@has_permission("routes_toggle")
@login_required
def toggle(id):
    recorrido = Route.query.filter_by(id=id).one()
    recorrido.status = not recorrido.status
    try:
        db.session.commit()
        flash("Se ha actualizado el estado del recorrido de evacuación.", "info")
    except:
        flash("No se ha podido actualizar el estado del recorrido de evacuación", "info")
    return redirect(url_for("recorrido_index"))



@has_permission("routes_update")
@login_required
def edit(id):
    recorrido = Route.query.filter_by(id=id).one()
    return render_template("recorrido/edit.html", recorrido=recorrido)




@has_permission("routes_update")
@login_required
def confirmEdited(id):
    Route.update(id, request.form)
    try:
        db.session.commit()
        flash("Se a modificado correctamente el recorrido de evacuación", "info")
    except:
        flash("No se ha podido modificar el recorrido de evacuación", "info")
    return redirect(url_for("recorrido_index"))

#region Search

@login_required
def search():
    """
    Resumen:
        Control que permite realizar la búsqueda de recorridos de evacuación,
        permitiendo filtrar por nombre y por el estado (todos/activo/inactivo)

    Arguments:
        Recibe un request con los parametros. El parámetro opcional "searchType"
        tiene el tipo de filtro de búsqueda (filtrar entre todas las zonas,
        las activas o las inactivas). Por defecto es 3, equivalente a todas las zonas.
        El parámetro opcional "searchFilter" contiene el substring usado para buscar
        y filtrar a través del nombre.


    Permissions:
        Usuario logueado
            ROL_ADMINISTRADOR
            ROL_OPERADOR

    Returns:
        HTML: Devuelve la renderización del index con la lista de recorridos de
            evacuación filtrados junto con los elementos de la paginación.
            Si no recibe parámetro "searchFilter" devuelve todos los nombres de
            recorridos de evacuación que coincidan con el filtro "searchType"
            aplicado. Si no existieran coincidencias para los filtros aplicados,
            se informa al usuario y se retorna la totalidad de los recorridos
            de evacuación sin filtrar.
    """
    # Obtengo la configuración de paginado
    page, per_page, order = getConfig()

    # Tomo los parámetros del request
    search_field = request.form["search_field"]
    search_status = request.form["search_status"]

    # Filtro entre todos los recorridos de evacuación (activos e inactivos)
    if search_status == "3":
        routes = searchAll(page, per_page, order, search_field)

    # Filtro entre los recorridos de evacuación activos o inactivos
    #   según lo indique el parámetro "searchType"
    else:
        routes = searchByStatus(page, per_page, order, search_field, search_status)

    if not routes.items:
        flash("No existen recorridos de evacuación para su búsqueda", "danger")
        routes = emptyRouteList(page, per_page, order, search_field)
    next_url = url_for(
        "recorrido_index", page=routes.next_num, search_status=search_status, search_field=search_field) if routes.has_next else None
    prev_url = url_for(
        "recorrido_index", page=routes.prev_num, search_status=search_status, search_field=search_field) if routes.has_prev else None
    return render_template(
        "recorrido/index.html",
        recorridos=routes.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field,
    )


#endregion


def searchByStatus(page, per_page, order, search_field, search_status):
    """
        Funcion auxiliar que permite realizar busquedas entre los
            recorridos de evacuación segun el estado (publicado o no
            publicado) indicado por el usuario

        Args:
            page (integer): pagina requerida
            elements (integer): elementos por pagina requeridos para la paginacion

        Returns:
            list: Retorna una lista con los recorridos de evacuación
                filtrados y con los valores de los inputs enviados por el usuario a
                traves del form
    """
    if order == 0:
        routes = searchByStatusAsc(page, per_page, search_status, search_field)
    else:
        routes = searchByStatusDesc(page, per_page, search_status, search_field)
    if not routes:
        routes = emptyFloodedList(page, per_page, order, search_field)
    return routes


def searchByStatusAsc(page, per_page, search_status, search_field):
    
    if (search_field):
        return (
            Route.query.filter(and_(Route.status == search_status, Route.name.contains(search_field)))
            .order_by(Route.name.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Route.query.filter(Route.status == search_status)
            .order_by(Route.name.asc())
            .paginate(page, per_page, False)
        )

def searchByStatusDesc(page, elements, search_status, search_field):
    return (
        Route.query.filter(
            and_(Route.status == search_status,
                 Route.name.contains(search_field))
        )
        .order_by(Route.name.desc())
        .paginate(page, elements, False)
    )
