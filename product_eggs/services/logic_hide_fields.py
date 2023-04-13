from collections import OrderedDict

from rest_framework.utils.serializer_helpers import ReturnDict

from users.models import CustomUser


def init_logic_user(user: CustomUser) -> bool:
    """
    Проверяет юзера по роли.
    Возвращает True если это логист.
    """
    if user.role == '4':
        return True
    else:
        return False


def get_return_edited_hide_data(
        serializer_many_data: ReturnDict) -> list[OrderedDict]:
    """
    Распаковывает данные и применяет к ним 
    функцию скрывающие поля.
    """
    return_data = list()
    for base_deal_serializer_data in serializer_many_data:
        return_data.append(hide_fields_in_data(base_deal_serializer_data))
    return return_data


def hide_fields_in_data(serializer_data: OrderedDict) -> dict:
    """
    Скрывает лишние поля, замещая их None.
    """
    LOGIC_FIELDS_HIDE = OrderedDict([
        ('seller_cB_cost', None), ('buyer_cB_cost', None),
        ('seller_c0_cost', None), ('buyer_c0_cost', None),
        ('seller_c1_cost', None), ('buyer_c1_cost', None), 
        ('seller_c2_cost', None), ('buyer_c2_cost', None), 
        ('seller_c3_cost', None), ('buyer_c3_cost', None),
        ('seller_dirt_cost', None), ('buyer_dirt_cost', None),
        ('margin', None)
    ])
    layer_dict = {a:b for a, b in serializer_data.items()}
    layer_dict.update(dict(LOGIC_FIELDS_HIDE))

    return layer_dict




