
# Create your models here.
from django.db import models

class StockInfotable(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    pruh = models.FloatField()
    pruh_yuh_close = models.FloatField()
    pruh_yuh = models.FloatField()
    day_compare = models.FloatField()
    delta_today = models.FloatField()
    delta_yesterday = models.FloatField()
    delta_total = models.FloatField()

class Scroltable(models.Model):
    max = models.FloatField()
    min = models.FloatField()
    max_symbol = models.CharField(max_length=10)
    min_symbol = models.CharField(max_length=10)