from datetime import date, datetime, timedelta
from collections import OrderedDict

from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.raw.balance import get_queryset_deals_debt_by_client,\
    get_queryset_deals_debt_by_client_logic

            
def add_marker_to_deal_return_data(
        return_data_deal_client: OrderedDict, client_model: tuple) -> list[dict]:
    """
    Add color marker to deal.
    """
    tmp = convert_ordered_dict_to_list_dicts(return_data_deal_client)
    for deals_debt in tmp:
        try:
            if tmp_date := convert_str_to_date(deals_debt[f'payback_day_for_{client_model[2]}']):
                 deals_debt['marker'] = add_color_marker(subtract_dates(tmp_date))  
        except TypeError:
            deals_debt['marker'] = 'black'
    return tmp


def convert_serializer_data_to_list_of_dicts(
        serializer_data: OrderedDict,
        seller=False, logic=False) -> list[dict]:
    """
    Convert OrderedDict to list[dict] and add fields.
    """
    tmp_dicts_list = convert_ordered_dict_to_list_dicts(serializer_data)
    for tmp_dict in tmp_dicts_list:
        if logic:
            filter_fields_for_current_client = \
                get_queryset_deals_debt_by_client_logic(tmp_dict['inn'])
        else:
            filter_fields_for_current_client = \
                get_queryset_deals_debt_by_client(tmp_dict['inn'], seller)
        if filter_fields_for_current_client:
            tmp_dict['debt_deals'] = filter_fields_for_current_client
    return tmp_dicts_list


def convert_ordered_dict_to_list_dicts(serializer_data: OrderedDict) -> list[dict]:
    return [dict(item.items()) for item in serializer_data]


@try_decorator_param(('TypeError',), return_value=f'cant convert date')
def convert_str_to_date(date_in_str: str) -> date:
    return datetime.strptime(date_in_str, '%Y-%m-%d').date()


def subtract_dates(payback_date: date) -> timedelta:
    return payback_date - date.today()


def add_color_marker(payday_delta: timedelta) -> str:
    if payday_delta.days < -1:
        return 'red'
    elif payday_delta.days > 1:
        return 'green'
    else:
        return 'yellow'
