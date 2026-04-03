import time
import webbrowser
import requests
from psp.auth.core import Auth


def run(auth: Auth, scope: str) -> tuple[str, str | None, float, float | None]:
    endpoints = auth.endpoints()
    device_info = requests.post(
        endpoints["device_authorization_endpoint"],
        data=auth.client_data() | {"scope": scope},
        timeout=(2, 10),
    ).json()

    complete_uri = device_info.get("verification_uri_complete")
    if complete_uri:
        print("Opening browser for login...")
        webbrowser.open(complete_uri)
        print(f"If it didn't open: {complete_uri}")
    else:
        print(f"Go to: {device_info['verification_uri']}")
        print(f"Enter code: {device_info['user_code']}")

    interval = device_info.get("interval", 5)
    while True:
        time.sleep(interval)
        r = requests.post(
            endpoints["token_endpoint"],
            data=auth.client_data() | {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_info["device_code"],
            },
            timeout=(2, 10),
        )
        if r.status_code == 200:
            data = r.json()
            access_token = data["access_token"]
            access_expires_at = float(auth.decode_token(access_token).claims["exp"])
            refresh_expires_at = (
                time.time() + data["refresh_expires_in"]
                if "refresh_expires_in" in data
                else None
            )
            return access_token, data.get("refresh_token"), access_expires_at, refresh_expires_at

        err = r.json().get("error") if r.status_code == 400 else None
        if err == "slow_down":
            interval += 5
        elif err not in ("authorization_pending", "slow_down"):
            raise RuntimeError(f"Auth error: {err or r.status_code}")
