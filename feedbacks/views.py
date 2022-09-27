from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from feedbacks.permissions import IsManagerOrRecipient
from feedbacks.serializers import (
    FeedbackCreatingSerializer,
    UserFeedbackSerializer,
    UserInfoFeedbackSerializer,
)
from feedbacks.services import (
    get_filtered_feedbacks,
    make_senders_anonymous,
    get_object_or_none,
)
from feedbacks.models import UserLastFeedbackInfo


class FeedbackCreatingView(CreateAPIView):
    """Creates new feedback"""

    serializer_class = FeedbackCreatingSerializer
    permission_classes = (IsAuthenticated,)

    # OrganisationInvitingView has the same method
    def get_serializer_context(self):
        context = super(FeedbackCreatingView, self).get_serializer_context()
        context.update(
            {"organisation_id": self.kwargs.get("pk"), "request": self.request}
        )
        return context


class CurrentUserFeedbackListView(APIView):
    """Shows all feedbacks of definite user in definite organisation"""

    permission_classes = (IsAuthenticated, IsManagerOrRecipient)

    def get(self, request, pk, user_id):
        queryset = get_filtered_feedbacks(pk, user_id)
        if not queryset:
            return Response(
                {"detail": "Feedbacks hasn't been found."},
                status=HTTP_404_NOT_FOUND,
            )
        self.check_object_permissions(request, queryset.first())
        make_senders_anonymous(queryset)
        feedbacks = UserFeedbackSerializer(queryset, many=True).data
        recipient_info = UserInfoFeedbackSerializer(
            get_object_or_none(
                UserLastFeedbackInfo, user_id=user_id, organisation_id=pk
            )
        ).data
        response = {
            "recipient_info": recipient_info,
            "feedbacks": feedbacks,
        }
        return Response(response)
