import pandas as pd
from config import Config
import os



def create_csv_db() -> pd.DataFrame:
    if not os.path.exists(Config.csv_database_path):
        users = pd.DataFrame(
            columns=[
                'user_id',
                'token_capacity',
                'token_usage',
                'context_capacity',
                'context_usage',
                'context'
            ]
        )
        users.set_index('user_id', inplace=True)
    else:
        users = pd.read_csv(Config.csv_database_path, index_col=0)
    return users

users_df = create_csv_db()

def create_new_user(user_id: int) -> pd.DataFrame:
    global users_df
    users_df.loc[user_id] = [Config.token_capacity, 0, Config.context_capacity, 0, '[]']
    return users_df

def check_user_registration(user_id: int) -> pd.DataFrame:
    global users_df
    return user_id in users_df.index


