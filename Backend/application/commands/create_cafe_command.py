from pydantic import BaseModel, Field
from typing import Optional

class CreateCafeCommand(BaseModel):
    name: str = Field(min_length=6, max_length = 10)
    description: str = Field(max_length=256)
    logo: Optional[str] = None
    location: str = Field(min_length=1, max_length=200)