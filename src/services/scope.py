from typing import List, Optional, Union
from flask import current_app

from src import db
from src.models.Scope import Scope


class ScopeService:

    @staticmethod
    def create(**kwargs) -> Scope:
        scope = Scope(**kwargs)

        db.session.add(scope)
        db.session.commit()

        current_app.logger.info("Created scope '{0}'.".format(scope.name))

        return scope

    @staticmethod
    def get(scope_id) -> Optional[Scope]:
        return Scope.query.get(scope_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[Scope], Optional[Scope]]:
        query = Scope.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()
