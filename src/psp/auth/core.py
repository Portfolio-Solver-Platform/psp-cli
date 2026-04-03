import requests
from joserfc import jwt
from joserfc.jwk import KeySet


class Auth:
    def __init__(self, metadata_url: str, client_id: str, client_secret: str):
        self._metadata_url = metadata_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._endpoints = None
        self._jwt_keys = None

    def endpoints(self) -> dict:
        if self._endpoints is None:
            r = requests.get(self._metadata_url, timeout=(2, 10))
            r.raise_for_status()
            self._endpoints = r.json()
        return self._endpoints

    def decode_token(self, token: str):
        if self._jwt_keys is None:
            r = requests.get(self.endpoints()["jwks_uri"], timeout=(2, 10))
            r.raise_for_status()
            self._jwt_keys = r.json()
        return jwt.decode(token, KeySet.import_key_set(self._jwt_keys))

    def client_data(self) -> dict:
        return {"client_id": self._client_id, "client_secret": self._client_secret}
