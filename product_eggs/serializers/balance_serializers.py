from rest_framework import serializers

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.serializers.base_deal_serializers import BaseDealEggsSerializer
from product_eggs.serializers.documents_serializers import DocumentsContractEggsSerializer
from product_eggs.serializers.requisites_serializers import RequisitesEggsModelSerializer
from product_eggs.serializers.tails_serializers import TailsEggsSerializer


class BalanceBaseClientEggsSerializer(serializers.ModelSerializer):
    current_tails = TailsEggsSerializer(read_only=True, source='tails')

    class Meta:
        model = BalanceBaseClientEggs
        fields = '__all__'


class StatisticClientSerializer(serializers.ModelSerializer):
    debt_deals = BaseDealEggsSerializer(source='basedealeggsmodel_set', many=True) #TODO fix all fields
    balance = BalanceBaseClientEggsSerializer(source='cur_balance', many=True)
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')
    percent = serializers.SerializerMethodField()

    def get_percent(self, instance):
        result = {}
        for i in instance.cur_balance.all():
            if i:
                if i.pay_limit and i.pay_limit_cash:
                    try:
                        if i.balance < 0:
                            percent = i.balance / (i.pay_limit + i.pay_limit_cash) * 100
                        else:
                            percent = (i.balance / 10000000) * 100
                        result[i.entity.inn] = percent
                    except ZeroDivisionError as e:
                        raise serializers.ValidationError(
                            f'В балансе {i.pk}, модели {instance} лимиты равны в сумме 0, проставьте данные для получения статистики.', e)
                else:
                    raise serializers.ValidationError(
                        f'В балансе {i.pk}, модели {instance} не установлены лимиты, проставьте их для получения статистики.')
        return result


class StatisticBuyerClientSerializer(StatisticClientSerializer):

    class Meta:
        model = BuyerCardEggs
        fields = '__all__'


class StatisticSellerClientSerializer(StatisticClientSerializer):

    class Meta:
        model = SellerCardEggs
        fields = '__all__'


class StatisticLogicClientSerializer(StatisticClientSerializer):

    class Meta:
        model = LogicCardEggs
        fields = '__all__'

