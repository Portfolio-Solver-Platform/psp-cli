import json
from psp.config import TOKEN_FILE, CONFIG_DIR


def save(access_token: str, refresh_token: str | None, access_expires_at: float, refresh_expires_at: float | None) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expires_at": access_expires_at,
        "refresh_token_expires_at": refresh_expires_at,
    }))


def load() -> dict | None:
    if not TOKEN_FILE.exists():
        return None
    return json.loads(TOKEN_FILE.read_text())


def clear() -> None:
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
