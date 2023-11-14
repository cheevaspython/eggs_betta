import os
import logging

import django
from config.settings import SECRET_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework.response import Response
from rest_framework_simplejwt.backends import jwt

from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser

User = get_user_model()

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_model(token):
    """
    Attempts to find and return a user using the given validated token.
    """
    try:
        if SECRET_KEY:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            userid = payload['user_id']
            user = CustomUser.objects.get(pk=userid)
            logger.info(f"Request received from user - {userid}")
            return user

    except jwt.ExpiredSignatureError as e:
        logger.info("Authentication token has expired", e)
        return Response("Authentication token has expired", status=401)

    except (jwt.DecodeError, jwt.InvalidTokenError) as e:
        logger.info("Authorization has failed, Please send valid token.", e)
        return Response("Authorization has failed, Please send valid token.", status=401)


class TokenAuthMiddleware(BaseMiddleware):
    """
    Get token from scope, check, and add user in scope.
    """
    async def __call__(self, scope, receive, send):
        close_old_connections()
        token = scope['subprotocols']
        scope['user'] = await get_model(token[0])
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)




