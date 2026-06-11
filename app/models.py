from pydantic import BaseModel
from typing import Any, Optional

class GameEvent(BaseModel):
    event_type: str
    user_id: str
    payload: Optional[dict[str, Any]] = {}
