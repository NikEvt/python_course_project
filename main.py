import asyncio

from aiogram import Bot, Dispatcher
import logging

from bot import image_router, main_router, control_router
from config import Config
from database import users_df

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(Config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(image_router)
    dp.include_router(main_router)
    dp.include_router(control_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        users_df.to_csv(Config.csv_database_path)
        logging.info("users_df has been saved successfully.")

if __name__ == '__main__':
    asyncio.run(main())
