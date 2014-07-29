from rest_framework import viewsets, mixins

from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Survey, UserSurvey
from .permissions import *
from .serializers import *


class Auth(object):
    authentication_classes = (SessionAuthentication, BasicAuthentication)

class SurveyView(Auth, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ This view gets the survey meta data, and survey parameters.

    TODO: list un-surveyed surveys for non-admin users only, so no one
    will be able to see something they cannot take.
    """

    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, GetOnly)

    queryset = Survey.objects.all()

    def get_queryset(self):
        """ If non-admin user, return unsurveyed surveys only as
        queryset.
        """
        user = self.request.user

        if user.is_anonymous():
            return []

        qs = self.queryset

        if not user.is_superuser:
            qs = self.queryset.exclude(usersurvey__user=user,
                                       usersurvey__completed__isnull=True)

        return qs

class UserSurveyView(viewsets.ModelViewSet):
    """ This view only handles submission and creation of user survey
    instances.

    TODO:
    TODO: permissions - only one submission per user per session
    TODO: permissions - anonymous submissions not allowed
    """

    pass

