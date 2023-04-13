from collections import OrderedDict

from django.db.models.query import RawQuerySet

from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs
from product_eggs.serializers.calc_deal_serializers_eggs import DealEggsSerializerDebt


def get_queryset_where_debt_positive() -> RawQuerySet:
        queryset = BuyerCardEggs.objects.raw(
            '''SELECT b."inn", b."pay_limit", b."name", b."general_manager",  b."phone",
            b."email", b."pay_type", b."comment", b."balance_debt", b."contact_person",
            b."manager_details", b."balance", b."balance_detail_json", b."documents_contract_id",
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address
            FROM "BuyerCardEggs" as b
            INNER JOIN "RequisitesEggs" as r on b.inn = r.inn 
            WHERE b.balance_debt > 0 ORDER BY b.balance_debt DESC;'''
        )
        return queryset


def get_queryset_where_debt_positive_cash() -> RawQuerySet:
        queryset = BuyerCardEggs.objects.raw(
            '''SELECT b."inn", b."pay_limit_cash", b."name", b."general_manager", b."phone",
            b."email", b."pay_type", b."comment", b."balance_debt_cash", b."contact_person", b."docs_cash_id",
            b."manager_details", b."balance", b."balance_detail_json", b."documents_contract_id",
            r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account, r.customers_pay_account,
            r.legal_address, r.physical_address
            FROM "BuyerCardEggs" as b
            LEFT JOIN "RequisitesEggs" as r on b.inn = r.inn 
            WHERE b.balance_debt > 0 ORDER BY b.balance_debt DESC;'''
        )
        return queryset


def get_queryset_deal_debt_by_current_buyer(current_buyer_inn: str) -> OrderedDict:
        queryset = DealEggs.objects.raw(
                f'''SELECT d.id, d.current_deal_buyer_debt, d.documents_id
                            FROM "DealEggs" as d
                            WHERE d.buyer_inn = '{current_buyer_inn}' AND d.current_deal_buyer_debt > 0;'''
        )
        data_query = DealEggsSerializerDebt(queryset, many=True)
        return data_query.data


def get_queryset_where_balance_seller_true() -> RawQuerySet:
        queryset = SellerCardEggs.objects.raw(
            '''SELECT s.inn, s.name, s.general_manager, s.phone, s.email, s.pay_type,
            s.comment, s.contact_person, s.balance, s.balance_detail_json, s.manager_details,
            s.documents_contract, r.inn, r.general_manager, r.bank_name, r.bic_bank, r.cor_account,
            r.customers_pay_account, r.legal_address, r.physical_address
            FROM "SellerCardEggs" as s
            INNER JOIN "RequisitesEggs" as r on s.inn = r.inn 
            WHERE balance != 0 ORDER BY balance DESC;'''
        )
        return queryset


def convert_ordereddict_data_to_list_of_dicts_and_add_field(serializer_data: OrderedDict) -> list[dict]:
        tmp_dicts_list = [dict(item.items()) for item in serializer_data]
        for tmp_dict in tmp_dicts_list:
            filter_fields_for_current_buyer = get_queryset_deal_debt_by_current_buyer(tmp_dict['inn'])
            if filter_fields_for_current_buyer:
                tmp_dict['debt_deals_this_buyer'] = [dict(item.items()) for item in filter_fields_for_current_buyer]
        return tmp_dicts_list


def try_check_serializer_data_for_encroachments(
        serializer_data: OrderedDict,
        find_fields: tuple[str, str, str, str] ) -> tuple[str, str] | None:
        try:
            if serializer_data[find_fields[0]] and serializer_data[find_fields[1]]:
                return find_fields[0], find_fields[1]
        except KeyError:
            return None
        try:
            if serializer_data[find_fields[2]] and serializer_data[find_fields[3]]:
                return find_fields[2], find_fields[3]
        except KeyError:
            return None
        
        return None

