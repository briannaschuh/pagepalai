from dotenv import load_dotenv
from pathlib import Path
import os

# load .env from the root of the project
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# database variables
DATABASE_URL_LOCAL = os.getenv("DATABASE_URL_LOCAL")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL_PROD = os.getenv("DATABASE_URL_PROD")

USE_REMOTE_DB = os.getenv("USE_REMOTE_DB", "False").lower() == "true" 

DATABASE_URL = DATABASE_URL_PROD if USE_REMOTE_DB else DATABASE_URL_LOCAL # uses db based on whether this is local or deployed

# openAI
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDINGS = os.getenv("OPENAI_EMBEDDINGS", "text-embedding-3-small")

#pagepal
PAGEPAL_API_KEY = os.getenv("PAGEPAL_API_KEY")