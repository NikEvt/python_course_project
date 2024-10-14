from AI.AI_API_template import AiApiTemplate
from openai import OpenAI
from dotenv import load_dotenv

from AI.openai_config import OpenAIConfig

load_dotenv()
client = OpenAI()

class GptAgent(AiApiTemplate):
    def __init__(self, sufix, prefix):
        super().__init__(sufix, prefix)
        self.client = OpenAI()

    def get_response(self,
                     prompt: str,
                     context: list) -> str:
        response = self.client.chat.completions.create(
            model=OpenAIConfig.gpt_model_name,
            messages=context + [
                {'role': 'system', 'content': self.prefix},
                {'role': 'user', 'content': prompt},
                {'role': 'system', 'content': self.sufix}
            ]
        )
        return response

