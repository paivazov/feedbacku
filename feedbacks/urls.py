from django.urls import path

from feedbacks.views import FeedbackCreatingView, CurrentUserFeedbackListView

urlpatterns = (
    path("feedbacks/", FeedbackCreatingView.as_view(), name="create-feedback"),
    path(
        "feedbacks/users/<int:user_id>/",
        CurrentUserFeedbackListView.as_view(),
        name="feedback-list",
    ),
)
