from os import getenv


class Config:
    BOT_TOKEN = getenv('BOT_TOKEN')
    csv_database_path = "database/users.csv"

    token_capacity = 5000
    context_capacity = 5000
