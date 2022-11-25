import json
import uvicorn
from fastapi import FastAPI
from fastapi import Request, Depends
from starlette.types import Message
from loguru import logger
import logging

from util_logger import setup_logging

from routers.router_default import router as router_1
from routers.router_hello_world import router as router_2
from DSutils.file_utils import yaml_reader

UVICORN_LOGGING_CONFIG = yaml_reader("./logger_config.yaml", verbose=False)
API_LOG_LEVEL_STR = "INFO"
UVICORN_LOG_LEVEL = "CRITICAL"
API_LOG_LEVEL = logging.getLevelName(API_LOG_LEVEL_STR)
UVICORN_LOG_LEVEL = logging.getLevelName(UVICORN_LOG_LEVEL)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}
    request._receive = receive

async def middleware_logging(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")

    if str(request.method) in ['POST', 'PUT', 'PATCH']:
        body = await request.body()
        await set_body(request, body)

        request_body = json.loads(body)
        logging.info("Request Body :")
        for k in request_body:
            logging.info({k: request_body[k]})

    response = await call_next(request)

    return response

app = FastAPI(title="Testing Uvicorn Logging Handlers")
app.middleware("http")(middleware_logging)

app.include_router(router_1)
app.include_router(router_2)


if __name__ == '__main__':

    setup_logging(log_level=API_LOG_LEVEL)

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8989,
        log_config=UVICORN_LOGGING_CONFIG,
        log_level=UVICORN_LOG_LEVEL,
        reload=False
    )