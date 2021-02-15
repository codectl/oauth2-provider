from authlib.oauth2.rfc7636 import CodeChallenge
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
)
from authlib.integrations.sqla_oauth2 import (
    create_revocation_endpoint
)

from server.src import db
from server.src.models.oauth2 import OAuth2Token
from server.src.oauth2.grants.OAuth2Grants import (
    grants,
    AuthorizationCodeGrant,
    PasswordGrant,
    RefreshTokenGrant
)
from server.src.oauth2.grants.OpenIDCGrants import (
    OpenIDCode,
    OpenIDHybridGrant,
    OpenIDImplicitGrant
)
from server.src.services.oauth2.client import OAuth2ClientService
from server.src.services.oauth2.token import OAuth2TokenService


def query_client(client_id):
    return OAuth2ClientService.find_by(client_id=client_id, fetch_one=True)


def save_token(token_data, request):
    if request.user:
        resource_owner_id = request.user.get_id()
    else:
        # client_credentials grant_type, the resource owner
        # becomes the one linked to the client
        resource_owner_id = request.client.resource_owner.id

    # TODO : delete authorization code

    OAuth2TokenService.create(
        client_id=request.client.client_id,
        resource_owner_id=resource_owner_id,
        **token_data
    )


authorization = AuthorizationServer()


def config_oauth(app):
    authorization.init_app(
        app,
        query_client=query_client,
        save_token=save_token
    )

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(AuthorizationCodeGrant, [
        CodeChallenge(required=True),
        OpenIDCode(require_nonce=True)
    ])
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)
    authorization.register_grant(OpenIDImplicitGrant)
    authorization.register_grant(OpenIDHybridGrant)

    # OAuth2 server configurations
    with app.app_context():
        AuthorizationCodeGrant.TOKEN_ENDPOINT_AUTH_METHODS = app.config.get('TOKEN_ENDPOINT_AUTH_METHODS', [])
        RefreshTokenGrant.INCLUDE_NEW_REFRESH_TOKEN = app.config.get('INCLUDE_NEW_REFRESH_TOKEN', False)

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)
