from django_filters import rest_framework as filters
from core.models import (
    CryptoCurrencyPair
)


class CryptoCurrencyPairFilter(filters.FilterSet):

    symbol = filters.CharFilter(field_name="symbol", lookup_expr="icontains")

    class Meta:
        model = CryptoCurrencyPair
        fields = ["symbol"]  