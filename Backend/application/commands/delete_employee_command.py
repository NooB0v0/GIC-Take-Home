from pydantic import BaseModel, Field

class DeleteEmployeeCommand(BaseModel):
    id: str = Field(min_length = 9, max_length = 9)