import logging
from functools import wraps
from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)
from authlib.oauth2 import OAuth2Error
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidIssuedAtError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError
)


logger = logging.getLogger('auth')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("/tmp/test.log")
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

logger.addHandler(fh)


def audit():
    def audit_wrapper(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except ExpiredSignatureError:
                return await HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail=f"{detail}",
                    headers={'WWW-Authenticate': 'Bearer'}
                )
        return wrapper
    return audit_wrapper


class JWTAuditAuthentication(object):
    def __init__(self):
        self.logger = logging.getLogger('audit')

    def _http_exception(self, detail):
        self.logger.warning(detail)
        return HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=f"{detail}",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    def __call__(self, fn):
        """Decorector to audit JWT validation"""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                token = fn(*args, **kwargs)
                logger.info(f"{token['preferred_username']} accessd ")
                return token
            except OAuth2Error:
                raise self._http_exception(
                    'invalid_token - JWK public key not found'
                )
            except KeyError:
                raise self._http_exception(
                    'invalid_token - JWK public key not found',
                )
            except DecodeError:
                raise self._http_exception(
                    'invalid_token - Authorization token cannot be decoded',
                )
            except ExpiredSignatureError:
                raise self._http_exception(
                    'invalid_token - Authorization token has expired'
                )
            except ImmatureSignatureError:
                raise self._http_exception(
                    'invalid_token - Authorization token immature',
                )
            except InvalidAlgorithmError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid algorithm',
                )
            except InvalidKeyError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid key error',
                )
            except InvalidIssuedAtError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid issue time',
                )
            except InvalidIssuerError:
                raise self._http_exception(
                    'invalid_token - Authorization token from unrecognized issuer'
                )
            except InvalidTokenError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid'
                )
            except InvalidAudienceError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid audience',
                )
            except MissingRequiredClaimError:
                raise self._http_exception(
                    'invalid_token - Authorization token missing required claims'
                )
        return wrapper
