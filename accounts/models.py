from django.db import models
from django.contrib.auth.models import AbstractUser


class CodetogetherUser(AbstractUser):
    avatar_url = models.CharField(
        max_length=150,
        default='https://res.cloudinary.com/dxgl4eyhq/image/upload/v1701036989/huddled/images/defaults/profile_ioi9ke.jpg'
    )
    bio = models.TextField()
    blog_url = models.CharField(max_length=100, null=True, blank=True)
    location = models.TextField()
