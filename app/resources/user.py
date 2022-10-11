from operator import and_
from flask import redirect, render_template, request, url_for
import flask
from flask.helpers import flash
from app.db import db
from app.models.configuration import Configuration
from app.models.role import Role
from app.models.user import User, UserRoles
from app.helpers.decorators import has_permission, login_required
from app.helpers.filters import parse_input


#### Protected resources #####

#region Index

@has_permission("user_index")
@login_required
def index():
    
    """
        Renderizacion del index del modulo de usuarios. Lista todos los
            usuarios del sistema de forma paginada.

        Returns:
            HTML: Pantalla del index de usuarios
    """

    # Obtengo la configuración de paginado
    page, per_page, order = getConfig()

    # Obtengo las listas de usuarios segun el orden por defecto
    users = searchAll(page, per_page, order)

    # Configuro la paginación
    next_url = url_for(
        "user_index", page=users.next_num) if users.has_next else None
    prev_url = url_for(
        "user_index", page=users.prev_num) if users.has_prev else None

    # Retorno la lista y la paginación
    return render_template(
        "user/index.html", users=users.items, next_url=next_url, prev_url=prev_url
    )

#endregion

#region Search
@has_permission("user_index")
@login_required
def search():
    """
        Metodo que permite la búsqueda de usuario/s:
            filtra por todos los usuarios, por los activos o por los bloqueados.

        Returns:
            HTML: retornan la lista de usuarios y los parametros recibidos para
            devolverlos a la nueva vista
    """

    # Obtengo la configuración de paginación
    page, per_page, order = getConfig()

    # Tomo los parámetros de búsqueda
    search_status = request.args.get("search_status")
    search_field = request.args.get("search_field")

    # Filtrar por todos los usuarios
    if search_status == "3":
        users = searchAll(page, per_page, order, search_field)

    # Filtrar por usuarios activos o inactivos según lo indicado
    else:
        users = searchByStatus(page, per_page, order, search_field, search_status)

    if not users.items:
        users = emptyUserList(page, per_page, order, search_field)
    next_url = url_for(
        "user_index", page=users.next_num, search_status=search_status, search_field=search_field) if users.has_next else None
    prev_url = url_for(
        "user_index", page=users.prev_num, search_status=search_status, search_field=search_field) if users.has_prev else None
    return render_template(
        "user/index.html",
        users=users.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field,
    )
#endregion

#region Query
def searchAll(page, per_page, order, search_field=None):
    """
        Funcion que permite realizar busquedas entre todos los usuarios
            (tanto activos como bloqueados)

        Args:
            page (integer): pagina requerida
            per_page (integer): elementos por pagina requeridos para la
                paginacion
            order (string): orde por defecto por el cual se requiere
                ordenar los registros paginados. Se obtiene del módulo
                de configuración y puede ser ascendente o descendente
            search_field (string): string con el filtro que se le aplica
                a la búsqueda (username total o parcial). Por defecto,
                si no se recibe nada, es None.

        Returns:
            list: Retorna una lista con los usuarios filtrados
    """

    # Búsqueda por orden ascendente (activos y bloqueados)

    if order == 0:
        users = searchAllAsc(page, per_page, search_field)
    
    # Búsqueda por orden descendente (activos y bloqueados)
    else:
        users = searchAllDesc(page, per_page, search_field)
    if not users.items:
        flash("No existen usuarios para su búsqueda", "danger")
        users = emptyUserList(page, per_page, order, search_field)
    return users

def searchFilteredAsc(page, elements, search_field):
    return (
        User.query.filter(User.username.contains(search_field))
        .order_by(User.username.asc())
        .paginate(page, elements, False)
    )

def searchFilteredDesc(page, elements, search_field):
    return (
        User.query.filter(User.username.contains(search_field))
        .order_by(User.username.desc())
        .paginate(page, elements, False)
    )

