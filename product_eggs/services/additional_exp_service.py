from dataclasses import asdict
from datetime import datetime
from typing import OrderedDict

from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.services.data_class import AdditionalExpenseData
from product_eggs.services.decorators import try_decorator_param


@try_decorator_param(('KeyError',))
def parse_additional_tmp_json(
        val_data: OrderedDict) -> AdditionalExpenseData | None:
    """
    Парсит данные на наличие tmp_json.
    """
    if val_data['tmp_json']:
        data_for_save = AdditionalExpenseData(**val_data['tmp_json'])
        return data_for_save

@try_decorator_param(('KeyError',))
def parse_additional_tmp_multi_json(
        instance: AdditionalExpenseEggs,
        val_data: OrderedDict) -> AdditionalExpenseEggs | None:
    """
    Парсит данные на наличие tmp_multi_json.
    """
    if val_data['tmp_multi_json']:
        for cur_tmp in list(val_data['tmp_multi_json'].values()):
            data_for_save = AdditionalExpenseData(**cur_tmp)
            if data_for_save.logic:
                instance.expense_detail_json.update(
                    {str(datetime.today()) : asdict(data_for_save)}
                )
                instance.logic_pay = float(data_for_save.expense)
            else:
                instance.expense_detail_json.update(
                    {str(datetime.today()) : asdict(data_for_save)}
                )
                if data_for_save.cash:
                    instance.expense_total_form_2 += float(data_for_save.expense)
                else:
                    instance.expense_total_form_1 += float(data_for_save.expense)
        instance.tmp_multi_json = {}
        instance.save()
        return instance
    return None
