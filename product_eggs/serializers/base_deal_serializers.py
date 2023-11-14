from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.comments_serializers import CommentEggWsSerializer
from product_eggs.serializers.documents_serializers import DocumentsDealGetEggsSerializer
from product_eggs.services.base_deal.deal_services import get_sum_buyer, get_sum_seller
from product_eggs.services.base_deal.finance_discipline import FinanceDiscipline


class CalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'additional_expense',

            'cash', 'import_application',
            'calc_to_confirm',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ]


class CalculateEggsNamesSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.ReadOnlyField(source='owner_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    seller_manager = serializers.ReadOnlyField(source='seller_manager_orm')
    buyer_manager = serializers.ReadOnlyField(source='buyer_manager_orm')
    sum_buyer = serializers.ReadOnlyField(source='sum_buyer_orm')
    sum_seller = serializers.ReadOnlyField(source='sum_seller_orm')
    expense_total = serializers.ReadOnlyField(source='expense_total_orm')
    expense_detail_json = serializers.ReadOnlyField(source='expense_detail_json_orm')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'calc_to_confirm',
            'additional_expense',

            'is_active',
            'cash', 'import_application',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'owner_name', 'buyer_name', 'seller_name',
            'seller_manager', 'buyer_manager', 'sum_buyer',
            'sum_seller', 'expense_total', 'expense_detail_json',
        ]


class CalculateEggsNamesSerializerObserver(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    seller_manager = serializers.SerializerMethodField()
    buyer_manager = serializers.SerializerMethodField()
    sum_seller = serializers.SerializerMethodField()
    sum_buyer = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_seller_manager(self, instance):
        return instance.seller.manager.username

    def get_buyer_manager(self, instance):
        return instance.buyer.manager.username

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_sum_seller(self, instance):
        return get_sum_seller(instance)

    def get_sum_buyer(self, instance):
        return get_sum_buyer(instance)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'calc_to_confirm',
            'additional_expense',

            'is_active',
            'cash', 'import_application',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'owner_name', 'buyer_name', 'seller_name',
            'seller_manager', 'buyer_manager', 'sum_buyer',
            'sum_seller', 'expense_total', 'expense_detail_json'
        ]


class ConfirmedCalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ]


class ConfirmedCalculateEggsNameSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.ReadOnlyField(source='owner_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    seller_manager = serializers.ReadOnlyField(source='seller_manager_orm')
    buyer_manager = serializers.ReadOnlyField(source='buyer_manager_orm')
    sum_buyer = serializers.ReadOnlyField(source='sum_buyer_orm')
    sum_seller = serializers.ReadOnlyField(source='sum_seller_orm')
    expense_total = serializers.ReadOnlyField(source='expense_total_orm')
    expense_detail_json = serializers.ReadOnlyField(source='expense_detail_json_orm')
    logic_inn = serializers.ReadOnlyField(source='logic_inn_orm')
    logic_name = serializers.ReadOnlyField(source='logic_name_orm')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed',
            'is_active',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json',
            'seller_manager', 'buyer_manager', 'sum_buyer', 'sum_seller'
        ]


class ConfirmedCalculateEggsNameSerializerObserver(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()
    seller_manager = serializers.SerializerMethodField()
    buyer_manager = serializers.SerializerMethodField()
    sum_seller = serializers.SerializerMethodField()
    sum_buyer = serializers.SerializerMethodField()

    def get_seller_manager(self, instance):
        return instance.seller.manager.username

    def get_buyer_manager(self, instance):
        return instance.buyer.manager.username

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_logic_name(self, instance):
        try:
            return instance.current_logic.requisites.name
        except AttributeError:
            return None

    def get_logic_inn(self, instance):
        try:
            return instance.current_logic.inn
        except AttributeError:
            return None

    def get_sum_seller(self, instance):
        return get_sum_seller(instance)

    def get_sum_buyer(self, instance):
        return get_sum_buyer(instance)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed',
            'is_active',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json',
            'seller_manager', 'buyer_manager', 'sum_buyer', 'sum_seller'
        ]


class BaseDealEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    actual_loading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    actual_unloading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    sum_seller = serializers.SerializerMethodField()
    sum_buyer = serializers.SerializerMethodField()

    def get_sum_seller(self, instance):
        return get_sum_seller(instance)

    def get_sum_buyer(self, instance):
        return get_sum_buyer(instance)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'sum_buyer', 'sum_seller',
        ]


