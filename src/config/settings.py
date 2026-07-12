import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

DATABASE_PATH = "src/database/scheduler.db"