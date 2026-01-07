import os

class BackendClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("BACKEND_URL")
        self.timeout = 10