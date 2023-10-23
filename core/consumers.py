import json,websockets,asyncio
from datetime import datetime
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer
from binance import ThreadedWebsocketManager
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer

"""
{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order Id
  "a": 50,          // Seller order Id
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore.
}

"""

def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

# from websocket import create_connection

# ws = create_connection("wss://stream.binance.com:9443/ws/bnbbtc@trade")
# print(ws.recv())

#!/usr/bin/env python

# import logging
# import time
# from binance.lib.utils import config_logging
# from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient
# # from examples.utils.prepare_env import get_api_key

# # api_key, api_secret = get_api_key()

# config_logging(logging, logging.DEBUG)


# def on_close(_):
#     logging.info("Do custom stuff when connection is closed")


# def message_handler(_, message):
#     logging.info(message)


# my_client = SpotWebsocketAPIClient(
#     stream_url="wss://testnet.binance.vision/ws",
#     api_key="aTAUCL0YiKsrgeNoFJ2Me9rnAIzTKW6JszjzQy6fLJPWgj3W51iHhHuiSBUgXjcz",
#     api_secret="vI9HwuIcKwj4DfpZScPbRXnWiuRrXYTW2QSgYyhPhm8MXahcUupE2qZHX9ds5wAN",
#     on_message=message_handler,
#     on_close=on_close,
# )


# my_client.get_order(symbol="BNBUSDT", orderId=1)

# time.sleep(2)

# logging.info("closing ws connection")
# my_client.stop()

    
class BotConsumer(WebsocketConsumer):

    # @sync_to_async
    def get_response(self,msg):
        print(msg)
        # self.channel_layer.group_send(
        #     self.group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': msg
        #     }
        # )
        
        self.send(text_data=json.dumps( 
            {
                "type":"connection_established",
                "message":"you are connected now!",
                "payload":{
                    "response":"Hello World!",
                }
            }
        ))
        
        

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name = 'room_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # symbol = 'BNBBTC'
        # twm = ThreadedWebsocketManager()
        # twm.start()
        # # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
        self.accept()
        # twm.start_trade_socket(callback=self.get_response, symbol=symbol)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        symbol = 'BNBBTC'
        twm = ThreadedWebsocketManager()
        twm.start()
        # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
        # self.accept()
        twm.start_trade_socket(callback=self.get_response, symbol=symbol)
        self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )



class AppConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = {}

    # async def get_response(self,msg):
    #     print(msg)
    #     await self.send(text_data=json.dumps( 
    #         {
    #             "type":"connection_established",
    #             "message":"you are connected now!",
    #             "payload":{
    #                 "response":"Hello World!",
    #             }
    #         }
    #     ))

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps( 
            {
                "type":"connection_established",
                "message":"you are connected now!",
                "payload":{
                    "response":{},
                }
            }
        ))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # async with websockets.connect("wss://stream.binance.com:9443/ws/btcbtc@trade") as worker_ws:
        #     result = json.loads(await worker_ws.recv())
        #     print(result)
        # async with websockets.connect("wss://stream.binance.com:9443/ws/bnbbtc@trade") as ws:
        # async with websockets.connect("wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m/btcusdt@kline_1m") as ws:
        async with websockets.connect("wss://stream.binance.com:9443/stream?streams=ethusdt@kline_1m") as ws:
            while True:
                start=datetime.now()
                response = await asyncio.wait_for(ws.recv(), timeout=20)
                response=json.loads(response)
                print(response)
                await self.send(text_data=json.dumps( 
                    {
                        "type":"connection_established",
                        "message":"you are connected now!",
                        "payload":{
                            "response":response,
                        }
                    }
                ))
                print(datetime.now() - start)
                await asyncio.sleep(0.5)
    
        asyncio.get_event_loop().run_until_complete(receive())

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

