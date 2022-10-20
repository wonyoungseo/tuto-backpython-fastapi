from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse # (1)
from pydantic import BaseModel


app = FastAPI()

@app.get("/ping")
async def ping():
    return "pong"

app.APP_USERS: dict = {}
app.INDEX_COUNT: int = 1


class NewUserInput(BaseModel): # (2)
    username: str
    email: str


@app.post("/sign_up") # (3)
async def sign_up(new_user: NewUserInput):

    new_user = new_user.dict()
    new_user["idx"]=app.INDEX_COUNT
    app.APP_USERS[new_user["idx"]] =new_user
    app.INDEX_COUNT += 1

    return JSONResponse(
        content = new_user,
        status_code= 200
    )

@app.get("/user_list") # (4)
async def return_user():
    return JSONResponse(
        content=app.APP_USERS,
        status_code=200
    )


# (1): JSONResponse - dict을 json으로 변환하여 http 응답으로 보낼 수 있음
# (2): Pydantic 데이터모델 - Http request를 통해 전달되는 데이터가 사전에 정의된 형태에 부합하는지 확인할 수 있음
# (3): 엔드포인트 sign_up - 유저명과 이메일을 입력하여 회원가입하는 엔드포인트
# (4): 엔드포인트 회원 리스트 출력 - Sign up을 통해 추가된 리스트 GET 메소드