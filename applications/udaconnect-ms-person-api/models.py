from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Date, func, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True,)
    first_name = Column(String)
    last_name = Column(String)
    company_name = Column(String)
    registration_time = Column(DateTime, server_default=func.now())


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey(Person.id))
    longitude = Column(Float)
    latitude = Column(Float)
    creation_time = Column(DateTime)


class Exposure(Base):
    __tablename__ = "exposures"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_a = Column(Integer, ForeignKey(Person.id)) 
    person_b = Column(Integer, ForeignKey(Person.id))
    location_a = Column(Integer, ForeignKey(Location.id))
    location_b = Column(Integer, ForeignKey(Location.id))
    date_exposed = Column(Date)
    min_distance = Column(Float)

    __table_args__ = (
        UniqueConstraint("person_a", "person_b", "date_exposed"), 
        CheckConstraint("person_a != person_b"), 
        CheckConstraint("location_a != location_b")
    )