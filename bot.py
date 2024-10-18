from json import loads

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import users_df, create_new_user, check_user_registration
from AI.openai_config import OpenAIConfig

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from AI import dalle_api, gpt_api

from aiogram.types import (
    Message
)

from parser import Parser

main_router = Router()
image_router = Router()
control_router = Router()

gpt_model = gpt_api.GptAgent(OpenAIConfig.gpt_sufix, OpenAIConfig.gpt_prefix)
dalle_model = dalle_api.DalleAgent(OpenAIConfig.dalle_sufix, OpenAIConfig.dalle_prefix)
improve_prompt_model = gpt_api.GptAgent("Improve and expand if it is too shortimage generation prompt.Make it no longer than 100 characters Original prompt:\n",
                                        "\nSave the context of the original prompt. Make sure that yourr answer only contains prompt.")


class States(StatesGroup):
    image: State = State()
    main: State = State()
    generate_image: State = State()


@main_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = message.from_user
    await state.set_state(States.main)
    if user.id in users_df.index:
        await message.answer(f'Nice to see you {user.first_name}')
    else:
        create_new_user(user.id)
        print(users_df)
        await message.answer(f'Welcome, {user.first_name}!')


@image_router.message(Command("image"))
async def image(message: Message, state: FSMContext):
    await message.answer("Type your prompt!")
    await state.set_state(States.image)


@image_router.message(States.image)
async def image(message: Message, state: FSMContext):
    await state.set_state(States.generate_image)
    user_prompt = message.text
    builder = ReplyKeyboardBuilder()
    builder.button(text=user_prompt)
    for i in range(0, 3):
        improved_prompt = improve_prompt_model.get_response(user_prompt, context = []).choices[0].message.content
        builder.button(text=improved_prompt)
    builder.adjust(1, 1, 1, 1)
    await message.answer("Choose best description of your desired photo: ", reply_markup=builder.as_markup(one_time_keyboard=True, resize_keyboard=True))


@image_router.message(States.generate_image)
async def image(message: Message, state: FSMContext):
    final_prompt = message.text
    try:
        link = dalle_model.get_response(final_prompt)
        await message.answer_photo(link)
        await state.clear()
    except Exception as e:
        await state.set_state(States.main)
        return await message.answer(f"Something went wrong...{e}")


@main_router.message(States.main)
async def handle_main(message: Message):
    user = message.from_user
    message_text = message.text

    if not check_user_registration(user.id): return await message.answer("Register first!")

    try:
        context = loads(users_df.loc[user.id, 'context']) + [{'role': 'user', 'content': message_text}]
        response = gpt_model.get_response(message_text, context)
    except Exception as e:
        return await message.answer(f"AI is not available, try again later...{e}")

    text_response = response.choices[0].message.content
    print(text_response)
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
        return await message.answer(f"Something went wrong...{e}")
