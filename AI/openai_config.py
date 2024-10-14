class OpenAIConfig:
    gpt_sufix = "Use a required formay so that your answer can be parsed"
    gpt_prefix = ('Answer short and useful. Use json format '
                  '{"text": "your_answer",'
                  '"image": "your prompt for arised picture"}')

    gpt_model_name = "gpt-4o-mini"

    dalle_model = "dall-e-3"
    dalle_resolution = '1024x1024'

    dalle_prefix = ""
    dalle_sufix = ""
