from loguru import logger
from util_logger import setup_logging

# LOG_LEVEL_STR = "INFO"
# LOG_LEVEL = logging.getLevelName(LOG_LEVEL_STR)
# setup_logging(LOG_LEVEL)

def say_hello_world():
    logger.info("from loguru - Saying hello world")
    logger.info("from loguru - Hello World")
    # print("from print - Saying hello world")
    # print("from print - Hello World")
    # print("from print - success !!")



if __name__ == "__main__":
    logger.add("logs/app.log")
    say_hello_world()