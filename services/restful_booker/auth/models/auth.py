from typing import Optional

from pydantic import BaseModel

class AuthResponse(BaseModel):
    token: Optional[str] = None
    reason: Optional[str] = 'Bad credentials'
