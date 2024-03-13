from starlette import status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import login


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
