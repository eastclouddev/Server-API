from sqlalchemy.orm import Session
import jwt

from models.devices import Devices
from models.access_token import AccessToken

def analysis_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, key='SECRET_KEY123', algorithms='HS256')
    if not decoded_jwt:
        return None
    user_id = decoded_jwt.get('user_id')
    return user_id

def find_device_info(db: Session, user_id: int):
    device = db.query(Devices).filter(Devices.user_id == user_id).first()
    if not device:
        return None
    return device

def delete(db: Session, user_id: int):
    device_info = find_device_info(db, user_id)
    if not device_info:
        return None
    db.delete(device_info)
    return device_info

def find_refresh_token(db: Session, user_id: int):
    return db.query(AccessToken).filter(AccessToken.user_id == user_id).first()

def delete_refresh_token(db: Session, user_id: int):
    found_token = find_refresh_token(db, user_id)
    if not found_token:
        return None
    db.delete(found_token)
    return found_token