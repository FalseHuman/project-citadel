from rest_framework import routers
from django.urls import path, include, re_path
from .views import *
# Создаем router и регистрируем наш ViewSet
router = routers.SimpleRouter()

router.register(r'user', UserViewSet)
router.register(r'create_user', CreateUser)
router.register(r'pays', PaysViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'templates', TempalatesViewSet)
router.register(r'password', ChangePasswordView)

# URLs настраиваются автоматически роутером
urlpatterns = [
    path("", include(router.urls)),
    path('update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path("token/", TokenGet.as_view(), name="token_get"),
    path("check_email/", CheckEmail.as_view(), name="check_email"),
    path("check_token/", CheckToken.as_view(), name="check_token"),
    #path('templates/', TempalatesViewSet.as_view(), name='templates'),
]