from typing import Any, Dict, List
import jwt
import requests
from datetime import datetime

import schemas
import exceptions

JWKS_URI_CACHE: Dict[str, str] = {}
JWK_CACHE: Dict[str, schemas.JWKInfo] = {}


def get_jwt_header(jwt_token: str) -> schemas.JWTHeader:
    headers: Dict[str, str] = jwt.get_unverified_header(jwt_token)
    return schemas.JWTHeader(**headers)


def get_jwt_payload(jwt_token: str) -> schemas.JWTPayload:
    unverified_payload: Dict[str, Any] = jwt.decode(
        jwt_token, options={"verify_signature": False}
    )
    return schemas.JWTPayload(**unverified_payload)


def fetch_jwk(key_id: str, auth_server_host: str) -> str:

    jwk_cache_id = f"{auth_server_host}_{key_id}"
    if jwk_cache_id in JWK_CACHE:
        return JWK_CACHE[jwk_cache_id].key

    jwks_uri = _fetch_jwks_uri(auth_server_host=auth_server_host)
    # Request the JWK URI to search for the right key.
    resp_jwks_uri = requests.get(
        url=jwks_uri
    )
    if resp_jwks_uri.status_code not in range(200, 300):
        raise exceptions.TokenValidationException()
    jwk: str = _find_key(key_id=key_id, key_set=resp_jwks_uri.json()["keys"])
    JWK_CACHE[jwk_cache_id] = schemas.JWKInfo(
        key_id=key_id,
        key=jwk,
        request_time=datetime.now()
    )

    return jwk


def _fetch_jwks_uri(auth_server_host: str) -> str:
    if auth_server_host in JWKS_URI_CACHE:
        return JWKS_URI_CACHE[auth_server_host]

    resp_well_known = requests.get(
        url=f"{auth_server_host}/.well-known/openid-configuration"
    )
    if resp_well_known.status_code not in range(200, 300):
        raise exceptions.TokenValidationException()
    jwks_uri: str = resp_well_known.json()["jwks_uri"]
    JWKS_URI_CACHE[auth_server_host] = jwks_uri
    return jwks_uri


def _find_key(key_id: str, key_set: List[Dict[str, str]]) -> str:

    for key_info in key_set:
        if key_info["kid"] == key_id:
            return key_info["n"]

    raise exceptions.TokenValidationException()
