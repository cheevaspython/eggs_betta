from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.origins import OriginsDealEggs
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.services.decorators import try_decorator_param


class CreatorNewModel():
    """
    Create new model.
    Save model.
    """
    _tmp = {   
        'AdditionalExpenseEggs': AdditionalExpenseEggs,
        'DocumentsDealEggsModel': DocumentsDealEggsModel,
        'OriginsDealEggs': OriginsDealEggs,
        'MessageToUserEggs': MessageToUserEggs,
        'BaseDealEggsModel': BaseDealEggsModel,
    }

    def __init__(self, models_name: tuple, **kwargs):
        self._models_name = models_name   
        self.kwargs = kwargs
        self.new_models = []

    @try_decorator_param(('KeyError',))
    def create(self):
        for model in self._models_name:
            new_model = self._tmp[model].objects.create(**self.kwargs)
            new_model.save()
            self.new_models.append(new_model)

    def __getitem__(self, item):
        return getattr(self, item)



