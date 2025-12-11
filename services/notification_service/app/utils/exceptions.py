from typing import Any, Dict, Union
from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, detail: Union[str, Dict[str, Any]], **kwargs: Dict[str, Any]):
        super().__init__(status_code=self.STATUS_CODE, detail=detail, **kwargs)


class BadRequest(CustomHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
