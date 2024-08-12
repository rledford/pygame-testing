from typing import Any
import pygame


class Entity:
    __id = 0

    def __init__(self, position: list = [0,0]):
        Entity.__id += 1
        self.id = Entity.__id
        self.position = list(position)

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.surface.Surface):
        pass

    def on_message(self, event: Any):
        pass

    def destroy(self):
        pass

