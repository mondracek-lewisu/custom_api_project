import requests
from abc import ABC, abstractmethod

class APIBase(ABC):
    def __init__(self, base_url, params, timeout):
        self.__url = base_url
        self.__params = params
        self.__timeout = timeout

        self._message = None
        self._status = -1 # Assume the api fails

    def get_api(self):
        try:
            resp = requests.get(self.__url, 
                            params=self.__params,
                            timeout=self.__timeout)
        
            resp.raise_for_status()  # 400 and 500 errors - optional
            data = resp.json()
            if not data:
                raise LookupError("No data found")
        except requests.exceptions.RequestException as e:
            self._message = f"A Network/HTTP error occurred: {e}"
        except LookupError as e:
            self._message = e
        except ValueError:
            self._message = "The server response was not valid JSON"
        except Exception as e:
            self._message = f"An unknown error occurred: {e}"
        else:
            self._status = 0    
            return data
        
    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message
    
    @abstractmethod
    def call_api(self):
        pass

    @abstractmethod
    def __str__(self):
        pass