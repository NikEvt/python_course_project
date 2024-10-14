from json import loads
from database import users_df, create_new_user, check_user_registration
from AI.openai_config import OpenAIConfig

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from AI import dalle_api, gpt_api

from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
)

from parser import Parser

main_router = Router()
image_router = Router()
control_router = Router()

gpt_model = gpt_api.GptAgent(OpenAIConfig.gpt_sufix, OpenAIConfig.gpt_prefix)
dalle_model = dalle_api.DalleAgent(OpenAIConfig.dalle_sufix, OpenAIConfig.dalle_prefix)
improve_prompt_model = gpt_api.GptAgent("Improve image generation prompt. Original prompt:\n",
                                        "\nSave the context of the original prompt.")


class States(StatesGroup):
    image: State = State()
    generate_image: State = State()


@main_router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    if user.id in users_df.index:
        await message.answer(f'Nice to see you {user.first_name}')
    else:
        create_new_user(user.id)
        await message.answer(f'Welcome {user.first_name}')


@image_router.message(Command("image"))
async def image(message: Message, state: FSMContext):
    await message.answer("Type your prompt!")
    await state.set_state(image)


@image_router.message(States.image)
async def image(message: Message, state: FSMContext):
    user_prompt = message.text
    keyboard = [[user_prompt]]
    for i in range(0, 3):
        keyboard[0].append(improve_prompt_model.get_response(user_prompt))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await state.set_state(States.generate_image)
    await message.answer("Choose best description of your desired photo: ", reply_markup=reply_markup)


@image_router.message(States.generate_image)
async def image(message: Message, state: FSMContext):
    final_prompt = message.text
    try:
        link = dalle_model.get_response(final_prompt)
        await message.answer_photo(link)
        await state.clear()
    except Exception as e:
        await state.clear()
        return await message.answer("Something went wrong...")


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
        parsed_response = Parser(text_response).get_data()
        for key, value in parsed_response.items():
            if key == "image":
                improve_prompt_model.get_response(value, context=[])
                image_link = dalle_model.get_response(value)
                await message.answer_photo(image_link)
            else:
                await message.answer(value)
    except Exception as e:
        return await message.answer("Something went wrong...")
