from rest_framework import serializers
from core.models import (
    CryptoCurrencyPair
)
class CryptoCurrencyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrencyPair
        fields = ['uid','symbol']