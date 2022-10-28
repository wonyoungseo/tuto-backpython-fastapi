from loguru import logger
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from modules.module import say_hello_world

router = APIRouter()

class ParamModel(BaseModel):
    param_int: int
    param_str: str

@router.post("/hello_world/")
async def hello_world(param: ParamModel):

    logger.info("From app: {} - {}".format(param.param_int, param.param_str))
    say_hello_world()
    return JSONResponse(
        content={
            "msg": "just said hello world"
        },
        status_code=200
    )