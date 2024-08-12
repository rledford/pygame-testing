from typing import Callable

from core.event import GameEvent


class EventBus:
    __registry: dict[int, dict[int, Callable[[GameEvent], None]]] = {}

    def __init__(self):
        raise Exception("Do not instantiate the event bus")

    @classmethod
    def on(cls, event: int, handler_id: int, cb: Callable[[GameEvent], None]):
        if not cls.__registry.get(event):
            cls.__registry[event] = {}
        cls.__registry[event][handler_id] = cb

    @classmethod
    def off(cls, event: int, handler_id: int):
        if not cls.__registry.get(event):
            return
        if not cls.__registry[event].get(handler_id):
            return
        cls.__registry[event].pop(handler_id)

    @classmethod
    def clear(cls, handler_id: int):
        for listeners in cls.__registry.values():
            if not listeners.get(handler_id):
                continue
            listeners.pop(handler_id)

    @classmethod
    def send(cls, handler_id: int, event: GameEvent):
        if not cls.__registry.get(event.code):
            return
        if not cls.__registry[event.code].get(handler_id):
            return
        cls.__registry[event.code][handler_id](event)

    @classmethod
    def broadcast(cls, event: GameEvent):
        for handler_id in cls.__registry.get(event.code, {}).keys():
            if handler_id == event.sender:
                continue
            cls.__registry[event.code][handler_id](event)

