from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.serializers.base_deal_serializers import (
    BaseCompDealEggsNameSerializer, BaseDealEggsNameSerializer,
    CalculateEggsNamesSerializer, ConfirmedCalculateEggsNameSerializer
)

base_deal_serializers = {
    'calculate': CalculateEggsNamesSerializer,
    'conf_calculate': ConfirmedCalculateEggsNameSerializer,
    'base_deal': BaseDealEggsNameSerializer,
    'comp_base_deal': BaseCompDealEggsNameSerializer,
}


def get_base_deal_orm_request(base_deal_status: int):

    match base_deal_status:
        case 1:
            calc_orm_request = CalculateEggsNamesSerializer(
                BaseDealEggsModel.objects.filter(is_active=True, status=1).select_related(
                    'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                    'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                ).annotate(
                    sum_seller_orm =
                    F('cB_white')*F('seller_cB_white_cost')+
                    F('cB_cream')*F('seller_cB_cream_cost')+
                    F('cB_brown')*F('seller_cB_brown_cost')+
                    F('c0_white')*F('seller_c0_white_cost')+
                    F('c0_cream')*F('seller_c0_cream_cost')+
                    F('c0_brown')*F('seller_c0_brown_cost')+
                    F('c1_white')*F('seller_c1_white_cost')+
                    F('c1_cream')*F('seller_c1_cream_cost')+
                    F('c1_brown')*F('seller_c1_brown_cost')+
                    F('c2_white')*F('seller_c2_white_cost')+
                    F('c2_cream')*F('seller_c2_cream_cost')+
                    F('c2_brown')*F('seller_c2_brown_cost')+
                    F('c3_white')*F('seller_c3_white_cost')+
                    F('c3_cream')*F('seller_c3_cream_cost')+
                    F('c3_brown')*F('seller_c3_brown_cost')+
                    F('dirt')*F('seller_dirt_cost'),

                    sum_buyer_orm =
                    F('cB_white')*F('buyer_cB_white_cost')+
                    F('cB_cream')*F('buyer_cB_cream_cost')+
                    F('cB_brown')*F('buyer_cB_brown_cost')+
                    F('c0_white')*F('buyer_c0_white_cost')+
                    F('c0_cream')*F('buyer_c0_cream_cost')+
                    F('c0_brown')*F('buyer_c0_brown_cost')+
                    F('c1_white')*F('buyer_c1_white_cost')+
                    F('c1_cream')*F('buyer_c1_cream_cost')+
                    F('c1_brown')*F('buyer_c1_brown_cost')+
                    F('c2_white')*F('buyer_c2_white_cost')+
                    F('c2_cream')*F('buyer_c2_cream_cost')+
                    F('c2_brown')*F('buyer_c2_brown_cost')+
                    F('c3_white')*F('buyer_c3_white_cost')+
                    F('c3_cream')*F('buyer_c3_cream_cost')+
                    F('c3_brown')*F('buyer_c3_brown_cost')+
                    F('dirt')*F('buyer_dirt_cost'),

                    seller_manager_orm = F('seller__manager__username'),
                    buyer_manager_orm = F('buyer__manager__username'),
                    owner_name_orm = F('owner__username'),
                    seller_name_orm = F('seller__requisites__name'),
                    buyer_name_orm = F('buyer__requisites__name'),
                    expense_total_orm = F('additional_expense__expense_total'),
                    expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                ), many=True)
            return calc_orm_request

        case 2:
            conf_calc_orm_request = ConfirmedCalculateEggsNameSerializer(
                BaseDealEggsModel.objects.filter(is_active=True, status=2).select_related(
                    'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                    'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                    'current_logic', 'current_logic__requisites',
                ).annotate(
                    sum_seller_orm =
                    F('cB_white')*F('seller_cB_white_cost')+
                    F('cB_cream')*F('seller_cB_cream_cost')+
                    F('cB_brown')*F('seller_cB_brown_cost')+
                    F('c0_white')*F('seller_c0_white_cost')+
                    F('c0_cream')*F('seller_c0_cream_cost')+
                    F('c0_brown')*F('seller_c0_brown_cost')+
                    F('c1_white')*F('seller_c1_white_cost')+
                    F('c1_cream')*F('seller_c1_cream_cost')+
                    F('c1_brown')*F('seller_c1_brown_cost')+
                    F('c2_white')*F('seller_c2_white_cost')+
                    F('c2_cream')*F('seller_c2_cream_cost')+
                    F('c2_brown')*F('seller_c2_brown_cost')+
                    F('c3_white')*F('seller_c3_white_cost')+
                    F('c3_cream')*F('seller_c3_cream_cost')+
                    F('c3_brown')*F('seller_c3_brown_cost')+
                    F('dirt')*F('seller_dirt_cost'),

                    sum_buyer_orm =
                    F('cB_white')*F('buyer_cB_white_cost')+
                    F('cB_cream')*F('buyer_cB_cream_cost')+
                    F('cB_brown')*F('buyer_cB_brown_cost')+
                    F('c0_white')*F('buyer_c0_white_cost')+
                    F('c0_cream')*F('buyer_c0_cream_cost')+
                    F('c0_brown')*F('buyer_c0_brown_cost')+
                    F('c1_white')*F('buyer_c1_white_cost')+
                    F('c1_cream')*F('buyer_c1_cream_cost')+
                    F('c1_brown')*F('buyer_c1_brown_cost')+
                    F('c2_white')*F('buyer_c2_white_cost')+
                    F('c2_cream')*F('buyer_c2_cream_cost')+
                    F('c2_brown')*F('buyer_c2_brown_cost')+
                    F('c3_white')*F('buyer_c3_white_cost')+
                    F('c3_cream')*F('buyer_c3_cream_cost')+
                    F('c3_brown')*F('buyer_c3_brown_cost')+
                    F('dirt')*F('buyer_dirt_cost'),

                    seller_manager_orm = F('seller__manager__username'),
                    buyer_manager_orm = F('buyer__manager__username'),
                    owner_name_orm = F('owner__username'),
                    seller_name_orm = F('seller__requisites__name'),
                    buyer_name_orm = F('buyer__requisites__name'),
                    expense_total_orm = F('additional_expense__expense_total'),
                    expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                    logic_inn_orm = F('current_logic__inn'),
                    logic_name_orm = F('current_logic__requisites__name'),
                ), many=True)
            return conf_calc_orm_request

        case 3:
            base_deal_orm_request = BaseDealEggsNameSerializer(
                BaseDealEggsModel.objects.filter(is_active=True, status=3).select_related(
                    'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                    'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                    'current_logic', 'current_logic__requisites', 'documents',
                ).annotate(
                    sum_seller_orm =
                    F('cB_white')*F('seller_cB_white_cost')+
                    F('cB_cream')*F('seller_cB_cream_cost')+
                    F('cB_brown')*F('seller_cB_brown_cost')+
                    F('c0_white')*F('seller_c0_white_cost')+
                    F('c0_cream')*F('seller_c0_cream_cost')+
                    F('c0_brown')*F('seller_c0_brown_cost')+
                    F('c1_white')*F('seller_c1_white_cost')+
                    F('c1_cream')*F('seller_c1_cream_cost')+
                    F('c1_brown')*F('seller_c1_brown_cost')+
                    F('c2_white')*F('seller_c2_white_cost')+
                    F('c2_cream')*F('seller_c2_cream_cost')+
                    F('c2_brown')*F('seller_c2_brown_cost')+
                    F('c3_white')*F('seller_c3_white_cost')+
                    F('c3_cream')*F('seller_c3_cream_cost')+
                    F('c3_brown')*F('seller_c3_brown_cost')+
                    F('dirt')*F('seller_dirt_cost'),

                    sum_buyer_orm =
                    F('cB_white')*F('buyer_cB_white_cost')+
                    F('cB_cream')*F('buyer_cB_cream_cost')+
                    F('cB_brown')*F('buyer_cB_brown_cost')+
                    F('c0_white')*F('buyer_c0_white_cost')+
                    F('c0_cream')*F('buyer_c0_cream_cost')+
                    F('c0_brown')*F('buyer_c0_brown_cost')+
                    F('c1_white')*F('buyer_c1_white_cost')+
                    F('c1_cream')*F('buyer_c1_cream_cost')+
                    F('c1_brown')*F('buyer_c1_brown_cost')+
                    F('c2_white')*F('buyer_c2_white_cost')+
                    F('c2_cream')*F('buyer_c2_cream_cost')+
                    F('c2_brown')*F('buyer_c2_brown_cost')+
                    F('c3_white')*F('buyer_c3_white_cost')+
                    F('c3_cream')*F('buyer_c3_cream_cost')+
                    F('c3_brown')*F('buyer_c3_brown_cost')+
                    F('dirt')*F('buyer_dirt_cost'),

                    seller_manager_orm = F('seller__manager__username'),
                    buyer_manager_orm = F('buyer__manager__username'),
                    owner_name_orm = F('owner__username'),
                    seller_name_orm = F('seller__requisites__name'),
                    buyer_name_orm = F('buyer__requisites__name'),
                    expense_total_orm = F('additional_expense__expense_total'),
                    expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                    logic_inn_orm = F('current_logic__inn'),
                    logic_name_orm = F('current_logic__requisites__name'),
                ), many=True)
            return base_deal_orm_request

        case 4:
            comp_base_deal_orm_request = BaseCompDealEggsNameSerializer(
                BaseDealEggsModel.objects.filter(is_active=True, status=4).select_related(
                    'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                    'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                    'current_logic', 'current_logic__requisites', 'documents',
                ).annotate(
                    sum_seller_orm =
                    F('cB_white')*F('seller_cB_white_cost')+
                    F('cB_cream')*F('seller_cB_cream_cost')+
                    F('cB_brown')*F('seller_cB_brown_cost')+
                    F('c0_white')*F('seller_c0_white_cost')+
                    F('c0_cream')*F('seller_c0_cream_cost')+
                    F('c0_brown')*F('seller_c0_brown_cost')+
                    F('c1_white')*F('seller_c1_white_cost')+
                    F('c1_cream')*F('seller_c1_cream_cost')+
                    F('c1_brown')*F('seller_c1_brown_cost')+
                    F('c2_white')*F('seller_c2_white_cost')+
                    F('c2_cream')*F('seller_c2_cream_cost')+
                    F('c2_brown')*F('seller_c2_brown_cost')+
                    F('c3_white')*F('seller_c3_white_cost')+
                    F('c3_cream')*F('seller_c3_cream_cost')+
                    F('c3_brown')*F('seller_c3_brown_cost')+
                    F('dirt')*F('seller_dirt_cost'),

                    sum_buyer_orm =
                    F('cB_white')*F('buyer_cB_white_cost')+
                    F('cB_cream')*F('buyer_cB_cream_cost')+
                    F('cB_brown')*F('buyer_cB_brown_cost')+
                    F('c0_white')*F('buyer_c0_white_cost')+
                    F('c0_cream')*F('buyer_c0_cream_cost')+
                    F('c0_brown')*F('buyer_c0_brown_cost')+
                    F('c1_white')*F('buyer_c1_white_cost')+
                    F('c1_cream')*F('buyer_c1_cream_cost')+
                    F('c1_brown')*F('buyer_c1_brown_cost')+
                    F('c2_white')*F('buyer_c2_white_cost')+
                    F('c2_cream')*F('buyer_c2_cream_cost')+
                    F('c2_brown')*F('buyer_c2_brown_cost')+
                    F('c3_white')*F('buyer_c3_white_cost')+
                    F('c3_cream')*F('buyer_c3_cream_cost')+
                    F('c3_brown')*F('buyer_c3_brown_cost')+
                    F('dirt')*F('buyer_dirt_cost'),

                    seller_manager_orm = F('seller__manager__username'),
                    buyer_manager_orm = F('buyer__manager__username'),
                    owner_name_orm = F('owner__username'),
                    seller_name_orm = F('seller__requisites__name'),
                    buyer_name_orm = F('buyer__requisites__name'),
                    expense_total_orm = F('additional_expense__expense_total'),
                    expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                    logic_inn_orm = F('current_logic__inn'),
                    logic_name_orm = F('current_logic__requisites__name'),
                ), many=True)
            return comp_base_deal_orm_request

        case _:
            pass


