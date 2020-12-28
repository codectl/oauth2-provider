import datetime

from src import db
from src.models.OAuth2ResourceOwner import OAuth2ResourceOwner
from src.models.Role import Role


class User(OAuth2ResourceOwner):
    __tablename__ = 'user'

    id = db.Column(db.Integer, db.ForeignKey(OAuth2ResourceOwner.id), primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    roles = db.relationship(Role, secondary='user_role', lazy="dynamic")

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    def is_authenticated(self):
        """ Flask-Login field """

        return self.authenticated

    def is_active(self):
        """ Flask-Login field """

        return self.active

    @staticmethod
    def is_anonymous():
        """ Flask-Login field """

        return False

    def get_id(self):
        """ Flask-Login field """

        return str(self.id)

    def __str__(self):
        return self.__dict__


UserRole = db.Table(
    'user_role',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey(Role.id, ondelete='CASCADE'), primary_key=True)
)
