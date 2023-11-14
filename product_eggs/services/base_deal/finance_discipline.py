from datetime import datetime, timedelta, date
from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel



class FinanceDiscipline():
    """
    get cur deal and type client
    find in jsons (form1 or form2) all payments
    compare payments and client payback_day
    return string, color
    """
    clients_payments_book = {
        'seller': 'payment_order_outcoming',
        'buyer': 'payment_order_incoming',
        'logic': 'payment_order_outcoming_logic',
        'tail': 'tail_payment',
        'multi': 'multi_pay_order',
    }

    def __init__(self,
             instance: BaseDealEggsModel,
             client_type: str):
        self.deal = instance
        self.client_type = client_type
        self.json_payments_list: list = []
        self.data_json: dict = {}

    def _check_client_pay_form(self):
        match self.client_type:
            case 'buyer':
                if self.deal.cash:
                    self.data_json: dict = self.deal.documents.data_number_json_cash
                else:
                    self.data_json: dict = self.deal.documents.data_number_json
            case 'seller':
                if self.deal.cash_sell:
                    self.data_json: dict = self.deal.documents.data_number_json_cash
                else:
                    self.data_json: dict = self.deal.documents.data_number_json
            case 'logic':
                if self.deal.delivery_form_payment == 1 or self.deal.delivery_form_payment == 2:
                    self.data_json: dict = self.deal.documents.data_number_json
                else:
                    self.data_json: dict = self.deal.documents.data_number_json_cash
            case _:
                raise serializers.ValidationError('wrong client type in FinanceDiscipline')

    def _python_finance_discipline(self) -> str:
        if self.data_json:
            for i in self.data_json.values():
                if i['client_type'] == self.client_type and i['doc_type'] == self.clients_payments_book[self.client_type]:
                    self.json_payments_list.append(i)
                elif i['client_type'] == self.client_type and i['doc_type'] == self.clients_payments_book['tail']:
                    self.json_payments_list.append(i)
                elif i['client_type'] == self.client_type and i['doc_type'] == self.clients_payments_book['multi']:
                    self.json_payments_list.append(i)
            if len(self.json_payments_list) == 0:
                raise serializers.ValidationError('python_finance_discipline error in json.keys')
            elif len(self.json_payments_list) == 1:
                date_json = self._convert_str_to_datetime(self.json_payments_list[0]['date'])
            else:
                last_pay = sorted(self.json_payments_list, key=lambda x: x['date'], reverse=True)[0]
                date_json = self._convert_str_to_datetime(last_pay['date'])
            match self.client_type:
                case 'seller':
                    delta_interval = self._get_interval(self.deal.payback_day_for_us, date_json)
                case 'seller':
                    delta_interval = self._get_interval(self.deal.payback_day_for_buyer, date_json)
                case 'seller':
                    delta_interval = self._get_interval(self.deal.payback_day_for_us_logic, date_json)
                case _:
                    raise serializers.ValidationError('wrong client type in FinanceDiscipline')
            return self._compare_timedelta(delta_interval)
        else:
            raise serializers.ValidationError('error json data in FinanceDiscipline')

    def _compare_timedelta(self, delta_interval: timedelta) -> str:
        green: list[int] = [-1, 0, 1]
        if delta_interval.days in green:
            return 'green'
        elif delta_interval.days < -1:
            return 'red'
        elif delta_interval.days > 1:
            return 'orange'
        else:
            raise serializers.ValidationError('FinanceDiscipline nevedoma oshibka UHADi')

    def _convert_str_to_datetime(self, json_str: str) -> date:
        return datetime.strptime(json_str,'%d/%m/%Y').date()

    def _get_interval(self, date1: date, date2: date) -> timedelta:
        return date1 - date2

    def main(self) -> str:
        self._check_client_pay_form()
        return self._python_finance_discipline()

