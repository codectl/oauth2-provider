from authlib.oauth2.rfc7636 import CodeChallenge
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
)
from authlib.integrations.sqla_oauth2 import (
    create_revocation_endpoint
)

from src import db
from src.models.OAuth2Client import OAuth2Client
from src.models.OAuth2Token import OAuth2Token
from src.oauth2.OAuth2Grants import (
    grants,
    AuthorizationCodeGrant,
    PasswordGrant,
    RefreshTokenGrant
)
from src.oauth2.OpenIDCGrants import (
    OpenIDCode,
    OpenIDHybridGrant,
    OpenIDImplicitGrant
)


def query_client(client_id):
    return OAuth2Client.query.filter_by(client_id=client_id).first()


def save_token(token_data, request):
    if request.user:
        resource_owner_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        resource_owner_id = request.client.user_id
    token = OAuth2Token(
        client_id=request.client.client_id,
        resource_owner_id=resource_owner_id,
        **token_data
    )
    db.session.add(token)
    db.session.commit()


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

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)
