from django.db import models

from users.models import CustomUser


class RoomSubscriber(models.Model):
    current_users = models.ManyToManyField(
        CustomUser, related_name="subscribe_room",
        blank=True,
    )
    def __str__(self):
        return "Await subscribe"
    

class SubscribeMessage(models.Model):
    room = models.ForeignKey(
        RoomSubscriber, on_delete=models.PROTECT,
        related_name='subscribe_messages',
    )
    sub_text = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='Детали приглашения',
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name='subscribe_messages',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"Message subscribe №{self.pk}"


class Room(models.Model):
    name = models.CharField(
        max_length=100, null=False,
        blank=False,
    )
    host = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name="rooms"
    )
    current_users = models.ManyToManyField(
        CustomUser, related_name="current_rooms",
        blank=True,
    )
    def __str__(self):
        return f"Room №{self.pk}, {self.name}, owner: {self.host}."


class Message(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT,
        related_name='messages',
    )
    text = models.TextField(max_length=500)
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
