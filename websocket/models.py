from django.db import models

from users.models import CustomUser


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(CustomUser, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"
