from general_layout.bases.models.contact_person import ContactPerson


class ContactPersonEggs(ContactPerson):

    class Meta:
        db_table = 'contact_person_eggs'
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
        ordering = ['pk']

    def __str__(self):
        return f'Контактное лицо {self.name}'
