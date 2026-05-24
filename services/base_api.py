import requests


class BaseAPI:
    """Базовый класс для работы с API."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.token_header = None
