import time
import requests
import typer
import psp.config as config
from psp.auth.core import Auth
from psp.auth import store

_LEEWAY = 15


def get_access_token() -> str:
    tokens = store.load()
    if tokens is None:
        typer.echo("Not logged in. Run: psp auth login", err=True)
        raise typer.Exit(1)

    now = time.time()
    if now < tokens["access_token_expires_at"] - _LEEWAY:
        return tokens["access_token"]

    refresh_token = tokens.get("refresh_token")
    refresh_expires_at = tokens.get("refresh_token_expires_at")
    if refresh_token and (refresh_expires_at is None or now < refresh_expires_at - _LEEWAY):
        cfg = config.load()
        auth = Auth(config.oidc_metadata_url(), cfg["client_id"], cfg["client_secret"])
        r = requests.post(
            auth.endpoints()["token_endpoint"],
            data=auth.client_data() | {"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=(2, 10),
        )
        if r.ok:
            data = r.json()
            new_access = data["access_token"]
            new_expires_at = float(auth.decode_token(new_access).claims["exp"])
            new_refresh_expires_at = (
                time.time() + data["refresh_expires_in"] if "refresh_expires_in" in data else None
            )
            store.save(new_access, data.get("refresh_token", refresh_token), new_expires_at, new_refresh_expires_at)
            return new_access

    typer.echo("Session expired. Run: psp auth login", err=True)
    raise typer.Exit(1)
