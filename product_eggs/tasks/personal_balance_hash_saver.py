from datetime import datetime
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q, QuerySet

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.personal_area import PersonalSalaryBalanceEggs
from users.models import CustomUser

logger = get_task_logger(__name__)


@shared_task
def personal_cur_balance_saver_to_hash() -> None:
    all_managers = CustomUser.objects.filter(Q(role=1), Q(role=2), Q(role=3), Q(role=4))
    cur_date = datetime.today()
    for cur_manager in all_managers:
        cur_balance_saver(cur_manager, cur_date)
    logger.info('run personal_cur_balance_saver_to_hash task')


def cur_balance_saver(manager: CustomUser, today: datetime) -> None:
    all_balances: QuerySet[PersonalSalaryBalanceEggs] = manager.manager_pa.all()
    str_date = str(today.year) + '-' + str(today.month)
    for balance in all_balances:
        balance.month_hash_dict[str_date] = balance.wage_balance
        balance.save()


# @shared_task
# def calc_wage_balance(cur_deal: BaseDealEggsModel):
#     if cur_deal.status == 4:
#         ...
#
#
# def add_wage_amount(manager_balance: PersonalSalaryBalanceEggs, pay_amount: float):


def get_wage():
    ...
    #TODO add logic then manager get salary
