from fastapi import HTTPException
import functools
import logging
from starlette.status import HTTP_401_UNAUTHORIZED
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


def oauth_exception(fn):
    '''
    Decorator to provid exceptions for OAuth2
    '''
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except OAuth2Error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='oauth2 - JWK public key not found'
            )
    return wrapper

def token_exception(fn):
    '''
    Decorector to provide exceptions for JWT validation
    '''
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - JWK public key not found',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except DecodeError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token cannot be decoded',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token has expired',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except ImmatureSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token immature',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidAlgorithmError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token invalid algorithm',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidAudienceError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token invalid audience',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidKeyError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token invalid key error',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidIssuedAtError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token invalid issue time',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidIssuerError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token from unrecognized issuer',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token invalid',
                headers={'WWW-Authenticate': 'Bearer'}
            )
        except MissingRequiredClaimError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='invalid_token - Authorization token missing claim(s)',
                headers={'WWW-Authenticate': 'Bearer'}
            )
    return wrapper
