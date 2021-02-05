from typing import List, Optional, Union

from flask import current_app

from src import db
from src.models.Role import Role, RolePermission


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

    @staticmethod
    def create_role_permission(**kwargs) -> RolePermission:
        role_permission = RolePermission(**kwargs)

        db.session.add(role_permission)
        db.session.commit()

        current_app.logger.info("Created Role Permission ('{0}', '{1}').".format(role_permission.role_id,
                                                                                 role_permission.permission_id))

        return role_permission

    @staticmethod
    def get_role_permission(role_id=None, permission_id=None) -> RolePermission:
        return RolePermission.query.filter_by(role_id=role_id, permission_id=permission_id).first()

    @staticmethod
    def delete_role_permission(role_permission: RolePermission):
        if role_permission:
            db.session.delete(role_permission)
            db.session.commit()
