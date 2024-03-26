from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends,Request 
from models.users import Users
from models.roles import Roles

def find_by_user(db: Session, user_id: int = Path(gt=0)):
    return db.query(Users).filter(Users.id == user_id).first()

def find_by_role(db: Session, role_id: int = Path(gt=0)):
    return db.query(Roles).filter(Roles.id == role_id).first()
