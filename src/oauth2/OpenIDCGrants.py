from authlib.oidc.core import grants, UserInfo

from src.oauth2 import db
from src.models.OAuth2AuthorizationCode import OAuth2AuthorizationCode
from src.oauth2.common import create_authorization_code

DUMMY_JWT_CONFIG = {
    'key': 'secret-key',
    'alg': 'HS256',
    'iss': 'https://authlib.org',
    'exp': 3600,
}


def exists_nonce(nonce, req):
    exists = OAuth2AuthorizationCode.query.filter_by(
        client_id=req.client_id, nonce=nonce
    ).first()
    return bool(exists)


def generate_user_info(user, scope):
    return UserInfo(sub=str(user.id), name=user.username)


class OpenIDCode(grants.OpenIDCode):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


class OpenIDImplicitGrant(grants.OpenIDImplicitGrant):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


class OpenIDHybridGrant(grants.OpenIDHybridGrant):
    def save_authorization_code(self, code, request):
        code = create_authorization_code(code=code, request=request)
        db.session.add(code)
        db.session.commit()
        return code

    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)
