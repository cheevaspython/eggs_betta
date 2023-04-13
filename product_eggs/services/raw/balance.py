from django.db.models.query import RawQuerySet

from product_eggs.models.base_client import SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.serializers.base_deal_serializers import BaseDealBalanceSerializer


def get_queryset_where_debt_positive() -> RawQuerySet:
    queryset = DocumentsContractEggsModel.objects.raw(
        '''SELECT b."inn", b."pay_limit", b."name", b."general_manager", b."phone",
            b."email", b."pay_type", b."comment", b."contact_person",
            b."manager_details", b."balance", b."documents_contract_id",
            b."balance_form_one", b."balance_form_two", b.pay_limit, b.pay_limit_cash,
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address, doc."data_number_json", doc.id, doc.contract,
            doc.contract_links_dict_json, doc.multi_pay_order, doc.multi_pay_order_links_dict_json,
            doc.tmp_json_for_multi_pay_order, doc.multy_pay_json
        FROM "BuyerCardEggs" AS b
        INNER JOIN "DocumentsConteragentsEggs" AS doc ON doc.id = b.documents_contract_id
        INNER JOIN "RequisitesEggs" AS r ON b.inn = r.inn 
        WHERE b.balance != 0 OR b.balance_form_one !=0 OR b.balance_form_two !=0  
        ORDER BY b.balance DESC;'''
    )
    return queryset


def get_queryset_deal_where_balance_seller_true() -> RawQuerySet:
    queryset = SellerCardEggs.objects.raw(
        '''SELECT s.inn, s.name, s.general_manager, s.phone, s.email, s.pay_type,
            s.comment, s.contact_person, s.balance, s.balance_detail_json, s.manager_details,
            s.documents_contract, r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account,
            r.customers_pay_account, r.legal_address, r.physical_address
        FROM "SellerCardEggs" AS s
        INNER JOIN "RequisitesEggs" AS r ON s.inn = r.inn 
        WHERE balance !=0 ORDER BY balance DESC;'''
    )
    return queryset


def get_queryset_deals_debt_by_client(current_client_inn: str, seller: bool) -> list[dict]:
    '''
    get queryset deals debt, bool true if seller - else buyer
    '''
    from product_eggs.services.balance_services import add_marker_to_deal_return_data

    client_model = ('seller', 'our', 'us', ) if seller else ('buyer', 'buyer', 'buyer',)
    queryset = BaseDealEggsModel.objects.raw(
        f'''SELECT d.id, d.current_deal_{client_model[1]}_debt, d.payback_day_for_us,
                d.payback_day_for_buyer, d.documents_id, d."deal_{client_model[1]}_debt_UPD",
                d.cash, d.current_deal_our_debt, d.current_deal_buyer_debt
            FROM "BaseDealModelEggs" AS d
            WHERE d.{client_model[0]}_id = '{current_client_inn}' 
            AND d.current_deal_{client_model[1]}_debt > 0 AND d.status = 3;'''
    )
    data_query = BaseDealBalanceSerializer(queryset, many=True)
    return add_marker_to_deal_return_data(data_query.data, client_model)
        
