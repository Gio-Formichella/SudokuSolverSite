import json
from json import JSONEncoder

import numpy
from channels.generic.websocket import AsyncWebsocketConsumer

from .backtracking_solver import backtracking_solver


class NumpyArrayEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, numpy.ndarray):
            return o.tolist()
        return JSONEncoder.default(self, o)


class BoardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, code):
        print(f"Connection closed with code: {code}")

    async def receive(self, text_data=None, bytes_data=None):
        # Method called when server receives data from the client over websocket
        puzzle = json.loads(text_data)
        board, assignments, backtracks,  = backtracking_solver(puzzle)

        message = json.dumps({
            "board": board,
            "msg": f"Solution found with {assignments} assignments and {backtracks} backtracks"
        }, cls=NumpyArrayEncoder)
        await self.send(text_data=message)
