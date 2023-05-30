from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.permissions import IsAuthenticated 
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

from product_eggs.models.messages import MessageToUserEggs
from product_eggs.serializers.base_deal_serializers import BaseDealEggsSerializer
from product_eggs.serializers.messages_serializers import MessageToUserEggsSerializer
from product_eggs.models.base_deal import BaseDealEggsModel
from users.serializers import CustomUserSerializer 
from users.models import CustomUser


class BaseDealConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = BaseDealEggsModel.objects.all()
    serializer_class = BaseDealEggsSerializer
    permission_classes = [IsAuthenticated]   


class ModelSubConsumer(GenericAsyncAPIConsumer):
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer

    @model_observer(MessageToUserEggs, serializer_class=MessageToUserEggsSerializer)
    async def comment_activity(self, message: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.reply(data=message, action=action, request_id=request_id)

    @action()
    async def subscribe_to_comment_activity(self, request_id: str, **kwargs):
        await self.comment_activity.subscribe(request_id=request_id)


