import os
from dotenv import load_dotenv


def show_token():
    token = os.getenv('DISCORD_BOT_TOKEN')
    print('Found token in environment variables:', token)


if __name__ == '__main__':
    load_dotenv()
    show_token()
