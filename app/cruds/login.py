from sqlalchemy.orm import Session
from datetime import datetime

from models.users import Users
from models.roles import Roles
from models.devices import Devices
from schemas.login import RequestBody


def find_by_user(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

def find_by_devices(db: Session, user_id: str):
    device =  db.query(Devices).filter(Devices.user_id == user_id).first()
    if not device:
        return None
    return device

def find_by_role(db: Session, user_role_id: str):
    return db.query(Roles).filter(Roles.id == user_role_id).first()

def create_device_info(db: Session,request: RequestBody,user_id: int):
    # info = dict(request)
    new_device = Devices(
        user_id = user_id,
        uuid = request.device_info.uuid,
        device_type = request.device_info.device_type,
        device_name = request.device_info.device_name,
        last_access = datetime.now()
    )
    db.add(new_device)
    return new_device