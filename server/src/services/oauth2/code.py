from typing import List, Optional, Union

from flask import current_app

from server.src import db
from server.src.models.oauth2.OAuth2AuthorizationCode import OAuth2AuthorizationCode


class OAuth2AuthorizationCodeService:

    @staticmethod
    def create(**kwargs) -> OAuth2AuthorizationCode:
        authorization_code = OAuth2AuthorizationCode(**kwargs)

        db.session.add(authorization_code)
        db.session.commit()

        current_app.logger.info("Created OAuth2 authorization code '{0}'.".format(authorization_code.code))

        return authorization_code

    @staticmethod
    def get(code_id) -> Optional[OAuth2AuthorizationCode]:
        return OAuth2AuthorizationCode.query.get(code_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[OAuth2AuthorizationCode], Optional[OAuth2AuthorizationCode]]:
        query = OAuth2AuthorizationCode.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()

    @staticmethod
    def delete(authorization_code: OAuth2AuthorizationCode):
        if authorization_code:
            db.session.delete(authorization_code)
            db.session.commit()

            current_app.logger.info("Deleted OAuth2 authorization code '{0}'.".format(authorization_code.code))
