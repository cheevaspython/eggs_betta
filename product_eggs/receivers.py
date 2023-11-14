from django.db.models.signals import post_delete
from django.dispatch import receiver

from product_eggs.tasks.entity_client import change_client_entity_list


@receiver(post_delete, sender=None, dispatch_uid="test_uid")
def change_client_entity_recever_delete(sender, instance, **kwargs) -> None:
    change_client_entity_list(instance, deleter=True)



