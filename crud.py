from sqlalchemy.orm import Session

import models
import schemas
import utils
import conf


def store_location_data(db: Session, data: schemas.InData):
    if get_num_vehicles(db) >= conf.MAX_NUMBER_OF_VEHICLES:
        raise utils.TooManyVehiclesException(f"{conf.MAX_NUMBER_OF_VEHICLES} vehicles already stored in database")
    db_data = models.LocationData(
        type_=data.t,
        timestamp=data.time,
        direction=data.hd,
        speed=data.sp,
        reference_id=data.refid,
        vehicle_id=data.vehicle_id,
        latitude=data.geo.lat,
        longitude=data.geo.lng,
        accuracy=data.geo.acc
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_num_vehicles(db: Session):
    num_vehicles = db.query(models.LocationData.vehicle_id).distinct().count()
    print(num_vehicles)
    return num_vehicles
