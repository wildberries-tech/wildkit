from typing import Any

import requests


class Client:
    def __init__(self, token: str):
        assert isinstance(token, str) and token != "", "No API token provided"

        self._client = requests.Session()
        self._client.headers.update({"Authorization": token})
        self._url = "https://suppliers-api.wildberries.ru"
        self._timeout_sec = 15.0

    def get(self, path: str,  **kwargs) -> Any:
        return self._invoke("get", path, **kwargs)

    def post(self, path: str,  **kwargs) -> Any:
        return self._invoke("post", path, **kwargs)

    def _invoke(self, method: str, path: str,  **kwargs) -> Any:
        r: requests.Response = getattr(self._client, method)(self._url + path, timeout=self._timeout_sec, **kwargs)

        if r.status_code != 200:
            raise Exception(f"Status {r.status_code} for {r.url}. Body: {r.text}")

        ct = r.headers.get("Content-Type")
        if ct != "application/json":
            raise Exception(f"Expected application/json content-type for {r.url}, got '{ct}'")

        # All Content methods return JSON body
        j = r.json()
        if j.get("error", False):
            raise Exception(f'Error for {r.url}: {j.get("errorText", "")}. {j.get("additionalErrors", "")}')

        return j
