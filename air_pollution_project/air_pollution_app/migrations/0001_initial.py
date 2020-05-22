# Generated by Django 3.0.6 on 2020-05-22 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirPollutionDataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=200, verbose_name='тест дата')),
                ('big_test', models.TextField(verbose_name='тестовый текст')),
                ('test_date', models.DateTimeField(verbose_name='тестовая дата')),
            ],
        ),
        migrations.CreateModel(
            name='SomeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test2', models.CharField(max_length=30, verbose_name='test2')),
                ('airPollutionDataItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='air_pollution_app.AirPollutionDataItem')),
            ],
        ),
    ]
