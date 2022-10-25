import json
import datetime
from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse # (1)
from fastapi import status
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def hello_world():
    return "Hello World"

@app.get("/ping")
async def ping():
    return "pong"

app.APP_USERS: dict = {}
app.USER_INDEX: int = 1
app.TWEET: List[dict] = []


#### Endpoint: Sign up

class NewUserInput(BaseModel): # (2)
    username: str
    email: str


@app.post("/sign_up") # (3)
async def sign_up(new_user: NewUserInput):

    new_user = new_user.dict()
    new_user["idx"]=app.USER_INDEX
    app.APP_USERS[new_user["idx"]] =new_user
    app.USER_INDEX += 1

    return JSONResponse(
        content = new_user,
        status_code = status.HTTP_201_CREATED
    )


#### Endpoint: Tweet

class TweetInput(BaseModel):
    user_index: int
    tweet: str

@app.post("/tweet")
async def tweet(tweet_input: TweetInput):

    user_idx = tweet_input.user_index
    tweet = tweet_input.tweet

    ### (5)
    if user_idx not in app.APP_USERS:
        return JSONResponse(
            content={"msg": "user id not exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if len(tweet) > 100:
        return JSONResponse(
            content={"msg": "tweet message exceeds 100 characters"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    app.TWEET.append(
        {'idx': user_idx,
         'tweet': tweet,
         'datetime': datetime.datetime.now()}
    )

    return JSONResponse(
        content={"input_tweet": tweet},
        status_code=status.HTTP_200_OK
    )

#### Endpoint: Follow

class FollowRequest(BaseModel):

    user_index_follow_from: int
    user_index_follow_to: int

class SetEncoder(json.JSONEncoder): # (7)
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

@app.post("/follow")
async def follow(follow_request: FollowRequest):

    user_idx_from = follow_request.user_index_follow_from
    user_idx_to = follow_request.user_index_follow_to

    if (user_idx_from not in app.APP_USERS) or (user_idx_to not in app.APP_USERS):
        return JSONResponse(
            content={"msg": "user id not exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user = app.APP_USERS[user_idx_from]
    user.setdefault('following', set()).add(user_idx_to)

    return JSONResponse(
        content=json.loads(json.dumps(user, cls=SetEncoder)),
        status_code=status.HTTP_200_OK
    )



# (1): JSONResponse - dict을 json으로 변환하여 http 응답으로 보낼 수 있음
# (2): Pydantic 데이터모델 - Http request를 통해 전달되는 데이터가 사전에 정의된 형태(타입)에 부합하는지 확인할 수 있음
# (3): 엔드포인트 sign_up - 유저명과 이메일을 입력하여 Sign up 하는 엔드포인트.
# (4): 엔드포인트 user_list - Sign up된 리스트 GET 메소드
# (5): 데이터 validation - tweet 엔드포인트에 전달하는 데이터의 검증을 pydantic.validator를 통해 검증.
# (6): 엔드포인트 follow
# (7): SetEncoder - `Object type set is not JSON serializable` 에러를 해결하기 위한 클래스
