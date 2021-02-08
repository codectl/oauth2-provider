from typing import List, Optional, Union

from flask import current_app

from src import db
from src.models.Role import Role
from src.services.scope import ScopeService


class RoleService:

    @staticmethod
    def create(**kwargs) -> Role:
        role = Role(**kwargs)

        db.session.add(role)
        db.session.commit()

        current_app.logger.info("Created role '{0}'.".format(role.name))

        return role

    @staticmethod
    def get(role_id) -> Optional[Role]:
        return Role.query.get(role_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[Role], Optional[Role]]:
        query = Role.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()

    @classmethod
    def default_role(cls):
        return cls.find_by(name='User', fetch_one=True)

    @classmethod
    def add_scope(cls, role_name, scope_name):
        role = cls.find_by(name=role_name, fetch_one=True)
        scope = ScopeService.find_by(name=scope_name, fetch_one=True)

        if role and scope:
            role.scopes.append(scope)
            db.session.commit()

            current_app.logger.info("Added scope '{0}' to role '{1}'.".format(scope_name, role_name))

    @classmethod
    def remove_scope(cls, role_name, scope_name):
        role = cls.find_by(name=role_name, fetch_one=True)
        scope = ScopeService.find_by(name=scope_name, fetch_one=True)

        if role and scope and scope not in role.scopes:
            role.scopes.remove(scope)
            db.session.commit()

            current_app.logger.info("Removed scope '{0}' from role '{1}'.".format(scope_name, role_name))
