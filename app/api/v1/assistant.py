import httpx
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from sqlalchemy.orm import Session

from app.core.config import AI_BASE_URL, AI_API_KEY, AI_TIMEOUT
from app.database.session import get_db
from app.database.models import ChatMessage
from app.schemas.user import QueryRequest

router = APIRouter(prefix="/assistant", tags=["assistant"])

async def ask_assistant(query: str, session_id: str, history: list = None):
    """Отправка запроса к AI-сервису"""
    async with httpx.AsyncClient(timeout=AI_TIMEOUT) as client:
        try:
            response = await client.post(
                f"{AI_BASE_URL}/assistant/query",
                headers={"X-API-Key": AI_API_KEY},
                json={
                    "query": query,
                    "session_id": session_id,
                    "history": history or []
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            # fallback, если AI недоступен
            return {
                "answer": "AI-ассистент временно недоступен. Попробуйте позже.",
                "sources": [],
                "tokens_used": 0,
                "category": "error"
            }

@router.post("/query")
async def query_assistant(
    request: QueryRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id

    # 1️⃣ Отправляем запрос на AI
    ai_response = await ask_assistant(
        query=request.query,
        session_id=request.session_id,
        history=request.history
    )

    # 2️⃣ Сохраняем сообщение пользователя
    db.add(ChatMessage(
        user_id=user_id,
        session_id=request.session_id,
        role="user",
        content=request.query
    ))

    # 3️⃣ Сохраняем сообщение ассистента
    db.add(ChatMessage(
        user_id=user_id,
        session_id=request.session_id,
        role="assistant",
        content=ai_response["answer"],
        tokens_used=ai_response.get("tokens_used", 0),
        category=ai_response.get("category")
    ))

    db.commit()

    return ai_response
