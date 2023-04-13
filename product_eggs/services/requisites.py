from typing import OrderedDict

from product_eggs.models.requisites import RequisitesEggs


def create_requisites_model(data: OrderedDict) -> RequisitesEggs:
    """
    Создает новую модель RequisitesEggs из данных.
    """
    new_requisites = RequisitesEggs.objects.create(general_manager=data['general_manager'],
        inn=data['inn'], bank_name=data['bank_name'], bic_bank=data['bic_bank'],
        cor_account=data['cor_account'], customers_pay_account=data['customers_pay_account'],
        legal_address=data['legal_address'], physical_address=data['physical_address'] )
    new_requisites.save()
    return new_requisites
