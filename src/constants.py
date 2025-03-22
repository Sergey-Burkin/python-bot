import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
api_key = os.getenv('YOUTUBE_API_KEY')

lists = [['Матан', 'PL4_hYwCyhAvYePPocxGQv8RsOnYepxCPY'],
         ['Алгем', 'PL4_hYwCyhAvYmJi6xJFMsb1lpcZ5zZo93'],
         ['ОКТЧ', 'PL4_hYwCyhAvbGZOQrBtdahOGy4QydyTAB'],
         ['Матлог', 'PL4_hYwCyhAvYLl1VsA8JGQkrxg0Ll2D9J'],
         ['C++', 'PL4_hYwCyhAvaWsj3-0gLH_yEZfKdTife0'],
         ['Рухович', 'PL4_hYwCyhAvYljQ1BQj1wQayqn79LL-1k']]

number_photos = 3
