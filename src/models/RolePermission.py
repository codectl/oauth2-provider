from src import db


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer(), db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)

# Relationships
roles = db.relationship('Role', secondary='role_permissions',
                        backref=backref("permissions", cascade="all"))
