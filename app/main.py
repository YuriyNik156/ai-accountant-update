from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import assistant
from app.api.v1.auth import router as auth_router
from app.database.base import Base
from app.database.session import engine

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

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

# --- HTML страницы ---

@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/login")
def login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/registration")
def registration():
    return FileResponse(os.path.join(FRONTEND_DIR, "registration.html"))

# --- Static files ---
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# --- API ---
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(assistant.router, prefix="/api/v1", tags=["assistant"])

# --- DB ---
Base.metadata.create_all(bind=engine)

