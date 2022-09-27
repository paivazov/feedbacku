from django.contrib import admin

from feedbacks.models import Feedback, UserLastFeedbackInfo

admin.site.register(Feedback)
admin.site.register(UserLastFeedbackInfo)
