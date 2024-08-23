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
    static: NotRequired[bool]
    bounds: NotRequired[list[int | float]]


class PhysicsEntity(Entity):
    def __init__(self, props: Optional[PhysicsEntityProps] = None):
        super().__init__()
        self.gravity: float = 0
        self.static: bool = False
        self.velocity: list[float] = [0, 0]
        self.bounds: list[float] = [0, 0, 0, 0]
        self._collider: Optional[pygame.Rect] = None

        self.set_props(props)

        if self.static:
            self._collider = self.get_collider()

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, bounds: {self.bounds}, collider: {self._collider}"

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, v: float):
        self.velocity[0] = v

    @property
    def vy(self):
        return self.velocity[1]

    @vy.setter
    def vy(self, v: float):
        self.velocity[1] = v

    def get_collider(
        self, x: Optional[float] = None, y: Optional[float] = None
    ) -> pygame.Rect:
        if self.static and self._collider:
            return self._collider

        x = x if x is not None else self.x
        y = y if y is not None else self.y

        return pygame.Rect(
            x + self.bounds[0] - self.bounds[2] * 0.5,
            y + self.bounds[1] - self.bounds[3] * 0.5,
            self.bounds[2],
            self.bounds[3],
        )

    def draw(self, surface: pygame.surface.Surface):
        color = (255,255,0) if self.static else (255,0,255)
        pygame.draw.rect(surface, color, self.get_collider(), 1)
