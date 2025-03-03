from fastapi import FastAPI

from src.routers.users import router as user_router

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"status": "OK"}


app.include_router(user_router)
