import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.utils.github_provider import GithubProvider
from accounts.utils.token_manager import TokenManager
from codetogether.utils import custom_exceptions as ce

User = get_user_model()

logger = logging.getLogger("accounts")


gh_provider = GithubProvider(
    client_id=settings.GITHUB_CLIENT_ID, client_secret=settings.GITHUB_CLIENT_SECRET
)
token_manager = TokenManager()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            logger.info(data)
            gh_auth_token = data.get("code")
            gh_access_token = gh_provider.get_access_token(gh_auth_token)

            if gh_access_token is None:
                return Response(
                    {
                        "success": False,
                        "status_code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Please login again",
                        "data": None,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            gh_emails = gh_provider.get_emails(gh_access_token)
            gh_primary_email = gh_provider.get_primary_email(gh_emails)

            if gh_primary_email is None:
                return Response(
                    {
                        "success": False,
                        "status_code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Make sure email visibility is public on github",
                        "data": None,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            gh_user = gh_provider.get_user(gh_access_token)

            db_user = User.objects.filter(email=gh_primary_email).first()

            if db_user is None:
                # Register user
                name_arr = gh_user.get("name").split(" ")
                first_name = name_arr[0] if len(name_arr) > 0 else None
                last_name = name_arr[1] if len(name_arr) > 1 else None
                user = User(
                    email=gh_primary_email,
                    username=gh_user.get("login"),
                    bio=gh_user.get("bio"),
                    blog_url=gh_user.get("blog"),
                    location=gh_user.get("location"),
                )
                if gh_user.get("avatar_url"):
                    user.avatar_url = gh_user.get("avatar_url")

                if first_name is not None:
                    user.first_name = first_name

                if last_name is not None:
                    user.last_name = last_name

                user.set_password("random")
                user.save()

                # Generate Access & Refresh token
                access_token = token_manager.create_access_token(user.id)
                refresh_token = token_manager.create_refresh_token(user.id)
                return Response(
                    {
                        "success": True,
                        "status_code": status.HTTP_201_CREATED,
                        "message": "User registered and tokens generated",
                        "data": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )

            try:
                user = User.objects.filter(email=gh_primary_email).first()
            except Exception as e:
                logger.error(f"LoginView - post: {e}")

            access_token = token_manager.create_access_token(user.id)
            refresh_token = token_manager.create_refresh_token(user.id)

            return Response(
                {
                    "success": True,
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Tokens generated",
                    "data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"LoginView - post: {e}")
            raise ce.InternalServerError
