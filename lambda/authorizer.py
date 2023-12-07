from abc import ABC, abstractmethod
import jwt

import schemas
import tools
import exceptions


class Authorizer(ABC):

    @abstractmethod
    def should_validate(self, token: str) -> bool:
        ...

    @abstractmethod
    def get_valid_info(self, token: str) -> schemas.TokenInfo:
        ...


class JWTAuthorizer(Authorizer):

    @abstractmethod
    def get_auth_server_host(self, jwt_info: schemas.JWTInfo) -> str:
        ...

    def get_valid_info(self, token: str) -> schemas.TokenInfo:

        # Get information about the JWT.
        header: schemas.JWTHeader = tools.get_jwt_header(jwt_token=token)
        payload: schemas.JWTPayload = tools.get_jwt_payload(
            jwt_token=token)
        jwt_info = schemas.JWTInfo(header=header, payload=payload)
        auth_server_host: str = self.get_auth_server_host(jwt_info=jwt_info)

        # Validate the token.
        jwk: str = tools.fetch_jwk(
            key_id=header.kid, auth_server_host=auth_server_host
        )
        try:
            jwt.decode(jwt=token, key=jwk, algorithms=[header.alg])
        except Exception as e:
            raise exceptions.TokenValidationException(*e.args)

        return schemas.TokenInfo(issuer=payload.iss, scopes=payload.scope.split(" "))
