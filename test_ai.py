import asyncio
from app.api.v1.assistant import query_assistant
from app.schemas.user import QueryRequest
from app.database.session import SessionLocal  # импорт твоего get_db
from sqlalchemy.orm import Session


async def test_ai():
    request = QueryRequest(
        query="Что ты умеешь?",
        session_id="test_session_001",
        history=[]
    )

    # создаем реальную сессию
    db: Session = SessionLocal()

    try:
        response = await query_assistant(request=request, user_id=1, db=db)
        print(response)
    finally:
        db.close()  # не забываем закрыть сессию


asyncio.run(test_ai())
