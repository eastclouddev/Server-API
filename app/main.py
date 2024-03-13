from starlette import status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis import logout

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    return "OK"

# ルーターの読み込み
app.include_router(logout.router)
