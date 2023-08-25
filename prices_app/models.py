from django.db import models


# Create your models here.

class Symbol(models.Model):
    symbol = models.CharField(max_length=50)
    icon = models.TextField(default=None, null=True)
    is_popular = models.BooleanField(null=False)
