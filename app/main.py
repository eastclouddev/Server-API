from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from apis import \
    login, logout, password_reset, news, state_progresses, \
    students, mentors, reviews, companies, users, \
    courses, curriculums, questions, billings, receipts, \
    rewards, progresses


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