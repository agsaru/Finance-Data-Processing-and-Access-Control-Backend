from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models.user import User
from models.transaction import TransactionRecord
from config.database import create_db_and_tables
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.transaction import router as transaction_router
from routes.dashboard import router as dashboard_router

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

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(dashboard_router)
@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)