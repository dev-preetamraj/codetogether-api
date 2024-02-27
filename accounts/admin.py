from django.contrib import admin
from accounts.models import CodetogetherUser, SubscriptionType, Subscription, Submission

# Register your models here.
admin.site.register(CodetogetherUser)
admin.site.register(SubscriptionType)
admin.site.register(Subscription)
admin.site.register(Submission)
