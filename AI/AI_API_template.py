
class AiApiTemplate:
    def __init__(self,
                 sufix: str = None,
                 prefix: str = None):
        self.sufix = sufix
        self.prefix = prefix

    def get_response(self, prompt: str):
        pass
