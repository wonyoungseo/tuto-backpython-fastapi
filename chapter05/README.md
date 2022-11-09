## basic

- 기존 Flask 코드의 스타일을 최대한 유지한 상태로 FastAPI로 구현함. 

### 실행

```shell
uvicorn chp05_app_01_basic:app --port=9292
```

### 엔드포인트에 리퀘스트 날리기

미리 작성해둔 `send_request_basic.sh` 을 실행하며 API가 작동하는 것을 확인할 수 있음

```shell
bash ./send_request_basic.sh
```

### 유저별 트윗 타임라인 출력하기

```shell
http -v GET "http://localhost:9292/timeline" user_id=1
```