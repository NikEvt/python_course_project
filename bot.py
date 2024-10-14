import asyncio
import logging
import sys
from json import JSONDecodeError
from os import getenv
from json import loads, dumps
import AI.gpt_api
import AI.openai_config
import utils
from config import Config
from database import users_df, create_new_user, check_user_registration
from AI.openai_config import OpenAIConfig

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


main_router = Router()
image_router = Router()
control_router = Router()

gpt_model = AI.gpt_api.GptAgent(OpenAIConfig.gpt_sufix, OpenAIConfig.gpt_prefix)

@main_router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    if user.id in users_df.index:
        await message.answer(f'Nice to see you {user.first_name}')
    else:
        create_new_user(user.id)
        await message.answer(f'Welcome {user.first_name}')

@main_router.message()
async def handle_main(message: Message):
    user = message.from_user
    message_text = message.text

    if not check_user_registration(user.id): return await message.answer("Register first!")

    try:
        context = loads(users_df.loc[user.id, 'context']) + [{'role': 'user', 'content': message_text}]
        text_response = gpt_model.get_response(message_text, context)
    except Exception as e:
        await message.answer("AI is not available, try again later...")
        return

    try:
        data = loads(text_response)
        for _, text_data in data.items():
            utils.process_context(text_data, message)
    except JSONDecodeError:
        return await message.answer("Something went wrong!")
    except Exception as e:
        return await message.answer("Something REALLY went wrong!")
