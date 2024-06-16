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
        received = json.loads(text_data)  # Holds a puzzle or a reset message
        match received["type"]:
            case "reset":
                self.solver_running = False
            case "solve":
                self.solver_running = True
                board, assignments, backtracks = await backtracking_solver(puzzle=received["puzzle"])

                if self.solver_running:  # No reset message has been received
                    message = json.dumps({
                        "type": "solve",
                        "board": board,
                        "msg": f"Solution found with {assignments} assignments and {backtracks} backtracks"
                    }, cls=NumpyArrayEncoder)
                    await self.send(text_data=message)

            case "step-by-step":
                self.solver_running = True
                # Method will call send_assignment_update
                await backtracking_solver(puzzle=received["puzzle"], consumer=self)

    async def send_assignment_update(self, row: int, col: int, value: int, assignments: int, backtracks: int):
        if self.solver_running:  # Non reset message has been received
            message = json.dumps({
                "type": "step-by-step",
                "row": row,
                "col": col,
                "value": value,
                "msg": f"Current state found with {assignments} assignments and {backtracks} backtracks",
                "count": assignments  # Using assignment count for message ordering
            })
            await self.send(text_data=message)
