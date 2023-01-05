# 엔드포인트 작성하기

## 베이직 구현 

- `chp05_app_01_basic.py`
  - 기존에 구현된 Flask 코드의 스타일을 최대한 유지한 상태로 FastAPI로 구현함.

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


## 응용 구현 

- `chp05_app_02_applied.py`
  - `_basic.py` 의 코드를 FastAPI의 best practice 에 맞게 구현함.