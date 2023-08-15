import inspect
import typing

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from notifiers import get_notifier

from app.config import settings


async def handle_exceptions(request: Request, call_next: typing.Callable):
    try:
        response = await call_next(request)
    except Exception as e:
        frame = inspect.trace()[-1]
        module_name = frame[1]
        function_name = frame[3]
        error_info = {
            "error": str(e),
            "module": module_name,
            "func": function_name,
            "line_number": frame[0].f_lineno,
            "endpoint": request.url.path,
            "method": request.method,
            "query_params": request.query_params,
            "path_params": request.path_params,
            "request_body": await request.body(),
        }
        logger.error(error_info)
        logger.exception(e)
        response = JSONResponse(
            content={"error": "Internal Server Error"}, status_code=500
        )
        telegram = get_notifier("telegram")
        telegram.notify(
            message=f"Произошла ошибка в приложении fastapi hotels!\n {error_info}",
            token=settings.TELEGRAM_TOKEN,
            chat_id=442077712,
        )
    return response
