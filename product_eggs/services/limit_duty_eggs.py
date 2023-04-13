from datetime import date, datetime, timedelta
from collections import OrderedDict

from django.db.models.query import RawQuerySet

from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.models.base_eggs import SellerCardEggs
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.serializers.calc_deal_serializers_eggs import DealEggsSerializerDebtBuyer


def get_queryset_where_debt_positive() -> RawQuerySet:
    queryset = DocumentsContractEggsModel.objects.raw(
        '''SELECT b."inn", b."pay_limit", b."name", b."general_manager", b."phone",
        b."email", b."pay_type", b."comment", b."contact_person",
        b."manager_details", b."balance", b."documents_contract_id",
        b."balance_form_one", b."balance_form_two", b.pay_limit, b.pay_limit_cash,
        r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
        r.legal_address, r.physical_address, doc."data_number_json", doc.id
        FROM "BuyerCardEggs" as b
        INNER JOIN "DocumentsConteragentsEggs" as doc on doc.id = b.documents_contract_id
        INNER JOIN "RequisitesEggs" as r on b.inn = r.inn 
        WHERE b.balance != 0 or b.balance_form_one !=0 or b.balance_form_two !=0  
        ORDER BY b.balance DESC;'''
    )
    return queryset


def get_queryset_deals_debt_by_client_seller_if_true(current_buyer_inn: str, seller: bool) -> list[dict]:
    '''
    get queryset deals debt, bool true if seller - else buyer
    '''
    client_model = ('seller', 'our', 'us', ) if seller else ('buyer', 'buyer', 'buyer',)
    queryset = DealEggs.objects.raw(
        f'''SELECT d.id, d.current_deal_{client_model[1]}_debt, d.payback_day_for_us,
            d.payback_day_for_buyer, d.documents_id, d."deal_{client_model[1]}_debt_UPD",
            d.cash
            FROM "DealEggs" as d
            WHERE d.{client_model[0]}_inn = '{current_buyer_inn}' 
            AND d.current_deal_{client_model[1]}_debt > 0;'''
    )
    data_query = DealEggsSerializerDebtBuyer(queryset, many=True)
    return add_marker_to_deal_return_data(data_query.data, client_model)


def add_marker_to_deal_return_data(
        return_data_deal_client: OrderedDict, client_model: tuple) -> list[dict]:
    tmp = convert_ordered_dict_to_list_dicts(return_data_deal_client)
    for deals_debt in tmp:
        if tmp_date := convert_str_to_date(deals_debt[f'payback_day_for_{client_model[2]}']):
            deals_debt['marker'] = add_color_marker(subtract_dates(tmp_date))  
        else:
            deals_debt['marker'] = 'error convert payback day'
    return tmp


def get_queryset_where_balance_seller_true() -> RawQuerySet:
    queryset = SellerCardEggs.objects.raw(
        '''SELECT s.inn, s.name, s.general_manager, s.phone, s.email, s.pay_type,
        s.comment, s.contact_person, s.balance, s.balance_detail_json, s.manager_details,
        s.documents_contract, r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account,
        r.customers_pay_account, r.legal_address, r.physical_address
        FROM "SellerCardEggs" as s
        INNER JOIN "RequisitesEggs" as r on s.inn = r.inn 
        WHERE balance !=0 ORDER BY balance DESC;'''
    )
    return queryset


def convert_ordereddict_data_to_list_of_dicts_and_add_field(serializer_data: OrderedDict) -> list[dict]:
    tmp_dicts_list = convert_ordered_dict_to_list_dicts(serializer_data)
    for tmp_dict in tmp_dicts_list:
        filter_fields_for_current_client = get_queryset_deals_debt_by_client_seller_if_true(tmp_dict['inn'], seller=False)
        if filter_fields_for_current_client:
            tmp_dict['debt_deals'] = filter_fields_for_current_client
    return tmp_dicts_list


def convert_str_to_date(date_in_str: str) -> date | None:
    try:
        return datetime.strptime(date_in_str, '%Y-%m-%d').date()
    except TypeError as e:
        print(f'cant convert date {e}')


def subtract_dates(payback_date: date) -> timedelta:
    return payback_date - date.today()


def add_color_marker(payday_delta: timedelta) -> str:
    if payday_delta.days < -1:
        return 'red'
    elif payday_delta.days > 1:
        return 'green'
    else:
        return 'yellow'


def convert_ordered_dict_to_list_dicts(serializer_data: OrderedDict) -> list[dict]:
    return [dict(item.items()) for item in serializer_data]
    


