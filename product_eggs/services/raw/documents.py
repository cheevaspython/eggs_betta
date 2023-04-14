from django.db.models.query import RawQuerySet
from product_eggs.models.documents import DocumentsDealEggsModel


def deal_docs_get_query(pk: int | None = None) -> RawQuerySet:

    status_calculate_is_active = DocumentsDealEggsModel.objects.raw(
        f"""SELECT id, payment_for_contract, payment_order_incoming, payment_order_outcoming,
                  specification_seller, account_to_seller, account_to_seller, account_to_buyer, 
                  application_contract_logic, account_to_logic, "UPD_incoming", account_invoicing_from_seller,
                  product_invoice_from_seller, "UPD_outgoing", account_invoicing_from_buyer, 
                  product_invoice_from_buyer, veterinary_certificate_buyer, veterinary_certificate_seller,
                  "international_deal_CMR", "international_deal_TTN", "UPD_logic", account_invoicing_logic, 
                  product_invoice_logic
            FROM "DocumentsDealEggs"
            WHERE id = {pk} 
            ORDER BY id;"""
    )
    return status_calculate_is_active
