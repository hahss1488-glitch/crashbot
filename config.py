import os
from dotenv import load_dotenv

load_dotenv()

# Bothost автоматически подставляет эти переменные
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
