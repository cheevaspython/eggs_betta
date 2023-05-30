from django.db.models.query import RawQuerySet

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
        

def deal_is_active_where_doc_id_as_deal_id(user_pk: int) -> RawQuerySet:
    deal_for_sidebar = BaseDealEggsModel.objects.raw(
        f"""
        SELECT deal.id as model_id, deal.documents_id as id,
            deal.deal_our_pay_amount, deal.deal_buyer_pay_amount,
            deal.logic_our_pay_amount, deal.is_active, deal.status, deal.owner_id
        FROM "BaseDealModelEggs" AS deal 
        WHERE deal.is_active = true AND deal.status = 3 AND deal.owner_id = {user_pk}
        ORDER BY deal.documents_id;
        """
    )
    return deal_for_sidebar
            

def conf_calc_is_active_where_doc_id_as_deal_id(user_pk: int) -> RawQuerySet:
    conf_calc_for_sidebar = BaseDealEggsModel.objects.raw(
        f"""
        SELECT deal.id as model_id, deal.documents_id as id,
            deal.deal_our_pay_amount, deal.deal_buyer_pay_amount,
            deal.logic_our_pay_amount, deal.is_active, deal.status, deal.owner_id
        FROM "BaseDealModelEggs" AS deal 
        WHERE deal.is_active = true AND deal.status = 2 AND deal.owner_id = {user_pk}
        ORDER BY deal.documents_id;
        """
    )
    return conf_calc_for_sidebar


def calc_is_active_where_doc_id_as_deal_id(user_pk: int) -> RawQuerySet:
    calc_for_sidebar = BaseDealEggsModel.objects.raw(
        f"""
        SELECT deal.id as model_id, deal.documents_id as id,
            deal.deal_our_pay_amount, deal.deal_buyer_pay_amount,
            deal.logic_our_pay_amount, deal.is_active, deal.status, deal.owner_id
        FROM "BaseDealModelEggs" AS deal 
        WHERE deal.is_active = true AND deal.status = 1 AND deal.owner_id = {user_pk}
        ORDER BY deal.documents_id;
        """
    )
    return calc_for_sidebar


def app_buyer_is_active_owner(user_pk: int) -> RawQuerySet:
    app_buyer = ApplicationFromBuyerBaseEggs.objects.raw(
        f"""
        SELECT b.id, b.owner_id, b.is_active
        FROM "ApplicationFromBuyerBaseEggs" AS b 
        WHERE b.is_active = true AND b.owner_id = {user_pk}
        ORDER BY b.id;
        """
    )
    return app_buyer


def app_seller_is_active_owner(user_pk: int) -> RawQuerySet:
    app_seller = ApplicationFromSellerBaseEggs.objects.raw(
        f"""
        SELECT s.id, s.owner_id, s.is_active
        FROM "ApplicationFromSellerBaseEggs" AS s 
        WHERE s.is_active = true AND s.owner_id = {user_pk}
        ORDER BY s.id;
        """
    )
    return app_seller
