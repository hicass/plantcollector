from django.db import models
from django.urls import reverse

class Plant(models.Model):
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    care = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'plant_id': self.id})