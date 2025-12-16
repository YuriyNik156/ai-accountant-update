from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(String(255), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' или 'assistant'
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    category = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
