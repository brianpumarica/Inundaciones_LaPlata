from app.db import db
from flask import redirect, request, render_template, session, flash, url_for
from app.models.complaint import Complaint
from app.models.follow_complaint import FollowComplaint
from app.models.user import User
from app.helpers.decorators import has_permission, login_required
from app.helpers.auth import authenticated
from datetime import datetime
from app.models.configuration import Configuration
from operator import and_


# Public resources
# Renderización del index ordenado las denuncias segun el orden predeterminado
@has_permission("complaint_index")
@login_required
def index():
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        complaints = Complaint.query.order_by(Complaint.title.asc()).paginate(
            page, int(criterion.per_page), False
        )
    else:
        complaints = Complaint.query.order_by(Complaint.title.desc()).paginate(
            page, int(criterion.per_page), False
        )
    if not complaints:
        flash("En estos momentos no hay denuncias en el sistema", "danger")
    next_url = (
        url_for("complaint_index", page=complaints.next_num)
        if complaints.has_next
        else None
    )
    prev_url = (
        url_for("complaint_index", page=complaints.prev_num)
        if complaints.has_prev
        else None
    )
    return render_template(
        "complaint/index.html",
        complaints=complaints.items,
        next_url=next_url,
        prev_url=prev_url,
    )

# busqueda de denuncias
@has_permission("complaint_index")
@login_required
def search():
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if request.form["search_status"] == "any_status":
        complaints, search_status, search_field = searchAll(
            page, int(criterion.per_page)
        )
    else:
        complaints, search_status, search_field = searchByStatus(
            page, int(criterion.per_page)
        )
    if not complaints.items:
        complaints, search_status, search_field = emptyComplaintsList()
    next_url = (
        url_for("complaint_index", page=complaints.next_num)
        if complaints.has_next
        else None
    )
    prev_url = (
        url_for("complaint_index", page=complaints.prev_num)
        if complaints.has_prev
        else None
    )
    return render_template(
        "complaint/index.html",
        complaints=complaints.items,
        next_url=next_url,
        prev_url=prev_url,
        search_status=search_status,
        search_field=search_field
    )

# Busca entre todos las denuncias 
def searchAll(page, elements):
    search_field = request.form["search_field"]
    fecha_inicial_del_input = request.form["fecha_inicial_del_input"]
    fecha_final_del_input = request.form["fecha_final_del_input"]

    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        complaints = (
            Complaint.query.filter(
                #Complaint.title.contains(search_field)
                and_(Complaint.title.contains(search_field), 
                Complaint.date_creation>=fecha_inicial_del_input
                ),
                and_(Complaint.date_creation>=fecha_inicial_del_input, 
                #repito la linea para poder usar el and_, que espera 2 parametros
                Complaint.date_creation<=fecha_final_del_input
                )
            )
            .order_by(Complaint.title.asc())
            .paginate(page, elements, False)
        )
    else:
        complaints = (
            Complaint.query.filter(
                #Complaint.title.contains(search_field)
                and_(Complaint.title.contains(search_field), 
                Complaint.date_creation>=fecha_inicial_del_input
                ),
                and_(Complaint.date_creation>=fecha_inicial_del_input, 
                #repito la linea para poder usar el and_, que espera 2 parametros
                Complaint.date_creation<=fecha_final_del_input
                )
            )
            .order_by(Complaint.title.desc())
            .paginate(page, elements, False)
        )


    if not complaints:
        complaints, search_status, search_field = emptyComplaintsList()
    else:
        search_status = request.form["search_status"]
    return complaints, search_status, search_field


# Busca entre denuncias (sin corfirmar, en curso, resuelta y cerrada)
def searchByStatus(page, elements):
    search_status = request.form["search_status"]
    search_field = request.form["search_field"]
    fecha_inicial_del_input = request.form["fecha_inicial_del_input"]
    fecha_final_del_input = request.form["fecha_final_del_input"]



    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    if criterion.order == 0:
        complaints = (
                Complaint.query.filter(
                    and_(Complaint.status == search_status, 
                    Complaint.title.contains(search_field)
                    ),
                    and_(Complaint.date_creation>=fecha_inicial_del_input,
                    Complaint.date_creation<=fecha_final_del_input
                    )
                )
                .order_by(Complaint.title.asc())
                .paginate(page, elements, False)
            )
    else:
        complaints = (
            Complaint.query.filter(
                and_(Complaint.status == search_status, 
                Complaint.title.contains(search_field)
                ),
                and_(Complaint.date_creation>=fecha_inicial_del_input,
                Complaint.date_creation<=fecha_final_del_input
                )
            )
            .order_by(Complaint.title.desc())
            .paginate(page, elements, False)
        )
    if not complaints:
        complaints, search_status, search_field = emptyComplaintsList()
    return complaints, search_status, search_field

