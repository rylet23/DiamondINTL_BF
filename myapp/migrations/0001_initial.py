# Generated by Django 4.2.6 on 2024-03-01 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scroltable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max', models.FloatField()),
                ('min', models.FloatField()),
                ('max_symbol', models.CharField(max_length=10)),
                ('min_symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('ticker', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('pruh', models.FloatField()),
                ('pruh_yuh_close', models.FloatField()),
                ('pruh_yuh', models.FloatField()),
                ('day_compare', models.FloatField()),
                ('delta_today', models.FloatField()),
                ('delta_yesterday', models.FloatField()),
                ('delta_total', models.FloatField()),
            ],
        ),
    ]
