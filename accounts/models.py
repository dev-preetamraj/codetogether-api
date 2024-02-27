import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class CodetogetherUser(AbstractUser):
    avatar_url = models.CharField(
        max_length=150,
        default="https://res.cloudinary.com/dxgl4eyhq/image/upload/v1701036989/huddled/images/defaults/profile_ioi9ke"
        ".jpg",
    )
    bio = models.TextField()
    blog_url = models.CharField(max_length=100, null=True, blank=True)
    location = models.TextField()


class SubscriptionType(models.Model):
    SUBSCRIPTION_TYPE_CHOICE = (
        ("Free", "Free"),
        ("Pro", "Pro"),
        ("Premium", "Premium"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=7, choices=SUBSCRIPTION_TYPE_CHOICE)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    submissions_per_day = models.IntegerField(default=10)
    autocompletion_enabled = models.BooleanField(default=False)
    cloud_savings_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user: CodetogetherUser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription"
    )
    subscription_type = models.ForeignKey("SubscriptionType", on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s subscription"


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user: CodetogetherUser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submission"
    )
    submission_counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s submission"
