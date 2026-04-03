import time
import typer
import psp.config as config
from psp.auth.core import Auth
from psp.auth.device_auth import run as device_auth_run
from psp.auth import store

app = typer.Typer()


@app.command()
def login():
    cfg = config.load()
    auth = Auth(config.oidc_metadata_url(), cfg["client_id"], cfg["client_secret"])
    access_token, refresh_token, access_expires_at, refresh_expires_at = device_auth_run(auth, cfg["scope"])
    store.save(access_token, refresh_token, access_expires_at, refresh_expires_at)
    typer.echo("Logged in successfully.")


@app.command()
def logout():
    store.clear()
    typer.echo("Logged out.")


@app.command()
def status():
    tokens = store.load()
    if tokens is None:
        typer.echo("Not logged in.")
        return

    expires_in = tokens["access_token_expires_at"] - time.time()
    if expires_in > 0:
        typer.echo(f"Logged in. Access token expires in {int(expires_in)}s.")
    else:
        typer.echo("Access token expired (will refresh automatically).")

    try:
        cfg = config.load()
        auth = Auth(config.oidc_metadata_url(), cfg["client_id"], cfg["client_secret"])
        claims = auth.decode_token(tokens["access_token"]).claims
        typer.echo(f"User: {claims.get('preferred_username', claims.get('sub', 'unknown'))}")
    except Exception:
        pass
