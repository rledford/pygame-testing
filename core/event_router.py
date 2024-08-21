from typing import Callable
from .events import GameEvent


class GameEventRouter:
    def __init__(self):
        self.registry: dict[int, dict[int, Callable[[GameEvent], None]]] = {}

    def on(self, event: int, handler_id: int, cb: Callable[[GameEvent], None]):
        if not self.registry.get(event):
            self.registry[event] = {}
        self.registry[event][handler_id] = cb

    def off(self, event: int, handler_id: int):
        if not self.registry.get(event):
            return
        if not self.registry[event].get(handler_id):
            return
        self.registry[event].pop(handler_id)

    def clear(self, handler_id: int):
        for listeners in self.registry.values():
            if not listeners.get(handler_id):
                continue
            listeners.pop(handler_id)

    def send(self, handler_id: int, event: GameEvent):
        if not self.registry.get(event.code):
            return
        if not self.registry[event.code].get(handler_id):
            return
        self.registry[event.code][handler_id](event)

    def broadcast(self, event: GameEvent):
        for handler_id in self.registry.get(event.code, {}).keys():
            if handler_id == event.sender:
                continue
            self.registry[event.code][handler_id](event)
