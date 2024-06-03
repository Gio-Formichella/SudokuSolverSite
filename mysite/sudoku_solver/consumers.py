from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BoardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, code):
        print(f"Connection closed with code: {code}")

    async def receive(self, text_data=None, bytes_data=None):
        # Method called when server receives data from the client over websocket
        text_data_json = json.loads(text_data)
        #message = text_data_json["message"]
        #sender = text_data_json["sender"]

        print("Got here")

        # Sending the message back to the client over the websocket
        await self.send(text_data=json.dumps({
            "message": "m"
        }))
