from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenInfo:
    issuer: str
    scopes: List[str]


@dataclass
class JWTHeader:
    alg: str
    kid: str


@dataclass
class JWTPayload:
    iss: str
    scope: str


@dataclass
class JWTInfo:
    header: JWTHeader
    payload: JWTPayload


@dataclass
class JWKInfo:
    key_id: str
    key: str
    request_time: datetime
