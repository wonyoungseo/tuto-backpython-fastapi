How to run

```shell
$ uvicorn chp05_app:app
```

Add users

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

get list of signed users

```shell
$ http GET http://localhost:8989/user_list                          
HTTP/1.1 200 OK
content-length: 166
content-type: application/json
date: Thu, 20 Oct 2022 05:06:52 GMT
server: uvicorn

{
    "1": {
        "email": "kim@world.com",
        "idx": 1,
        "username": "kim"
    },
    "2": {
        "email": "den@world.com",
        "idx": 2,
        "username": "den"
    }
}
```