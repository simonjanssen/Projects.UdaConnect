from datetime import datetime
from pydantic import BaseModel, Field


class LocationIngest(BaseModel):
    person_id: int = Field(examples=[123])
    longitude: str = Field(examples=["123.456"])
    latitude: str = Field(examples=["123.456"])
    creation_time: datetime = Field(examples=["2023-10-03T07:06:08.210215"])

    class Config:
        from_attributes = True  # orm mode


class LocationRetrieve(BaseModel):
    id: int = Field(examples=[123])
    person_id: int = Field(examples=[123])
    longitude: str = Field(examples=["123.456"])
    latitude: str = Field(examples=["123.456"])
    creation_time: datetime = Field(examples=["2023-10-03T07:06:08.210215"])

    class Config:
        from_attributes = True  # orm mode
