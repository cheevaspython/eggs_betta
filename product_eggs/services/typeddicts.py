from typing import TypedDict, OrderedDict
from datetime import datetime


class DictDataDetailsForSaveJson(TypedDict):
        user: str
        document_date: datetime
        document_number: int
        pay_quantity: float
        inn: str
        document_type: str
        deal: str
        documents_id: int


def create_dict_data_detail_for_save(
        user_id: int,
        ord_dict_data: OrderedDict,
        deal_id: int ) -> DictDataDetailsForSaveJson:

        dict_data_detail_for_json = DictDataDetailsForSaveJson(
                user=str(user_id),
                document_date=ord_dict_data['date'],
                document_number=ord_dict_data['number'],
                pay_quantity=ord_dict_data['pay_quantity'],
                inn=ord_dict_data['inn'],
                document_type=ord_dict_data['doc_type'],
                deal=str(deal_id),
                documents_id=ord_dict_data['documents_id'],
        ) 
        return dict_data_detail_for_json
