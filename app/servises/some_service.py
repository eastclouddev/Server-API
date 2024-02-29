from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.some_model import User
from app.database.some_database import SessionLocal
from app.schemas.some_schema import UserCreate, UserUpdate

class UserService:
    def __init__(self, db):
        self.db = SessionLocal()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=user_create.password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            return None
        for field, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id=user_id)
        print(user.name)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

