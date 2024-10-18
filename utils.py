from aiogram.types import Message
from json import  dumps, loads
import pandas as pd

def process_context(response,
                    message: Message):
    user = message.from_user
    text_response = response.choices[0].message.content
    users = pd.read_csv('users.csv', index_col=0)

    context = loads(users.loc[user.id, 'context']) + [{'role': 'user', 'content': message.text}]

    context_len = users.loc[user.id, 'context_usage']
    context_capacity = users.loc[user.id, 'context_capacity']

    context = context + [{'role': 'assistant', 'content': text_response}]
    context_len += len(text_response)

    while context_len > context_capacity:
        context_len -= len(context[0]['content'])
        context = context[1:]

    users.loc[user.id, 'token_usage'] += response['usage']['total_tokens']
    users.loc[user.id, 'context_usage'] += context_len
    users.loc[user.id, 'context'] = dumps(context)
