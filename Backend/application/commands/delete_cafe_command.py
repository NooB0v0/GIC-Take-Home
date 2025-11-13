from pydantic import BaseModel
from uuid import UUID

class DeleteCafeCommand(BaseModel):
    id: UUID