from fastapi import FastAPI
from app.api.v1 import assistant, auth
from app.database.base import Base
from app.database.session import engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router

app = FastAPI(title="AI Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем все таблицы, если их нет
Base.metadata.create_all(bind=engine)

# Роутеры
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(assistant.router, prefix="/api/v1", tags=["assistant"])