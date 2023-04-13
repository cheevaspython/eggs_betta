from typing import OrderedDict, Union

from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import QuerySet

from product_eggs.services.get_patch_data_before_save import get_object_from_patch_data
from product_eggs.services.messages_library import send_message_note_to_calc_owner
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs


def check_data_for_note(data: OrderedDict, instance: CalculateEggs | ConfirmedCalculateEggs) -> None:
    """
    Проверяет наличие note в данных, отправляет note в виде сообщения  если находит.
    """
    if data['note']:
        send_message_note_to_calc_owner(data['note'], instance)    
        instance.note = data['note']
        instance.save()


def try_get_file_name(request_data: OrderedDict) -> Union[str, int]:    
    """
    Ищет в коллекции в поле files_upload имя файла, возвращает если находит.
    """
    try:
        file_name = request_data['files_upload']
        return file_name
    except MultiValueDictKeyError:
        return 0
    except TypeError:
        return 0
    except KeyError:
        return 0


def check_val_data_to_files_upload(validated_data: OrderedDict) -> Union[str, int]:   
    """
    Ищет в коллекции в поле files_upload линк файла, возвращает если находит.
    """
    try:
        files_link = validated_data['files_upload']
        return files_link
    except TypeError:
        return 0
    except KeyError:
        return 0


def add_files_path_to_uploads_list(files_link: str, parse_id: int, queryset: QuerySet) -> None:
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
