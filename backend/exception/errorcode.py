from enum import Enum

class Errorcode(Enum):
    LOGIN_FAILED = (2000, "Tên đăng nhập hoặc mật khẩu không chính xác")
    UNAUTHORIZED = (2001, "Bạn không có quyền truy cập")
    USER_NOT_FOUND = (3001, "Không tìm thấy người dùng")
    INVALID_PASSWORD = (3002, "Mật khẩu không chính xác")
    USER_ALREADY_BLOCKED = (3003, "Người dùng đã bị khóa")
    USER_BLOCKED = (3002, "Tài khoản đã bị khóa")
    TOKEN_INVALID = (4001, "Token không hợp lệ")
    TOKEN_EXPIRED = (4001, "Token đã hết hạn")
    REFRESH_TOKEN_INVALID = (4003, "Refresh token không hợp lệ")
    MESSAGE_NOT_FOUND = (5001, "Không tìm thấy tin nhắn")
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message