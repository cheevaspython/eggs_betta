from django.db.models.query import RawQuerySet
from rest_framework.serializers import ReturnDict

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.serializers.base_deal_serializers import BaseDealBalanceSerializer


def get_queryset_buyer_debt_positive() -> RawQuerySet:
    queryset = DocumentsContractEggsModel.objects.raw(
        '''SELECT b."inn", b."pay_limit", b."name", b."general_manager", b."phone",
            b."email", b."pay_type", b."comment", b."contact_person", b.tails_id,
            b."manager_id", b."balance", b."documents_contract_id",
            b."balance_form_one", b."balance_form_two", b.pay_limit, b.pay_limit_cash,
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address, doc."data_number_json", doc.id, doc.contract,
            doc.contract_links_dict_json, doc.multi_pay_order, doc.multi_pay_order_links_dict_json,
            doc.tmp_json_for_multi_pay_order, doc.multy_pay_json, doc.cash_docs, 
            doc.cash_docs_links_dict_json, doc.data_number_json_cash
        FROM "BuyerCardEggs" AS b
        INNER JOIN "DocumentsConteragentsEggs" AS doc ON doc.id = b.documents_contract_id
        INNER JOIN "RequisitesEggs" AS r ON b.inn = r.inn 
        WHERE b.balance != 0 OR b.balance_form_one !=0 OR b.balance_form_two !=0  
        ORDER BY b.balance DESC;'''
    )
    return queryset


def get_queryset_seller_balance() -> RawQuerySet:
    queryset = DocumentsContractEggsModel.objects.raw(
        '''SELECT s.inn, s.name, s.general_manager, s.phone, s.tails_id,
            s.email, s.pay_type, s.comment, s.contact_person,
            s.manager_id, s.balance, s.documents_contract_id,
            s.balance_form_one, s.balance_form_two,  
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address, doc."data_number_json", doc.id, doc.contract,
            doc.contract_links_dict_json, doc.multi_pay_order, doc.multi_pay_order_links_dict_json,
            doc.tmp_json_for_multi_pay_order, doc.multy_pay_json, doc.cash_docs, 
            doc.cash_docs_links_dict_json, doc.data_number_json_cash
        FROM "SellerCardEggs" AS s
        INNER JOIN "DocumentsConteragentsEggs" AS doc ON doc.id = s.documents_contract_id
        INNER JOIN "RequisitesEggs" AS r ON r.inn = s.inn 
        WHERE s.balance != 0 OR s.balance_form_one !=0 OR s.balance_form_two !=0  
        ORDER BY s.balance DESC;'''
    )
    return queryset


def get_queryset_logic_balance() -> RawQuerySet:
    queryset = DocumentsContractEggsModel.objects.raw(
        '''SELECT l.inn, l.name, l.general_manager, l.phone, 
            l.email, l.comment, l.contact_person,
            l.balance, l.documents_contract_id,
            l.balance_form_one, l.balance_form_two,  
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address, doc."data_number_json", doc.id, doc.contract,
            doc.contract_links_dict_json, doc.multi_pay_order, doc.multi_pay_order_links_dict_json,
            doc.tmp_json_for_multi_pay_order, doc.multy_pay_json, doc.cash_docs, 
            doc.cash_docs_links_dict_json, doc.data_number_json_cash
        FROM "LogicCardEggs" AS l
        INNER JOIN "DocumentsConteragentsEggs" AS doc ON doc.id = l.documents_contract_id
        INNER JOIN "RequisitesEggs" AS r ON r.inn = l.inn 
        WHERE l.balance != 0 OR l.balance_form_one !=0 OR l.balance_form_two !=0  
        ORDER BY l.balance DESC;'''
    )
    return queryset


def get_queryset_deals_debt_by_client(
        current_client_inn: str, seller: bool = False) -> list[dict]:
    '''
    get queryset deals debt, bool true if seller - else buyer
    '''
    from product_eggs.services.balance_services import add_marker_to_deal_return_data

    client_model = ('seller', 'our', 'us', ) if seller else ('buyer', 'buyer', 'buyer',)
    queryset = BaseDealEggsModel.objects.raw(
        f'''SELECT d.id, d.payback_day_for_buyer, d.payback_day_for_us,
                d.documents_id, d."deal_our_debt_UPD", d."deal_buyer_debt_UPD",
                d.cash, d.current_deal_our_debt, d.current_deal_buyer_debt, 
                d.logic_our_debt_current, d.logic_our_debt_for_app_contract
            FROM "BaseDealModelEggs" AS d
            WHERE d.{client_model[0]}_id = '{current_client_inn}' 
            AND d.current_deal_{client_model[1]}_debt > 0;'''
    )
    data_query = BaseDealBalanceSerializer(queryset, many=True)
    return add_marker_to_deal_return_data(data_query.data, client_model)
        

def get_queryset_deals_debt_by_client_logic(
        current_client_inn: str) -> ReturnDict:
    '''
    get queryset deals debt, bool true if seller - else buyer
    '''
    queryset = BaseDealEggsModel.objects.raw(
        f'''SELECT d.id, d.payback_day_for_buyer, d.payback_day_for_us,
                d.documents_id, d."deal_our_debt_UPD", d."deal_buyer_debt_UPD",
                d.cash, d.current_deal_our_debt, d.current_deal_buyer_debt, 
                d.logic_our_debt_current, d.logic_our_debt_for_app_contract
            FROM "BaseDealModelEggs" AS d
            WHERE d.current_logic_id = '{current_client_inn}' 
            AND d.logic_our_debt_current > 0;'''
    )
    data_query = BaseDealBalanceSerializer(queryset, many=True)
    return data_query.data



