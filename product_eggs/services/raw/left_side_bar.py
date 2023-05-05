from django.db.models.query import RawQuerySet

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
            

