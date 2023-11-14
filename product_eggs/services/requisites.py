from typing import OrderedDict

from rest_framework import serializers

from product_eggs.models.requisites import RequisitesEggs


def create_requisites_model(data: OrderedDict) -> RequisitesEggs:
    """
    Создает новую модель RequisitesEggs из данных.
    """
    try:
        new_requisites, created = RequisitesEggs.objects.get_or_create(
            general_manager=data['general_manager'], inn=data['inn'], kpp=data['kpp'],
            bank_name=data['bank_name'], bic_bank=data['bic_bank'], cor_account=data['cor_account'],
            customers_pay_account=data['customers_pay_account'], legal_address=data['legal_address'],
            register_date= data['register_date'], physical_address=data['physical_address'],
        )
        new_requisites.save()
        return new_requisites

    except Exception as e:
        print('error requisites get_or_create -> base_client', e)
        raise serializers.ValidationError(e)


def create_requisites_model_from_exel(
        name: str,
        inn: str,
        kpp: str | None,
        register_date: str | None,
        # legal_address: str,
        # physical_address: str | None,
        # mail_address: str | None,
        country: str | None,
        region: str | None,
        city: str | None,
        email: str | None,
        site: str | None,
        # phone: str | None,
        phone2: str | None,
        phone_with_out_code: str | None,
        ) -> tuple[RequisitesEggs, bool]:

    cur_requisites, created = RequisitesEggs.objects.get_or_create(
        name=name,
        inn=inn,
        kpp=kpp,
        # legal_address=legal_address,
        # physical_address=physical_address,
        # mail_address=mail_address,
        register_date=register_date,
        country=country,
        region=region,
        city=city,
        email=email,
        site=site,
        # phone=phone,
        phone2=phone2,
        phone_with_out_code=phone_with_out_code,
    )
    return (cur_requisites, created,)


