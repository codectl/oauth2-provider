from authlib.oauth2.rfc6749 import grants
from flask import current_app

from src.services.user import UserService
from src.services.oauth2.code import OAuth2AuthorizationCodeService
from src.services.oauth2.token import OAuth2TokenService


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
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
        OAuth2AuthorizationCodeService.delete(authorization_code=authorization_code)

    def authenticate_user(self, authorization_code):
        return UserService.get(authorization_code.resource_owner.id)


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = UserService.find_by(username=username, fetch_one=True)
        if user and UserService.authenticate(username, password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = OAuth2TokenService.find_by(refresh_token=refresh_token, fetch_one=True)
        if token and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential):
        return UserService.get(credential.resource_owner.id)

    def revoke_old_credential(self, credential):
        OAuth2TokenService.update(credential.id, revoked=True)

