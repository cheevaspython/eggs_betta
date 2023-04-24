from datetime import datetime
from typing import OrderedDict, Union

from django.db.models import QuerySet
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.documents_parse_tmp_json import DealDocumentsPaymentParser, \
    MultiDocumentsPaymentParser
from product_eggs.services.documents.documents_static import DOC_CONTRACT_CASH, DOC_CONTRACT_CONTRACT, \
    DOC_CONTRACT_MULTY_PAY
from product_eggs.services.get_anything.get_patch_data_before_save import get_object_from_patch_data
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from users.models import CustomUser


@try_decorator_param(('MultiValueDictKeyError', 'AttributeError', 'KeyError'))
def check_data_for_note(
        data: OrderedDict,
        instance: BaseDealEggsModel,
        note: str) -> None:
    """
    Проверяет наличие note в данных,
    отправляет note в виде сообщения если находит.
    """
    note_dict = {
        'note_calc': instance.note_calc,
        'note_conf_calc': instance.note_conf_calc,
    }
    if note in note_dict.keys():
        if data[note]:
            new_message = MessageLibrarrySend(
                note,    
                instance,
                data[note],
            )
            new_message.send_message()
            note_dict[note] = data[note]
            instance.save()


@try_decorator_param(('TypeError', 'KeyError', 'MultiValueDictKeyError'), return_value=0)
def get_file_name(request_data: OrderedDict) -> Union[str, int]:    
    """
    Ищет в коллекции в поле files_upload имя файла, возвращает если находит.
    """
    file_name = request_data['files_upload']
    return file_name


@try_decorator_param(('TypeError', 'KeyError'), return_value=0)
def check_val_data_to_files_upload(validated_data: OrderedDict) -> Union[str, int]:   
    """
    Ищет в коллекции в поле files_upload линк файла, возвращает если находит.
    """
    files_link = validated_data['files_upload']
    return files_link


def add_files_path_to_uploads_list(
        files_link: str, parse_id: int, queryset: QuerySet) -> None:
    """
    Добавляет путь к загруженному файлу.
    """
    current_obj = get_object_from_patch_data(queryset, parse_id)
    files_path_data = current_obj.files_upload_list
    if files_path_data:
        current_obj.files_upload_list = f'{files_path_data}, {files_link}'  
        current_obj.save() 
    else:
        current_obj.files_upload_list = files_link
        current_obj.save() 


@try_decorator_param(('KeyError',))
def check_serializer_val_data(funk): 
    return funk()


@try_decorator_param(('KeyError',))
def check_validated_data_for_tmp_json(
        serializer_data: OrderedDict,
        instance: DocumentsDealEggsModel, 
        user: CustomUser) -> None:

    if serializer_data['tmp_json']:
        parser = DealDocumentsPaymentParser(
            serializer_data['tmp_json'],
            user,
            instance,
        )
        parser.main_default()
        instance.tmp_json = {}
        instance.save()


@try_decorator_param(('KeyError',))
def check_val_data_contract_for_multy_pay(
        serializer_data: OrderedDict,
        instance: DocumentsContractEggsModel,  
        user: CustomUser) -> None:

    if serializer_data['multi_pay_order']:
        instance.multi_pay_order_links_dict_json.update(
            {str(datetime.today())[:-7] : (DOC_CONTRACT_MULTY_PAY +
                str(serializer_data['multi_pay_order']))}
        )
        parse_multi = MultiDocumentsPaymentParser(
            serializer_data['tmp_json_for_multi_pay_order'],
            user,
            instance,
            cash=False,
        )
    elif serializer_data['cash_docs']:
        instance.cash_docs_links_dict_json.update(
            {str(datetime.today())[:-7] : (DOC_CONTRACT_CASH +
                str(serializer_data['cash_docs']))}
        )
    parse_multi = MultiDocumentsPaymentParser(
        serializer_data['tmp_json_for_multi_pay_order'],
        user,
        instance,
    )
    parse_multi.main()
    instance.save()


@try_decorator_param(('KeyError',))
def check_val_data_contract_for_contract(
        serializer_data: OrderedDict,
        instance: DocumentsContractEggsModel) -> None: 
    if serializer_data['contract']:
        instance.contract_links_dict_json.update(
            {str(datetime.today())[:-7]: (DOC_CONTRACT_CONTRACT +
                str(serializer_data['contract']))}
        )
        instance.save()

