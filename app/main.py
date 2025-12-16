from fastapi import FastAPI
from app.api.v1 import auth
from app.database.base import Base
from app.database.session import engine

app = FastAPI(title="AI Assistant Backend")

app.include_router(auth.router)
