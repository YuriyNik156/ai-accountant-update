from sqlalchemy.orm import Session
from app.database.session import engine  # твой SQLAlchemy engine
from app.database.models import ChatMessage

def check_history(session_id: str):
    with Session(engine) as db:
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
        if not messages:
            print(f"История для session_id='{session_id}' пустая")
            return
        for msg in messages:
            print(f"[{msg.role}] {msg.content} (tokens: {msg.tokens_used}, category: {msg.category}, created_at: {msg.created_at})")

if __name__ == "__main__":
    check_history("test_session_001")
