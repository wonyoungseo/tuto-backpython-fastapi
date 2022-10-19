How to run

```shell
$ uvicorn chp03_app:app
```

```shell
$ http -v GET http://localhost:8989/ping
GET /ping HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8989
User-Agent: HTTPie/3.2.1



HTTP/1.1 200 OK
content-length: 6
content-type: application/json
date: Wed, 19 Oct 2022 04:23:23 GMT
server: uvicorn

"pong"
```