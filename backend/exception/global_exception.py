from fastapi import FastAPI, Request
from exception import Errorcode, AppException
from dto.response import ApiResponse
from fastapi.responses import JSONResponse
def GlobalException(app: FastAPI):
    @app.exception_handler(AppException)
    def handleAppException(request: Request, exception: AppException):
        res = ApiResponse(code=exception.code, message=exception.message)
        return JSONResponse(content=res.model_dump(exclude_none=True))