import json
import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ValidationError
from pydantic import BaseModel
from pydantic import validator
from sqlalchemy import create_engine
from sqlalchemy.sql import text

db_config = {
    'username': 'root',
    'password': '{YOUR_DB_PASSWORD}',
    'host': 'localhost',
    'port': 3306,
    'database': 'miniter'
}

app = FastAPI()
db_url = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}?charset=utf8".format(
    username=db_config['username'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    database=db_config['database']
)
db = create_engine(db_url, encoding='utf-8', max_overflow=0)
app.database = db


@app.get("/")
async def hello_world():
    return "Hello World"

@app.get("/ping")
async def ping():
    return "pong"


class NewUserInput(BaseModel): # (2)
    name: str
    email: str
    password: str
    profile: str


@app.post("/sign_up") # (3)
async def sign_up(new_user: NewUserInput):
    new_user = new_user.dict()
    new_user_id = app.database.execute(text(
        """
        INSERT INTO users(name, email, profile, hashed_password)
        VALUES(:name, :email, :profile, :password)
        """), new_user
    ).lastrowid

    row = app.database.execute(text("""
    SELECT id, name, email, profile 
    FROM users 
    WHERE id = :user_id 
    """), {'user_id': new_user_id}).fetchone()

    created_user = {
        'id' : row['id'],
        'name': row['name'],
        'email': row['email'],
        'profile': row['profile']
    } if row else None

    return JSONResponse(
        content = new_user,
        status_code = status.HTTP_201_CREATED
    )


