from datetime import datetime, date
from typing import Iterator
from celery import shared_task
from celery.utils.log import get_task_logger

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.services.messages.messages_library import MessageLibrarrySend


logger = get_task_logger(__name__)


@shared_task
def applications_actual_checker() -> None:
    app_seller = ApplicationFromSellerBaseEggs.objects.\
        filter(is_active=True).only('id', 'created_date_time',
        'edited_date_time', 'owner_id').iterator() 
    app_buyer = ApplicationFromBuyerBaseEggs.objects.\
        filter(is_active=True).only('id', 'created_date_time',
        'edited_date_time', 'owner_id').iterator() 

    run_for_query(app_seller)
    run_for_query(app_buyer)

    logger.info('run beat task')


def applications_actual_checker_test() -> None:
    app_seller = ApplicationFromSellerBaseEggs.objects.\
        filter(is_active=True).only('id', 'created_date_time',
        'edited_date_time', 'owner_id').iterator() 
    app_buyer = ApplicationFromBuyerBaseEggs.objects.\
        filter(is_active=True).only('id', 'created_date_time',
        'edited_date_time', 'owner_id').iterator() 

    run_for_query(app_seller)
    run_for_query(app_buyer)


def check_delta_date_applications(app_date: date) -> bool:
    delta = datetime.today().date() - app_date 
    if delta.days > 3:
        return True
    else:
        return False


def run_for_query(
        iter_query: Iterator[ApplicationFromSellerBaseEggs] | \
        Iterator[ApplicationFromBuyerBaseEggs]) -> None:

    for app in iter_query:
        if check_delta_date_applications(app.created_date_time.date()):
            app.is_actual = False
            app.save()
            MessageLibrarrySend(
                'applications_actual',
                app,
            )





