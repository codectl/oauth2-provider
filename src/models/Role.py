from src import db
from src.models.Scope import Scope


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    # Relationships
    scopes = db.relationship(Scope, secondary='role_scope')

    def __repr__(self):
        return "<Role '{0}'>".format(self.name)


db.Table(
    'role_scope',
    db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey(Role.id, ondelete='CASCADE'), primary_key=True),
    db.Column('scope_id', db.Integer, db.ForeignKey(Scope.id, ondelete='CASCADE'), primary_key=True)
)
