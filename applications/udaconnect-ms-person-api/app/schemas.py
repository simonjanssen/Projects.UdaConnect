from datetime import datetime
from pydantic import BaseModel, Field


class Person(BaseModel):
    id: int = Field(examples=[123])
    first_name: str = Field(examples=["Thomas"])
    last_name: str = Field(examples=["Mueller"])
    company_name: str = Field(examples=["FC Bayern"])

    class Config:
        from_attributes = True  # orm mode
