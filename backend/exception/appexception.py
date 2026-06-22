from .errorcode import Errorcode

class AppException(Exception):
    def __init__(self, err: Errorcode):
        self.code = err.code
        self.message = err.message