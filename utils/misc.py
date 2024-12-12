import hashlib
import json
from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional, Type, Union
from pytz import timezone

import jwt
import tomlkit
from jwt import InvalidAlgorithmError, InvalidTokenError, algorithms

from utils.errors import TokenBackendError

try:
    from jwt import PyJWKClient, PyJWKClientError

    JWK_CLIENT_AVAILABLE = True
except ImportError:
    JWK_CLIENT_AVAILABLE = False

ALLOWED_ALGORITHMS = {
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
    "ES256",
    "ES384",
    "ES512",
}


def customize_json_serializer(value):
    if isinstance(value, datetime):
        return value.isoformat()
    else:
        return value.__dict__


def to_json(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=True, default=customize_json_serializer)


async def json_or_text(response):
    text = await response.text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    return text


def get_project_meta(file):
    with open(file) as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)["tool"]["poetry"]


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def aware_utcnow():
    return datetime.utcnow()


def datetime_from_epoch(ts):
    return datetime.utcfromtimestamp(ts)


class TokenBackend:
    def __init__(
            self,
            algorithm,
            signing_key=None,
            verifying_key="",
            audience=None,
            issuer=None,
            jwk_url: str = None,
            leeway: Union[float, int, timedelta] = None,
            json_encoder: Optional[Type[json.JSONEncoder]] = None,
    ):
        self._validate_algorithm(algorithm)

        self.algorithm = algorithm
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.audience = audience
        self.issuer = issuer

        if JWK_CLIENT_AVAILABLE:
            self.jwks_client = PyJWKClient(jwk_url) if jwk_url else None
        else:
            self.jwks_client = None

        self.leeway = leeway
        self.json_encoder = json_encoder

    def _validate_algorithm(self, algorithm):
        """
        Ensure that the nominated algorithm is recognized, and that cryptography is installed for those
        algorithms that require it
        """
        if algorithm not in ALLOWED_ALGORITHMS:
            raise TokenBackendError(f"Unrecognized algorithm type '{algorithm}'")

        if algorithm in algorithms.requires_cryptography and not algorithms.has_crypto:
            raise TokenBackendError(f"You must have cryptography installed to use {algorithm}.")

    def get_leeway(self) -> timedelta:
        if self.leeway is None:
            return timedelta(seconds=0)
        elif isinstance(self.leeway, (int, float)):
            return timedelta(seconds=self.leeway)
        elif isinstance(self.leeway, timedelta):
            return self.leeway
        else:
            raise TokenBackendError(
                f"Unrecognized type '{self.leeway}', 'leeway' must be of type int, float or timedelta.")

    def get_verifying_key(self, token):
        if self.algorithm.startswith("HS"):
            return self.signing_key

        if self.jwks_client:
            try:
                return self.jwks_client.get_signing_key_from_jwt(token).key
            except PyJWKClientError as ex:
                raise TokenBackendError("Token is invalid or expired") from ex

        return self.verifying_key

    def encode(self, payload):
        """
        Returns an encoded token for the given payload dictionary.
        """
        jwt_payload = payload.copy()
        if self.audience is not None:
            jwt_payload["aud"] = self.audience
        if self.issuer is not None:
            jwt_payload["iss"] = self.issuer

        token = jwt.encode(
            jwt_payload,
            self.signing_key,
            algorithm=self.algorithm,
            json_encoder=self.json_encoder,
        )
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.

        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        try:
            return jwt.decode(
                token,
                self.get_verifying_key(token),
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                leeway=self.get_leeway(),
                options={
                    "verify_aud": self.audience is not None,
                    "verify_signature": verify,
                },
            )
        except InvalidAlgorithmError as ex:
            raise TokenBackendError("Invalid algorithm specified") from ex
        except InvalidTokenError as ex:
            raise TokenBackendError("Token is invalid or expired") from ex