def searchAllAsc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todos los usuarios paginando de manera
        ascendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todos los usuarios filtrados de manera ascendente
    """
    if (search_field):
        return (
            User.query.filter(User.username.contains(search_field))
            .order_by(User.username.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            User.query.order_by(User.username.asc()).paginate(page, per_page, False)
        )

def searchAllDesc(page, per_page, search_field=None):
    """
    Metodo auxiliar que busca entre todos los usuarios paginando de manera
        descendente

    Args:
        page (integer): página requerida
        per_page (integer): elementos por página requeridos

    Returns:
        list: Lista de todos los usuarios filtrados de manera descendente
    """
    if (search_field):
        return (
            User.query.filter(User.username.contains(search_field))
            .order_by(User.username.desc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            User.query.order_by(User.username.desc()).paginate(page, per_page, False)
        )

def emptyUserList(page, per_page,order, search_field=None):
    """
    Función auxiliar utilizada cuando una query retorna una lista vacia
    Informa al usuario a través de un flash message y retorna la lista
    completa de los usuarios.

    Returns:
        list: retorna una lista con todos los usuarios
    """
    if (search_field):
        # Obtengo las listas de usuarios segun el orden por defecto
        if order == 0:
            users = searchAllAsc(page, per_page)
        else:
            users = searchAllDesc(page, per_page)
        return users
    else:
        return None

def searchByStatusAsc(page, per_page, search_status, search_field):
    
    if (search_field):
        return (
            User.query.filter(and_(User.active == search_status, User.username.contains(search_field)))
            .order_by(User.username.asc())
            .paginate(page, per_page, False)
        )
    else:
        return (
            User.query.filter(User.active == search_status)
            .order_by(User.username.asc())
            .paginate(page, per_page, False)
        )

def searchByStatusDesc(page, elements, search_status, search_field):
    return (
        User.query.filter(
            and_(User.active == search_status,
                 User.username.contains(search_field))
        )
        .order_by(User.username.desc())
        .paginate(page, elements, False)
    )

def searchByStatus(page, per_page, order, search_field, search_status):
    """
        Funcion auxiliar que permite realizar busquedas entre los usuarios segun
            el estado (activo o bloqueado) indicado por el usuario

        Args:
            page (integer): pagina requerida
            elements (integer): elementos por pagina requeridos para la paginacion

        Returns:
            list: Retorna una lista con los usuarios filtrados y con los valores
            de los inputs enviados por el usuario a traves del form
    """
    if order == 0:
        users = searchByStatusAsc(page, per_page, search_status, search_field)
    else:
        users = searchByStatusDesc(page, per_page, search_status, search_field)
    if not users.items:
        flash("No existen usuarios para su búsqueda", "danger")
        users = emptyUserList(page, per_page, order, search_field)
    return users

#endregion

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

def isoperator(id):
    """
    Función auxiliar que indica, a partir de un id, si un usuario posee
    UNICAMENTE el rol operador.

    Args:
        id (integer): id del usuario

    Returns:
        boolean: Devuelve true si el usuario es UNICAMENTE operador.
        Caso contrario, false.
    """
    consulta = (
        db.session.query(User, Role)
        .join(User.roles)
        .where(Role.name != "ROL_ADMINISTRADOR")
        .where(Role.name == "ROL_OPERADOR")
        .where(User.id == id)
        .first()
    )
    return consulta
def validateNoEmpty(form):
    """
    Función auxiliar. Funcion que realiza la validación del
    formulario de creacion/edicion de usuario (verifica que no tenga
    campos vacios)

    Args:
        form (request.form): formulario enviado por el usuario a traves de
        los respectivos inputs

    Returns:
        boolean: Devuelve true si no hay ningun campo vacio del
        formulario y false caso contrario
    """
    noempty = True
    for input in form:
        if not form[input]:
            flash(
                "El campo {} no puede estar vacío".format(
                    flask.escape(parse_input(input))
                ),
                "danger",
            )
            noempty = False
    return noempty


def validateUsername(form, id):
    """
    Función auxiliar. Función que realiza la validación del nombre de
    usuario del formulario (verifica que no este repetido)


    Args:
        form (request.form): formulario enviado por el usuario a traves de
            los respectivos inputs
        id (integer): id del usuario

    Returns:
        [boolean]: [Devuelve true si es un nombre de usuario valido y false
         caso contrario]
    """
    if id == None:
        if (
            db.session.query(User.username).filter_by(
                username=form["username"]).first()
            is not None
        ):
            flash("El nombre de usuario ya existe", "danger")
            return False
        return True
    else:
        if (
            db.session.query(User.username)
            .filter_by(username=form["username"])
            .filter(User.id != id)
            .first()
            is not None
        ):
            flash("El nombre de usuario ya existe", "danger")
            return False
        return True


def validateEmail(form, id):
    """
    Función auxiliar que realiza la validación del email del usuario del
    formulario (verifica que no este repetido)

    Args:
        form (request.form): formulario enviado por el usuario a traves de
            los respectivos inputs
        id (integer): id del usuario

    Returns:
        boolean: Devuelve true si es un email valido y false caso contrario
    """
    if id == None:
        if (
            db.session.query(User.email).filter_by(email=form["email"]).first()
            is not None
        ):
            flash("El email ya existe", "danger")
            return False
        return True
    else:
        if (
            db.session.query(User.email)
            .filter_by(email=form["email"])
            .filter(User.id != id)
            .first()
            is not None
        ):
            flash("El email ya existe", "danger")
            return False
        return True


def validateForm(form, id=None):
    """
    Función auxiliar que valida un formulario, verificando que no contenga campos
    vacios y que el nombre de usuario y el email sean validos

    Args:
        form (request.form): formulario enviado por el usuario a traves de
            los respectivos inputs
        id (integer): id del usuario

    Returns:
        boolean: Devuelve true si el formulario es valido, false caso contrario.
    """
    return (
        validateNoEmpty(form)
        and validateUsername(form, id)
        and validateEmail(form, id)
    )

#endregion

#region New
def new():
    """
    Renderización del formulario de creación de usuarios

    Returns:
        HTML: Pantalla de creacion de usuario nuevo
    """
    return render_template("user/new.html")

# @has_permission("user_new")
# @login_required
def creation(form):
    """
    Metodo que crea un usuario a partir de los datos ingresados por un
    formulario (guardando en base de datos). Se realiza la validacion del
    lado del servidor y se informa el resultado.

    Args:
        form (request.form): formulario enviado por el usuario a traves de
         los respectivos inputs

    Returns:
        boolean: Retorna true si el usuario pudo ser creado correctamente,
         false caso contrario
    """
    new_user = User(**form)
    if validateForm(form):
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("El usuario fue creado correctamente", category="success")
            return True
        except:
            flash("El usuario no se pudo crear. Vuelva a intentar.", category="danger")
    return False

# @has_permission("user_new")
# @login_required
def create():
    """
    Metodo que permite la creacion de un usuario renderizando la pantalla
    de inicio en caso de haberse creado con exito o la pagina de creacion
    de usuario en caso de haber fallado el alta, mostrando las validaciones.

    Returns:
        HTML: Pantalla de inicio del modulo de usuarios si la creacion tuvo
        exito o pantalla de creacion de usuarios en caso contrario
    """
    if creation(request.form):
        return redirect(url_for("home"))
    else:
        return render_template(
            "user/new.html",
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            username=request.form["username"],
            email=request.form["email"],
        )


#endregion

#region Delete
@has_permission("user_destroy")
@login_required
def confirm_delete(id):
    """
    Metodo que renderiza la pantalla de confirmacion de eliminar usuario

    Args:
        id (integer): id del usuario

    Returns:
        HTML: Pantalla de confirmacion de eliminar usuario
    """
    user = User.query.filter_by(id=id).one()
    return render_template("user/delete.html", user=user)


@has_permission("user_destroy")
@login_required
def delete(id):
    """
    Metodo que permite y confirma la eliminacion de un usuario

    Args:
        id (integer): id del usuario

    Returns:
        HTML: Retorna la pantalla de inicio del modulo usuarios (index)
        informando al usuario el exito o el fallo de su accion
    """
    user = User.query.filter_by(id=id).one()
    db.session.delete(user)
    try:
        db.session.commit()
        flash("Se eliminó el usuario", "success")
    except:
        flash("Error al eliminar al usuario", "danger")
    return index()


#endregion

#region Update
@has_permission("user_update")
@login_required
def edit(id):
    """
    Metodo que renderiza la pantalla de edicion de informacion de un usuario

    Args:
        id (integer): id del usuario

    Returns:
        HTML: Retorna la pantalla de edicion de la informacion del usuario
         especificado por parametro con su respectivo formulario
    """
    usr = User.query.filter_by(id=id).one()
    return render_template("user/edit.html", user=usr)


@has_permission("user_update")
@login_required
def edit_confirmed(id):
    """
    Metodo que permite enviar los cambios durante la edicion de la
    informacion de un usuario. Realiza las validaciones e informa al
    usuario sobre su accion

    Args:
        id (integer): id del usuario

    Returns:
        HTML: Pantalla de inicio del modulo de usuarios si la edicion
        tuvo exito o pantalla de edicion del usuario en caso contrario
    """
    usuario = User.query.filter_by(id=id).one()
    usr = User.update(usuario, request.form)

    # Borrado de los permisos existentes del usuario

    roles = UserRoles.query.filter_by(user_id=id)

    for each in roles:
        db.session.delete(each)
    
    # Agrego los nuevos roles

    selected_role = request.form["role"]

    if selected_role == '0':
        new_role1 = UserRoles(id, 1)
        db.session.add(new_role1)
        new_role2 = UserRoles(id, 2)
        db.session.add(new_role2)
    elif selected_role == '1':
        new_role = UserRoles(usuario.id, 1)
        db.session.add(new_role)
    elif selected_role == '2':
        new_role = UserRoles(usuario.id, 2)
        db.session.add(new_role)
    

    if validateForm(request.form, id):
        db.session.add(usr)

        try:
            db.session.commit()
            flash("El usuario fue actualizado correctamente", "success")
            return redirect(url_for("user_index"))
        except:
            flash("El usuario no se pudo actualizar. Vuelva a intentar.", "danger")
            return redirect(url_for("user_edit", id=id))
    else:
        return redirect(url_for("user_edit", id=id))

#endregion
#region Toggle
@has_permission("user_toggle")
@login_required
def toggle(id):
    """
    Funcion conmutador del estado del usuario. Si esta activo pasa a
        bloqueado y si esta bloqueado pasa a activo


    Args:
        id (integer): id del usuario

    Returns:
        HTML: Retorna nuevamente la pantalla de inicio del modulo de usuarios,
         informando al usuario sobre su accion
    """
    user = User.query.filter_by(id=id).one()

    consulta = (
        db.session.query(User, Role)
        .join(User.roles)
        .where(Role.name == "ROL_ADMINISTRADOR")
        .where(User.id == id)
        .first()
    )

    if consulta is None:
        user.active = not user.active
        try:
            db.session.commit()
            flash("Se cambió el estado del usuario", "success")
        except:
            flash("Error al cambiar el estado del usuario", "danger")
        return redirect(url_for("user_index"))
    else:
        flash("No se puede cambiar el estado de un usuario administrador", "danger")
        return redirect(url_for("user_index"))
#endregion

@login_required
def show(id):
    """
    Metodo que renderiza la pantalla de vista del perfil de usuario

    Args:
        id (integer): id del usuario

    Returns:
        HTML: Pantalla de vista del perfil de usuario
    """
    user = User.query.filter_by(id=id).one()
    return render_template("user/show.html", user=user)