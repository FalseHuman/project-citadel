from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field =  'username'


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all().order_by('-id')
    serializer_class = PaysSerializer

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UpdateUserSerializer
    lookup_field =  'username'