from django.db import models

from users.models import CustomUser


class MessageToUser(models.Model):
	class Meta:
		abstract = True

	message_to = models.ForeignKey(
		CustomUser, related_name='notification_to',
		on_delete=models.SET_NULL, null=True
	)
	message = models.TextField(null=False)
	created_date = models.DateTimeField(
		auto_now_add=True, verbose_name='Создана'
	)
	is_active = models.BooleanField(
		editable=True, default=True, verbose_name='is_active'
	)
	not_read = models.BooleanField(
		editable=True, default=True, verbose_name='not_read'
	)

	def __str__(self):
		return f'Сообщение для {self.message_to}'
