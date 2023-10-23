import uuid
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Exchange(BaseModel):
    name = models.CharField(max_length=128,unique=True)

    class Meta:
        verbose_name_plural = "Exchanges"

    def __str__(self):
        return f"Exchange : {self.name}"



class CryptoCurrencyPair(BaseModel):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Crypto Currencies"

    def __str__(self):
        return f"Exchange : {self.exchange.name} --> Symbol :{self.symbol}"
