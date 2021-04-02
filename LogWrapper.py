LOGURU_ENABLE = True
# Optional dependencies: loguru
# if you want to disable logging, set LOGURU_ENABLE = False


if LOGURU_ENABLE:
    from loguru import logger



def logDebug(text:str):
    if LOGURU_ENABLE:
        logger.debug(text)

def logInfo(text:str):
    if LOGURU_ENABLE:
        logger.info(text)

def logWarning(text:str):
    if LOGURU_ENABLE:
        logger.warning(text)

def logError(text:str):
    if LOGURU_ENABLE:
        logger.error(text)   

if LOGURU_ENABLE:
    logger.add("/home/dom/loguru.log")