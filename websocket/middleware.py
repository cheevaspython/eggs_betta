import os 

from datetime import datetime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from jwt import decode
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.db import close_old_connections
from django.contrib.auth import get_user_model


User = get_user_model()

ALGORITHM = ["HS256"]


@database_sync_to_async
def get_user(token):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    except:
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()

        for item in scope['headers']:
            if item[0].decode('utf-8') == 'token':
                token_key = item[1].decode('utf-8')
             
        scope['token_key'] = token_key 
        scope['user'] = await get_user(token_key)

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)



