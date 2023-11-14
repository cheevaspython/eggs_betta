import logging

from datetime import datetime

from typing import OrderedDict

from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.serializers.applications_serializers import (
    ApplicationBuyerEggsSerializer, ApplicationSellerEggsSerializer
)
from product_eggs.serializers.base_deal_serializers import BaseDealEggsSerializer
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.comment import CommentEggs
from product_eggs.services.data_class import CommentData
from product_eggs.services.decorators import try_decorator_param

from users.models import CustomUser

logger = logging.getLogger(__name__)


@try_decorator_param(('KeyError',))
def parse_comment_tmp_json(
        val_data: OrderedDict, user: CustomUser) -> CommentData | None:

    if val_data['tmp_json']:
        val_data['tmp_json']['owner_id'] = user.pk
        val_data['tmp_json']['owner_name'] = user.username
        val_data['tmp_json']['date_time'] = str(datetime.today())[:16]
        data_for_save = CommentData(**val_data['tmp_json'])
        return data_for_save


def get_instance_for_comment(
        model_id: int, model_type: str
        ) -> None | ApplicationFromBuyerBaseEggs | ApplicationFromSellerBaseEggs| BaseDealEggsModel:

    TRUSED_MODEL_TYPES = {
        'app_seller': ApplicationFromSellerBaseEggs,
        'app_buyer': ApplicationFromBuyerBaseEggs,
        'base_deal': BaseDealEggsModel,
    }
    try:
        if model_type in TRUSED_MODEL_TYPES.keys():
            instance = TRUSED_MODEL_TYPES[model_type].objects.get(pk=model_id)
            return instance

    except (TypeError, ObjectDoesNotExist) as e:
        raise serializers.ValidationError(
            'wrong model_id or model_type in tmp_json comment', e)


def get_log_to_comment(data_for_save: CommentData) -> dict[str, dict]:
    """
    get model, serialize, return fields as dict for updat comment log
    """
    if model_for_comment := get_instance_for_comment(
            data_for_save.model_id,
            data_for_save.model_type
            ):
        cur_model_serializers = {
            'app_seller': ApplicationSellerEggsSerializer,
            'app_buyer': ApplicationBuyerEggsSerializer,
            'base_deal': BaseDealEggsSerializer,
        }
        log_data = {
            str(datetime.today()): {
                **cur_model_serializers[data_for_save.model_type](model_for_comment).data
            }
        }
        return log_data
    else:
        logging.warning('get_instance_for_comment error')
        raise serializers.ValidationError('get_instance_for_comment error')

