from django.db import models

class AirPollutionDataItem(models.Model):
    test = models.CharField('тест дата', max_length=200)
    big_test = models.TextField('тестовый текст')
    test_date = models.DateTimeField('тестовая дата')
    # aqi = models.AutoField()    #'Индекс загрязнения воздуха'

    class Meta:
        verbose_name = 'Some AirPollution data'
        verbose_name_plural = 'Some AirPollution datas'


class SomeData(models.Model):
    airPollutionDataItem = models.ForeignKey(AirPollutionDataItem, on_delete=models.CASCADE)
    test2 = models.CharField('test2', max_length=30)

    class Meta:
        verbose_name = 'Some SomeData data'
        verbose_name_plural = 'Some SomeData datas'

