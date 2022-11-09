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
app.USER_ID: int = 1
app.TWEET: List[dict] = []


#### Endpoint: Sign up

class NewUserInput(BaseModel): # (2)
    username: str
    email: str


@app.post("/sign_up") # (3)
async def sign_up(new_user: NewUserInput):

    new_user = new_user.dict()
    new_user["user_id"]=app.USER_ID
    app.APP_USERS[new_user["user_id"]] =new_user
    app.USER_ID += 1

    return JSONResponse(
        content = new_user,
        status_code = status.HTTP_201_CREATED
    )


#### Endpoint: Tweet

class TweetInput(BaseModel):
    user_id: int
    tweet: str

@app.post("/tweet")
async def tweet(tweet_input: TweetInput):

    user_id = tweet_input.user_id
    tweet = tweet_input.tweet

    ### (5)
    if user_id not in app.APP_USERS:
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
        {'user_id': user_id,
         'tweet': tweet,
         'datetime': str(datetime.datetime.now())}
    )

    return JSONResponse(
        content={"input_tweet": tweet},
        status_code=status.HTTP_200_OK
    )

#### Endpoint: Follow & Unfollow

class FollowRequest(BaseModel):

    user_id_follow_origin: int
    user_id_follow_target: int

class SetEncoder(json.JSONEncoder): # (7)
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

@app.post("/follow")
async def follow(follow_request: FollowRequest):

    user_id_origin = follow_request.user_id_follow_origin
    user_id_target = follow_request.user_id_follow_target

    if user_id_origin == user_id_target:
        return JSONResponse(
            content={"msg": "intend to follow oneself"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if (user_id_origin not in app.APP_USERS) or (user_id_target not in app.APP_USERS):
        return JSONResponse(
            content={"msg": "user id not exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user = app.APP_USERS[user_id_origin]
    user.setdefault('following', set()).add(user_id_target)

    return JSONResponse(
        content=json.loads(json.dumps(user, cls=SetEncoder)),
        status_code=status.HTTP_200_OK
    )

class UnfollowRequest(BaseModel):

    user_id_unfollow_origin: int
    user_id_unfollow_target: int

@app.post("/unfollow")
async def unfollow(unfollow_request: UnfollowRequest):

    user_id_origin = unfollow_request.user_id_unfollow_origin
    user_id_target = unfollow_request.user_id_unfollow_target

    if user_id_origin == user_id_target:
        return JSONResponse(
            content={"msg": "intend to unfollow oneself"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if (user_id_origin not in app.APP_USERS) or (user_id_target not in app.APP_USERS):
        return JSONResponse(
            content={"msg": "user id not exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user = app.APP_USERS[user_id_origin]
    user.setdefault("following", set()).discard(user_id_target)

    return JSONResponse(
        content=json.loads(json.dumps(user, cls=SetEncoder)),
        status_code=status.HTTP_200_OK
    )

#### Endpoint: Timeline

class UserID(BaseModel):
    user_id: int

@app.get("/timeline/") # (8)
async def timeline(user_id: UserID):
    uid = user_id.user_id
    if uid not in app.APP_USERS:
        return JSONResponse(
            content={"msg": "user not exist"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_list = app.APP_USERS[uid].get("following", set())
    user_list.add(uid)

    timeline = [t for t in app.TWEET if t['user_id'] in user_list]

    return JSONResponse(
        content = {
            "user_id": uid,
            "timeline": timeline
        },
        status_code=200
    )



# (1): JSONResponse - dict을 json으로 변환하여 http 응답으로 보낼 수 있음
# (2): Pydantic 데이터모델 - Http request를 통해 전달되는 데이터가 사전에 정의된 형태(타입)에 부합하는지 확인할 수 있음
# (3): 엔드포인트 sign_up - 유저명과 이메일을 입력하여 Sign up 하는 엔드포인트.
# (4): 엔드포인트 user_list - Sign up된 리스트 GET 메소드
# (5): 데이터 validation - tweet 엔드포인트에 전달하는 데이터의 검증을 pydantic.validator를 통해 검증.
# (6): SetEncoder - `Object type set is not JSON serializable` 에러를 해결하기 위한 클래스
# (7): 엔드포인트 follow / unfollow - 다른 유저를 팔로우하거나 언팔로우
# (8): 엔드포인트 timeline - 타겟 유저와 팔로우 하는 유저의 트윗을 출력
