from django.db import models


class Foo(models.Model):
    latlng = models.CharField('lat/lon', blank=True, max_length=100)
    # address = models.CharField("address",blank=True,  max_length=100)
# Create your models here.
