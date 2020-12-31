from src import db
from src.models.Permission import Permission


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    # Relationships
    permissions = db.relationship(Permission, secondary='role_permission')

    def __repr__(self):
        return '<Role {0}>'.format(self.id)


RolePermission = db.Table(
    'role_permission',
    db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey(Role.id, ondelete='CASCADE'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey(Permission.id, ondelete='CASCADE'), primary_key=True)
)
