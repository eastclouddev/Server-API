from sqlalchemy.orm import Session
from models.companies import Companies

from logging import getLogger

logger = getLogger("uvicorn.app")

def find_companies(db:Session):
    return db.query(Companies).all()