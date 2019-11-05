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
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except OAuth2Error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="oauth2 - JWK public key not found"
            )
    return wrapper

def token_exception(fn):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - JWK public key not found"
            )
        except DecodeError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token cannot be decoded"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token has expired"
            )
        except ImmatureSignatureError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token immature"
            )
        except InvalidAlgorithmError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token invalid algorithm"
            )
        except InvalidAudienceError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token invalid audience"
            )
        except InvalidKeyError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token invalid key error"
            )
        except InvalidIssuedAtError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token invalid issue time"
            )
        except InvalidIssuerError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token from unrecognized issuer"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token invalid"
            )
        except MissingRequiredClaimError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="invalid_token - Authorization token missing claim(s)"
            )
    return wrapper
