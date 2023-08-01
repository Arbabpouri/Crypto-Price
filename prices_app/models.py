from django.db import models


# Create your models here.

class Symbol(models.Model):
    symbol = models.CharField(max_length=50, primary_key=True, )

    def __str__(self) -> str:
        return self.symbol
