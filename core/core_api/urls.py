from django.urls import path
from core.core_api.views import (
    ExchangeInfo,
    CryptoCurrencyPairs,
    Exchanges,
    CryptoCurrencyPairsList
)

urlpatterns = [

    path("exchangeInfo/",ExchangeInfo.as_view(),name="exchangeInfo"),
    path("get_exchanges/",Exchanges.as_view(),name="get_exchanges"),
    path("get_crypto_currency_pairs/",CryptoCurrencyPairsList.as_view(),name="get_crypto_currency_pairs"),

]