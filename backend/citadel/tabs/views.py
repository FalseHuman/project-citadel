from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponseRedirect
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .service import vk
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from uuid import uuid4
from .tasks import delay_send_email
from .pagination import StandardResultsSetPagination


class TokenGet(APIView):
    def post(self, request, format=None):
        try:
            Token.objects.get(key=request.data['auth-token'])
            return Response({"token": "exists"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"token": "not exists"}, status=status.HTTP_400_BAD_REQUEST)


class CheckEmail(APIView):
    def post(self, request, format=None):
        #print(User.objects.get(email=request.data['email']))
        try:
            user = User.objects.get(email=request.data['email'])
            rand_token = uuid4()
            TokenReset.objects.create(token_for_user= user, token=rand_token)
            subject, message = "Восстановление пароля", f"Здравствуйте, {user.username} \nТокен для восстановления пароля - {rand_token} Вставьте токен в форму без пробелов\nЕсли это были не вы просто проигнорируйте данное сообщение"
            delay_send_email.delay(
                subject=subject,
                message=message,
                user_email = user.email,
                fail_silently=False,
            )
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"email": "Пользователя с таким адресом эл.почты не существует или некорректно введён адрес."}, status=status.HTTP_400_BAD_REQUEST)

class CheckToken(APIView):
    def post(self, request, format=None):
        #print(request.data['token'])
        try:
            token = TokenReset.objects.get(token=request.data['token'])
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except TokenReset.DoesNotExist:
            return Response({"token": "Токен введён не правильно."}, status=status.HTTP_400_BAD_REQUEST)

class VK_Auth(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, format=None):
        if request.query_params.get('code'):
            token = vk.vk_auth(request.query_params.get('code'))
            res = HttpResponseRedirect('http://92.255.107.252/')
            res.set_cookie(key="auth_token", value=token)
            return res
        else:
            res = HttpResponseRedirect('http://92.255.107.252/login')
            return res


class CreateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        #print('user', self.request.user)
        return User.objects.filter(username=self.request.user)


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = PaysSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date').split('-')
        print(date)
        return self.request.user.pays.filter(data__year=date[0], data__month=date[1])

    @action(detail=True, methods=['delete'])
    def delete_pays(self, request, pk=None):
        try:
            Pays.objects.get(id=pk).delete()
        except Pays.DoesNotExist:
            pass

        return Response(status=204)


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotesSerializer

    def get_queryset(self):
        return self.request.user.notes.all()

    @action(detail=True, methods=['post'])
    def edit_notes(self, request, pk=None):
        try:
            notes = Notes.objects.get(id=pk)
            notes.person.username = request.user
            notes.title = request.data.get("title")
            notes.body = request.data.get("body")
            notes.save()
        except Notes.DoesNotExist:
            pass

        return Response(status=204)

    @action(detail=True, methods=['delete'])
    def delete_notes(self, request, pk=None):
        try:
            Notes.objects.get(id=pk).delete()
        except Notes.DoesNotExist:
            pass

        return Response(status=204)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UpdateUserSerializer

    def put(self, request, format=None):
        user = User.objects.get(username=request.user.username)
        serializer = UpdateUserSerializer(
            data=request.data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class TempalatesViewSet(viewsets.ModelViewSet):
    queryset = Templates.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TemplatesSerializer

    def get_queryset(self):
        return self.request.user.templates.all()

    def post(self, request, format=None):
        # print(request.data)
        serializer = TemplatesSerializer(
            data=request.data)
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
            print(request.data.get("password_1") ==
                  request.data.get("password_2"))
            if request.data.get("password_1") == request.data.get("password_2"):
                if is_password_good(request.data.get("password_1")) == True:
                    username.set_password(request.data.get("password_1"))
                    username.save()
                else:
                    message = "Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов. Он должен содержать  заглавную букву. Введённый пароль слишком широко распространён. Введённый пароль состоит только из цифр."
                    return Response({'password_1': message, 'password_2': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'password_1': "Пароли не совпадают.", 'password_2': "Пароли не совпадают."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'login': "Пользователь не существует."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
