from django.shortcuts import render
from django.contrib.auth.models import Group
from users.models import User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer

from rest_framework.response import Response
from  rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def getData(request):
    person = {'name':'Dennis', 'age':12}
    return Response(person)