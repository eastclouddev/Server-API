from sqlalchemy.orm import Session
from models.user_rewards import UserRewards 


def find_by_mentor_id(db: Session, mentor_id: int):
    return db.query(UserRewards).filter(UserRewards.user_id == mentor_id).all()
