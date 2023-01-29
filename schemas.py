from typing import Union

from pydantic import BaseModel


class GeoData(BaseModel):
    lat: float  # Latitude
    lng: float  # Longitude
    acc: int  # Accuracy Level


class InData(BaseModel):
    t: str  # Type of data
    time: int  # Timestamp in milliseconds
    hd: float  # Direction
    sp: float  # Speed
    refid: str  # Reference ID
    vehicle_id: str  # Vehicle ID
    geo: GeoData  # Geo data


class BaseData(BaseModel):
    type_: str
    direction: float
    speed: float
    reference_id: str
    vehicle_id: str
    latitude: float
    longitude: float
    accuracy: float


class Data(BaseData):
    id_: int
    timestamp: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class TokenInData(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str


class TokenPayload(BaseModel):
    sub: str
    exp: int
