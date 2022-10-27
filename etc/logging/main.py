import os
import json
import uvicorn
from fastapi import FastAPI
# from starlette.requests import Request
from fastapi import Request
from loguru import logger
import logging
from util_logger import setup_logging
from module import say_hello_world
from fastapi.responses import JSONResponse
from pydantic import BaseModel

UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        # "uvicorn.error": {"level": "INFO"},
        # "uvicorn.access": {"level": "INFO", "propagate": False},
    },
}

# LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
LOG_LEVEL_STR = "INFO"
LOG_LEVEL = logging.getLevelName(LOG_LEVEL_STR)


app = FastAPI(title="Testing Uvicorn Logging Handlers")

#logging request body with middleware
@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    if request.query_params:
        body = None
        async for chunk in request.stream():
            if body is None:
                body = json.loads(chunk)
        logger.debug('Request body: {}'.format(body))
        logger.debug('Header: {}'.format(request.headers.items()))

    response = await call_next(request)
    return response


@app.get("/")
async def index():

    return JSONResponse(
        content={
            "msg" : "default processing"
        },
        status_code=200
    )

class ParamModel(BaseModel):
    param_int: int
    param_str: str

@app.post("/hello_world/")
async def hello_world(param: ParamModel):

    logger.info("From app: {} - {}".format(param.param_int, param.param_str))
    say_hello_world()
    return JSONResponse(
        content={
            "msg": "just said hello world"
        },
        status_code=200
    )


if __name__ == '__main__':

    setup_logging(log_level=LOG_LEVEL)

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8989,
        log_config=UVICORN_LOGGING_CONFIG,
        log_level=LOG_LEVEL,
        reload=False
    )