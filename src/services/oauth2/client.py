import datetime
from typing import List, Optional, Union

from flask import current_app
from werkzeug.security import gen_salt

from src.models.oauth2.OAuth2Client import OAuth2Client
from src import db


class OAuth2ClientService:

    @staticmethod
    def create(**kwargs) -> OAuth2Client:
        client = OAuth2Client(
            client_id=kwargs.pop('client_id', gen_salt(24)),
            client_id_issued_at=kwargs.pop('client_id_issued_at', datetime.datetime.utcnow),
            **kwargs
        )

        client.set_client_metadata(kwargs.get('client_metadata', {}))

        # Skip secret if no client authentication method is set
        if kwargs.get('token_endpoint_auth_method') == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        db.session.add(client)
        db.session.commit()

        current_app.logger.info("Created OAuth2 client '{0}'.".format(client.client_id))

        return client

    @staticmethod
    def get(client_id) -> Optional[OAuth2Client]:
        return OAuth2Client.query.get(client_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[OAuth2Client], Optional[OAuth2Client]]:
        query = OAuth2Client.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()