## basic

- 기존 Flask 코드의 스타일을 최대한 유지한 상태로 FastAPI로 구현함. 

### 실행

```shell
$ uvicorn chp05_app_01_basic:app
```

### 회원가입

- Query Parameter를 통해 전달

```shell
$ http POST http://localhost:8989/sign_up username=kim email=kim@world.com
HTTP/1.1 200 OK
content-length: 50
content-type: application/json
date: Thu, 20 Oct 2022 05:03:16 GMT
server: uvicorn

{
    "email": "kim@world.com",
    "idx": 1,
    "username": "kim"
}
```

### 가입된 회원 리스트 출력

```shell
http POST http://localhost:8989/sign_up username=den email=den@world.com
HTTP/1.1 200 OK
content-length: 50
content-type: application/json
date: Thu, 20 Oct 2022 05:03:57 GMT
server: uvicorn

{
    "email": "den@world.com",
    "idx": 2,
    "username": "den"
}
```

트윗 작성

- 존재하지 않는 user_idx로 작성 시, 에러 메세지 발생

```shell
http POST http://localhost:8989/tweet user_index=99 tweet="Hello World"
HTTP/1.1 400 Bad Request
content-length: 28
content-type: application/json
date: Fri, 21 Oct 2022 07:12:34 GMT
server: uvicorn

{
    "msg": "user id not exists"
}
```

- 트윗 작성

```shell
http POST http://localhost:8989/tweet user_index=1 tweet="Hello World"
HTTP/1.1 200 OK
content-length: 29
content-type: application/json
date: Fri, 21 Oct 2022 07:14:16 GMT
server: uvicorn

{
    "input_tweet": "Hello World"
}
```