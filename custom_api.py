from abc_api_base import APIBase

BASE_URL = ""

class CustomAPI(APIBase):
    def __init__(self, params, timeout=10):
        super().__init__(BASE_URL, params, timeout)

    def call_api(self):
        self.__data = self.get_api()
            
    def __str__(self) -> str:
        data = self.__data