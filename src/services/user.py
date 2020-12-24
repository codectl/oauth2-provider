from typing import List, Optional

from flask import current_app, session

from src import db
from src.models.User import User


class UserService:

    @classmethod
    def create(cls, **kwargs) -> User:
        user = User(**kwargs)

        db.session.add(user)
        db.session.commit()

        current_app.logger.info("Created User {0}.".format(user.id))

        return user

    @staticmethod
    def get(user_id) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def find_by(**filters) -> List[User]:
        return User.query.filter_by(**filters).all()

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user against his credentials.
        """

        # TODO: change
        # return UserService.create(username=username)
        return True

    @classmethod
    def current_user(cls):
        """
        Retrieve user in session.
        """
        return cls.get(session.get('id'))
