import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def ping():
    return "pong"


if __name__ == "__main__":

    uvicorn.run(
        app="app:main_app",
        host="127.0.0.1",
        port=8989
    )