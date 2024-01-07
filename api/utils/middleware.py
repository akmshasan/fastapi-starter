import time

from fastapi import Request

from api.utils.logger import logger


async def log_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "process time": process_time,
        "client ip": request.client.host,
    }
    logger.info(log_dict, extra=log_dict)
    return response
