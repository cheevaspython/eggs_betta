import os

from django.http import FileResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from product_eggs.models.documents import (
    DocumentsDealEggsModel, DocumentsContractEggsModel
)


class DownloadDocumentsLink():
    """
    Парсит pk и возвращает link
    """
    docs_deal_titles = ('payment_order_incoming', 'payment_order_outcoming',
    'specification_seller', 'account_to_seller', 'specification_buyer',
    'account_to_buyer', 'application_contract_logic', 'account_to_logic',
    'UPD_incoming', 'account_invoicing_from_seller', 'product_invoice_from_seller',
    'UPD_outgoing', 'account_invoicing_from_buyer', 'product_invoice_from_buyer',
    'veterinary_certificate_buyer', 'veterinary_certificate_seller',
    'international_deal_CMR', 'international_deal_TTN_seller', 'UPD_logic',
    'account_invoicing_logic', 'product_invoice_logic', 'payment_order_outcoming_logic',
    'UPD_outgoing_signed', 'international_deal_TTN_buyer', 'contract',
    )
    docs_contract_titles = ('contract')

    def __init__(self, pk_data: str):
        self.parce_pk_data = pk_data.replace('-', ' ').split()
        try:
            self.pk = int(self.parce_pk_data[0])
            self.title = self.parce_pk_data[1]
        except ValueError:
            raise serializers.ValidationError('Wrong pk_data in DownloadDocumentsLink')

    def _get_doc_contract_instance(self) -> DocumentsContractEggsModel:
        """
        Получает модель документов client.
        """
        try:
            if self.title in self.docs_contract_titles:
                return DocumentsContractEggsModel.objects.get(pk=self.pk)
            else:
                raise serializers.ValidationError('Wrong title in DownloadDocumentsLink')
        except (ValueError, ObjectDoesNotExist) as e:
            raise serializers.ValidationError('Wrong titile for model in download pk', e)

    def _get_doc_deal_instance(self) -> DocumentsDealEggsModel:
        """
        Получает модель документов Deal.
        """
        try:
            if self.title in self.docs_deal_titles:
                return DocumentsDealEggsModel.objects.get(pk=self.pk)
            else:
                raise serializers.ValidationError('Wrong title in DownloadDocumentsLink')
        except (ValueError, ObjectDoesNotExist) as e:
            raise serializers.ValidationError('Wrong titile for model in download pk', e)

    def _get_file_link(self) -> str:
        """
        Сверяет строчные данные и возвращает линк.
        """
        match self.title:
            case 'contract':
                return str(self._get_doc_contract_instance().contract)
            case 'payment_order_incoming':
                return str(self._get_doc_deal_instance().payment_order_incoming)
            case 'payment_order_outcoming_logic':
                return str(self._get_doc_deal_instance().payment_order_outcoming_logic)
            case 'payment_order_outcoming':
                return str(self._get_doc_deal_instance().payment_order_outcoming)
            case 'specification_seller':
                return str(self._get_doc_deal_instance().specification_seller)
            case 'account_to_seller':
                return str(self._get_doc_deal_instance().account_to_seller)
            case 'specification_buyer':
                return str(self._get_doc_deal_instance().specification_buyer)
            case 'account_to_buyer':
                return str(self._get_doc_deal_instance().account_to_buyer)
            case 'application_contract_logic':
                return str(self._get_doc_deal_instance().application_contract_logic)
            case 'account_to_logic':
                return str(self._get_doc_deal_instance().account_to_logic)
            case 'UPD_incoming':
                return str(self._get_doc_deal_instance().UPD_incoming)
            case 'account_invoicing_from_seller':
                return str(self._get_doc_deal_instance().account_invoicing_from_seller)
            case 'product_invoice_from_seller':
                return str(self._get_doc_deal_instance().product_invoice_from_seller)
            case 'UPD_outgoing':
                return str(self._get_doc_deal_instance().UPD_outgoing)
            case 'UPD_outgoing_signed':
                return str(self._get_doc_deal_instance().UPD_outgoing_signed)
            case 'account_invoicing_from_buyer':
                return str(self._get_doc_deal_instance().account_invoicing_from_buyer)
            case 'product_invoice_from_buyer':
                return str(self._get_doc_deal_instance().product_invoice_from_buyer)
            case 'veterinary_certificate_buyer':
                return str(self._get_doc_deal_instance().veterinary_certificate_buyer)
            case 'veterinary_certificate_seller':
                return str(self._get_doc_deal_instance().veterinary_certificate_seller)
            case 'international_deal_CMR':
                return str(self._get_doc_deal_instance().international_deal_CMR)
            case 'international_deal_TTN_seller':
                return str(self._get_doc_deal_instance().international_deal_TTN_seller)
            case 'international_deal_TTN_buyer':
                return str(self._get_doc_deal_instance().international_deal_TTN_buyer)
            case 'UPD_logic':
                return str(self._get_doc_deal_instance().UPD_logic)
            case 'account_invoicing_logic':
                return str(self._get_doc_deal_instance().account_invoicing_logic)
            case 'product_invoice_logic':
                return str(self._get_doc_deal_instance().product_invoice_logic)
            case _:
                raise serializers.ValidationError('Wrong title in DownloadDocumentsLink')

    def get_auto_download_response(self) -> FileResponse:
        """
        Возвращает ссылку на скачивание документа.
        """
        module_dir = os.path.join(settings.MEDIA_ROOT, self._get_file_link())
        try:
            return FileResponse(open(module_dir, 'rb'), as_attachment=True)
        except IsADirectoryError:
            raise serializers.ValidationError('File not found')





