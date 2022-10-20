from fastapi import FastAPI

app = FastAPI() # (1)

@app.get("/ping") # (2)
async def ping():
    return "pong"

# (1) FastAPI 클래스를 객체화
# (2) 데코레이터를 통해 함수를 엔드포인트에 등록.
