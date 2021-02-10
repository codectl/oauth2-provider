from typing import List, Optional, Union

from flask import current_app

from src import db
from src.models.oauth2.OAuth2Token import OAuth2Token


class OAuth2TokenService:

    @staticmethod
    def create(**kwargs) -> OAuth2Token:
        token = OAuth2Token(**kwargs)

        db.session.add(token)
        db.session.commit()

        current_app.logger.info("Created OAuth2 token '{0}'.".format(token.access_token))

        return token

    @staticmethod
    def get(token_id) -> Optional[OAuth2Token]:
        return OAuth2Token.query.get(token_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[OAuth2Token], Optional[OAuth2Token]]:
        query = OAuth2Token.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()

    @classmethod
    def update(cls, token_id, **kwargs):
        token = cls.get(token_id)
        for key, value in kwargs.items():
            if hasattr(token, key):
                setattr(token, key, value)
        db.session.commit()

        current_app.logger.info("Updated token '{0}' with the following attributes: '{1}'."
                                .format(token.access_token, kwargs))

    @staticmethod
    def delete(token: OAuth2Token):
        if token:
            db.session.delete(token)
            db.session.commit()

            current_app.logger.info("Deleted OAuth2 token '{0}'.".format(token.access_token))
