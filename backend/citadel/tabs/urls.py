from rest_framework import routers
from django.urls import path, include, re_path
from .views import *
# Создаем router и регистрируем наш ViewSet
router = routers.SimpleRouter()

router.register(r'user', UserViewSet)
router.register(r'pays', PaysViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'templates', TempalatesViewSet)
router.register(r'password', ChangePasswordView)

# URLs настраиваются автоматически роутером
urlpatterns = [
    path("", include(router.urls)),
    path('update_profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path("token/", TokenGet.as_view(), name="token_get"),
    #path('templates/', TempalatesViewSet.as_view(), name='templates'),
]