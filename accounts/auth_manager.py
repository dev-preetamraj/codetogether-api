import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from jose import jwt, JWTError
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from codetogether.utils import custom_exceptions as ce

User = get_user_model()


logger = logging.getLogger("accounts")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.headers.get("Authorization")

            if auth_header is None:
                return None

            access_token = auth_header.split(" ")[1]
            payload = jwt.decode(
                access_token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )

            user_id = payload.get("user_id")

            user = User.objects.filter(id=user_id).first()
            if user is None:
                raise exceptions.NotFound(detail="User not found")

            return user, None
        except JWTError:
            raise ce.JWTError
