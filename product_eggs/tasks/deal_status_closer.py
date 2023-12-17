import logging
from celery import shared_task

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.base_deal.deal_status_change import DealStatusChanger
from users.models import CustomUser

logger = logging.getLogger(__name__)


@shared_task
def check_and_close_deal(instance: BaseDealEggsModel, user: CustomUser, close_doc_date: str) -> None:
    """
    close deal if buyer all pay
    """
    if check_buyer_close_payments(instance):
        instance.deal_status_ready_to_change = True
        deal = DealStatusChanger(instance, user, close=close_doc_date)
        deal.status_changer_main()


def check_buyer_close_payments(cur_deal: BaseDealEggsModel) -> bool:
    """
    check for UPD + check payments
    if UPD == all payments (deal_buyer_pay_amount==0)
    return True
    else False
    """
    if cur_deal.deal_status == 10:
        if cur_deal.deal_buyer_debt_UPD:
            return True if not cur_deal.deal_buyer_pay_amount else False

    return False




