from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DECIMAL,
    VARCHAR
)

import database


class LocationData(database.Base):
    """
    Database model
    """
    __tablename__ = "locationData"
    id_ = Column(Integer, name='id', primary_key=True, index=True)
    type_ = Column(String, name='type')
    timestamp = Column(BigInteger, nullable=False)
    direction = Column(DECIMAL, default=0.0)
    speed = Column(DECIMAL, default=0.0)
    reference_id = Column(VARCHAR, name='refId', index=True, nullable=False, unique=True)
    vehicle_id = Column(String, name='vehicleID', index=True, nullable=False)
    latitude = Column(DECIMAL, default=0.0)
    longitude = Column(DECIMAL, default=0.0)
    accuracy = Column(DECIMAL, default=0.0)
