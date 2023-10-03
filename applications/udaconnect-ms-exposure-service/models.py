from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Date
from sqlalchemy.orm import relationship

from .database import Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True,)
    first_name = Column(String)
    last_name = Column(String)
    company_name = Column(String)
    registration_time = Column(DateTime)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    longitude = Column(Float)
    latitude = Column(Float)
    creation_time = Column(DateTime)


class Exposure(Base):
    __tablename__ = "exposures"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_a = Column(Integer, ForeignKey("persons.id")) 
    person_b = Column(Integer, ForeignKey("persons.id"))
    location_a = Column(Integer, ForeignKey("locations.id"))
    location_b = Column(Integer, ForeignKey("locations.id"))
    date_exposed = Column(Date)
    min_distance = Column(Float)
