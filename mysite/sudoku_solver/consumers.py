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
    solver_running = False  # Flag

    async def connect(self):
        print("Connected")
        self.solver_running = False
        await self.accept()

    async def disconnect(self, code):
        print(f"Connection closed with code: {code}")

    async def receive(self, text_data=None, bytes_data=None):
        # Method called when server receives data from the client over websocket
        received = json.loads(text_data)  # Is a puzzle or a reset message
        if "reset" in received:
            self.solver_running = False
        else:  # user has sent a puzzle
            self.solver_running = True
            board, assignments, backtracks,  = backtracking_solver(received)

            if self.solver_running:  # No reset message has been received
                message = json.dumps({
                    "board": board,
                    "msg": f"Solution found with {assignments} assignments and {backtracks} backtracks"
                }, cls=NumpyArrayEncoder)
                await self.send(text_data=message)
