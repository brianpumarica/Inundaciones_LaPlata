import flask
from app.db import db
from flask import redirect, render_template, request, url_for, flash
from app.helpers.decorators import has_permission, login_required
from app.models.configuration import Configuration
from app.models.locations import Location
from operator import and_
from app.helpers.filters import from_string_to_bool, parse_input

# Public resources

@has_permission("location_index")
@login_required
def index():
    """
    Renderizacion del index del modulo de puntos de encuentro. Lista todos
    los puntos de encuentro del sistema de forma paginada.

    Returns:
        HTML: Pantalla del index de puntos de encuentro
    """
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        locations = Location.query.order_by(Location.name.asc()).paginate(
            page, int(criterion.per_page), False
        )
    else:
        locations = Location.query.order_by(Location.name.desc()).paginate(
            page, int(criterion.per_page), False
        )
    if not locations:
        flash("En estos momentos no hay puntos de encuentro en el sistema", "danger")
    next_url = (
        url_for("location_index", page=locations.next_num)
        if locations.has_next
        else None
    )
    prev_url = (
        url_for("location_index", page=locations.prev_num)
        if locations.has_prev
        else None
    )
    return render_template(
        "location/index.html",
        locations=locations.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@login_required
def search():
    """
    Metodo que permite la búsqueda de puntos de encuentros: filtra por todos
        los puntos de encuentro, por los publicados o por los no publicados.

    Returns:
        HTML: retornan la lista de puntos de encuentro y los parametros recibidos
            para devolverlos a la nueva vista
    """
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if request.form["search_status"] == "3":
        locations, search_status, search_field = searchAll(
            page, int(criterion.per_page)
        )
    else:
        locations, search_status, search_field = searchByStatus(
            page, int(criterion.per_page)
        )
    if not locations.items:
        locations, search_status, search_field = emptyLocationList()
    next_url = (
        url_for("location_index", page=locations.next_num)
        if locations.has_next
        else None
    )
    prev_url = (
        url_for("location_index", page=locations.prev_num)
        if locations.has_prev
        else None
    )
    return render_template(
        "location/index.html",
        locations=locations.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field,
    )


def searchAll(page, elements):
    """
    Funcion que permite realizar busquedas entre todos los puntos de
        encuentro (tanto publicados como no publicados)

    Args:
        page (integer): pagina requerida
        elements (integer): elementos por pagina requeridos para la
            paginacion

    Returns:
        list: Retorna una lista con los puntos de encuentro filtrados y con los
            valores de los inputs enviados por el usuario a traves del form
    """
    search_field = request.form["search_field"]
    
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        locations = (
            Location.query.filter(Location.name.contains(search_field))
            .order_by(Location.name.asc())
            .paginate(page, elements, False)
        )
    else:
        locations = (
                Location.query.filter(Location.name.contains(search_field))
                .order_by(Location.name.desc())
                .paginate(page, elements, False)
        )

    if not locations:
        locations, search_status, search_field = emptyLocationList()
    else:
        search_status = request.form["search_status"]
    return locations, search_status, search_field


def searchByStatus(page, elements):
    """
    Funcion auxiliar que permite realizar busquedas entre los puntos de
        encuentro segun el estado (publicado o no publicado) indicado
        por el usuario

    Args:
        page (integer): pagina requerida
        elements (integer): elementos por pagina requeridos para la paginacion

    Returns:
        list: Retorna una lista con los puntos de encuentro filtrados y con los
            valores de los inputs enviados por el usuario a traves del form
    """
    search_status = request.form["search_status"]
    search_field = request.form["search_field"]
    
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        locations = (
                Location.query.filter(
                    and_(Location.status == search_status, Location.name.contains(search_field))
                )
                .order_by(Location.name.asc())
                .paginate(page, elements, False)
            )
    else:
        locations = (
            Location.query.filter(
                and_(Location.status == search_status, Location.name.contains(search_field))
            )
            .order_by(Location.name.desc())
            .paginate(page, elements, False)
        )
        
    if not locations:
        locations, search_status, search_field = emptyLocationList()
    return locations, search_status, search_field


# un mensaje de que no encontro p.d.e y devuelte todos los puntos de encuentro
def emptyLocationList():
    """
    Función auxiliar utilizada cuando una query retorna una lista vacia
    Informa al usuario a través de un flash message y retorna la lista
    completa de los puntos de encuentro.

    Returns:
        list: retorna una lista con una lista de todos los puntos de encuentro
            y dos elementos None que limpian los campos de busqueda
            en el index.
    """
    flash("No se encontraron puntos de encuentro con esos requerimientos", "danger")
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    locations = Location.query.order_by(Location.name.asc()).paginate(
        page, int(criterion.per_page), False
    )
    return locations, None, None


# Renderización de la vista view, con los detalles del punto de encuentro
@has_permission("location_show")
@login_required
def view(id):
    """Metodo que permite la visualización de puntos de encuentro:
        muestra el detalle de un punto de encuentro específico.

    Args:
        id (integer): punto de encuentro requerido para su visualización


    Returns:
        HTML: retorna la vista de un punto de de encuentro y su detalle
    """
    location = Location.query.filter_by(id=id).one()
    return render_template("location/view.html", location=location)


# Renderización del formulario de creación de punto de encuentro
@has_permission("location_new")
@login_required
def new():
    """
    Renderización del formulario de creación de punto de encuentro

    Returns:
        HTML: Pantalla de creacion de punto de encuentro nuevo
    """
    return render_template("location/new.html")

def validateName(form, id):
    """
    Función auxiliar. Función que realiza la validación del nombre de
    punto de encuentro del formulario (verifica que no este repetido)


    Args:
        form (request.form): formulario enviado por el usuario a traves de
            los respectivos inputs
        id (integer): id del punto de encuentro (para la edición)

    Returns:
        [boolean]: [Devuelve true si es un nombre de punto de encuentro
        valido y false caso contrario]
    """
    if id == None:
        if (
            db.session.query(Location.name).filter_by(
                name=form["name"]).first()
            is not None
        ):
            flash("El nombre de punto de encuentro ya existe", "danger")
            return False
        return True
    else:
        if (
            db.session.query(Location.name)
            .filter_by(name=form["name"])
            .filter(Location.id != id)
            .first()
            is not None
        ):
            flash("El nombre de punto de encuentro ya existe", "danger")
            return False
        return True


def validateNoEmpty(form):
    """
    Función auxiliar. Funcion que realiza la validación del
    formulario de creacion/edicion de punto de encuentro
    (verifica que no tenga campos vacios)

    Args:
        form (request.form): formulario enviado por el usuario a traves de
        los respectivos inputs

    Returns:
        boolean: Devuelve true si no hay ningun campo vacio del
        formulario y false caso contrario
    """
    noempty = True
    # for input in form:
    #     if not form[input]:
    #         flash(
    #             "El campo {} no puede estar vacío".format(
    #                 flask.escape(parse_input(input))
    #             ),
    #             "danger",
    #         )
    #         noempty = False
    return noempty


def validateForm(form, id=None):
    """
    Función auxiliar que valida un formulario, verificando que no contenga campos
    vacios y que el nombre sea valido (no duplicado)

    Args:
        form (request.form): formulario enviado por el usuario a traves de
            los respectivos inputs
        id (integer): id del punto de encuentro, para la edición

    Returns:
        boolean: Devuelve true si el formulario es valido, false caso contrario.
    """
    return (
        validateNoEmpty(form)
        and validateName(form, id)
    )

@has_permission("location_new")
@login_required
def creation(form):
    """
    Metodo que crea un punto de encuentro a partir de los datos ingresados
    por un formulario (guardando en base de datos). Se realiza la validacion
    del lado del servidor y se informa el resultado.

    Args:
        form (request.form): formulario enviado por el usuario a traves de
         los respectivos inputs

    Returns:
        boolean: Retorna true si el punto de encuentro pudo ser creado
        correctamente, false caso contrario
    """
    new_location = Location(**request.form)
    Location.set_attributes_default(new_location)
    if validateForm(form):
        db.session.add(new_location)
        try:
            db.session.commit()
            flash("El punto de encuentro fue creado correctamente", "success")
            return True
        except:
            flash("El punto de encuentro no se pudo crear. Vuelva a intentar.", "danger")
    return False

# Creación de punto de encuentro.
@has_permission("location_new")
@login_required
def create():
    """
    Metodo que permite la creacion de un punto de encuentro
    renderizando la pantalla de inicio en caso de haberse creado con
    exito o la pagina de creacion de punto de encuentro en caso de
    haber fallado el alta, mostrando las validaciones.

    Returns:
        HTML: Pantalla de inicio del modulo de puntos de encuentro si
        la creacion tuvo exito o pantalla de creacion de puntos de
        encuentro en caso contrario
    """
    if creation(request.form):
        return redirect(url_for("location_index"))
    else:
        return render_template(
            "location/new.html",
            name=request.form["name"],
            address=request.form["address"],
            telephone=request.form["telephone"],
            email=request.form["email"]
        )


@has_permission("location_destroy")
@login_required
def confirmDelete(id):
    """
    Metodo que renderiza la pantalla de confirmacion de eliminar punto
    de encuentro

    Args:
        id (integer): id del punto de encuentro

    Returns:
        HTML: Pantalla de confirmacion de eliminar punto de encuentro
    """
    location = Location.query.filter_by(id=id).one()
    return render_template("location/delete.html", location=location)


# Borrado de un punto de encuentro
@has_permission("location_destroy")
@login_required
def delete(id):
    """
    Metodo que permite y confirma la eliminacion de un punto de encuentro

    Args:
        id (integer): id del punto de encuentro

    Returns:
        HTML: Retorna la pantalla de inicio del modulo puntos de
        encuentro (index) informando al usuario el exito o el fallo de
        su accion
    """
    loc = Location.query.filter_by(id=id).one()
    db.session.delete(loc)
    try:
        db.session.commit()
        flash("Se elimino correctamente el punto de encuentro.", "success")
    except:
        flash("No se pudo eliminar el punto de encuentro.", "danger")
    return redirect(url_for("location_index"))


@has_permission("location_toggle")
@login_required
def toggle(id):
    """
    Funcion conmutador del estado del punto de encuentro. Si esta
    publicado pasa a despublicado y si esta despublicado pasa a
    publicado

    Args:
        id (integer): id del punto de encuentro

    Returns:
        HTML: Retorna nuevamente la pantalla de inicio del modulo de puntos de
        encuentro, informando al usuario sobre su accion
    """
    location = Location.query.filter_by(id=id).one()
    location.status = not location.status
    try:
        db.session.commit()
        flash("Se modifico el estado del punto de encuentro.", "success")
    except:
        flash("No se pudo editar el punto de encuentro.", "danger")
    return redirect(url_for("location_index"))

@has_permission("location_update")
@login_required
def edit(id):
    """
    Metodo que renderiza la pantalla de edicion de informacion de un punto
    de encuentro

    Args:
        id (integer): id del punto de encuentro

    Returns:
        HTML: Retorna la pantalla de edicion de la informacion del punto de
        encuentro especificado por parametro con su respectivo formulario
    """
    location = Location.query.filter_by(id=id).one()
    return render_template("location/edit.html", location=location)


@has_permission("location_update")
@login_required
def confirmEdited(id):
    """
    Metodo que permite enviar los cambios durante la edicion de la
    informacion de un punto de encuentro. Realiza las validaciones e informa
    al usuario sobre su accion

    Args:
        id (integer): id del punto de encuentro

    Returns:
        HTML: Pantalla de inicio del modulo de puntos de encuentro si la edicion
        tuvo exito o pantalla de edicion del punto de encuentro en caso contrario
    """
    loc = Location.update(id, request.form)

    if validateForm(request.form, id):
        db.session.add(loc)
        try:
            db.session.commit()
            flash("Se modifico correctamente, el punto de encuentro.", "success")
        except:
            flash("No se pudo editar el punto de encuentro. Vuelva a intentar", "danger")
    return redirect(url_for("location_index"))
