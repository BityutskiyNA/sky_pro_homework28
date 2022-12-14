import csv

from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=2000)
    is_published = models.BooleanField()


class Categori(models.Model):
    name = models.CharField(max_length=200)
