import os
import ccxt
import requests
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from binance.client import Client
from core.models import (
    Exchange,
    CryptoCurrencyPair
)
from .pagination import (
    StandardPagesPagination
)
from rest_framework import generics
from .serializers import (
    CryptoCurrencyPairSerializer
)
from .filters import (
    CryptoCurrencyPairFilter
)

from django_filters.rest_framework import DjangoFilterBackend

# BINANCE & KUCOIN EXCHANGE INFO
class ExchangeInfo(APIView):
    def get(self, request, *args, **kwargs):
        get_exchange_name = self.request.query_params.get("exchange_name")
        if get_exchange_name == "Binance":
            client = Client(os.environ.get("BINANCE_API_KEY"),
                            os.environ.get("BINANCE_SECRET_KEY"))
            exchange_info = client.get_exchange_info()
            df = pd.DataFrame(exchange_info['symbols'])
            df['symbols'] = df['baseAsset'] + "/" + df['quoteAsset']
            symbols = df['symbols'].to_list()
            try:
                exchange_list = ["Binance", "KuCoin", "MEXC", "ByBit", "digifinex", "bitforex", "Kraken", "Phemex", "YoBit"]
                exchange_list = list(map(lambda x : x.lower(),exchange_list))
                exchange_dict = {}
                for i in exchange_list:
                    exchange_name = getattr(ccxt,i)()
                    exchange_dict[i] = exchange_name.symbols
                print(exchange_dict)
            except Exception as exception:
                pass
            context = {
                "status": status.HTTP_200_OK,
                "success": True,
                "response": symbols
            }
            return Response(context, status=status.HTTP_200_OK)
        elif get_exchange_name == "Kucoin":
            kucoin_request = requests.get(
                'https://api.kucoin.com/api/v1/symbols')
            exchange_info = kucoin_request.json()['data']
            df = pd.DataFrame(exchange_info)
            df['symbols'] = df['baseCurrency'] + "/" + df['quoteCurrency']
            symbols = df['symbols'].to_list()
            context = {
                "status": status.HTTP_200_OK,
                "success": True,
                "response": symbols
            }
            return Response(context, status=status.HTTP_200_OK)


class Exchanges(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # exchange_list = ["Binance", "KuCoin", "MEXC", "ByBit", "digifinex", "bitforex", "Kraken", "Phemex", "YoBit"]
            # exchange_list = list(map(lambda x : x.lower(),exchange_list))
            # exchange_dict = {}
            # for i in exchange_list:
            #     try:
            #         exchange_name = getattr(ccxt,i)()
            #         exchange_name.load_markets()
            #         exchange_dict[i] = exchange_name.symbols
            #     except Exception as exception:
            #         pass
            # get_exchanges_pairs = [i for i in exchange_dict.values()]
            # df = pd.DataFrame()
            # df['CryptoCurrency'] = list(np.concatenate(get_exchanges_pairs))
            # df.drop_duplicates(inplace=True)
            
            pairs = Exchange.objects.only("name").values("uid","name")
            context = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "response": pairs
                }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                "status":status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response":str(exception),
            }

class CryptoCurrencyPairsList(generics.ListAPIView):
    # queryset = Oyunlar.objects.all()
    pagination_class = StandardPagesPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['symbol']
    filterset_class = CryptoCurrencyPairFilter
    serializer_class = CryptoCurrencyPairSerializer
    def get_queryset(self):
        if self.request.query_params.get('symbol',None):
            get_symbol = self.request.query_params.get('symbol')
            queryset=CryptoCurrencyPair.objects.only("uid","symbol").distinct("symbol")
            return queryset
        return CryptoCurrencyPair.objects.only("uid","symbol").distinct("symbol")

        return queryset
    
    # def get(self,request,*args,**kwargs):
    #     queryset = self.get_queryset()
    #     serializer=CryptoCurrencyPairSerializer(queryset,many=True)
    #     page=self.paginate_queryset(serializer.data)
    #     return self.get_paginated_response(page)


class CryptoCurrencyPairs(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # exchange_list = ["Binance", "KuCoin", "MEXC", "ByBit", "digifinex", "bitforex", "Kraken", "Phemex", "YoBit"]
            # exchange_list = list(map(lambda x : x.lower(),exchange_list))
            # exchange_dict = {}
            # for i in exchange_list:
            #     try:
            #         exchange_name = getattr(ccxt,i)()
            #         exchange_name.load_markets()
            #         exchange_dict[i] = exchange_name.symbols
            #     except Exception as exception:
            #         pass
            # get_exchanges_pairs = [i for i in exchange_dict.values()]
            # df = pd.DataFrame()
            # df['CryptoCurrency'] = list(np.concatenate(get_exchanges_pairs))
            # df.drop_duplicates(inplace=True)
            
            pairs = CryptoCurrencyPair.objects.only("symbol").values_list("symbol",flat=True).distinct("symbol")
            context = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "response": pairs
                }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                "status":status.HTTP_400_BAD_REQUEST,
                "success": False,
                "response":str(exception),
            }
    