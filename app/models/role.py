from app.db import db
from app.models.permission import Permission


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.relationship(
        "Permission", secondary="roles_permissions", lazy="dynamic"
    )


class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"
    id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
    permission_id = db.Column(
        db.Integer(), db.ForeignKey("permissions.id", ondelete="CASCADE")
    )
