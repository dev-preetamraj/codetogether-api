import logging

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer

User = get_user_model()

logger = logging.getLogger("accounts")


class ProfileView(APIView):

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)

        return Response(
            {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "User profile fetched",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
