import logging
import traceback
from functools import wraps
from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc6749 import(
    InsecureTransportError,
    InvalidRequestError,
    InvalidClientError,
    InvalidGrantError,
    UnauthorizedClientError,
    UnsupportedGrantTypeError,
    InvalidScopeError,
    AccessDeniedError,
    MissingAuthorizationError,
    UnsupportedTokenTypeError,
    MissingCodeException,
    MissingTokenException,
    MissingTokenTypeException,
    MismatchingStateException,
)
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

class HTTPAuditMixin(object):
    def _http_exception(self, detail):
        self.logger.warning(detail)
        return HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'}
        )

class OAuth2Audit(HTTPAuditMixin):
    def __init__(self):
        self.logger = logging.getLogger('oauth')

    def __call__(self, fn):
        """Decorector to audit JWT validation"""
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except OAuth2Error:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except InsecureTransportError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except InvalidRequestError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except InvalidClientError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except InvalidGrantError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except UnauthorizedClientError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except UnsupportedGrantTypeError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except InvalidScopeError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except AccessDeniedError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except MissingAuthorizationError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except UnsupportedTokenTypeError:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except MissingCodeException:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except MissingTokenException:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except MissingTokenTypeException:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
            except MismatchingStateException:
                raise self._http_exception(
                    'unauthorized - access denied'
                )
        return wrapper

class JWTAudit(HTTPAuditMixin):
    def __init__(self):
        self.logger = logging.getLogger('jwt')

    def __call__(self, fn):
        """Decorector to audit JWT validation"""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                token = fn(*args, **kwargs)
                logger.info(f"{token['preferred_username']} accessed ")
                return token
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
            except InvalidAudienceError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid audience',
                )
            except MissingRequiredClaimError:
                raise self._http_exception(
                    'invalid_token - Authorization token missing required claims'
                )
            except InvalidTokenError:
                raise self._http_exception(
                    'invalid_token - Authorization token invalid'
                )
        return wrapper
