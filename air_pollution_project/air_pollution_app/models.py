from django.db import models


class City(models.Model):
    alias_name = models.CharField('city alias name', max_length=10, default='alias')
    name = models.CharField('city name', max_length=30, default='city')
    longitude = models.FloatField(default='0.0')
    latitude = models.FloatField(default='0.0')

    class Meta:
        verbose_name = 'City data'
        verbose_name_plural = 'City item data'

    def __str__(self):
        return f'{self.name}'