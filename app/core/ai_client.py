import httpx
from typing import List, Dict

async def ask_assistant(query: str, session_id: str, history: List[Dict] = None, api_key: str = "your-api-key") -> Dict:
    async with httpx.AsyncClient(timeout=35.0) as client:
        response = await client.post(
            "http://146.103.101.95:8056/api/v1/assistant/query",
            headers={"X-API-Key": api_key},
            json={
                "query": query,
                "session_id": session_id,
                "history": history or []
            }
        )
        response.raise_for_status()
        return response.json()
