from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = getenv('BOT_TOKEN')
    csv_database_path = "database/users.csv"

    token_capacity = 5000
    context_capacity = 5000
