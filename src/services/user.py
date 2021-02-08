from typing import List, Optional, Union

from flask import current_app

from src import db
from src.models.User import User
from src.services.role import RoleService


class UserService:

    @classmethod
    def create(cls, **kwargs) -> User:
        user = User(**kwargs)

        db.session.add(user)
        db.session.commit()

        current_app.logger.info("Created user '{0}'.".format(user.username))

        # Setting default role for this user
        default_role = RoleService.default_role()
        if default_role:
            cls.add_role(user.username, role_name=default_role.name)

        return user

    @staticmethod
    def get(user_id) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[User], Optional[User]]:
        query = User.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()

    @classmethod
    def update(cls, user_id, **kwargs):
        user = cls.get(user_id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()

        current_app.logger.info("Updated user '{0}' with the following attributes: '{1}'."
                                .format(user.username, kwargs))

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user against his credentials.
        """

        # TODO: change
        # return UserService.create(username=username)
        return True

    @classmethod
    def add_role(cls, username, role_name):
        user = cls.find_by(username=username, fetch_one=True)
        role = RoleService.find_by(name=role_name, fetch_one=True)

        if user and role and role not in user.roles:
            user.roles.append(role)
            db.session.commit()

            current_app.logger.info("Added role '{0}' to user '{1}'.".format(role_name, username))

    @classmethod
    def remove_role(cls, username, role_name):
        user = cls.find_by(username=username, fetch_one=True)
        role = RoleService.find_by(name=role_name, fetch_one=True)

        if user and role:
            user.roles.remove(role)
            db.session.commit()

            current_app.logger.info("Removed role '{0}' from user '{1}'.".format(role_name, username))
