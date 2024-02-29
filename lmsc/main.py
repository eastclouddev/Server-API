from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# from db_connect import models, crud, database
# from db_connect.models import Base, ENGINE
import databases
import sqlalchemy
from pydantic import BaseModel

# models.Base.metadata.create_all(bind=models.ENGINE)
# Base.metadata.create_all(bind=ENGINE)
user_name = "user"
password = "lmsc"
container = "database"
database_name = "lmsc-db"
DATABASE_URL = f"mysql+pymysql://{user_name}:{password}@{container}/{database_name}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

test = sqlalchemy.Table(
    "test",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255)),
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestData(BaseModel):
    id: int
    name: str

async def get_database_connection():
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/tests/")
async def read_tests(connection: databases.Database=Depends(get_database_connection)):
    query = test.select()
    result = await connection.fetch_all(query)
    data = [TestData(id=row['id'], name=row['name']) for row in result]
    return {"message": f"{data[0]}"}

# @app.post("/users/")
# def create_user(name: str, db: Session = Depends(database.get_db)):
#     return crud.create_user(db=db, name=name)

# @app.get("/users/")
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

# @app.get("/users/{user_id}")
# def read_user(user_id: int, db: Session = Depends(database.get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user