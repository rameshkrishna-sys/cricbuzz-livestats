import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)

class Config:

    try:
        RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    except:
        RAPIDAPI_KEY = os.getenv("API_KEY")

    RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT", 3306))