from src.models.OAuth2AuthorizationCode import OAuth2AuthorizationCode


def create_authorization_code(code, request):
    return OAuth2AuthorizationCode(
        code=code,
        client_id=request.client.client_id,
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        resource_owner_id=request.user.id,
        code_challenge=request.data.get('code_challenge'),
        code_challenge_method=request.data.get('code_challenge_method'),
        nonce=request.data.get('nonce')
    )
