from datetime import datetime, date
from pydantic import BaseModel, Field


class LocationIngest(BaseModel):
    person_id: int = Field(examples=[123])
    longitude: float = Field(examples=[123.456])
    latitude: float = Field(examples=[123.456])
    creation_time: datetime = Field(examples=["2023-10-03T07:06:08.210215"])

    class Config:
        from_attributes = True  # orm mode


class LocationRetrieve(BaseModel):
    id: int = Field(examples=[123])
    person_id: int = Field(examples=[123])
    longitude: float = Field(examples=[123.456])
    latitude: float = Field(examples=[123.456])
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


class ConnectionRequest(BaseModel):
    person_id: int = Field(examples=[123])
    start_date: date = Field(examples=["2023-10-03"])
    end_date: date = Field(examples=["2023-10-03"])
    meters: float = Field(examples=[5.0])


class Connection(BaseModel):
    person: Person
    location: LocationRetrieve

    class Config:
        from_attributes = True  # orm mode