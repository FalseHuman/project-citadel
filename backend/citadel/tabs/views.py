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


class ChangePasswordView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """ Код с курса https://stepik.org/lesson/334150/step/5?unit=317559 """
        def is_password_good(password):
            count, count1, count2 = 0, 0, 0
            for i in range(len(password)):
                if '0' <= password[i] <= '9':
                    count += 1
                if 'A' <= password[i] <= 'Z':
                    count1 += 1
                if 'a' <= password[i] <= 'z':
                    count2 += 1
            return len(password) >= 8 and count >= 1 and count1 >= 1 and count2 >= 1
        user = User.objects
        try:
            username = user.get(username=request.data.get("login"))
            if request.data.get("password_1") == request.data.get("password_2"):
                if is_password_good(request.data.get("password_1")) == True:
                    username.set_password(request.data.get("password_1"))
                    username.save()
                else:
                    return Response({"Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов. Он должен содержать  заглавную букву. Введённый пароль слишком широко распространён. Введённый пароль состоит только из цифр."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"Пользователь не существует."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
