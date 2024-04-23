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
from authenticate import \
    authenticate_user, create_access_token, create_refresh_token, \
    find_user_by_id, get_current_user, Token, TokenData

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
    form_data: OAuth2PasswordRequestForm = Depends()
): # TODO:ログイン画面に応じてform_dataのスキーマが変更になる
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(db, user.user_id)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


# 認証の使い方サンプル
# 処理をまとめて関数化する
@app.get("/users/me/")
async def read_users_me(db: DbDependency,  token_data: TokenData = Depends(get_current_user)):
    if token_data.token_type == "refresh_token":
        access_token = create_access_token(token_data.user_id)
        refresh_token = create_refresh_token(db, token_data.user_id)

    user = find_user_by_id(db, token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
