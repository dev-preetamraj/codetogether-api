import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from accounts.utils.github_provider import GithubProvider
from accounts.utils.token_manager import TokenManager
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger('accounts')

GITHUB_CLIENT_SECRET = '515e227943e8040263be01e49e495a8341cc80c8'
GITHUB_CLIENT_ID = '9d32be63c83194ffa4ed'

gh_provider = GithubProvider(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET
)
token_manager = TokenManager()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        gh_auth_token = data.get('code')
        gh_access_token = gh_provider.get_access_token(gh_auth_token)

        if gh_access_token is None:
            return Response({
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Please login again',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)

        gh_emails = gh_provider.get_emails(gh_access_token)
        gh_primary_email = gh_provider.get_primary_email(gh_emails)

        if gh_primary_email is None:
            return Response({
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Make sure email visibility is public on github',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)

        gh_user = gh_provider.get_user(gh_access_token)
        name_arr = gh_user.get('name').split(' ')
        first_name = name_arr[0] if len(name_arr) > 0 else None
        last_name = name_arr[1] if len(name_arr) > 1 else None

        db_user = User.objects.filter(email=gh_primary_email).first()

        if db_user is None:
            # Register user
            user = User(
                email=gh_primary_email,
                username=gh_user.get('login'),
                first_name=first_name,
                last_name=last_name,
                bio=gh_user.get('bio'),
                blog_url=gh_user.get('blog'),
                location=gh_user.get('location'),
            )
            if gh_user.get('avatar_url'):
                user.avatar_url = gh_user.get('avatar_url')
            user.set_password('random')
            user.save()

            # Generate Access & Refresh token
            access_token = token_manager.create_access_token(user.id)
            refresh_token = token_manager.create_refresh_token(user.id)
            return Response({
                'success': True,
                'status_code': status.HTTP_201_CREATED,
                'message': 'User registered and tokens generated',
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            }, status=status.HTTP_201_CREATED)

        try:
            user = User.objects.filter(email=gh_primary_email).first()
        except Exception as e:
            logger.error(f'LoginView - post: {e}')

        access_token = token_manager.create_access_token(user.id)
        refresh_token = token_manager.create_refresh_token(user.id)

        return Response({
            'success': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Tokens generated',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        }, status=status.HTTP_201_CREATED)
