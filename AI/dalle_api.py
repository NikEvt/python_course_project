from sys import prefix

from AI.AI_API_template import AiApiTemplate
from openai import OpenAI
from dotenv import load_dotenv

from AI.openai_config import OpenAIConfig

load_dotenv()
client = OpenAI()


class DalleAgent(AiApiTemplate):
    def __init__(self, sufix, prefix):
        super().__init__(sufix, prefix)
        self.client = OpenAI()

    def get_response(self, prompt: str) -> str:
        img_response = client.images.generate(
            model=OpenAIConfig.dalle_model,
            prompt=self.prefix + prompt + self.sufix,
            quality="standard",
            n=1,
            size=OpenAIConfig.dalle_resolution,
        )
        image_link = img_response.data[0].url
        return image_link
