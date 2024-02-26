from django.urls import path
from accounts.api_views.login_view import LoginView
from accounts.api_views.profile_view import ProfileView
from accounts.api_views.tokens_view import VerifyTokenView, RefreshTokenView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('me', ProfileView.as_view(), name='profile'),
    path('token/verify', VerifyTokenView.as_view(), name='verify_token'),
    path('token/refresh', RefreshTokenView.as_view(), name='refresh_token'),
]
