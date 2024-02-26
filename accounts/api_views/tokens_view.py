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
token_manager = TokenManager()


class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        if token_manager.verify_access_token(access_token):
            return Response({
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Access token verified',
                'data': None
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Access token is expired or invalid',
            'data': None
        }, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not token_manager.verify_refresh_token(refresh_token):
            return Response({
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Refresh token is expired or invalid',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)

        access_token = token_manager.refresh_access_token(refresh_token)
        if access_token is None:
            return Response({
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Refresh token is expired or invalid',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Access token refreshed',
            'data': {
                'access_token': access_token
            }
        }, status=status.HTTP_200_OK)
