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


class Person(BaseModel):
    id: int = Field(examples=[123])
    first_name: str = Field(examples=["Thomas"])
    last_name: str = Field(examples=["Mueller"])
    company_name: str = Field(examples=["FC Bayern"])

    class Config:
        from_attributes = True  # orm mode


class Connection(BaseModel):
    person: Person
    location: LocationRetrieve

    class Config:
        from_attributes = True  # orm mode