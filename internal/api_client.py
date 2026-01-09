import os
import time
import httpx
from helper.prettier import Prettier
from helper.utils import Utils

class BackendClient():
    def __init__(self, prettier: Prettier, utils: Utils) -> None:
        self.base_url = os.getenv("BACKEND_URL")
        self.timeout = 10
        self.prettier = prettier
        self.utils = utils
        self.headers = {"JWT_TOKEN": os.getenv("BACKEND_JWT_TOKEN")}

    def search(self, query:str, filter:str, limit:int) -> list[str]:
        url = self.base_url + "/api/search"
        index_list = self.utils.get_index_list()

        payload = {
            "Index": index_list,
            "Query": query,
            "Filter": filter,
            "Limit": limit,
        }

        start_time = round(time.time() * 1000)
        response = httpx.post(url=url, headers=self.headers, json=payload)
        end_time = round(time.time() * 1000)
        elapsed_time = f"{(end_time - start_time):.2f}ms"

        if response.status_code == 200:
            data = response.json()
            hits = data["data"]
            if hits != None:
                message_list = []
                for hit in hits:
                    message = self.prettier.yaml_prettier(data=hit, time=elapsed_time)
                    message_list.append(message)
                return message_list
        return ""