from authlib.oauth2.rfc6749 import grants

from src import db
from src.models.oauth2.OAuth2Token import OAuth2Token
from src.services.user import UserService
from src.services.oauth2.code import OAuth2AuthorizationCodeService


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]

    def save_authorization_code(self, code, request):
        return OAuth2AuthorizationCodeService.create(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            response_type=request.response_type,
            scope=request.scope,
            resource_owner_id=request.user.id,
            code_challenge=request.data.get('code_challenge'),
            code_challenge_method=request.data.get('code_challenge_method'),
            nonce=request.data.get('nonce')
        )

    def query_authorization_code(self, code, client):
        auth_code = OAuth2AuthorizationCodeService.find_by(
            code=code,
            client_id=client.client_id,
            fetch_one=True
        )
        if auth_code and not auth_code.is_expired():
            return auth_code

    def delete_authorization_code(self, authorization_code):
        OAuth2AuthorizationCodeService.delete(
            authorization_code=OAuth2AuthorizationCodeService.find_by(code=authorization_code, fetch_one=True)
        )

    def authenticate_user(self, authorization_code):
        return UserService.get(authorization_code.resource_owner.id)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = UserService.find_by(username=username, fetch_one=True)
        if user and UserService.authenticate(username, password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if token and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential):
        return UserService.get(credential.user_id)

    def revoke_old_credential(self, credential):
        credential.revoked = True
        db.session.add(credential)
        db.session.commit()
