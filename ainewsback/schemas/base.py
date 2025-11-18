from typing import Any, Generic, TypeVar, Union

from pydantic import BaseModel

T = TypeVar('T')


class BaseResponseModel(BaseModel, Generic[T]):
    host: int | None = None
    code: int
    errorMessage: str | None = None
    data: T | None = None

def resp(code: int, data: Union[list, dict, str, Any] = None,
             message: str = 'success') -> BaseResponseModel:
    return BaseResponseModel(code=code, errorMessage=message, data=data)

def resp_200(data: Union[list, dict, str, Any] = None,
             message: str = 'success') -> BaseResponseModel:
    return BaseResponseModel(code=200, errorMessage=message, data=data)


def resp_500(data: Union[list, dict, str, Any] = None,
             message: str = 'error') -> BaseResponseModel:
    return BaseResponseModel(code=500, errorMessage=message, data=data)
