from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.origins import OriginsDealEggs


def expense_model_creator() -> AdditionalExpenseEggs:
    """
    Создает модель AdditionalExpenseEggs.
    """
    model = AdditionalExpenseEggs.objects.create()
    model.save()
    return model


def documents_model_creator() -> DocumentsDealEggsModel:
    """
    Создает модель DocumentsDealEggsModel.
    """
    model = DocumentsDealEggsModel.objects.create()
    model.save()
    return model


def origins_model_creator() -> OriginsDealEggs:
    """
    Создает модель OriginsDealEggs.
    """
    model = OriginsDealEggs.objects.create()
    model.save()
    return model