# un mensaje de que no encontro denuncias y devuelte todas las denuncias
def emptyComplaintsList():
    flash("No se encontraron puntos de encuentro con esos requerimientos", "danger")
    criterion = Configuration.query.first()
    page = request.args.get("page", 1, type=int)
    complaints = Complaint.query.order_by(Complaint.title.asc()).paginate(
        page, int(criterion.per_page), False
    )
    return complaints, None, None


# Renderización de la vista view, con los detalles de la denuncia
@has_permission("complaint_index")
@login_required
def view(id):
    # users = User.query.all()
    users = User.query.where(User.id == id).first()
    complaint = Complaint.query.filter_by(id=id).one()
    return render_template("complaint/view.html", complaint=complaint, users=users )


# Renderización del formulario de creación de la denuncia
@has_permission("complaint_new")
@login_required
def new():
    return render_template("complaint/new.html")


# Creación de la denuncia
@has_permission("complaint_new")
@login_required
def create():
    new_complaint = Complaint(**request.form)
    Complaint.set_attributes_default(new_complaint)
    db.session.add(new_complaint)
    try:
        db.session.commit()
        flash("Se creo correctamente la denuncia.", "success")
    except:
        flash("No se pudo crear la denuncia.", "danger")
    return redirect(url_for("complaint_index"))


# Renderización de la pantalla de confirmación de eliminar denuncia
@has_permission("complaint_destroy")
@login_required
def confirmDelete(id):
    complaint = Complaint.query.filter_by(id=id).one()
    return render_template("complaint/delete.html", complaint=complaint)


# Borrado de una denuncia
@has_permission("complaint_destroy")
@login_required
def delete(id):
    complaint = Complaint.query.filter_by(id=id).one()
    db.session.delete(complaint)
    try:
        db.session.commit()
        flash("Se elimino correctamente la denuncia.", "success")
    except:
        flash("No se pudo eliminar la denuncia.", "danger")
    return redirect(url_for("complaint_index"))


# Renderización de la pantalla de edición de información de una denuncia
@has_permission("complaint_update")
@login_required
def edit(id):
    complaint = Complaint.query.filter_by(id=id).one()
    return render_template("complaint/edit.html", complaint=complaint)


# Edición de una denuncia
@has_permission("complaint_update")
@login_required
def confirmEdited(id):
    Complaint.update(id, request.form)
    try:
        db.session.commit()
        flash("Se modifico correctamente, la denuncia.", "success")
    except:
        flash("No se pudo editar la denuncia.", "danger")
    return redirect(url_for("complaint_index"))

# Renderización del index ordenado del seguimiento de las denuncias
@has_permission("follow_complaint_index")
@login_required
def index_follow(id):
    complaint = Complaint.query.filter_by(id=id).one()
    follow_complaints = FollowComplaint.query.filter_by(id_complaint=id)
    #user_comp = User.query.filter_by(id=follow_complaints.author).one()
#    return render_template("complaint/index_follow.html", complaint= complaint, follow_complaints=follow_complaints, user = user)
    return render_template("complaint/index_follow.html", complaint= complaint, follow_complaints=follow_complaints)

# Renderización del formulario para crear un seguimiento de denuncia
@has_permission("follow_complaint_new")
@login_required
def new_follow(id):
    return render_template("complaint/new_follow.html", id_complaint=id)

# creación del seguimiento de la denuncia
@has_permission("follow_complaint_new")
@login_required
def create_follow():
    follow_complaint = FollowComplaint(**request.form)
    follow_complaint = FollowComplaint.set_attributes_default(follow_complaint)
    try:
        db.session.add(follow_complaint)
        db.session.commit()
        flash("Se creo correctamente el seguimiento de la denuncia.", "success")
    except:
        flash("No se pudo crear el seguimiento de la denuncia.", "danger")
    return redirect(url_for("complaint_index_follow", id=follow_complaint.id_complaint))

@has_permission("complaint_index")
@login_required
def toggle(id):
    complaint = Complaint.query.filter_by(id=id).one()
    Complaint.not_call(complaint)
    try:
        db.session.commit()
    except:
        #si imprimo algo, imprimiría 2 cosas - ya que #not_call - linea 233, tambien imprime
        print('nothing')
    return redirect(url_for("complaint_index"))
