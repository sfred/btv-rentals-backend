# settings.py
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

config = {
    "DATABASE_URL": os.getenv("DATABASE_URL"),
    "DATABASE_DEBUG": os.getenv("DATABASE_DEBUG") == 'true',
    "DEVELOPMENT_DATA_CACHE": os.getenv("DEVELOPMENT_DATA_CACHE") == 'true'
}
