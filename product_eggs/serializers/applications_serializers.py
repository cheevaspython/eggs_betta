from rest_framework import serializers

from product_eggs.serializers.comments_serializers import CommentEggWsSerializer
from product_eggs.models.applications import (
    ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs
)
from product_eggs.serializers.base_client_serializers import (
    BuyerCardEggsPlusRequisitesSerializer, SellerCardEggsDetailSerializer,
    BuyerCardEggsDetailSerializer, SellerCardEggsPlusRequisitesSerializer
)
from product_eggs.services.validation.check_validated_data import match_data_for_fresh_app
from users.serializers import CustomUserSerializer


class ApplicationSellerEggsDetailSerializer(serializers.ModelSerializer):
    seller_card_detail = SellerCardEggsDetailSerializer(read_only=True, source='current_seller')
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от продавца')

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'current_seller', 'seller_card_detail',
            'loading_address', 'comment', 'owner_detail', 'title', 'region',
            'import_application', 'postponement_pay', 'edited_date_time',
            'is_actual', 'comment_json', 'comment_detail',
            'await_add_cost',
        ]


class ApplicationSellerEggsWsGetSerializer(serializers.ModelSerializer):
    seller_card_detail = SellerCardEggsPlusRequisitesSerializer(read_only=True, source='current_seller')
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    title = serializers.SerializerMethodField()
    app_fresh = serializers.SerializerMethodField()

    def get_app_fresh(self, instance):
        return match_data_for_fresh_app(instance.edited_date_time)

    def get_title(self, instance):
        return ('Заявка от продавца')

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'current_seller', 'seller_card_detail',
            'loading_address', 'comment', 'owner_detail', 'title', 'region',
            'import_application', 'postponement_pay', 'edited_date_time',
            'app_fresh', 'comment_json', 'is_active', 'comment_detail',
            'await_add_cost', 'is_actual',
        ]


class ApplicationBuyerEggsDetailSerializer(serializers.ModelSerializer):
    buyer_card_detail = BuyerCardEggsDetailSerializer(read_only=True, source='current_buyer')
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от покупателя')

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'current_buyer', 'buyer_card_detail',
            'unloading_address', 'comment', 'owner_detail', 'title', 'region',
            'postponement_pay', 'edited_date_time', # 'app_fresh',
            'is_actual', 'comment_json', 'comment_detail',
            'await_add_cost',
        ]


class ApplicationBuyerEggsWsGetSerializer(serializers.ModelSerializer):
    buyer_card_detail = BuyerCardEggsPlusRequisitesSerializer(read_only=True, source='current_buyer')
    comment_detail = CommentEggWsSerializer(read_only=True, source='comment_json')
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    title = serializers.SerializerMethodField()
    app_fresh = serializers.SerializerMethodField()

    def get_app_fresh(self, instance):
        return match_data_for_fresh_app(instance.edited_date_time)

    def get_title(self, instance):
        return ('Заявка от покупателя')

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'current_buyer', 'buyer_card_detail',
            'unloading_address', 'comment', 'owner_detail', 'title', 'region',
            'postponement_pay', 'edited_date_time', 'app_fresh',
            'comment_json', 'is_active', 'comment_detail',
            'await_add_cost', 'is_actual',
        ]


class ApplicationSellerEggsSerializer(serializers.ModelSerializer):
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'region', 'loading_address',
            'current_seller', 'import_application',
            'postponement_pay', 'comment', 'comment_json',
            'await_add_cost',
        ]


class ApplicationBuyerEggsSerializer(serializers.ModelSerializer):
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])
    await_add_cost = serializers.DateField(
        required=False, allow_null=True, input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = [
            'id', 'owner', 'delivery_window_from', 'delivery_window_until',
            'cB_any_color', 'c0_any_color', 'c1_any_color', 'c2_any_color', 'c3_any_color',
            'shtamp_cB_white', 'shtamp_cB_cream', 'shtamp_cB_brown',
            'shtamp_c0_white', 'shtamp_c0_cream', 'shtamp_c0_brown',
            'shtamp_c1_white', 'shtamp_c1_cream', 'shtamp_c1_brown',
            'shtamp_c2_white', 'shtamp_c2_cream', 'shtamp_c2_brown',
            'shtamp_c3_white', 'shtamp_c3_cream', 'shtamp_c3_brown',
            'shtamp_dirt',
            'cB_white', 'cB_cream', 'cB_brown',
            'cB_white_cost', 'cB_cream_cost', 'cB_brown_cost',
            'c0_white', 'c0_cream', 'c0_brown',
            'c0_white_cost', 'c0_cream_cost', 'c0_brown_cost',
            'c1_white', 'c1_cream', 'c1_brown',
            'c1_white_cost', 'c1_cream_cost', 'c1_brown_cost',
            'c2_white', 'c2_cream', 'c2_brown',
            'c2_white_cost', 'c2_cream_cost', 'c2_brown_cost',
            'c3_white', 'c3_cream', 'c3_brown',
            'c3_white_cost', 'c3_cream_cost', 'c3_brown_cost',
            'cB_white_fermer', 'cB_cream_fermer', 'cB_brown_fermer',
            'c0_white_fermer', 'c0_cream_fermer', 'c0_brown_fermer',
            'c1_white_fermer', 'c1_cream_fermer', 'c1_brown_fermer',
            'dirt', 'dirt_cost',
            'current_buyer', 'region', 'postponement_pay',
            'unloading_address', 'comment',
            'comment_json',
            'await_add_cost',
        ]


class ApplicationSellerEggsSerializerSideBar(serializers.ModelSerializer):
    seller_name = serializers.ReadOnlyField(source='name')
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от продавца')

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = [
            'id', 'title', 'seller_name', 'is_actual', 'await_add_cost'
        ]


class ApplicationSellerEggsSerializerSideBarObserver(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от продавца')

    def get_seller_name(self, instance):
        return instance.current_seller.requisites.name

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = [
            'id', 'title', 'seller_name', 'is_actual', 'await_add_cost'
        ]


class ApplicationBuyerEggsSerializerSideBarObserver(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от покупателя')

    def get_buyer_name(self, instance):
        return instance.current_buyer.requisites.name

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = [
            'id', 'title', 'buyer_name', 'is_actual', 'await_add_cost'
        ]


class ApplicationBuyerEggsSerializerSideBar(serializers.ModelSerializer):
    buyer_name = serializers.ReadOnlyField(source='name')
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от покупателя')

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = [
            'id', 'title', 'buyer_name', 'is_actual', 'await_add_cost'
        ]

