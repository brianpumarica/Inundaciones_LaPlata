from app.db import db


class UserRoles(db.Model):
    """es la tabla intermedia entre usuarios y roles"""

    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id