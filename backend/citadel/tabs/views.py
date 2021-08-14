from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaysSerializer

    @action(detail=True, methods=['delete'])
    def delete_pays(self, request, pk=None):
        try:
            Pays.objects.get(id=pk).delete()
        except Pays.DoesNotExist:
            pass

        return Response(status=204)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UpdateUserSerializer
    lookup_field = 'username'


class UserAvatarUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserAvatarSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