class BaseDealEggsNameSerializer(serializers.ModelSerializer):
    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.ReadOnlyField(source='owner_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    seller_manager = serializers.ReadOnlyField(source='seller_manager_orm')
    buyer_manager = serializers.ReadOnlyField(source='buyer_manager_orm')
    sum_buyer = serializers.ReadOnlyField(source='sum_buyer_orm')
    sum_seller = serializers.ReadOnlyField(source='sum_seller_orm')
    expense_total = serializers.ReadOnlyField(source='expense_total_orm')
    expense_detail_json = serializers.ReadOnlyField(source='expense_detail_json_orm')
    logic_inn = serializers.ReadOnlyField(source='logic_inn_orm')
    logic_name = serializers.ReadOnlyField(source='logic_name_orm')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed',
            'is_active',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer',
            'deal_our_debt_UPD', 'deal_buyer_debt_UPD',
            'deal_buyer_pay_amount', 'deal_our_pay_amount',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
            'seller_manager', 'buyer_manager', 'sum_seller', 'sum_buyer',
        ]


class BaseDealEggsNameSerializerObserver(serializers.ModelSerializer):
    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()
    seller_manager = serializers.SerializerMethodField()
    buyer_manager = serializers.SerializerMethodField()
    sum_seller = serializers.SerializerMethodField()
    sum_buyer = serializers.SerializerMethodField()

    def get_seller_manager(self, instance):
        return instance.seller.manager.username

    def get_buyer_manager(self, instance):
        return instance.buyer.manager.username

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_logic_name(self, instance):
        return instance.current_logic.requisites.name

    def get_logic_inn(self, instance):
        return instance.current_logic.inn

    def get_sum_seller(self, instance):
        return get_sum_seller(instance)

    def get_sum_buyer(self, instance):
        return get_sum_buyer(instance)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',
            'comment_json', 'comment_detail',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed',
            'is_active',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer',
            'deal_our_debt_UPD', 'deal_buyer_debt_UPD',
            'deal_buyer_pay_amount', 'deal_our_pay_amount',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
            'seller_manager', 'buyer_manager', 'sum_seller', 'sum_buyer',
        ]


class CompleteDealEggsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status', 'is_active',

            'log_status_calc_query', 'log_status_conf_calc_query',
            'log_status_deal_query',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ]


class BaseCompDealEggsNameSerializer(serializers.ModelSerializer): #TODO
    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.ReadOnlyField(source='owner_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    seller_manager = serializers.ReadOnlyField(source='seller_manager_orm')
    buyer_manager = serializers.ReadOnlyField(source='buyer_manager_orm')
    sum_buyer = serializers.ReadOnlyField(source='sum_buyer_orm')
    sum_seller = serializers.ReadOnlyField(source='sum_seller_orm')
    expense_total = serializers.ReadOnlyField(source='expense_total_orm')
    expense_detail_json = serializers.ReadOnlyField(source='expense_detail_json_orm')
    logic_inn = serializers.ReadOnlyField(source='logic_inn_orm')
    logic_name = serializers.ReadOnlyField(source='logic_name_orm')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status', 'is_active',
            'comment_json', 'comment_detail',

            'log_status_calc_query', 'log_status_conf_calc_query',
            'log_status_deal_query',
            'is_active',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
            'seller_manager', 'buyer_manager', 'sum_buyer', 'sum_seller',
        ]


class BaseCompDealEggsNameSerializerObserver(serializers.ModelSerializer):
    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()
    seller_manager = serializers.SerializerMethodField()
    buyer_manager = serializers.SerializerMethodField()
    sum_seller = serializers.SerializerMethodField()
    sum_buyer = serializers.SerializerMethodField()

    def get_seller_manager(self, instance):
        return instance.seller.manager.username

    def get_buyer_manager(self, instance):
        return instance.buyer.manager.username

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_logic_name(self, instance):
        return instance.current_logic.requisites.name

    def get_logic_inn(self, instance):
        return instance.current_logic.inn

    def get_sum_seller(self, instance):
        return get_sum_seller(instance)

    def get_sum_buyer(self, instance):
        return get_sum_buyer(instance)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status', 'is_active',
            'comment_json', 'comment_detail',

            'log_status_calc_query', 'log_status_conf_calc_query',
            'log_status_deal_query',
            'is_active',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner', 'entity',
            'current_logic', 'additional_expense', 'documents',

            'cash', 'import_application',
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer',
            'loading_address', 'unloading_address',
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD', 'payback_day_for_us_logic',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD',

            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'seller_cB_white_cost', 'seller_cB_cream_cost', 'seller_cB_brown_cost',
            'buyer_cB_white_cost', 'buyer_cB_cream_cost', 'buyer_cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'seller_c0_white_cost', 'seller_c0_cream_cost', 'seller_c0_brown_cost',
            'buyer_c0_white_cost', 'buyer_c0_cream_cost', 'buyer_c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'seller_c1_white_cost', 'seller_c1_cream_cost', 'seller_c1_brown_cost',
            'buyer_c1_white_cost', 'buyer_c1_cream_cost', 'buyer_c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'seller_c2_white_cost', 'seller_c2_cream_cost', 'seller_c2_brown_cost',
            'buyer_c2_white_cost', 'buyer_c2_cream_cost', 'buyer_c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'seller_c3_white_cost', 'seller_c3_cream_cost', 'seller_c3_brown_cost',
            'buyer_c3_white_cost', 'buyer_c3_cream_cost', 'buyer_c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'buyer_dirt_cost', 'seller_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
            'seller_manager', 'buyer_manager', 'sum_buyer', 'sum_seller',
        ]


