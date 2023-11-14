from django.db import models
from product_eggs.models.base_deal import BaseDealEggsModel

from users.models import CustomUser


class GeneralRoom(models.Model):
    """
    Общая комната.
    """
    current_users = models.ManyToManyField(
        CustomUser, related_name="general_room",
        blank=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='is_active',
    )
    def __str__(self):
        return f"General room - {self.pk}"


class GeneralWsMessage(models.Model):
    gen_room = models.ForeignKey(
        GeneralRoom, on_delete=models.PROTECT,
        related_name='general_messages',
    )
    sub_text = models.JSONField(
        blank=True, null=True,
        default=dict, verbose_name='Детали приглашения',
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name='gen_messages',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='is_active',
    )
    def __str__(self):
        return f"Message subscribe №{self.pk}"


class CustomRoom(models.Model):
    name = models.CharField(
        max_length=100, null=False,
        blank=False,
    )
    host = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name="host_rooms",
    )
    current_users = models.ManyToManyField(
        CustomUser, related_name="current_rooms",
        blank=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='is_active',
    )
    zakrep = models.CharField(
        max_length=255, verbose_name='Тема',
        blank = True, null = True,
    )
    zakrep_model = models.ForeignKey(
        BaseDealEggsModel, on_delete=models.PROTECT,
        related_name='custom_room',
        blank = True, null = True,
    )
    def __str__(self):
        return f"Room №{self.pk}, {self.name}, owner: {self.host}."


class WsMessage(models.Model):
    room = models.ForeignKey(
        CustomRoom, on_delete=models.PROTECT,
        related_name='messages',
    )
    text = models.TextField(max_length=500)
    room_cur_users = models.CharField(
        max_length=100, blank=True,
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='is_active',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"Message({self.user} {self.room})"
