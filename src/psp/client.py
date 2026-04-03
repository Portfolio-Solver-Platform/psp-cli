import requests
import typer
import psp.config as config
from psp.auth import get_access_token

_TIMEOUT = (2, 60)


def _headers() -> dict:
    return {"Authorization": f"Bearer {get_access_token()}"}


def _raise(r: requests.Response) -> None:
    if not r.ok:
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        typer.echo(f"Error {r.status_code}: {detail}", err=True)
        raise typer.Exit(1)


def get(path: str, **kwargs) -> requests.Response:
    r = requests.get(config.api_url(path), headers=_headers(), timeout=_TIMEOUT, **kwargs)
    _raise(r)
    return r


def post(path: str, **kwargs) -> requests.Response:
    r = requests.post(config.api_url(path), headers=_headers(), timeout=_TIMEOUT, **kwargs)
    _raise(r)
    return r


def patch(path: str, **kwargs) -> requests.Response:
    r = requests.patch(config.api_url(path), headers=_headers(), timeout=_TIMEOUT, **kwargs)
    _raise(r)
    return r


def put(path: str, **kwargs) -> requests.Response:
    r = requests.put(config.api_url(path), headers=_headers(), timeout=_TIMEOUT, **kwargs)
    _raise(r)
    return r


def delete(path: str, **kwargs) -> requests.Response:
    r = requests.delete(config.api_url(path), headers=_headers(), timeout=_TIMEOUT, **kwargs)
    _raise(r)
    return r
