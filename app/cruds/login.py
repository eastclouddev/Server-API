from sqlalchemy.orm import Session
from models.users import Users
from models.roles import Roles
from models.devices import Devices


def find_by_user(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

def find_by_devices(db: Session, user_id: str):
    return db.query(Devices).filter(Devices.user_id == user_id).first()

def find_by_role(db: Session, user_role_id: str):
    return db.query(Roles).filter(Roles.id == user_role_id).first()

