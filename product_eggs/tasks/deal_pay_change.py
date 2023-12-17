import logging
from celery import shared_task

from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.services.base_deal.margin import calculate_margin

logger = logging.getLogger(__name__)


@shared_task
def change_client_balance(
        cur_balance_model: BalanceBaseClientEggs,
        delta: float, cash: bool) -> None:
    """
    Task changed Client balance, then change
    deal balance.
    """
    if cash:
        cur_balance_model.balance_form_two += delta
        cur_balance_model.save()
    else:
        cur_balance_model.balance_form_one += delta
        cur_balance_model.save()


@shared_task
def task_calc_margin(cur_model: Model) -> float | None:
    from product_eggs.models.base_deal import BaseDealEggsModel
    from product_eggs.models.additional_expense import AdditionalExpenseEggs

    if isinstance(cur_model, BaseDealEggsModel):
        return calculate_margin(cur_model)

    if isinstance(cur_model, AdditionalExpenseEggs):
        try:
            cur_deal = cur_model.base_deal_model
            cur_deal.margin = calculate_margin(cur_deal)
            cur_deal.save()
        except ObjectDoesNotExist:
            pass











