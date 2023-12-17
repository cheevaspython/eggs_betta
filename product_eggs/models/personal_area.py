from django.db import models

from general_layout.balance.models.personal_area import PersonalSalaryBalance
from product_eggs.models.entity import EntityEggs
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


class PersonalSalaryBalanceEggs(PersonalSalaryBalance):

    class Meta:
        db_table = 'PersonalSalaryBalanceEggs'
        verbose_name = 'Личный баланс'
        verbose_name_plural = 'Личные балансы'
        ordering = ['pk']

    current_manager = models.ForeignKey(
        CustomUser, related_name='manager_pa',
        verbose_name='Менеджер',
        on_delete=models.PROTECT,
        null=True,
    )
    entity = models.ForeignKey(
        EntityEggs, related_name='entity_pa',
        verbose_name='Юр. лицо',
        on_delete=models.PROTECT,
        null=True,
    )

    def check_lock_relations(self):
        if self.current_manager != self.__current_manager:
            raise custom_error(
                f'PersonalSalaryBalanceEggs wrong (cant change manager)', 433
            )
        if self.entity != self.__entity:
            raise custom_error(
                f'PersonalSalaryBalanceEggs wrong (cant change entity)', 433
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_manager = self.current_manager
        self.__entity = self.entity

    def save(self, *args, **kwargs):
        creating = not bool(self.pk)
        if creating:
            res = super().save(*args, **kwargs)
            return res

        self.check_lock_relations()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Персональный баланс №{self.pk}'




