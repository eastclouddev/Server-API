from sqlalchemy.orm import Session

from models.users import Users
from models.roles import Roles
from models.devices import Devices


def find_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

def find_device_by_user_id(db: Session, user_id: str):
    return db.query(Devices).filter(Devices.user_id == user_id).first()

def find_role_by_role_id(db: Session, role_id: int):
    return db.query(Roles).filter(Roles.id == role_id).first()