import csv
import io
from operator import and_
from flask import redirect, render_template, request, url_for, flash
import flask
from sqlalchemy.sql.functions import random
from app.helpers.filters import parse_input, list_converter
from app.models.configuration import Configuration
from app.models.inundable import Inundable
from app.db import db
from app.helpers.decorators import has_permission, login_required
from random import randint
import random


# Protected resources

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

@has_permission("floodable_index")
@login_required
def index():
    """
    Resumen:
        Control que permite renderizar el index de zonas inundables,
        listando todas las zonas inundables disponibles con sus principales
        datos.

    Arguments:
        Recibe un request con los parametros "page" con el numero de pagina
        solicitado (es opcional, por defecto es 1).

    Permissions:
        Usuario logueado
            ROL_ADMINISTRADOR
            ROL_OPERADOR

    Returns:
        HTML: Devuelve la renderización del index con la lista de zonas inundables
        junto con los elementos de la paginación.
    """
    hay_items = Inundable.query.all()
    if (not hay_items):
        return render_template(
            "inundable/index.html"
        )

    # Obtengo la configuración de paginado
    page, per_page, order = getConfig()

    # Obtengo las listas de zonas inundables segun el orden por defecto
    flooded = searchAll(page, per_page, order)

    # Configuro la paginación
    next_url = (
        url_for("inundable_index", page=flooded.next_num)
        if flooded.has_next
        else None
    )

    prev_url = (
        url_for("inundable_index", page=flooded.prev_num)
        if flooded.has_prev
        else None
    )

    # Retorno la vista con las variables
    return render_template(
        "inundable/index.html",
        flooded=flooded.items,
        next_url=next_url,
        prev_url=prev_url,
    )

def emptyFloodedList(page, per_page,order, search_field=None):
    """
    Función auxiliar utilizada cuando una query retorna una lista vacia
    Informa al usuario a través de un flash message y retorna la lista
    completa de las zonas inundables.

    Returns:
        list: retorna una lista con una lista de todos las zonas inundables
            y dos elementos None que limpian los campos de busqueda en el index.
    """
    if (search_field):
        # Obtengo las listas de zonas inundables segun el orden por defecto
        if order == 0:
            flooded = searchAllAsc(page, per_page)
        else:
            flooded = searchAllDesc(page, per_page)
        return flooded
    else:
        return None