def get_base_deal_orm_request_param(base_deal_status: int, model_pk: int):

    try:
        match base_deal_status:

            case 1:
                calc_orm_request = CalculateEggsNamesSerializer(
                    BaseDealEggsModel.objects.filter(pk=model_pk).select_related(
                        'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                        'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                    ).annotate(
                        sum_seller_orm =
                        F('cB_white')*F('seller_cB_white_cost')+
                        F('cB_cream')*F('seller_cB_cream_cost')+
                        F('cB_brown')*F('seller_cB_brown_cost')+
                        F('c0_white')*F('seller_c0_white_cost')+
                        F('c0_cream')*F('seller_c0_cream_cost')+
                        F('c0_brown')*F('seller_c0_brown_cost')+
                        F('c1_white')*F('seller_c1_white_cost')+
                        F('c1_cream')*F('seller_c1_cream_cost')+
                        F('c1_brown')*F('seller_c1_brown_cost')+
                        F('c2_white')*F('seller_c2_white_cost')+
                        F('c2_cream')*F('seller_c2_cream_cost')+
                        F('c2_brown')*F('seller_c2_brown_cost')+
                        F('c3_white')*F('seller_c3_white_cost')+
                        F('c3_cream')*F('seller_c3_cream_cost')+
                        F('c3_brown')*F('seller_c3_brown_cost')+
                        F('dirt')*F('seller_dirt_cost'),

                        sum_buyer_orm =
                        F('cB_white')*F('buyer_cB_white_cost')+
                        F('cB_cream')*F('buyer_cB_cream_cost')+
                        F('cB_brown')*F('buyer_cB_brown_cost')+
                        F('c0_white')*F('buyer_c0_white_cost')+
                        F('c0_cream')*F('buyer_c0_cream_cost')+
                        F('c0_brown')*F('buyer_c0_brown_cost')+
                        F('c1_white')*F('buyer_c1_white_cost')+
                        F('c1_cream')*F('buyer_c1_cream_cost')+
                        F('c1_brown')*F('buyer_c1_brown_cost')+
                        F('c2_white')*F('buyer_c2_white_cost')+
                        F('c2_cream')*F('buyer_c2_cream_cost')+
                        F('c2_brown')*F('buyer_c2_brown_cost')+
                        F('c3_white')*F('buyer_c3_white_cost')+
                        F('c3_cream')*F('buyer_c3_cream_cost')+
                        F('c3_brown')*F('buyer_c3_brown_cost')+
                        F('dirt')*F('buyer_dirt_cost'),

                        seller_manager_orm = F('seller__manager__username'),
                        buyer_manager_orm = F('buyer__manager__username'),
                        owner_name_orm = F('owner__username'),
                        expense_total_orm = F('additional_expense__expense_total'),
                        expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                        seller_name_orm = F('seller__requisites__name'),
                        buyer_name_orm = F('buyer__requisites__name'),
                    ), many=True)
                return calc_orm_request

            case 2:
                conf_calc_orm_request = ConfirmedCalculateEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(pk=model_pk).select_related(
                        'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                        'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                        'current_logic', 'current_logic__requisites',
                    ).annotate(
                        sum_seller_orm =
                        F('cB_white')*F('seller_cB_white_cost')+
                        F('cB_cream')*F('seller_cB_cream_cost')+
                        F('cB_brown')*F('seller_cB_brown_cost')+
                        F('c0_white')*F('seller_c0_white_cost')+
                        F('c0_cream')*F('seller_c0_cream_cost')+
                        F('c0_brown')*F('seller_c0_brown_cost')+
                        F('c1_white')*F('seller_c1_white_cost')+
                        F('c1_cream')*F('seller_c1_cream_cost')+
                        F('c1_brown')*F('seller_c1_brown_cost')+
                        F('c2_white')*F('seller_c2_white_cost')+
                        F('c2_cream')*F('seller_c2_cream_cost')+
                        F('c2_brown')*F('seller_c2_brown_cost')+
                        F('c3_white')*F('seller_c3_white_cost')+
                        F('c3_cream')*F('seller_c3_cream_cost')+
                        F('c3_brown')*F('seller_c3_brown_cost')+
                        F('dirt')*F('seller_dirt_cost'),

                        sum_buyer_orm =
                        F('cB_white')*F('buyer_cB_white_cost')+
                        F('cB_cream')*F('buyer_cB_cream_cost')+
                        F('cB_brown')*F('buyer_cB_brown_cost')+
                        F('c0_white')*F('buyer_c0_white_cost')+
                        F('c0_cream')*F('buyer_c0_cream_cost')+
                        F('c0_brown')*F('buyer_c0_brown_cost')+
                        F('c1_white')*F('buyer_c1_white_cost')+
                        F('c1_cream')*F('buyer_c1_cream_cost')+
                        F('c1_brown')*F('buyer_c1_brown_cost')+
                        F('c2_white')*F('buyer_c2_white_cost')+
                        F('c2_cream')*F('buyer_c2_cream_cost')+
                        F('c2_brown')*F('buyer_c2_brown_cost')+
                        F('c3_white')*F('buyer_c3_white_cost')+
                        F('c3_cream')*F('buyer_c3_cream_cost')+
                        F('c3_brown')*F('buyer_c3_brown_cost')+
                        F('dirt')*F('buyer_dirt_cost'),

                        seller_manager_orm = F('seller__manager__username'),
                        buyer_manager_orm = F('buyer__manager__username'),
                        owner_name_orm = F('owner__username'),
                        seller_name_orm = F('seller__requisites__name'),
                        buyer_name_orm = F('buyer__requisites__name'),
                        expense_total_orm = F('additional_expense__expense_total'),
                        expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                        logic_inn_orm = F('current_logic__inn'),
                        logic_name_orm = F('current_logic__requisites__name'),
                    ), many=True)
                return conf_calc_orm_request

            case 3:
                base_deal_orm_request = BaseDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(pk=model_pk).select_related(
                        'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                        'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                        'current_logic', 'current_logic__requisites', 'documents',
                    ).annotate(
                        sum_seller_orm =
                        F('cB_white')*F('seller_cB_white_cost')+
                        F('cB_cream')*F('seller_cB_cream_cost')+
                        F('cB_brown')*F('seller_cB_brown_cost')+
                        F('c0_white')*F('seller_c0_white_cost')+
                        F('c0_cream')*F('seller_c0_cream_cost')+
                        F('c0_brown')*F('seller_c0_brown_cost')+
                        F('c1_white')*F('seller_c1_white_cost')+
                        F('c1_cream')*F('seller_c1_cream_cost')+
                        F('c1_brown')*F('seller_c1_brown_cost')+
                        F('c2_white')*F('seller_c2_white_cost')+
                        F('c2_cream')*F('seller_c2_cream_cost')+
                        F('c2_brown')*F('seller_c2_brown_cost')+
                        F('c3_white')*F('seller_c3_white_cost')+
                        F('c3_cream')*F('seller_c3_cream_cost')+
                        F('c3_brown')*F('seller_c3_brown_cost')+
                        F('dirt')*F('seller_dirt_cost'),

                        sum_buyer_orm =
                        F('cB_white')*F('buyer_cB_white_cost')+
                        F('cB_cream')*F('buyer_cB_cream_cost')+
                        F('cB_brown')*F('buyer_cB_brown_cost')+
                        F('c0_white')*F('buyer_c0_white_cost')+
                        F('c0_cream')*F('buyer_c0_cream_cost')+
                        F('c0_brown')*F('buyer_c0_brown_cost')+
                        F('c1_white')*F('buyer_c1_white_cost')+
                        F('c1_cream')*F('buyer_c1_cream_cost')+
                        F('c1_brown')*F('buyer_c1_brown_cost')+
                        F('c2_white')*F('buyer_c2_white_cost')+
                        F('c2_cream')*F('buyer_c2_cream_cost')+
                        F('c2_brown')*F('buyer_c2_brown_cost')+
                        F('c3_white')*F('buyer_c3_white_cost')+
                        F('c3_cream')*F('buyer_c3_cream_cost')+
                        F('c3_brown')*F('buyer_c3_brown_cost')+
                        F('dirt')*F('buyer_dirt_cost'),

                        seller_manager_orm = F('seller__manager__username'),
                        buyer_manager_orm = F('buyer__manager__username'),
                        owner_name_orm = F('owner__username'),
                        seller_name_orm = F('seller__requisites__name'),
                        buyer_name_orm = F('buyer__requisites__name'),
                        expense_total_orm = F('additional_expense__expense_total'),
                        expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                        logic_inn_orm = F('current_logic__inn'),
                        logic_name_orm = F('current_logic__requisites__name'),
                    ), many=True)
                return base_deal_orm_request

            case 4:
                comp_base_deal_orm_request = BaseCompDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(pk=model_pk).select_related(
                        'seller', 'buyer', 'owner', 'seller__requisites', 'buyer__requisites',
                        'comment_json', 'seller__manager', 'buyer__manager', 'additional_expense',
                        'current_logic', 'current_logic__requisites', 'documents',
                    ).annotate(
                        sum_seller_orm =
                        F('cB_white')*F('seller_cB_white_cost')+
                        F('cB_cream')*F('seller_cB_cream_cost')+
                        F('cB_brown')*F('seller_cB_brown_cost')+
                        F('c0_white')*F('seller_c0_white_cost')+
                        F('c0_cream')*F('seller_c0_cream_cost')+
                        F('c0_brown')*F('seller_c0_brown_cost')+
                        F('c1_white')*F('seller_c1_white_cost')+
                        F('c1_cream')*F('seller_c1_cream_cost')+
                        F('c1_brown')*F('seller_c1_brown_cost')+
                        F('c2_white')*F('seller_c2_white_cost')+
                        F('c2_cream')*F('seller_c2_cream_cost')+
                        F('c2_brown')*F('seller_c2_brown_cost')+
                        F('c3_white')*F('seller_c3_white_cost')+
                        F('c3_cream')*F('seller_c3_cream_cost')+
                        F('c3_brown')*F('seller_c3_brown_cost')+
                        F('dirt')*F('seller_dirt_cost'),

                        sum_buyer_orm =
                        F('cB_white')*F('buyer_cB_white_cost')+
                        F('cB_cream')*F('buyer_cB_cream_cost')+
                        F('cB_brown')*F('buyer_cB_brown_cost')+
                        F('c0_white')*F('buyer_c0_white_cost')+
                        F('c0_cream')*F('buyer_c0_cream_cost')+
                        F('c0_brown')*F('buyer_c0_brown_cost')+
                        F('c1_white')*F('buyer_c1_white_cost')+
                        F('c1_cream')*F('buyer_c1_cream_cost')+
                        F('c1_brown')*F('buyer_c1_brown_cost')+
                        F('c2_white')*F('buyer_c2_white_cost')+
                        F('c2_cream')*F('buyer_c2_cream_cost')+
                        F('c2_brown')*F('buyer_c2_brown_cost')+
                        F('c3_white')*F('buyer_c3_white_cost')+
                        F('c3_cream')*F('buyer_c3_cream_cost')+
                        F('c3_brown')*F('buyer_c3_brown_cost')+
                        F('dirt')*F('buyer_dirt_cost'),

                        seller_manager_orm = F('seller__manager__username'),
                        buyer_manager_orm = F('buyer__manager__username'),
                        owner_name_orm = F('owner__username'),
                        seller_name_orm = F('seller__requisites__name'),
                        buyer_name_orm = F('buyer__requisites__name'),
                        expense_total_orm = F('additional_expense__expense_total'),
                        expense_detail_json_orm = F('additional_expense__expense_detail_json'),
                        logic_inn_orm = F('current_logic__inn'),
                        logic_name_orm = F('current_logic__requisites__name'),
                    ), many=True)
                return comp_base_deal_orm_request

            case _:
                pass

    except ObjectDoesNotExist as e:
        raise serializers.ValidationError('error model pk in ws get_models param', e)


















