import time
from typing import List, Optional, Union

from flask import current_app
from werkzeug.security import gen_salt

from src import db
from src.models.oauth2.OAuth2Client import OAuth2Client


class OAuth2ClientService:

    @staticmethod
    def create(**kwargs) -> OAuth2Client:
        client_metadata = kwargs.pop('client_metadata', {})
        client = OAuth2Client(
            client_id=kwargs.pop('client_id', gen_salt(24)),
            client_id_issued_at=kwargs.pop('client_id_issued_at', int(time.time())),
            **kwargs
        )

        client.set_client_metadata(client_metadata)

        # Skip secret if no client authentication method is set
        if kwargs.get('token_endpoint_auth_method') == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        db.session.add(client)
        db.session.commit()

        current_app.logger.info("Created OAuth2 client '{0}'.".format(client_metadata.get('client_name')))

        return client

    @staticmethod
    def get(client_id) -> Optional[OAuth2Client]:
        # client_id for this case refers to 'id' attribute
        # as opposed to 'client_id'
        return OAuth2Client.query.get(client_id)

    @staticmethod
    def find_by(fetch_one=False, **filters) -> Union[List[OAuth2Client], Optional[OAuth2Client]]:
        query = OAuth2Client.query.filter_by(**filters)
        return query.all() if not fetch_one else query.one_or_none()
