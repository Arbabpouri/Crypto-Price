from django.db import models


# Create your models here.

class Symbol(models.Model):
    symbol = models.CharField(max_length=50, verbose_name="coin name")
    icon = models.TextField(null=True, default=None, blank=True, verbose_name="icon encode with base64")
    is_popular = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coins"
