from typing import Any

from rest_framework.request import Request


def parse_patch_data_get_id(request_from_patch: Request) -> int: 
    """
    Парсинг не сериализованных данных.
    """
    parse_id = request_from_patch.META['PATH_INFO'].replace('/', ' ').split()[-1]
    return parse_id


def get_object_from_patch_data(obj_queryset, parse_id: int) -> Any:
    """
    Получает модель из данных. 
    """
    retrieved_obj = obj_queryset.get(id=parse_id)
    return retrieved_obj
