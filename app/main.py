import uvicorn

from fastapi import FastAPI
from app.api.v1.endpoints import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "i`m alive\n go to http://localhost:8000/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000)

