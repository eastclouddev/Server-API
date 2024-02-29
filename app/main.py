from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.some_endpoint import router as api_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

app.include_router(api_router)

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
