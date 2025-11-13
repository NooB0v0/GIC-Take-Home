from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from uuid import UUID

class CreateEmployeeCommand(BaseModel):
    name: str = Field(min_length=6, max_length=10)
    email_address: EmailStr 
    phone_number: str = Field(min_length=8, max_length=8)
    gender: str

    assigned_cafe_id: Optional[UUID] = None

    @field_validator('phone_number')
    def validator_phone(cls, v):
        if not (v.startswith('8') or v.startswith('9')):
            raise ValueError('Phone number must start with 8 or 9')
        return v
    
    @field_validator('gender')
    def validator_gender(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female')
        return v