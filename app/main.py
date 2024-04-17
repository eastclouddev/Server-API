from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

from apis import \
    login, logout, password_reset, news, state_progresses, \
    students, mentors, reviews, companies, users, \
    courses, curriculums, questions, billings, receipts, \
    rewards, progresses
from authenticate import authenticate_user
from authenticate import create_access_token
from authenticate import create_refresh_token
from authenticate import get_user_id
from authenticate import get_current_user
from authenticate import Token

DbDependency = Annotated[Session, Depends(get_db)]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# for Health heck
@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    return "OK"

# ルーターの読み込み
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(password_reset.router)
app.include_router(news.router)
app.include_router(state_progresses.router)
app.include_router(students.router)
app.include_router(mentors.router)
app.include_router(reviews.router)
app.include_router(companies.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(curriculums.router)
app.include_router(questions.router)
app.include_router(billings.router)
app.include_router(receipts.router)
app.include_router(rewards.router)
app.include_router(progresses.router)

@app.post("/token")
async def login_for_access_token(
    db: DbDependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):                                   # uesrnameにemailを入れる
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(db, data=user    )
    refresh_token = create_refresh_token(db, data=user)
    return Token(access_token=access_token,refresh_token = refresh_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(db: DbDependency,  token_info= Depends(get_current_user)):
    current_user_payload, token = token_info
    token_type: str = current_user_payload["token_type"]
    user_id: int = current_user_payload["user_id"]
    #リフレッシュトークンの場合、アクセストークンを発行
    if token_type == "refresh_token":
        refresh_token = token
        user = {"user_id": user_id}
        access_token = create_access_token(db, data=user)

    user = get_user_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@app.get("/users/me/items/")
async def read_own_items(db: DbDependency, current_user = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]