from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = 'Not authorized', headers: dict = None):
        if headers is None:
            headers = {'WWW-Authenticate': 'Bearer'}
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, 
                         detail=detail,
                         headers=headers
                         )

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = 'Forbidden'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
