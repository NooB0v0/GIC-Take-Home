from pydantic import BaseModel, Field
from typing import Optional

class GetEmployeesQuery(BaseModel):
    cafe_name: Optional[str] = Field(default=None)