from typing import OrderedDict

from product_eggs.services.data_class import AdditionalExpenseData
from product_eggs.services.decorators import try_decorator_param


@try_decorator_param(('KeyError',))
def parse_additional_tmp_json(
        val_data: OrderedDict) -> AdditionalExpenseData | None:

    if val_data['tmp_json']:
        data_for_save = AdditionalExpenseData(**val_data['tmp_json'])
        return data_for_save
