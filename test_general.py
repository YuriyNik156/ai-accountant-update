import asyncio
import httpx
from app.database.session import SessionLocal
from app.database.models import ChatMessage

# -------------------------------
# 1️⃣ Авторизация
# -------------------------------
async def get_access_token(email: str, password: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/auth/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Авторизация успешна. Access token получен.\n")
        return data["access_token"]

# -------------------------------
# 2️⃣ Запрос к ИИ через backend
# -------------------------------
async def query_ai(token: str, query: str, session_id: str, history: list):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "session_id": session_id,
        "history": history
    }

    async with httpx.AsyncClient(timeout=35.0) as client:
        response = await client.post(
            "http://127.0.0.1:8000/api/v1/assistant/query",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print("✅ Запрос к ИИ выполнен.\n")
        print("💡 Ответ ассистента:\n")
        print(data["answer"])
        print("\n📊 Источники:")
        for src in data.get("sources", []):
            doc = src.get("document")
            article = src.get("article")
            clause = src.get("clause")
            print(f"- {doc}, статья {article}, пункт {clause}")
        print(f"\n💰 Tokens used: {data.get('tokens_used')}, category: {data.get('category')}\n")
        return data

# -------------------------------
# 3️⃣ Проверка истории в БД
# -------------------------------
def print_history(session_id: str):
    db = SessionLocal()
    try:
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
        print("📝 История сообщений для сессии", session_id)
        print("-" * 50)
        for msg in messages:
            print(f"[{msg.role}] {msg.content} (tokens: {msg.tokens_used}, category: {msg.category}, created_at: {msg.created_at})")
        print("-" * 50 + "\n")
    finally:
        db.close()

# -------------------------------
# 4️⃣ Главная функция
# -------------------------------
async def main():
    session_id = "test_session_001"
    email = "test1"
    password = "1231"

    # предыдущие сообщения для истории
    history = [
        {"role": "user", "content": "Как долго хранится кредитная история?"},
        {"role": "assistant", "content": "7 лет..."}
    ]

    token = await get_access_token(email, password)
    await query_ai(token, "А в архиве сколько?", session_id, history)
    print_history(session_id)

if __name__ == "__main__":
    asyncio.run(main())
