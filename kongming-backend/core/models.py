
from pydantic import BaseModel
from typing import Dict, List, Optional


class SessionInfo(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int


class ChatRequest(BaseModel):
    question: str
    session_id: str = None


class RestoreSessionRequest(BaseModel):
    session_id: str
    history: List[Dict]


class UpdateSessionTitleRequest(BaseModel):
    session_id: str
    title: str
