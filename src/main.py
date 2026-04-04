from fastapi import FastAPI
import uvicorn
from database import create_db_and_tables
app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Database connected")


@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)