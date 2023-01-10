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


class NewUserInput(BaseModel):
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


class TweetInput(BaseModel):
    user_id: int
    tweet: str

@app.post("/tweet")
async def tweet(tweet_input: TweetInput):

    tweet = tweet_input.dict()

    if len(tweet) > 100:
        return JSONResponse(
            content={"msg": "tweet message exceeds 100 characters"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    app.database.execute(text(
        """
        INSERT INTO tweets (user_id, tweet)
        VALUES (:user_id, :tweet)
        """), tweet)

    return JSONResponse(
        content={"input_tweet": tweet},
        status_code=status.HTTP_200_OK
    )


class FollowRequest(BaseModel):

    user_id_origin: int
    user_id_target: int

class SetEncoder(json.JSONEncoder): # (7)
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

@app.post("/follow")
async def follow(follow_request: FollowRequest):

    follow_request = follow_request.dict()

    if follow_request['user_id_origin'] == follow_request['user_id_target']:
        return JSONResponse(
            content={"msg": "user cannot follow oneself"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    app.database.execute(text("""
    INSERT INTO users_follow_list (user_id, follow_user_id) 
    VALUES (:user_id_origin, :user_id_target)
    """), follow_request)

    return JSONResponse(
        content='{} following {}'.format(follow_request['user_id_origin'],
                                         follow_request['user_id_target']),
        status_code=status.HTTP_200_OK
    )

class UnfollowRequest(BaseModel):

    user_id_origin: int
    user_id_target: int

@app.post("/unfollow")
async def unfollow(unfollow_request: UnfollowRequest):

    unfollow_request = unfollow_request.dict()

    if unfollow_request['user_id_origin'] == unfollow_request['user_id_target']:
        return JSONResponse(
            content={"msg": "user cannot unfollow oneself"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    app.database.execute(text("""
    DELETE FROM users_follow_list
    WHERE user_id = :user_id_origin AND
          follow_user_id = :user_id_target
    """), unfollow_request)

    return JSONResponse(
        content='{} unfollowed {}'.format(unfollow_request['user_id_origin'],
                                          unfollow_request['user_id_target']),
        status_code=status.HTTP_200_OK
    )


class UserID(BaseModel):
    user_id: int

@app.get("/timeline/")
async def timeline(user_id: UserID):
    uid = user_id.user_id

    rows = app.database.execute(text("""
    SELECT
        t.user_id,
        t.tweet
    FROM tweets as t
    LEFT JOIN users_follow_list as ufl ON ufl.user_id = :user_id
    WHERE t.user_id = :user_id OR 
          t.user_id = ufl.follow_user_id
    """), {"user_id": uid}).fetchall()

    timeline = [
        {
            'user_id': row['user_id'],
            'tweet': row['tweet']
        } for row in rows
    ]

    return JSONResponse(
        content={"timeline": timeline},
        status_code=status.HTTP_200_OK
    )