from typing import Any
from typing_extensions import NotRequired, Optional, TypedDict
import pygame


class EntityProps(TypedDict):
    position: NotRequired[list[float]]


class Entity:
    __id = 0

    def __init__(self, props: Optional[EntityProps] = None):
        Entity.__id += 1
        self.id: int = Entity.__id
        self.position: list[float] = [0, 0]

        self.set_props(props)

    def set_props(self, props: Optional[EntityProps] = None):
        if props is None:
            return
        for k, v in props.items():
            self.__setattr__(k, v)

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, v: float):
        self.position[0] = v

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, v):
        self.position[1] = v

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.surface.Surface):
        pass

    def handle_event(self, event: Any):
        pass

    def destroy(self):
        pass


class PhysicsEntityProps(EntityProps):
    gravity: NotRequired[float]


class PhysicsEntity(Entity):
    def __init__(self, props: Optional[PhysicsEntityProps] = None):
        super().__init__()
        self.velocity: list[float] = [0, 0]
        self.hitbox: list[float] = [0, 0, 0, 0]

        self.set_props(props)

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, v: float):
        self.velocity[0] = v

    @property
    def vy(self):
        return self.velocity[0]

    @vy.setter
    def vy(self, v: float):
        self.velocity[1] = v
