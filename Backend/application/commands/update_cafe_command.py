from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class UpdateCafeCommand(BaseModel):
    id: UUID
    name: Optional[str] = Field(default=None, min_length=6, max_length=10)
    description: Optional[str]
    logo: Optional[str] = None
    location: Optional[str]