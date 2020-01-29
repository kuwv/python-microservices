import logging
# import traceback
from functools import wraps
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc6749 import (
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
    MismatchingStateException
)

logger = logging.getLogger('auth')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("/tmp/test.log")
fh.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

fh.setFormatter(formatter)

logger.addHandler(fh)


# def audit():
#     def audit_wrapper(fn):
#         @wraps(fn)
#         async def wrapper(*args, **kwargs):
#             try:
#                 return await fn(*args, **kwargs)
#             except ExpiredSignatureError:
#                 return await HTTPException(
#                     status_code=HTTP_401_UNAUTHORIZED,
#                     detail=f"{detail}",
#                     headers={'WWW-Authenticate': 'Bearer'}
#                 )
#         return wrapper
#     return audit_wrapper


class HTTPAuditMixin(object):
    def _http_exception(self, detail):
        self.logger.warning(detail)
        return HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'}
        )


class AuthAudit(HTTPAuditMixin):
    def __init__(self):
        self.logger = logging.getLogger('oauth')

    def __call__(self, fn):
        """Decorector to audit JWT validation"""
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                token = await fn(*args, **kwargs)
                self.logger.info(
                    f"{token.claims['preferred_username']} accessed "
                )
                return token
            except InsecureTransportError:
                raise self._http_exception(
                    'unauthorized - insecure transport error'
                )
            except InvalidRequestError:
                raise self._http_exception(
                    'unauthorized - invalid request error'
                )
            except InvalidClientError:
                raise self._http_exception(
                    'unauthorized - invalid client error'
                )
            except InvalidGrantError:
                raise self._http_exception(
                    'unauthorized - invalide grant error'
                )
            except UnauthorizedClientError:
                raise self._http_exception(
                    'unauthorized - unauthorized client error'
                )
            except UnsupportedGrantTypeError:
                raise self._http_exception(
                    'unauthorized - unsupported grant type error'
                )
            except InvalidScopeError:
                raise self._http_exception(
                    'unauthorized - invalid scope error'
                )
            except AccessDeniedError:
                raise self._http_exception(
                    'unauthorized - access denied error'
                )
            except MissingAuthorizationError:
                raise self._http_exception(
                    'unauthorized - missing authorization error'
                )
            except UnsupportedTokenTypeError:
                raise self._http_exception(
                    'unauthorized - unsupported token type error'
                )
            except MissingCodeException:
                raise self._http_exception(
                    'unauthorized - missing code exception'
                )
            except MissingTokenException:
                raise self._http_exception(
                    'unauthorized - missing token exception'
                )
            except MissingTokenTypeException:
                raise self._http_exception(
                    'unauthorized - missing token type exception'
                )
            except MismatchingStateException:
                raise self._http_exception(
                    'unauthorized - mismatching state exception'
                )
            except OAuth2Error:
                raise self._http_exception(
                    'unauthorized - oauth error occured'
                )
        return wrapper
