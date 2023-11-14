from product_eggs.models.applications import (
    ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel


def field_is_active_offer_for_title_search(title: str, object_id: int) -> None:
    """
    Делает модель не активной, по названию.
    """
    tmp_title_book = {
        'Заявка от продавца': ApplicationFromSellerBaseEggs,
        'Заявка от покупателя': ApplicationFromBuyerBaseEggs,
        'Просчет': BaseDealEggsModel,
        'Подтвержденный просчет': BaseDealEggsModel,
        'Сделка': BaseDealEggsModel,
    }
    if title in tmp_title_book.keys():
        obj = tmp_title_book[title].objects.get(id=object_id)
        obj.is_active = False
        obj.save()
    else:
        raise ValueError('field_is_active_offer_for_title_search title value ERROR')


def turn_off_fields_is_active(*field_object) -> None:
    """
    Общая функция работы с полем is_аctive.
    """
    try:
        for item in field_object[0]:
            item.is_active = False
            item.save()
    except TypeError:
        field_object[0].is_active = False
        field_object[0].save()


