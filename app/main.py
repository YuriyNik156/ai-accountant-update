from fastapi import FastAPI
from app.api.v1 import auth
from app.database.base import Base
from app.database.session import engine

app = FastAPI(title="AI Assistant Backend")

# Создаем все таблицы, если их нет
Base.metadata.create_all(bind=engine)

# Роутеры
from app.api.v1.auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["auth"])
