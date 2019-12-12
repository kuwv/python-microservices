# ALT: https://docs.authlib.org/en/latest/specs/rfc7523.html#jwt-grant-type
# https://docs.authlib.org/en/latest/client/starlette.html

# Overview: auth to keycloak to interconnect microservices on backend

from authlib.oauth2.rfc6749.grants import (
    ClientCredentialsGrant,
    RefreshTokenGrant
)
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name='webapp',
    client_id='{{ your-github-client-id }}',
    client_secret='{{ your-github-client-secret }}',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


class ClientCredentials(ClientCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]


class RefreshToken(RefreshTokenGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic', 'client_secret_post'
    ]

    def authenticate_refresh_token(self, refresh_token):
        item = Token.query.filter_by(refresh_token=refresh_token).first()
        # define is_refresh_token_valid by yourself
        # usually, you should check if refresh token is expired and revoked
        if item and item.is_refresh_token_valid():
            return item

    def authenticate_user(self, credential):
        return User.query.get(credential.user_id)

    def revoke_old_credential(self, credential):
        credential.revoked = True
        db.session.add(credential)
        db.session.commit()

server.register_grant(ClientCredentialsGrant)
server.register_grant(RefreshTokenGrant)
