from flask import current_app

from src import db
from src.services.role import RoleService
from src.services.user import UserService


def seed():

    # Seeding Roles
    if not RoleService.find_by():
        RoleService.create(name='Admin',
                           description='Administrative operations role')
        RoleService.create(name='User',
                           description='Default user role.')
        current_app.logger.info('Roles seeded.')

    # Admin user
    if not UserService.find_by():
        root = UserService.create(username='root')
        root.roles.append(RoleService.find_by(name='Admin', fetch_one=True))
        db.session.commit()
