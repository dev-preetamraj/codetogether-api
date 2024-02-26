from rest_framework import status
from rest_framework.exceptions import APIException


class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Something went wrong'
    default_code = 'internal_server_error'


class JWTError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is invalid or expired'
    default_code = 'jwt_error'
