# Optional dependencies: loguru
# if you want to disable logging, set LOGURU_ENABLE = False

LOGURU_ENABLE = True


if LOGURU_ENABLE:
    from loguru import logger


def LogDebug(text:str):
    if LOGURU_ENABLE:
        logger.debug(text)
    else:
        print(text)

def LogInfo(text:str):
    if LOGURU_ENABLE:
        logger.info(text)
    else:
        print(text)

def LogWarning(text:str):
    if LOGURU_ENABLE:
        logger.warning(text)
    else:
        print(text)

def LogError(text:str):
    if LOGURU_ENABLE:
        logger.error(text)  
    else:
        print(text)