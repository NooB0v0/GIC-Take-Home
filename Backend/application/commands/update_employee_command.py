from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from uuid import UUID

class UpdateEmployeeCommand(BaseModel):
    id: str = Field(min_length=9, max_length=9)

    name: Optional[str] = Field(default=None, min_length=6, max_length=10)
    email_address: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, min_length=8, max_length=8)
    gender: Optional[str] = None
    
    assigned_cafe_id: Optional[UUID] = None 

    @field_validator('phone_number')
    def validate_sg_phone(cls, v):
        if v is not None and not (v.startswith('8') or v.startswith('9')):
            raise ValueError('Phone number must start with 8 or 9.')
        return v
        
    @field_validator('gender')
    def validate_gender(cls, v):
        if v is not None and v not in ['Male', 'Female']:
            raise ValueError('Gender must be Male or Female.')
        return v