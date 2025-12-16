# app/api/v1/assistant.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import ChatMessage
from app.core.ai_client import ask_assistant  # твой async HTTP клиент к AI

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/query")
async def query_assistant(query: str, session_id: str, history: list = None, user_id: int = 1, db: Session = Depends(get_db)):
    history = history or []

    # 1️⃣ Отправка запроса на AI
    try:
        ai_response = await ask_assistant(query=query, session_id=session_id, history=history)
    except Exception:
        ai_response = {
            "answer": "AI-ассистент временно недоступен. Попробуйте позже.",
            "sources": [],
            "tokens_used": 0,
            "category": "error"
        }

    # 2️⃣ Сохраняем сообщение пользователя
    db.add(ChatMessage(
        user_id=user_id,
        session_id=session_id,
        role="user",
        content=query
    ))

    # 3️⃣ Сохраняем сообщение ассистента
    db.add(ChatMessage(
        user_id=user_id,
        session_id=session_id,
        role="assistant",
        content=ai_response["answer"],
        tokens_used=ai_response.get("tokens_used", 0),
        category=ai_response.get("category")
    ))

    db.commit()

    return ai_response
