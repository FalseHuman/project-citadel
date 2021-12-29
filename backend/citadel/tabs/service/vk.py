import requests, json
from ..models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.conf import settings

def get_vk_email(code: str):
    url = f'https://oauth.vk.com/access_token?client_id={settings.VK_CLIENT_ID }&client_secret={settings.VK_SECRET}&redirect_uri=http%3A%2F%2Flocalhost%3A8002%2Fvk-callback&code={code}'
    res = requests.get(url)
    if res.status_code == 200:
        r = res.json()
        return r
    else:
        return None

def vk_auth(code: str):
    user_data = get_vk_email(code)
    if user_data is not None:
        try:
            user = User.objects.get(email=user_data.get('email'))
        except User.DoesNotExist:
            user = User.objects.create(email=user_data.get('email'), username= 'id_' + str(user_data.get('user_id')))
        token = Token.objects.get_or_create(user=user)
        return f'{token[0]}'
    else:
        raise AuthenticationFailed(code=403, detail=f'Bad token VK or user not email in profile VK')
