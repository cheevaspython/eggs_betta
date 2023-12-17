import json
import logging

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action

from users.models import CustomUser
from websocket.middleware import get_model

logger = logging.getLogger(__name__)


class CustomAPIConsumer(GenericAsyncAPIConsumer, ObserverModelInstanceMixin):
    auth = False
    user = None

    async def auth_close(self):
        await super().close()

    @action()
    async def authorization(self, request_id: str, action: str, **kwargs):
        if kwargs['token']:
            try:
                self.user = await get_model(kwargs['token'])
                if isinstance(self.user, CustomUser):
                    self.auth = True
                    await self.reply(
                        data={'authorization': True, 'user': self.user.pk}, action=action)
                else:
                    await self.reply(
                        data={'authorization': False}, action=action)
                    await self.auth_close()

            except AttributeError as e:
                logger.info('wrong token in ws auth', e)
                await self.reply(
                    data={'authorization': False}, action=action)
                await self.auth_close()

            except TypeError as e:
                logger.info('wrong token in ws auth', e)
                await self.reply(
                    data={'authorization': False}, action=action)
                await self.auth_close()
        else:
            await self.reply(
                data={'authorization': False}, action=action)
            await self.auth_close()
            await self.auth_close()

    async def encode_json(self, content):
        return json.dumps(content, ensure_ascii=False)

    async def check_action(self, message: str, action: str, request_id: str):
        allow_methhods = ('delete', 'create', 'update')
        if action in allow_methhods:
            await self.reply(data=message, action=action, request_id=request_id)

    async def check_action_side_bar(self, message: str, action: str, request_id: str):
        allow_methhods = ('delete', 'create', )
        if action in allow_methhods:
            await self.reply(data=message, action=action, request_id=request_id)
