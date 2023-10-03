from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person_id = Column(Integer)  # todo: relationship to persons table
    longitude = Column(String)
    latitude = Column(String)
    creation_time = Column(DateTime)
