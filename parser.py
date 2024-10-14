from json import loads
from json import JSONDecodeError

class Parser:
    def __init__(self, text_api_response):
        try:
            data = loads(text_api_response)
            self._data = data
        except JSONDecodeError:
            raise Exception(message="Invalid json string")
        except Exception as e:
            raise Exception(message=f"Unknown exceprtion: {e}")

    def get_data(self) -> dict:
        return self._data
