from functools import wraps
import traceback
from typing import Callable, Generic, TypeVar

from fastapi.responses import Response as FastAPIResponse, JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class FailureDetails(BaseModel):
    reason: str


class Response(BaseModel):
    success: bool


class ResponseWithData(Response, Generic[T]):
    data: T


def success_with_data(data: T) -> Response:
    return ResponseWithData(data=data, success=True)


def failure_with_reason(reason: str) -> Response:
    return ResponseWithData(data=FailureDetails(reason=reason), success=False)


def json_on_success(func: Callable[..., BaseModel]):
    @wraps(func)
    def handle(*args, **kwargs):
        result = func(*args, **kwargs)
        content = result.dict() if hasattr(result, "dict") else {"data": {}}
        return JSONResponse(status_code=200, content=content)

    return handle


def default_exception_handling(func: Callable[..., FastAPIResponse]):
    @wraps(func)
    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return JSONResponse(
                status_code=400, content=failure_with_reason(str(e)).dict()
            )

    return handle
