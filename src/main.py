from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models.user_model import User
from models.financial_rec_model import FinancialRecord
from database import create_db_and_tables
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Database connected")


@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)