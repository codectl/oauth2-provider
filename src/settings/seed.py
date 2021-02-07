from flask import current_app

from src.services.role import RoleService
from src.services.scope import ScopeService
from src.services.user import UserService


def seed():

    # Seed Scopes
    if not ScopeService.find_by():
        current_app.logger.info('* Seeding scopes *')
        ScopeService.create(name='view:profile',
                            description='View profile information')
        current_app.logger.info('... Scopes seeded.')

    # Seed Roles
    if not RoleService.find_by():
        current_app.logger.info('* Seeding roles *')
        RoleService.create(name='Admin',
                           description='Administrative operations role')
        RoleService.create(name='User',
                           description='Default user role.')

        # Add scopes to roles
        RoleService.add_scope(role_name='Admin', scope_name='view:profile')
        RoleService.add_scope(role_name='User', scope_name='view:profile')

        current_app.logger.info('... Roles seeded.')

    # Admin user
    if not UserService.find_by():
        current_app.logger.info('* Seeding users *')
        UserService.create(username='admin')
        UserService.add_role(username='admin', role_name='Admin')
        current_app.logger.info('... Users seeded.')
