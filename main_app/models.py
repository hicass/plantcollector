from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class GrowingMedia(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('growing_med_detail', kwargs={'pk': self.id})


class Plant(models.Model):
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    care = models.TextField(max_length=250)
    growing_media = models.ManyToManyField(GrowingMedia)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'plant_id': self.id})


class Watering(models.Model):
    date = models.DateField('Watering Date')

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f'Watered on: {self.date}'

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for plant_id: {self.plant_id} @{self.url}'
