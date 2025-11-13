from pydantic import BaseModel, Field
from typing import Optional

class GetCafeQuery(BaseModel):
    location: Optional[str] = Field(default=None)