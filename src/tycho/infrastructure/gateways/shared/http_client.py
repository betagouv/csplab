import requests

from domain.services.http_client_interface import IHttpClient


class SyncHttpClient(IHttpClient):
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, url, **kwargs)
