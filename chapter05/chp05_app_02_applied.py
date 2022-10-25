# FastAPI applied ver.
# applied followings;
# - error exception handling

import json
import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ValidationError
from pydantic import BaseModel
from pydantic import validator


app = FastAPI()

app.APP_USERS: dict = {}
app.USER_INDEX: int = 1
app.TWEET: List[dict] = []


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):

    json.loads(exc.json())
    response = {"msg": []}

    for error in json.loads(exc.json()):
        response["msg"].append("{loc}: {msg}".format(loc=error['loc'][-1],
                                                     msg=error['msg']))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response
    )

@app.get("/")
async def hello_world():
    return "Hello World"

@app.get("/ping")
async def ping():
    return "pong"


class NewUserInput(BaseModel): # (2)
    username: str
    email: str

    @validator("username")
    def username_must_unique(cls, v):
        username_ls = [app.APP_USERS[k]['username'] for k in app.APP_USERS.keys()]
        if v in username_ls:
            raise ValueError("Duplicated username")
        return v

    @validator("email")
    def email_must_unique(cls, v):
        email_ls = [app.APP_USERS[k]['email'] for k in app.APP_USERS.keys()]
        if v in email_ls:
            raise ValueError("Duplicated email address")
        return v


@app.post("/sign_up") # (3)
async def sign_up(new_user: NewUserInput):

    new_user = new_user.dict()
    new_user["idx"]=app.USER_INDEX
    app.APP_USERS[new_user["idx"]] = new_user
    app.USER_INDEX += 1

    return JSONResponse(
        content = new_user,
        status_code= status.HTTP_200_OK
    )

@app.get("/user_list") # (4)
async def get_user_list():
    return JSONResponse(
        content=app.APP_USERS,
        status_code=status.HTTP_200_OK
    )

class TweetInput(BaseModel):
    user_index: int
    tweet: str

    @validator("user_index")
    def user_index_check(cls, v):
        if v not in app.APP_USERS.keys():
            raise ValueError("User does not exist")
        return v

    @validator("tweet")
    def tweet_length(cls, v):
        if len(v) > 300:
            raise ValueError("Tweet message exceeds 300 characters")
        return v


@app.post("/tweet/new_tweet")
async def new_tweet(tweet_input: TweetInput):

    user_idx = tweet_input.user_index
    tweet = tweet_input.tweet

    app.TWEET.append({
        'idx': user_idx,
        'tweet': tweet,
        'datetime': str(datetime.datetime.now())
    })

    return JSONResponse(
        content={"input_tweet": tweet},
        status_code=status.HTTP_200_OK
    )

@app.get("/tweet/data")
async def get_tweet_list():
    return JSONResponse(
        content = {
            "output": app.TWEET
        },
        status_code= status.HTTP_200_OK
    )

if __name__ == "__main__":
    uvicorn.run(app="chp05_app_02_applied:app",
                host="0.0.0.0",
                port=8989,
                log_level='info',
                access_log=True,
                use_colors=True,
                reload=False)