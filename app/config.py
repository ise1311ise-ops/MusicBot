import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN", "")
    sunoapi_key: str = os.getenv("SUNOAPI_KEY", "")
    sunoapi_base: str = os.getenv("SUNOAPI_BASE", "https://api.sunoapi.org")
    results_dir: str = os.getenv("RESULTS_DIR", "./results")
    public_base_url: str = os.getenv("PUBLIC_BASE_URL", "")

settings = Settings()

if not settings.bot_token:
    raise RuntimeError("BOT_TOKEN not set")
if not settings.sunoapi_key:
    raise RuntimeError("SUNOAPI_KEY not set")
