from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['date_joined', 'groups', 'is_active', 'is_staff',
                   'is_superuser', 'last_login', 'password', 'user_permissions']
