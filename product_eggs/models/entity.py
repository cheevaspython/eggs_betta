from django.db import models

from general_layout.bases.models.entity import Entity


class EntityEggs(Entity):

    class Meta:
        db_table = 'EntityEggs'
        verbose_name = 'Юр. лицо'
        verbose_name_plural = 'Юр. лица'
        ordering = ['name']

    def __str__(self):
      return f'Юр. лицо: {self.name}/{self.inn}'
