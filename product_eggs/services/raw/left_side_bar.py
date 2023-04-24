from django.db.models.query import RawQuerySet

from product_eggs.models.base_deal import BaseDealEggsModel
        

def deal_is_active_where_doc_id_as_deal_id() -> RawQuerySet:
    deal_for_sidebar = BaseDealEggsModel.objects.raw(
        """
        SELECT deal.id as model_id, deal.documents_id as id,
            deal.current_deal_our_debt, deal.current_deal_buyer_debt,
            deal.logic_our_debt_current, deal.is_active, deal.status 
        FROM "BaseDealModelEggs" AS deal 
        WHERE deal.is_active = true AND deal.status = 3
        ORDER BY deal.documents_id;
        """
    )
    return deal_for_sidebar
            

