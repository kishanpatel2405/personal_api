import json
from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional, Type, Union
import tomlkit

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
