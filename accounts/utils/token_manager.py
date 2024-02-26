import logging
from datetime import datetime
from django.conf import settings
from jose import jwt, JWTError
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger('accounts')


class TokenManager:
    def __init__(self):
        pass

    @staticmethod
    def create_access_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow()
            + settings.JWT_SETTINGS.get('ACCESS_TOKEN_LIFETIME'),
            "iat": datetime.utcnow(),
        }

        access_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm="HS256")

        return access_token

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow()
            + settings.JWT_SETTINGS.get('REFRESH_TOKEN_LIFETIME'),
            "iat": datetime.utcnow(),
        }

        refresh_token = jwt.encode(
            payload, settings.REFRESH_SECRET_KEY, algorithm="HS256")

        return refresh_token

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str | None:
        try:
            payload = jwt.decode(
                refresh_token, key=settings.REFRESH_SECRET_KEY, algorithms=[
                    "HS256"]
            )
            user_id = payload.get("user_id")
            user = User.objects.filter(id=user_id).first()

            if not user:
                return None

            access_token = cls.create_access_token(user_id)
            return access_token

        except JWTError as jwt_err:
            logger.error(jwt_err)
            return None

        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def verify_access_token(access_token: str) -> bool:
        try:
            jwt.decode(access_token, key=settings.SECRET_KEY,
                       algorithms=["HS256"])
            return True
        except JWTError as jwt_err:
            logger.error(jwt_err)
            return False
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def verify_refresh_token(refresh_token: str) -> bool:
        try:
            jwt.decode(refresh_token, key=settings.REFRESH_SECRET_KEY,
                       algorithms=["HS256"])
            return True
        except JWTError as jwt_err:
            logger.error(jwt_err)
            return False
        except Exception as e:
            logger.error(e)
            return False
