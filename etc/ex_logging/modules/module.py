from loguru import logger

def say_hello_world():
    logger.info("from loguru - Saying hello world")
    logger.info("from loguru - Hello World")


if __name__ == "__main__":
    logger.add("logs/app.log")
    say_hello_world()