from datetime import datetime
from typing import Iterator
from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils import timezone

from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs,
)
from product_eggs.services.messages.messages_library import MessageLibrarrySend

logger = get_task_logger(__name__)


@shared_task
def applications_actual_checker() -> None:
    app_seller = ApplicationFromSellerBaseEggs.objects.filter(
        is_active=True
    ).only(
        'id', 'created_date_time',
        'edited_date_time', 'await_add_cost', 'owner_id'
    ).iterator()
    app_buyer = ApplicationFromBuyerBaseEggs.objects.filter(
        is_active=True
    ).only(
        'id', 'created_date_time',
        'edited_date_time', 'await_add_cost', 'owner_id'
    ).iterator()
    run_data_checker_for_query(app_seller)
    run_data_checker_for_query(app_buyer)
    logger.info('run beat task')


def check_delta_date_applications(app_date: datetime) -> bool:
    interval = timezone.now() - app_date
    if interval.days < 4:
        return False
    else:
        return True


def check_date_for_await_cost(app_date: datetime) -> bool:
    interval = timezone.now() - app_date
    if interval.days <= 0:
        return False
    else:
        return True


def run_data_checker_for_query(
        iter_query: Iterator[ApplicationFromSellerBaseEggs] |
        Iterator[ApplicationFromBuyerBaseEggs]
    ) -> None:

    for app in iter_query:
        if isinstance(app.await_add_cost, datetime):
            if check_date_for_await_cost(app.await_add_cost):
                app.is_actual = False
                app.await_add_cost = None
                app.save()
                mess_model = MessageLibrarrySend(
                    'applications_await_cost',
                    app,
                )
                mess_model.send_message()
        else:
            if check_delta_date_applications(app.edited_date_time):
                app.is_actual = False
                app.save()
                mess_model = MessageLibrarrySend(
                    'applications_actual',
                    app,
                )
                mess_model.send_message()










