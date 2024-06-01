import nullable as nullable
from db.db import Base
from sqlalchemy import Column, Integer, CHAR, String, Float


class GpsModel(Base):
    __tablename__ = "locations"

    id = Column('ID', Integer, nullable=False, primary_key=True, index=True)
    longitude = Column('longitude', Float, nullable=True)
    latitude = Column('latitude', Float, nullable=True)

    message = Column('message', String, nullable=True, default="Marker")
    group = Column('group', Integer, nullable=True, default=0)
