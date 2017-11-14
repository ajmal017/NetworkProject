from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

class Data(models.Model):
	id = models.IntegerField(primary_key=True, null=False)
	data_point = models.FloatField(null=False)

	def __str__(self):
		return str(self.data_point)

	class Meta:
		managed = True
		db_table = 'data'
