from django.db import models

# Create your models here.
class ShopUnit(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    parentId = models.UUIDField(null=True)
    type = models.CharField(max_length=8)
    price = models.IntegerField(null=True)
