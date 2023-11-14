from django.db.models.query import QuerySet

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.services.turn_off_fields import turn_off_fields_is_active


def search_done_base_deal_messages_and_turn_off(
        current_deal: BaseDealEggsModel) -> None:
    """
    Ищет все сообщения для конкретной сделки.
    Переводит их поле is_active в False.
    """
    current_deal_messages = MessageToUserEggs.objects.filter(
    current_base_deal=current_deal)
    turn_off_fields_is_active(current_deal_messages)


def find_messages_where_base_deal_and_not_done(base_deal_pk: int) -> QuerySet:
    return  MessageToUserEggs.objects.filter(
        current_base_deal=base_deal_pk, done=False)


def change_fileld_done_to_true(queryset: QuerySet):
    for query in queryset:
        query.done = True
        query.save()
