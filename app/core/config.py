from dotenv import load_dotenv
import os

load_dotenv()

# AI
AI_BASE_URL = os.getenv("AI_BASE_URL")
AI_API_KEY = os.getenv("AI_API_KEY")
AI_TIMEOUT = float(os.getenv("AI_TIMEOUT", 35.0))

# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

if not AI_BASE_URL or not AI_API_KEY:
    raise RuntimeError("AI_BASE_URL или AI_API_KEY не заданы в окружении")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY не задан в окружении")
