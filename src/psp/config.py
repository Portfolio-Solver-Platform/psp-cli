import tomllib
import tomli_w
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "psp"
CONFIG_FILE = CONFIG_DIR / "config.toml"
TOKEN_FILE = CONFIG_DIR / "tokens.json"

DEFAULTS: dict = {
    "base_url": "http://local",
    "client_id": "third-party-app",
    "client_secret": "",
    "scope": (
        "solver-director:projects:read solver-director:projects:write "
        "solver-director:problems:read solver-director:problems:write "
        "solver-director:groups:read solver-director:groups:write "
        "solver-director:solvers:read solver-director:solvers:write "
        "solver-director:resources:read solver-director:resources:write"
    ),
}


def load() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        return dict(DEFAULTS)
    with open(CONFIG_FILE, "rb") as f:
        data = tomllib.load(f)
    return DEFAULTS | data


def save(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(data, f)


def api_url(path: str) -> str:
    return load()["base_url"].rstrip("/") + "/api/solverdirector/v1" + path


def oidc_metadata_url() -> str:
    return load()["base_url"].rstrip("/") + "/api/user/v1/.well-known/openid-configuration"
