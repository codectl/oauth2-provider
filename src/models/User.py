from src import db
from src.models.OAuth2ResourceOwner import OAuth2ResourceOwner
from src.models.Role import Role


class User(OAuth2ResourceOwner):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.ForeignKey(OAuth2ResourceOwner.id), primary_key=True)
    username = db.Column(db.String(40), unique=True)

    # Relationships
    roles = db.relationship(Role, secondary='user_role', lazy="dynamic")

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    def get_user_id(self):
        return self.id

    def __str__(self):
        return self.username


db.Table(
    'user_role',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey(Role.id, ondelete='CASCADE'), primary_key=True)
)
