from authlib.oidc.core import grants, UserInfo

from server.src.services.oauth2.code import OAuth2AuthorizationCodeService

DUMMY_JWT_CONFIG = {
    'key': 'secret-key',
    'alg': 'HS256',
    'iss': 'https://authlib.org',
    'exp': 3600,
}


def exists_nonce(nonce, req):
    exists = OAuth2AuthorizationCodeService.find_by(
        client_id=req.client_id,
        nonce=nonce,
        fetch_one=True
    )
    return bool(exists)


def generate_user_info(user):
    return UserInfo(sub=str(user.id), name=user.username)


class OpenIDCode(grants.OpenIDCode):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user)


class OpenIDImplicitGrant(grants.OpenIDImplicitGrant):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


class OpenIDHybridGrant(grants.OpenIDHybridGrant):
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

    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)