class BaseDealEggsGetPaymentsSerializer(serializers.ModelSerializer):
    logic_name = serializers.ReadOnlyField(source='logic_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_status', 'cash', 'entity',
            'seller', 'buyer', 'current_logic', 'documents',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'payback_day_for_us_logic', 'logic_our_pay_amount',
            'seller_name', 'buyer_name', 'logic_name',
        ]


class BaseDealEggsFinanceDisciplineSellerSerializer(serializers.ModelSerializer):
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    finance_discipline = serializers.SerializerMethodField()

    def get_finance_discipline(self, instance):
        fin_obj = FinanceDiscipline(instance, 'seller')
        return fin_obj.main()

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_status', 'cash', 'entity',
            'seller', 'buyer', 'current_logic', 'documents',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'payback_day_for_us_logic', 'logic_our_pay_amount',
            'seller_name',
            'finance_discipline',
        ]


class BaseDealEggsFinanceDisciplineBuyerSerializer(serializers.ModelSerializer):
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')
    finance_discipline = serializers.SerializerMethodField()

    def get_finance_discipline(self, instance):
        fin_obj = FinanceDiscipline(instance, 'buyer')
        return fin_obj.main()

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_status', 'cash', 'entity',
            'seller', 'buyer', 'current_logic', 'documents',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'payback_day_for_us_logic', 'logic_our_pay_amount',
            'buyer_name',
            'finance_discipline',
        ]


class BaseDealEggsFinanceDisciplineLogicSerializer(serializers.ModelSerializer):
    logic_name = serializers.ReadOnlyField(source='logic_name_orm')
    finance_discipline = serializers.SerializerMethodField()

    def get_finance_discipline(self, instance):
        fin_obj = FinanceDiscipline(instance, 'logic')
        return fin_obj.main()

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_status', 'cash', 'entity',
            'seller', 'buyer', 'current_logic', 'documents',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount',
            'deal_buyer_pay_amount', 'payback_day_for_us_logic', 'logic_our_pay_amount',
            'logic_name',
            'finance_discipline',
        ]


class BaseDealBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_buyer_pay_amount', 'documents', 'cash', 'logic_our_debt_UPD',
            'deal_buyer_debt_UPD', 'payback_day_for_us', 'payback_day_for_buyer',
            'deal_our_pay_amount', 'deal_our_debt_UPD', 'logic_our_pay_amount',
            'logic_our_debt_for_app_contract', 'delivery_form_payment', 'entity',
        ]


class CalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')

    def get_title(self, instance):
        return ('Просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name'
        ]


class CalculateEggsSerializerSideBarObserver(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_title(self, instance):
        return ('Просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name'
        ]


class ConfirmedCalculateEggsSerializerSideBarObserver(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_title(self, instance):
        return ('Подтвержденный просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name'
        ]


class ConfirmedCalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')

    def get_title(self, instance):
        return ('Подтвержденный просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name'
        ]


class DealEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.ReadOnlyField(source='seller_name_orm')
    buyer_name = serializers.ReadOnlyField(source='buyer_name_orm')

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name', 'deal_status'
        ]


class DealEggsSerializerSideBarObserver(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()

    def get_seller_name(self, instance):
        return instance.seller.requisites.name

    def get_buyer_name(self, instance):
        return instance.buyer.requisites.name

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'title', 'seller_name', 'buyer_name', 'deal_status'
        ]
