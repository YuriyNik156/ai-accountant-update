from pydantic import BaseModel
from typing import List, Optional

class HistoryItem(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    query: str
    session_id: str
    history: Optional[List[HistoryItem]] = []