def searchAllAsc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todos las zonas inundables
        paginando de manera ascendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todas las zonas inundables filtradas de manera ascendente
    """
    if (search_field):
        return (
            Inundable.query.filter(Inundable.name.contains(search_field))
            .order_by(Inundable.name.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Inundable.query.order_by(Inundable.name.asc()).paginate(page, per_page, False)
        )
def searchAllDesc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todas las zonas inundables
        paginando de manera descendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todas las zonas inundables filtrados de manera descendente
    """
    if (search_field):
        return (
            Inundable.query.filter(Inundable.name.contains(search_field))
            .order_by(Inundable.name.desc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Inundable.query.order_by(Inundable.name.desc()).paginate(page, per_page, False)
        )

def searchAll(page, per_page, order, search_field=None):
    """
    Funcion que permite realizar busquedas entre todos las zonas inundables
    (tanto publicadas como no publicadas)

    Args:
        page (integer): pagina requerida
        elements (integer): elementos por pagina requeridos para la
            paginacion

    Returns:
        list: Retorna una lista con las zonas inundables filtradas y con los
            valores de los inputs enviados por el usuario a traves del form
    """
    # Búsqueda por orden ascendente (publicadas y despublicadas)

    if order == 0:
        flooded = searchAllAsc(page, per_page, search_field)
    
    # Búsqueda por orden descendente (publicadas y despublicadas)
    else:
        flooded = searchAllDesc(page, per_page, search_field)
    if not flooded.items:
        flash("No existen zonas inundables para su búsqueda", "danger")
        flooded = emptyFloodedList(page, per_page, order, search_field)
    return flooded

def searchByStatusAsc(page, per_page, search_status, search_field):
    
    if (search_field):
        return (
            Inundable.query.filter(and_(Inundable.status == search_status, Inundable.name.contains(search_field)))
            .order_by(Inundable.name.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            Inundable.query.filter(Inundable.status == search_status)
            .order_by(Inundable.name.asc())
            .paginate(page, per_page, False)
        )

def searchByStatusDesc(page, elements, search_status, search_field):
    return (
        Inundable.query.filter(
            and_(Inundable.status == search_status,
                 Inundable.name.contains(search_field))
        )
        .order_by(Inundable.name.desc())
        .paginate(page, elements, False)
    )

def searchByStatus(page, per_page, order, search_field, search_status):
    """
        Funcion auxiliar que permite realizar busquedas entre las zonas
            inundables segun el estado (publicado o no publicado)
            indicado por el usuario

        Args:
            page (integer): pagina requerida
            elements (integer): elementos por pagina requeridos para la paginacion

        Returns:
            list: Retorna una lista con las zonas inundables filtradas y con los
            valores de los inputs enviados por el usuario a traves del form
    """
    if order == 0:
        flooded = searchByStatusAsc(page, per_page, search_status, search_field)
    else:
        flooded = searchByStatusDesc(page, per_page, search_status, search_field)
    if not flooded.items:
        flash("No existen zonas inundables para su búsqueda", "danger")
        flooded = emptyFloodedList(page, per_page, order, search_field)
    return flooded


@login_required
def search():
    """
    Resumen:
        Control que permite realizar la búsqueda de zonas inundables,
        permitiendo filtrar por nombre y por el estado (todas/activo/inactivo)

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
        HTML: Devuelve la renderización del index con la lista de zonas inundables
        filtradas junto con los elementos de la paginación.
        Si no recibe parámetro "searchFilter" devuelve todos los nombres de zonas
        inundables que coincidan con el filtro "searchType" aplicado.
        Si no existieran coincidencias para los filtros aplicados, se informa al usuario
        y se retorna la totalidad de las zonas inundables sin filtrar.
    """
    # Obtengo la configuración de paginado
    page, per_page, order = getConfig()

    # Tomo los parámetros del request
    search_field = request.args.get("search_field")
    search_status = request.args.get("search_status")

    # Filtro entre todas las zonas inundables (activas e inactivas)
    if search_status == "3":
        flooded = searchAll(page, per_page, order, search_field)

    # Filtro entre las zonas inundables activas o inactivas según lo indique el parámetro "searchType"
    else:
        flooded = searchByStatus(page, per_page, order, search_field, search_status)
    
    if not flooded.items:
        flooded = emptyFloodedList(page, per_page, order, search_field)
    next_url = url_for(
        "inundable_index", page=flooded.next_num, search_status=search_status, search_field=search_field) if flooded.has_next else None
    prev_url = url_for(
        "inundable_index", page=flooded.prev_num, search_status=search_status, search_field=search_field) if flooded.has_prev else None
    return render_template(
        "inundable/index.html",
        flooded=flooded.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field,
    )


@has_permission("floodable_import")
@login_required
def new():
    """
    Summary:
        Control que permite la carga de un CSV con zonas inundables.

    Permission:
        Operadores y Administradores

    Returns:
        Index de inundables: Listado con todas las zonas inundables
        cargadas en el sistema, paginado segun parametros del modulo de configuracion
    """

    try:
        # Tomo el archivo recibido por parámetro
        f = request.files["fileCSV"]

        # Valido que sea un archivo
        if not f:
            flash("No se subio ningun archivo", "danger")

        # Parseo el csv y lo guardo en base
        else:
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            next(csv_input)
            for row in csv_input:
                
                try:
                    # Obtengo las coordenadas
                    coord = row[1]

                    # Obtengo el nombre de la zona indundable
                    getName = row[0]
                except:
                    flash("El archivo cargado es inválido", "danger")
                    return index()

                # Genero un codigo aleatorio de 6 cifras
                code = randint(000000, 999999)

                # Genero un codigo de color hex aleatorio
                color = "%06x" % random.randint(0, 0xFFFFFF)

                zona = Inundable(code, getName, coord, 1, str("#" + color))

                aux = Inundable.query.filter_by(name=getName).first()
                if (aux):
                    aux.coordinates = coord
                    db.session.add(aux)
                else:
                    db.session.add(zona)
            try:
                db.session.commit()
                flash("El archivo fue importado correctamente", "success")
            except:
                db.session.rollback()
                flash(
                    "El archivo no se pudo importar. Vuelva a intentar.", "danger")
    except:
        flash("El archivo cargado es inválido", "danger")
    return index()


# @ login_required
# def edit(id):
#     """
#     Summary:
#         Control que permite editar una zona inundable.

#     Permission:
#         Operadores y Administradores

#     Returns:
#     """
#     inundable = Inundable.query.filter_by(id=id).one()
#     return render_template("inundable/edit.html", inundable=inundable)


# Auxiliar resources

# Validación del formulario de creacion/edicion de usuario (que no tenga campos vacios)


def validateNoEmpty(kwargs):
    noempty = True
    for input in kwargs:
        if not kwargs[input]:
            flash(
                "El campo {} no puede estar vacío".format(
                    flask.escape(parse_input(input))
                ),
                "danger",
            )
            noempty = False
    return noempty


# Validación del codigo de la zona inundable del formulario (que no este repetido)


def validateCode(kwargs):
    if (
        db.session.query(Inundable.code)
        .filter_by(code=kwargs["code"])
        .filter(Inundable.id != id)
        .first()
        is not None
    ):
        flash("El codigo ya existe", "danger")
        return False
    return True



# @ login_required
# def edit_confirmed(id):
#     inundable = Inundable.query.filter_by(id=id).one()
#     inundable = Inundable.update(inundable, request.form)
#     if validateNoEmpty(request.form) and validateCode(request.form):
#         db.session.add(inundable)
#         try:
#             db.session.commit()
#             flash("La zona inundable fue actualizada correctamente", "success")
#             return redirect(url_for("inundable_index"))
#         except:
#             flash(
#                 "La zona inundable no se pudo actualizar. Vuelva a intentar.", "danger"
#             )
#     return redirect(url_for("inundable_edit", id=id))


# Renderización de la pantalla de confirmación de eliminar zona inundable


@ has_permission("floodable_destroy")
@ login_required
def confirm_delete(id):
    inundable = Inundable.query.filter_by(id=id).one()
    lista_ = list_converter(inundable.coordinates)
    return render_template("inundable/delete.html", inundable=inundable, lista=lista_)


# Borrado de una zona inundable


@ has_permission("floodable_destroy ")
@ login_required
def delete(id):
    inundable = Inundable.query.filter_by(id=id).one()
    db.session.delete(inundable)
    try:
        db.session.commit()
        flash("Se eliminó la zona inundable", "success")
    except:
        flash("Error al eliminar la zona inundable", "danger")
    return redirect(url_for("inundable_index"))


@ has_permission("floodable_show")
@ login_required
def view(id):
    inundable = Inundable.query.filter_by(id=id).one()
    lista_ = list_converter(inundable.coordinates)
    return render_template("inundable/view.html", inundable=inundable, lista=lista_)


@ has_permission("floodable_toggle")
@ login_required
def toggle(id):
    inundable = Inundable.query.filter_by(id=id).one()
    inundable.status = not inundable.status
    try:
        db.session.commit()
        flash("Se cambió el estado de la zona inundable", "success")
    except:
        flash("Error al cambiar el estado de la zona inundable", "danger")
    return redirect(url_for("inundable_index"))
